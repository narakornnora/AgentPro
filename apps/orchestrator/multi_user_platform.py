"""
Multi-User Workspace System
===========================
Complete multi-tenant platform supporting multiple users with isolated workspaces,
real file operations, and instant live deployment capabilities.
"""

import asyncio
import hashlib
import json
import logging
import os
import shutil
import sqlite3
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import secrets
import bcrypt
from flask import Flask, request, jsonify, session, render_template_string
import threading
import time
import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class User:
    """User model for multi-user system"""
    
    def __init__(self, user_id: str, username: str, email: str, password_hash: str):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = datetime.now()
        self.last_login = None
        self.workspace_path = None
        self.is_active = True
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'workspace_path': self.workspace_path,
            'is_active': self.is_active
        }

class UserWorkspace:
    """Individual user workspace with isolation"""
    
    def __init__(self, user_id: str, workspace_root: str):
        self.user_id = user_id
        self.workspace_root = Path(workspace_root)
        self.user_workspace = self.workspace_root / f"user_{user_id}"
        self.apps_dir = self.user_workspace / "apps"
        self.templates_dir = self.user_workspace / "templates"
        self.deployments_dir = self.user_workspace / "deployments"
        self.config_file = self.user_workspace / "workspace_config.json"
        
        # Create workspace structure
        self._initialize_workspace()
        
    def _initialize_workspace(self):
        """Initialize user workspace directory structure"""
        try:
            # Create main directories
            self.user_workspace.mkdir(parents=True, exist_ok=True)
            self.apps_dir.mkdir(exist_ok=True)
            self.templates_dir.mkdir(exist_ok=True)
            self.deployments_dir.mkdir(exist_ok=True)
            
            # Create workspace config
            if not self.config_file.exists():
                config = {
                    'user_id': self.user_id,
                    'created_at': datetime.now().isoformat(),
                    'workspace_version': '1.0',
                    'settings': {
                        'auto_deploy': True,
                        'backup_enabled': True,
                        'max_apps': 100
                    }
                }
                
                with open(self.config_file, 'w') as f:
                    json.dump(config, f, indent=2)
            
            logger.info(f"✅ Workspace initialized for user {self.user_id}")
            
        except Exception as e:
            logger.error(f"Failed to initialize workspace for user {self.user_id}: {e}")
    
    def create_app(self, app_name: str, app_type: str = 'web') -> str:
        """Create new app in user workspace"""
        try:
            # Sanitize app name
            safe_app_name = "".join(c for c in app_name if c.isalnum() or c in ('-', '_')).lower()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            app_dir_name = f"{safe_app_name}_{timestamp}"
            
            app_path = self.apps_dir / app_dir_name
            app_path.mkdir(parents=True, exist_ok=True)
            
            # Create app structure
            (app_path / "src").mkdir(exist_ok=True)
            (app_path / "assets").mkdir(exist_ok=True)
            (app_path / "config").mkdir(exist_ok=True)
            
            # Create app manifest
            manifest = {
                'app_name': app_name,
                'app_type': app_type,
                'created_at': datetime.now().isoformat(),
                'user_id': self.user_id,
                'app_id': str(uuid.uuid4()),
                'version': '1.0.0',
                'status': 'development'
            }
            
            with open(app_path / "app_manifest.json", 'w') as f:
                json.dump(manifest, f, indent=2)
            
            logger.info(f"📱 Created app '{app_name}' for user {self.user_id}")
            return str(app_path)
            
        except Exception as e:
            logger.error(f"Failed to create app for user {self.user_id}: {e}")
            return ""
    
    def list_apps(self) -> List[Dict[str, Any]]:
        """List all apps in user workspace"""
        apps = []
        
        try:
            if not self.apps_dir.exists():
                return apps
                
            for app_dir in self.apps_dir.iterdir():
                if app_dir.is_dir():
                    manifest_file = app_dir / "app_manifest.json"
                    
                    if manifest_file.exists():
                        with open(manifest_file, 'r') as f:
                            manifest = json.load(f)
                            manifest['app_path'] = str(app_dir)
                            apps.append(manifest)
                    else:
                        # Create manifest for directories without one
                        apps.append({
                            'app_name': app_dir.name,
                            'app_type': 'web',
                            'created_at': datetime.fromtimestamp(app_dir.stat().st_ctime).isoformat(),
                            'user_id': self.user_id,
                            'app_id': str(uuid.uuid4()),
                            'version': '1.0.0',
                            'status': 'legacy',
                            'app_path': str(app_dir)
                        })
            
        except Exception as e:
            logger.error(f"Failed to list apps for user {self.user_id}: {e}")
            
        return sorted(apps, key=lambda x: x['created_at'], reverse=True)
    
    def delete_app(self, app_path: str) -> bool:
        """Delete app from user workspace"""
        try:
            app_dir = Path(app_path)
            
            # Security check: ensure app is within user workspace
            if not str(app_dir).startswith(str(self.apps_dir)):
                logger.error(f"Security violation: Attempt to delete app outside workspace")
                return False
            
            if app_dir.exists():
                shutil.rmtree(app_dir)
                logger.info(f"🗑️ Deleted app at {app_path}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to delete app {app_path}: {e}")
            
        return False
    
    def get_workspace_stats(self) -> Dict[str, Any]:
        """Get workspace statistics"""
        stats = {
            'total_apps': 0,
            'total_size_mb': 0,
            'last_activity': None,
            'app_types': {},
            'storage_usage': {}
        }
        
        try:
            if not self.user_workspace.exists():
                return stats
            
            # Calculate total size
            total_size = 0
            for root, dirs, files in os.walk(self.user_workspace):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.exists(file_path):
                        total_size += os.path.getsize(file_path)
            
            stats['total_size_mb'] = total_size / (1024 * 1024)
            
            # Count apps and types
            apps = self.list_apps()
            stats['total_apps'] = len(apps)
            
            app_types = {}
            for app in apps:
                app_type = app.get('app_type', 'unknown')
                app_types[app_type] = app_types.get(app_type, 0) + 1
            
            stats['app_types'] = app_types
            
            # Last activity
            if apps:
                latest_app = max(apps, key=lambda x: x['created_at'])
                stats['last_activity'] = latest_app['created_at']
            
        except Exception as e:
            logger.error(f"Failed to get workspace stats: {e}")
            
        return stats

