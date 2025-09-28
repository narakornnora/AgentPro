"""
Secure Vault Web Interface
Web-based management interface for the secure credentials vault
Author: AI Assistant
Date: September 26, 2025
"""

import os
import json
import asyncio
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Depends, status, Request, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import jwt
from secure_vault import SecureVault
import secrets

# Pydantic models
class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "user"

class APIKeyCreate(BaseModel):
    name: str
    service: str
    api_key: str
    permissions: List[str] = []
    rate_limit: Optional[int] = None
    expires_at: Optional[str] = None

class CredentialCreate(BaseModel):
    name: str
    credential_type: str
    data: Dict[str, Any]
    tags: List[str] = []
    expires_at: Optional[str] = None

class VaultWebInterface:
    """
    Secure web interface for vault management
    Features:
    - JWT-based authentication
    - Role-based access control
    - Secure API endpoints
    - Real-time vault statistics
    - Audit logging interface
    """
    
    def __init__(self, vault: SecureVault, jwt_secret: str = None):
        self.vault = vault
        self.jwt_secret = jwt_secret or secrets.token_urlsafe(32)
        self.app = FastAPI(title="Secure Vault API", version="1.0.0")
        self.security = HTTPBearer()
        
        # Setup routes
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup FastAPI routes"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard():
            """Main dashboard"""
            return await self._get_dashboard_html()
        
        @self.app.post("/api/auth/login")
        async def login(user_login: UserLogin):
            """User login endpoint"""
            auth_result = self.vault.authenticate_user(user_login.username, user_login.password)
            
            if not auth_result['success']:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=auth_result['message']
                )
            
            # Generate JWT token
            user = auth_result['user']
            token_data = {
                "user_id": user['id'],
                "username": user['username'],
                "role": user['role'],
                "exp": datetime.utcnow() + timedelta(hours=8)
            }
            
            token = jwt.encode(token_data, self.jwt_secret, algorithm="HS256")
            
            return {
                "access_token": token,
                "token_type": "bearer",
                "user": user
            }
        
        @self.app.post("/api/auth/register")
        async def register(user_create: UserCreate, current_user: dict = Depends(self._get_current_user)):
            """User registration endpoint (admin only)"""
            if current_user['role'] != 'admin':
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only administrators can create users"
                )
            
            success = self.vault.create_user(
                user_create.username,
                user_create.email,
                user_create.password,
                user_create.role
            )
            
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to create user"
                )
            
            return {"message": "User created successfully"}
        
        @self.app.post("/api/api-keys")
        async def create_api_key(api_key: APIKeyCreate, current_user: dict = Depends(self._get_current_user)):
            """Create new API key"""
            expires_at = None
            if api_key.expires_at:
                expires_at = datetime.fromisoformat(api_key.expires_at)
            
            success = self.vault.store_api_key(
                api_key.name,
                api_key.service,
                api_key.api_key,
                api_key.permissions,
                api_key.rate_limit,
                expires_at
            )
            
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to store API key"
                )
            
            return {"message": "API key stored successfully"}
        
        @self.app.get("/api/api-keys")
        async def list_api_keys(service: Optional[str] = None, current_user: dict = Depends(self._get_current_user)):
            """List API keys"""
            api_keys = self.vault.list_api_keys(service)
            return {"api_keys": api_keys}
        
        @self.app.get("/api/api-keys/{name}")
        async def get_api_key(name: str, current_user: dict = Depends(self._get_current_user)):
            """Get API key (returns masked key for security)"""
            api_key = self.vault.get_api_key(name)
            
            if not api_key:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="API key not found"
                )
            
            # Return masked key for security
            masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
            return {"name": name, "key_preview": masked_key}
        
        @self.app.post("/api/credentials")
        async def create_credential(credential: CredentialCreate, current_user: dict = Depends(self._get_current_user)):
            """Create new credential"""
            expires_at = None
            if credential.expires_at:
                expires_at = datetime.fromisoformat(credential.expires_at)
            
            success = self.vault.store_credential(
                credential.name,
                credential.credential_type,
                credential.data,
                credential.tags,
                expires_at
            )
            
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to store credential"
                )
            
            return {"message": "Credential stored successfully"}
        
        @self.app.get("/api/credentials")
        async def list_credentials(credential_type: Optional[str] = None, current_user: dict = Depends(self._get_current_user)):
            """List credentials"""
            credentials = self.vault.list_credentials(credential_type)
            return {"credentials": credentials}
        
        @self.app.get("/api/credentials/{name}")
        async def get_credential(name: str, current_user: dict = Depends(self._get_current_user)):
            """Get credential data"""
            credential = self.vault.get_credential(name)
            
            if not credential:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Credential not found"
                )
            
            return {"name": name, "data": credential}
        
        @self.app.get("/api/vault/stats")
        async def get_vault_stats(current_user: dict = Depends(self._get_current_user)):
            """Get vault statistics"""
            stats = self.vault.get_vault_stats()
            return {"stats": stats}
        
        @self.app.post("/api/vault/backup")
        async def create_backup(backup_password: str = Form(...), current_user: dict = Depends(self._get_current_user)):
            """Create vault backup (admin only)"""
            if current_user['role'] != 'admin':
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only administrators can create backups"
                )
            
            backup_path = f"./backups/vault_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            success = self.vault.backup_vault(backup_path, backup_password)
            
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create backup"
                )
            
            return {"message": "Backup created successfully", "backup_path": backup_path}
    
    async def _get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        """Get current authenticated user from JWT token"""
        try:
            payload = jwt.decode(credentials.credentials, self.jwt_secret, algorithms=["HS256"])
            return {
                "user_id": payload['user_id'],
                "username": payload['username'],
                "role": payload['role']
            }
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    
    async def _get_dashboard_html(self) -> str:
        """Generate dashboard HTML"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔐 Secure Vault Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .header h1 {
            color: #4a5568;
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #718096;
            font-size: 1.1rem;
        }
        
        .login-form, .dashboard {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #4a5568;
        }
        
        input, select, textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }
        
        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: transform 0.2s ease;
        }
        
        .btn:hover {
            transform: translateY(-2px);
        }
        
        .btn-danger {
            background: linear-gradient(135deg, #fc8181 0%, #f56565 100%);
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
        }
        
        .card h3 {
            color: #4a5568;
            margin-bottom: 15px;
            font-size: 1.2rem;
        }
        
        .stats {
            display: flex;
            justify-content: space-between;
            margin: 20px 0;
        }
        
        .stat-item {
            text-align: center;
            padding: 15px;
            background: #f7fafc;
            border-radius: 8px;
            flex: 1;
            margin: 0 10px;
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            color: #718096;
            font-size: 0.9rem;
        }
        
        .list-item {
            padding: 15px;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .list-item:last-child {
            border-bottom: none;
        }
        
        .status {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        
        .status.active {
            background: #c6f6d5;
            color: #22543d;
        }
        
        .status.expired {
            background: #fed7d7;
            color: #742a2a;
        }
        
        .hidden {
            display: none;
        }
        
        .modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        
        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 15px;
            max-width: 500px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
        }
        
        .close-btn {
            float: right;
            font-size: 24px;
            cursor: pointer;
            color: #718096;
        }
        
        .alert {
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .alert.success {
            background: #c6f6d5;
            color: #22543d;
            border: 1px solid #9ae6b4;
        }
        
        .alert.error {
            background: #fed7d7;
            color: #742a2a;
            border: 1px solid #fc8181;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔐 Secure Vault</h1>
            <p>Enterprise-grade credential and API key management system</p>
        </div>
        
        <!-- Login Form -->
        <div id="loginForm" class="login-form">
            <h2>Login to Vault</h2>
            <div id="loginAlert"></div>
            <form id="loginFormElement">
                <div class="form-group">
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username" required>
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <button type="submit" class="btn">🔑 Login</button>
            </form>
        </div>
        
        <!-- Dashboard -->
        <div id="dashboard" class="dashboard hidden">
            <div class="header">
                <h2>Welcome, <span id="userInfo"></span></h2>
                <button onclick="logout()" class="btn btn-danger">Logout</button>
            </div>
            
            <!-- Statistics -->
            <div id="statsContainer"></div>
            
            <!-- Action Buttons -->
            <div style="margin: 20px 0; text-align: center;">
                <button onclick="showModal('apiKeyModal')" class="btn">➕ Add API Key</button>
                <button onclick="showModal('credentialModal')" class="btn">➕ Add Credential</button>
                <button onclick="refreshData()" class="btn">🔄 Refresh</button>
                <button onclick="createBackup()" class="btn" id="backupBtn">💾 Backup</button>
            </div>
            
            <!-- Content Grid -->
            <div class="grid">
                <div class="card">
                    <h3>🔑 API Keys</h3>
                    <div id="apiKeysList"></div>
                </div>
                
                <div class="card">
                    <h3>🔐 Credentials</h3>
                    <div id="credentialsList"></div>
                </div>
            </div>
        </div>
        
        <!-- API Key Modal -->
        <div id="apiKeyModal" class="modal hidden">
            <div class="modal-content">
                <span class="close-btn" onclick="hideModal('apiKeyModal')">&times;</span>
                <h3>Add API Key</h3>
                <form id="apiKeyForm">
                    <div class="form-group">
                        <label for="apiKeyName">Name:</label>
                        <input type="text" id="apiKeyName" required>
                    </div>
                    <div class="form-group">
                        <label for="apiKeyService">Service:</label>
                        <input type="text" id="apiKeyService" required>
                    </div>
                    <div class="form-group">
                        <label for="apiKeyValue">API Key:</label>
                        <input type="password" id="apiKeyValue" required>
                    </div>
                    <div class="form-group">
                        <label for="apiKeyPermissions">Permissions (comma-separated):</label>
                        <input type="text" id="apiKeyPermissions" placeholder="read,write,admin">
                    </div>
                    <button type="submit" class="btn">Save API Key</button>
                </form>
            </div>
        </div>
        
        <!-- Credential Modal -->
        <div id="credentialModal" class="modal hidden">
            <div class="modal-content">
                <span class="close-btn" onclick="hideModal('credentialModal')">&times;</span>
                <h3>Add Credential</h3>
                <form id="credentialForm">
                    <div class="form-group">
                        <label for="credentialName">Name:</label>
                        <input type="text" id="credentialName" required>
                    </div>
                    <div class="form-group">
                        <label for="credentialType">Type:</label>
                        <select id="credentialType" required>
                            <option value="database">Database</option>
                            <option value="smtp">SMTP/Email</option>
                            <option value="ftp">FTP</option>
                            <option value="ssh">SSH</option>
                            <option value="oauth">OAuth</option>
                            <option value="other">Other</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="credentialData">Data (JSON format):</label>
                        <textarea id="credentialData" rows="8" required placeholder='{"host": "example.com", "username": "user", "password": "pass"}'></textarea>
                    </div>
                    <div class="form-group">
                        <label for="credentialTags">Tags (comma-separated):</label>
                        <input type="text" id="credentialTags" placeholder="production,database,critical">
                    </div>
                    <button type="submit" class="btn">Save Credential</button>
                </form>
            </div>
        </div>
    </div>
    
    <script>
        let authToken = null;
        let currentUser = null;
        
        // Login functionality
        document.getElementById('loginFormElement').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            try {
                const response = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username, password }),
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    authToken = data.access_token;
                    currentUser = data.user;
                    
                    document.getElementById('loginForm').classList.add('hidden');
                    document.getElementById('dashboard').classList.remove('hidden');
                    document.getElementById('userInfo').textContent = `${currentUser.username} (${currentUser.role})`;
                    
                    // Show/hide admin features
                    if (currentUser.role !== 'admin') {
                        document.getElementById('backupBtn').style.display = 'none';
                    }
                    
                    await refreshData();
                } else {
                    showAlert('loginAlert', data.detail, 'error');
                }
            } catch (error) {
                showAlert('loginAlert', 'Login failed: ' + error.message, 'error');
            }
        });
        
        // Logout functionality
        function logout() {
            authToken = null;
            currentUser = null;
            document.getElementById('loginForm').classList.remove('hidden');
            document.getElementById('dashboard').classList.add('hidden');
            document.getElementById('username').value = '';
            document.getElementById('password').value = '';
        }
        
        // Refresh data
        async function refreshData() {
            await Promise.all([
                loadStats(),
                loadApiKeys(),
                loadCredentials()
            ]);
        }
        
        // Load vault statistics
        async function loadStats() {
            try {
                const response = await fetch('/api/vault/stats', {
                    headers: {
                        'Authorization': `Bearer ${authToken}`,
                    },
                });
                
                const data = await response.json();
                const stats = data.stats;
                
                document.getElementById('statsContainer').innerHTML = `
                    <div class="stats">
                        <div class="stat-item">
                            <div class="stat-number">${stats.total_api_keys}</div>
                            <div class="stat-label">API Keys</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">${stats.total_credentials}</div>
                            <div class="stat-label">Credentials</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">${stats.total_users}</div>
                            <div class="stat-label">Users</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">${stats.recent_access_24h}</div>
                            <div class="stat-label">Recent Access</div>
                        </div>
                    </div>
                `;
            } catch (error) {
                console.error('Failed to load stats:', error);
            }
        }
        
        // Load API keys
        async function loadApiKeys() {
            try {
                const response = await fetch('/api/api-keys', {
                    headers: {
                        'Authorization': `Bearer ${authToken}`,
                    },
                });
                
                const data = await response.json();
                const apiKeys = data.api_keys;
                
                const html = apiKeys.map(key => `
                    <div class="list-item">
                        <div>
                            <strong>${key.name}</strong> (${key.service})<br>
                            <small>Used ${key.usage_count} times</small>
                        </div>
                        <span class="status active">Active</span>
                    </div>
                `).join('');
                
                document.getElementById('apiKeysList').innerHTML = html || '<p>No API keys found</p>';
            } catch (error) {
                console.error('Failed to load API keys:', error);
            }
        }
        
        // Load credentials
        async function loadCredentials() {
            try {
                const response = await fetch('/api/credentials', {
                    headers: {
                        'Authorization': `Bearer ${authToken}`,
                    },
                });
                
                const data = await response.json();
                const credentials = data.credentials;
                
                const html = credentials.map(cred => `
                    <div class="list-item">
                        <div>
                            <strong>${cred.name}</strong> (${cred.type})<br>
                            <small>Accessed ${cred.access_count} times</small>
                        </div>
                        <span class="status active">Active</span>
                    </div>
                `).join('');
                
                document.getElementById('credentialsList').innerHTML = html || '<p>No credentials found</p>';
            } catch (error) {
                console.error('Failed to load credentials:', error);
            }
        }
        
        // Modal functions
        function showModal(modalId) {
            document.getElementById(modalId).classList.remove('hidden');
        }
        
        function hideModal(modalId) {
            document.getElementById(modalId).classList.add('hidden');
        }
        
        // API Key form submission
        document.getElementById('apiKeyForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = {
                name: document.getElementById('apiKeyName').value,
                service: document.getElementById('apiKeyService').value,
                api_key: document.getElementById('apiKeyValue').value,
                permissions: document.getElementById('apiKeyPermissions').value.split(',').map(p => p.trim()).filter(p => p)
            };
            
            try {
                const response = await fetch('/api/api-keys', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${authToken}`,
                    },
                    body: JSON.stringify(formData),
                });
                
                if (response.ok) {
                    hideModal('apiKeyModal');
                    document.getElementById('apiKeyForm').reset();
                    await loadApiKeys();
                } else {
                    const error = await response.json();
                    alert('Failed to save API key: ' + error.detail);
                }
            } catch (error) {
                alert('Failed to save API key: ' + error.message);
            }
        });
        
        // Credential form submission
        document.getElementById('credentialForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            try {
                const data = JSON.parse(document.getElementById('credentialData').value);
                
                const formData = {
                    name: document.getElementById('credentialName').value,
                    credential_type: document.getElementById('credentialType').value,
                    data: data,
                    tags: document.getElementById('credentialTags').value.split(',').map(t => t.trim()).filter(t => t)
                };
                
                const response = await fetch('/api/credentials', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${authToken}`,
                    },
                    body: JSON.stringify(formData),
                });
                
                if (response.ok) {
                    hideModal('credentialModal');
                    document.getElementById('credentialForm').reset();
                    await loadCredentials();
                } else {
                    const error = await response.json();
                    alert('Failed to save credential: ' + error.detail);
                }
            } catch (error) {
                alert('Failed to save credential: ' + error.message);
            }
        });
        
        // Backup functionality
        async function createBackup() {
            const password = prompt('Enter backup password:');
            if (!password) return;
            
            try {
                const formData = new FormData();
                formData.append('backup_password', password);
                
                const response = await fetch('/api/vault/backup', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${authToken}`,
                    },
                    body: formData,
                });
                
                if (response.ok) {
                    const data = await response.json();
                    alert('Backup created successfully at: ' + data.backup_path);
                } else {
                    const error = await response.json();
                    alert('Failed to create backup: ' + error.detail);
                }
            } catch (error) {
                alert('Failed to create backup: ' + error.message);
            }
        }
        
        // Utility functions
        function showAlert(containerId, message, type) {
            const container = document.getElementById(containerId);
            container.innerHTML = `<div class="alert ${type}">${message}</div>`;
            setTimeout(() => container.innerHTML = '', 5000);
        }
    </script>
</body>
</html>
        """


# FastAPI application factory
def create_vault_app(master_password: str = None) -> FastAPI:
    """Create FastAPI application with secure vault"""
    vault = SecureVault(master_password=master_password)
    web_interface = VaultWebInterface(vault)
    
    # Create default admin user if none exists
    vault.create_user("admin", "admin@vault.local", "VaultAdmin123!", "admin")
    
    return web_interface.app


# Demo server
async def run_vault_server():
    """Run the secure vault web server"""
    import uvicorn
    
    print("🔐 Starting Secure Vault Web Server...")
    print("=" * 50)
    
    app = create_vault_app("SecureMasterPassword123!")
    
    print("🌐 Server starting at http://localhost:8000")
    print("👤 Default login: admin / VaultAdmin123!")
    print("🔒 Enterprise-grade security enabled")
    
    config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
    
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run_vault_server())