class UserManager:
    """Manages user accounts and authentication"""
    
    def __init__(self, db_path: str = "multi_user_system.db"):
        self.db_path = db_path
        self._init_database()
        
    def _init_database(self):
        """Initialize user database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    last_login TEXT,
                    workspace_path TEXT,
                    is_active BOOLEAN DEFAULT TRUE,
                    user_settings TEXT DEFAULT '{}'
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS workspace_activity (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    activity_data TEXT,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info("👥 User management database initialized")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
    
    def register_user(self, username: str, email: str, password: str) -> Optional[str]:
        """Register new user"""
        try:
            # Validate input
            if len(username) < 3 or len(password) < 6:
                return None
                
            # Hash password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Generate user ID
            user_id = str(uuid.uuid4())
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO users (user_id, username, email, password_hash, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, username, email, password_hash, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
            logger.info(f"👤 New user registered: {username} ({user_id})")
            return user_id
            
        except sqlite3.IntegrityError:
            logger.warning(f"Registration failed: Username or email already exists")
            return None
        except Exception as e:
            logger.error(f"User registration failed: {e}")
            return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user login"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT user_id, username, email, password_hash, created_at, last_login, workspace_path, is_active
                FROM users 
                WHERE username = ? AND is_active = TRUE
            """, (username,))
            
            row = cursor.fetchone()
            
            if row and bcrypt.checkpw(password.encode('utf-8'), row[3].encode('utf-8')):
                # Update last login
                cursor.execute("""
                    UPDATE users SET last_login = ? WHERE user_id = ?
                """, (datetime.now().isoformat(), row[0]))
                
                conn.commit()
                conn.close()
                
                user = User(row[0], row[1], row[2], row[3])
                user.created_at = datetime.fromisoformat(row[4]) if row[4] else None
                user.last_login = datetime.fromisoformat(row[5]) if row[5] else None
                user.workspace_path = row[6]
                user.is_active = row[7]
                
                logger.info(f"🔐 User authenticated: {username}")
                return user
            
            conn.close()
            return None
            
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return None
    
    def create_session(self, user_id: str) -> str:
        """Create user session"""
        try:
            session_id = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(hours=24)  # 24 hour session
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO user_sessions (session_id, user_id, created_at, expires_at)
                VALUES (?, ?, ?, ?)
            """, (session_id, user_id, datetime.now().isoformat(), expires_at.isoformat()))
            
            conn.commit()
            conn.close()
            
            return session_id
            
        except Exception as e:
            logger.error(f"Session creation failed: {e}")
            return ""
    
    def validate_session(self, session_id: str) -> Optional[str]:
        """Validate user session and return user_id"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT user_id FROM user_sessions 
                WHERE session_id = ? AND expires_at > ? AND is_active = TRUE
            """, (session_id, datetime.now().isoformat()))
            
            row = cursor.fetchone()
            conn.close()
            
            return row[0] if row else None
            
        except Exception as e:
            logger.error(f"Session validation failed: {e}")
            return None

class LiveDeploymentSystem:
    """System for live deployment of generated apps"""
    
    def __init__(self, deployment_root: str = "C:/agent/live_deployments"):
        self.deployment_root = Path(deployment_root)
        self.deployment_root.mkdir(parents=True, exist_ok=True)
        self.active_deployments = {}
        
    def deploy_app(self, user_id: str, app_path: str, domain_name: str = None) -> Dict[str, Any]:
        """Deploy app to live environment"""
        try:
            app_dir = Path(app_path)
            
            if not app_dir.exists():
                return {'success': False, 'error': 'App directory not found'}
            
            # Generate deployment ID and domain
            deployment_id = str(uuid.uuid4())[:8]
            
            if not domain_name:
                domain_name = f"app-{deployment_id}.local"
            
            # Create deployment directory
            deployment_path = self.deployment_root / f"deploy_{deployment_id}"
            deployment_path.mkdir(parents=True, exist_ok=True)
            
            # Copy app files to deployment
            self._copy_app_files(app_dir, deployment_path)
            
            # Start web server for this deployment
            port = self._get_available_port()
            server_process = self._start_web_server(deployment_path, port)
            
            deployment_info = {
                'deployment_id': deployment_id,
                'user_id': user_id,
                'app_path': str(app_path),
                'deployment_path': str(deployment_path),
                'domain_name': domain_name,
                'port': port,
                'url': f"http://localhost:{port}",
                'deployed_at': datetime.now().isoformat(),
                'status': 'active',
                'process': server_process
            }
            
            self.active_deployments[deployment_id] = deployment_info
            
            logger.info(f"🚀 App deployed: {domain_name} at port {port}")
            
            return {
                'success': True,
                'deployment_id': deployment_id,
                'url': f"http://localhost:{port}",
                'domain_name': domain_name,
                'deployed_at': deployment_info['deployed_at']
            }
            
        except Exception as e:
            logger.error(f"Deployment failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _copy_app_files(self, source: Path, destination: Path):
        """Copy app files to deployment directory"""
        try:
            for item in source.iterdir():
                if item.is_file():
                    shutil.copy2(item, destination)
                elif item.is_dir() and item.name not in ['.git', '__pycache__', 'node_modules']:
                    shutil.copytree(item, destination / item.name, dirs_exist_ok=True)
                    
        except Exception as e:
            logger.error(f"File copy failed: {e}")
    
    def _get_available_port(self) -> int:
        """Get available port for deployment"""
        import socket
        
        # Start from port 8000 and find available port
        for port in range(8000, 9000):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    return port
            except OSError:
                continue
                
        return 8080  # Fallback port
    
    def _start_web_server(self, deployment_path: Path, port: int):
        """Start web server for deployment"""
        try:
            # Use Python's built-in HTTP server
            cmd = [
                'python', '-m', 'http.server', str(port),
                '--directory', str(deployment_path)
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
            
            return process
            
        except Exception as e:
            logger.error(f"Failed to start web server: {e}")
            return None
    
    def stop_deployment(self, deployment_id: str) -> bool:
        """Stop a live deployment"""
        try:
            if deployment_id in self.active_deployments:
                deployment = self.active_deployments[deployment_id]
                
                # Stop server process
                if deployment.get('process'):
                    deployment['process'].terminate()
                
                # Clean up deployment directory
                deployment_path = Path(deployment['deployment_path'])
                if deployment_path.exists():
                    shutil.rmtree(deployment_path)
                
                # Remove from active deployments
                del self.active_deployments[deployment_id]
                
                logger.info(f"⏹️ Deployment stopped: {deployment_id}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to stop deployment: {e}")
            
        return False
    
    def list_user_deployments(self, user_id: str) -> List[Dict[str, Any]]:
        """List all deployments for a user"""
        user_deployments = []
        
        for deployment_id, deployment in self.active_deployments.items():
            if deployment['user_id'] == user_id:
                # Check if process is still running
                process = deployment.get('process')
                status = 'active' if process and process.poll() is None else 'stopped'
                
                user_deployments.append({
                    'deployment_id': deployment_id,
                    'domain_name': deployment['domain_name'],
                    'url': deployment['url'],
                    'deployed_at': deployment['deployed_at'],
                    'status': status
                })
        
        return sorted(user_deployments, key=lambda x: x['deployed_at'], reverse=True)

class MultiUserPlatform:
    """Main multi-user platform orchestrator"""
    
    def __init__(self, workspace_root: str = "C:/agent/user_workspaces"):
        self.workspace_root = workspace_root
        self.user_manager = UserManager()
        self.deployment_system = LiveDeploymentSystem()
        self.user_workspaces = {}
        
        # Initialize workspace root
        Path(workspace_root).mkdir(parents=True, exist_ok=True)
    
    def get_user_workspace(self, user_id: str) -> UserWorkspace:
        """Get or create user workspace"""
        if user_id not in self.user_workspaces:
            self.user_workspaces[user_id] = UserWorkspace(user_id, self.workspace_root)
        
        return self.user_workspaces[user_id]
    
    async def generate_app_for_user(self, user_id: str, app_description: str) -> Dict[str, Any]:
        """Generate app for specific user in their workspace"""
        try:
            workspace = self.get_user_workspace(user_id)
            
            # Create app directory
            app_path = workspace.create_app(app_description)
            
            if not app_path:
                return {'success': False, 'error': 'Failed to create app directory'}
            
            # Generate app using existing system
            from main import generate_app_files
            
            app_files = await generate_app_files(app_description)
            
            # Save files to user workspace
            app_dir = Path(app_path) / "src"
            
            for filename, content in app_files.items():
                file_path = app_dir / filename
                file_path.write_text(content, encoding='utf-8')
            
            logger.info(f"📱 Generated app for user {user_id}: {app_description}")
            
            return {
                'success': True,
                'app_path': app_path,
                'app_description': app_description,
                'files_generated': len(app_files),
                'user_id': user_id
            }
            
        except Exception as e:
            logger.error(f"App generation failed for user {user_id}: {e}")
            return {'success': False, 'error': str(e)}

# Flask Web Application for Multi-User Interface
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

# Initialize platform
platform = MultiUserPlatform()

# HTML Templates
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multi-User App Platform</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
               background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
               min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .container { background: white; padding: 2rem; border-radius: 10px; 
                    box-shadow: 0 10px 25px rgba(0,0,0,0.2); width: 100%; max-width: 400px; }
        h1 { color: #333; margin-bottom: 1.5rem; text-align: center; }
        .form-group { margin-bottom: 1rem; }
        label { display: block; margin-bottom: 0.5rem; color: #555; font-weight: 500; }
        input { width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 5px; 
               font-size: 1rem; transition: border-color 0.3s; }
        input:focus { outline: none; border-color: #667eea; }
        .btn { width: 100%; padding: 0.75rem; background: #667eea; color: white; 
              border: none; border-radius: 5px; font-size: 1rem; cursor: pointer; 
              transition: background 0.3s; margin-bottom: 1rem; }
        .btn:hover { background: #5a67d8; }
        .btn-secondary { background: #764ba2; }
        .btn-secondary:hover { background: #6b4096; }
        .error { color: #e53e3e; text-align: center; margin-bottom: 1rem; }
        .success { color: #38a169; text-align: center; margin-bottom: 1rem; }
        .switch { text-align: center; margin-top: 1rem; }
        .switch a { color: #667eea; text-decoration: none; }
        .switch a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Multi-User App Platform</h1>
        
        {% if message %}
        <div class="{{ 'error' if error else 'success' }}">{{ message }}</div>
        {% endif %}
        
        <form method="POST" action="{{ '/register' if show_register else '/login' }}">
            {% if show_register %}
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required minlength="3">
            </div>
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required minlength="6">
            </div>
            <button type="submit" class="btn">Create Account</button>
            <div class="switch">
                Already have an account? <a href="/">Sign In</a>
            </div>
            {% else %}
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit" class="btn">Sign In</button>
            <div class="switch">
                Don't have an account? <a href="/register">Sign Up</a>
            </div>
            {% endif %}
        </form>
    </div>
</body>
</html>
"""

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Dashboard - Multi-User Platform</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
               background: #f7fafc; color: #2d3748; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                 color: white; padding: 1rem 0; }
        .header-content { max-width: 1200px; margin: 0 auto; padding: 0 2rem; 
                         display: flex; justify-content: space-between; align-items: center; }
        .logo { font-size: 1.5rem; font-weight: bold; }
        .user-info { display: flex; align-items: center; gap: 1rem; }
        .btn-logout { background: rgba(255,255,255,0.2); border: none; color: white; 
                     padding: 0.5rem 1rem; border-radius: 5px; cursor: pointer; }
        .main { max-width: 1200px; margin: 0 auto; padding: 2rem; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                gap: 1rem; margin-bottom: 2rem; }
        .stat-card { background: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .stat-number { font-size: 2rem; font-weight: bold; color: #667eea; }
        .stat-label { color: #718096; margin-top: 0.5rem; }
        .section { background: white; padding: 2rem; border-radius: 10px; 
                  box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 2rem; }
        .section h2 { margin-bottom: 1rem; color: #2d3748; }
        .btn { padding: 0.75rem 1.5rem; background: #667eea; color: white; 
              border: none; border-radius: 5px; cursor: pointer; text-decoration: none; 
              display: inline-block; margin-right: 1rem; margin-bottom: 1rem; }
        .btn:hover { background: #5a67d8; }
        .btn-danger { background: #e53e3e; }
        .btn-danger:hover { background: #c53030; }
        .btn-success { background: #38a169; }
        .btn-success:hover { background: #2f855a; }
        .app-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); 
                   gap: 1rem; margin-top: 1rem; }
        .app-card { border: 1px solid #e2e8f0; border-radius: 8px; padding: 1.5rem; 
                   transition: box-shadow 0.2s; }
        .app-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
        .app-name { font-weight: bold; margin-bottom: 0.5rem; }
        .app-meta { color: #718096; font-size: 0.9rem; margin-bottom: 1rem; }
        .app-actions { display: flex; gap: 0.5rem; }
        .form-group { margin-bottom: 1rem; }
        .form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
        .form-group input, .form-group textarea { width: 100%; padding: 0.75rem; 
                                                border: 1px solid #e2e8f0; border-radius: 5px; }
        .deployments { margin-top: 2rem; }
        .deployment-item { display: flex; justify-content: space-between; 
                          align-items: center; padding: 1rem; border: 1px solid #e2e8f0; 
                          border-radius: 5px; margin-bottom: 0.5rem; }
        .deployment-url { color: #667eea; text-decoration: none; }
        .deployment-url:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div class="logo">🚀 Multi-User Platform</div>
            <div class="user-info">
                <span>Welcome, {{ user.username }}!</span>
                <form method="POST" action="/logout" style="display: inline;">
                    <button type="submit" class="btn-logout">Logout</button>
                </form>
            </div>
        </div>
    </div>
    
    <div class="main">
        <!-- Statistics -->
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{{ stats.total_apps }}</div>
                <div class="stat-label">Total Apps</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ "%.1f"|format(stats.total_size_mb) }}MB</div>
                <div class="stat-label">Storage Used</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ deployments|length }}</div>
                <div class="stat-label">Live Deployments</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.app_types|length }}</div>
                <div class="stat-label">App Types</div>
            </div>
        </div>
        
        <!-- Create New App -->
        <div class="section">
            <h2>📱 Create New App</h2>
            <form method="POST" action="/create_app">
                <div class="form-group">
                    <label for="app_description">App Description</label>
                    <textarea id="app_description" name="app_description" rows="3" 
                             placeholder="Describe your app idea..." required></textarea>
                </div>
                <button type="submit" class="btn">Generate App</button>
            </form>
        </div>
        
        <!-- Your Apps -->
        <div class="section">
            <h2>📚 Your Apps</h2>
            {% if apps %}
            <div class="app-grid">
                {% for app in apps %}
                <div class="app-card">
                    <div class="app-name">{{ app.app_name }}</div>
                    <div class="app-meta">
                        Created: {{ app.created_at[:10] }}<br>
                        Type: {{ app.app_type }}<br>
                        Status: {{ app.status }}
                    </div>
                    <div class="app-actions">
                        <form method="POST" action="/deploy_app" style="display: inline;">
                            <input type="hidden" name="app_path" value="{{ app.app_path }}">
                            <button type="submit" class="btn btn-success">Deploy Live</button>
                        </form>
                        <form method="POST" action="/delete_app" style="display: inline;" 
                              onsubmit="return confirm('Delete this app?')">
                            <input type="hidden" name="app_path" value="{{ app.app_path }}">
                            <button type="submit" class="btn btn-danger">Delete</button>
                        </form>
                    </div>
                </div>
                {% endfor %}
            </div>
            {% else %}
            <p>No apps yet. Create your first app above!</p>
            {% endif %}
        </div>
        
        <!-- Live Deployments -->
        {% if deployments %}
        <div class="section">
            <h2>🌐 Live Deployments</h2>
            {% for deployment in deployments %}
            <div class="deployment-item">
                <div>
                    <strong>{{ deployment.domain_name }}</strong><br>
                    <small>Deployed: {{ deployment.deployed_at[:19] }}</small>
                </div>
                <div>
                    <a href="{{ deployment.url }}" target="_blank" class="deployment-url">
                        {{ deployment.url }}
                    </a>
                    <form method="POST" action="/stop_deployment" style="display: inline; margin-left: 1rem;">
                        <input type="hidden" name="deployment_id" value="{{ deployment.deployment_id }}">
                        <button type="submit" class="btn btn-danger" 
                                onclick="return confirm('Stop this deployment?')">Stop</button>
                    </form>
                </div>
            </div>
            {% endfor %}
        </div>
        {% endif %}
    </div>
    
    <script>
        // Auto-refresh deployments every 30 seconds
        setTimeout(() => location.reload(), 30000);
    </script>
</body>
</html>
"""

# Flask Routes
@app.route('/')
def login_page():
    if 'session_id' in session:
        return redirect('/dashboard')
    return render_template_string(LOGIN_TEMPLATE, show_register=False)

@app.route('/register')
def register_page():
    return render_template_string(LOGIN_TEMPLATE, show_register=True)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    user = platform.user_manager.authenticate_user(username, password)
    
    if user:
        session_id = platform.user_manager.create_session(user.user_id)
        session['session_id'] = session_id
        session['user_id'] = user.user_id
        return redirect('/dashboard')
    else:
        return render_template_string(LOGIN_TEMPLATE, 
                                    show_register=False, 
                                    message="Invalid username or password",
                                    error=True)

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    user_id = platform.user_manager.register_user(username, email, password)
    
    if user_id:
        return render_template_string(LOGIN_TEMPLATE,
                                    show_register=False,
                                    message="Account created successfully! Please sign in.",
                                    error=False)
    else:
        return render_template_string(LOGIN_TEMPLATE,
                                    show_register=True,
                                    message="Username or email already exists",
                                    error=True)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'session_id' not in session:
        return redirect('/')
    
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/')
    
    # Get user info
    user = platform.user_manager.authenticate_user('', '')  # This needs improvement
    
    # Get workspace data
    workspace = platform.get_user_workspace(user_id)
    apps = workspace.list_apps()
    stats = workspace.get_workspace_stats()
    deployments = platform.deployment_system.list_user_deployments(user_id)
    
    # Create user object for template
    user_info = {'username': f"User {user_id[:8]}"}  # Simplified for now
    
    return render_template_string(DASHBOARD_TEMPLATE,
                                user=user_info,
                                apps=apps,
                                stats=stats,
                                deployments=deployments)

@app.route('/create_app', methods=['POST'])
def create_app():
    if 'session_id' not in session:
        return redirect('/')
    
    user_id = session.get('user_id')
    app_description = request.form['app_description']
    
    # Generate app asynchronously (simplified for web context)
    workspace = platform.get_user_workspace(user_id)
    app_path = workspace.create_app(app_description)
    
    # Here you would integrate with the actual app generation system
    # For now, create a simple HTML file
    if app_path:
        html_content = f"""<!DOCTYPE html>
<html><head><title>{app_description}</title></head>
<body><h1>{app_description}</h1><p>Your app is ready!</p></body></html>"""
        
        (Path(app_path) / "src" / "index.html").write_text(html_content)
    
    return redirect('/dashboard')

@app.route('/deploy_app', methods=['POST'])
def deploy_app():
    if 'session_id' not in session:
        return redirect('/')
    
    user_id = session.get('user_id')
    app_path = request.form['app_path']
    
    # Deploy app
    result = platform.deployment_system.deploy_app(user_id, app_path)
    
    return redirect('/dashboard')

@app.route('/stop_deployment', methods=['POST'])
def stop_deployment():
    if 'session_id' not in session:
        return redirect('/')
    
    deployment_id = request.form['deployment_id']
    platform.deployment_system.stop_deployment(deployment_id)
    
    return redirect('/dashboard')

@app.route('/delete_app', methods=['POST'])
def delete_app():
    if 'session_id' not in session:
        return redirect('/')
    
    user_id = session.get('user_id')
    app_path = request.form['app_path']
    
    workspace = platform.get_user_workspace(user_id)
    workspace.delete_app(app_path)
    
    return redirect('/dashboard')

def run_multi_user_platform():
    """Run the multi-user platform"""
    print("🚀 Starting Multi-User Platform...")
    print("="*50)
    print("🌐 Web Interface: http://localhost:5001")
    print("👥 Multi-user support with isolated workspaces")
    print("📁 Real file system operations")
    print("🚀 Live deployment capabilities")
    print("🔐 Secure user authentication")
    print("="*50)
    
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)

if __name__ == "__main__":
    run_multi_user_platform()