#!/usr/bin/env python3
"""
🏥 Lovable Clone - System Health Check
ตรวจสอบสุขภาพระบบทั้งหมด พร้อมรายงานปัญหาและวิธีแก้ไข
"""

import os
import sys
import subprocess
import requests
import json
from pathlib import Path
import time

class HealthChecker:
    def __init__(self):
        self.base_path = Path("C:/agent")
        self.results = []
        
    def print_header(self):
        print("=" * 50)
        print("🏥 LOVABLE CLONE - SYSTEM HEALTH CHECK")
        print("=" * 50)
        print()
        
    def check_files(self):
        """ตรวจสอบไฟล์สำคัญ"""
        print("📁 Checking Critical Files...")
        
        critical_files = [
            "lovable_landing.html",
            "lovable_chat.html", 
            "apps/orchestrator/main.py",
            "apps/orchestrator/requirements.txt",
            "docker-compose.yml",
            "TESTING_GUIDE.md"
        ]
        
        for file in critical_files:
            path = self.base_path / file
            if path.exists():
                print(f"   ✅ {file}")
                self.results.append(("FILE", file, "OK"))
            else:
                print(f"   ❌ {file} - MISSING!")
                self.results.append(("FILE", file, "MISSING"))
        print()
        
    def check_python_env(self):
        """ตรวจสอบ Python environment"""
        print("🐍 Checking Python Environment...")
        
        try:
            version = sys.version.split()[0]
            print(f"   ✅ Python version: {version}")
            self.results.append(("PYTHON", "version", version))
            
            # Check required packages
            required_packages = [
                "fastapi", "uvicorn", "openai", "requests", 
                "jinja2", "aiofiles", "python-multipart"
            ]
            
            for package in required_packages:
                try:
                    __import__(package)
                    print(f"   ✅ {package}")
                    self.results.append(("PACKAGE", package, "OK"))
                except ImportError:
                    print(f"   ❌ {package} - NOT INSTALLED!")
                    self.results.append(("PACKAGE", package, "MISSING"))
                    
        except Exception as e:
            print(f"   ❌ Python check failed: {e}")
            self.results.append(("PYTHON", "check", f"ERROR: {e}"))
        print()
        
    def check_api_server(self):
        """ตรวจสอบ API server"""
        print("🌐 Checking API Server...")
        
        try:
            # Try to connect to FastAPI server
            response = requests.get("http://localhost:8001/health", timeout=5)
            if response.status_code == 200:
                print("   ✅ FastAPI server is running")
                self.results.append(("API", "server", "RUNNING"))
            else:
                print(f"   ⚠️ Server responding with status: {response.status_code}")
                self.results.append(("API", "server", f"STATUS_{response.status_code}"))
                
        except requests.exceptions.ConnectionError:
            print("   ❌ FastAPI server not running")
            self.results.append(("API", "server", "NOT_RUNNING"))
        except Exception as e:
            print(f"   ❌ API check failed: {e}")
            self.results.append(("API", "server", f"ERROR: {e}"))
        print()
        
    def check_ports(self):
        """ตรวจสอบ ports"""
        print("🔌 Checking Ports...")
        
        important_ports = [8001, 8000, 3000]
        
        for port in important_ports:
            try:
                # Simple socket check
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex(('localhost', port))
                sock.close()
                
                if result == 0:
                    print(f"   ✅ Port {port} is in use")
                    self.results.append(("PORT", str(port), "IN_USE"))
                else:
                    print(f"   ⚪ Port {port} is available")
                    self.results.append(("PORT", str(port), "AVAILABLE"))
                    
            except Exception as e:
                print(f"   ❌ Port {port} check failed: {e}")
                self.results.append(("PORT", str(port), f"ERROR: {e}"))
        print()
        
    def check_docker(self):
        """ตรวจสอบ Docker"""
        print("🐳 Checking Docker...")
        
        try:
            result = subprocess.run(["docker", "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"   ✅ {version}")
                self.results.append(("DOCKER", "version", "OK"))
                
                # Check docker-compose
                result = subprocess.run(["docker-compose", "--version"], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"   ✅ Docker Compose available")
                    self.results.append(("DOCKER", "compose", "OK"))
                else:
                    print("   ⚠️ Docker Compose not available")
                    self.results.append(("DOCKER", "compose", "NOT_AVAILABLE"))
                    
            else:
                print("   ❌ Docker not available")
                self.results.append(("DOCKER", "version", "NOT_AVAILABLE"))
                
        except Exception as e:
            print(f"   ❌ Docker check failed: {e}")
            self.results.append(("DOCKER", "check", f"ERROR: {e}"))
        print()
        
    def check_environment_vars(self):
        """ตรวจสอบ environment variables"""
        print("🔐 Checking Environment Variables...")
        
        env_file = self.base_path / ".env"
        if env_file.exists():
            print("   ✅ .env file exists")
            self.results.append(("ENV", "file", "EXISTS"))
            
            # Check for important variables
            important_vars = ["OPENAI_API_KEY", "SECRET_KEY"]
            
            with open(env_file, 'r') as f:
                content = f.read()
                
            for var in important_vars:
                if var in content and f"{var}=" in content:
                    print(f"   ✅ {var} is set")
                    self.results.append(("ENV", var, "SET"))
                else:
                    print(f"   ⚠️ {var} not found")
                    self.results.append(("ENV", var, "NOT_SET"))
        else:
            print("   ❌ .env file not found")
            self.results.append(("ENV", "file", "NOT_FOUND"))
        print()
        
    def generate_report(self):
        """สร้างรายงานผล"""
        print("📊 HEALTH CHECK REPORT")
        print("-" * 30)
        
        total_checks = len(self.results)
        passed_checks = len([r for r in self.results if r[2] in ["OK", "RUNNING", "EXISTS", "SET"]])
        
        print(f"Total Checks: {total_checks}")
        print(f"Passed: {passed_checks}")
        print(f"Issues: {total_checks - passed_checks}")
        print(f"Health Score: {(passed_checks/total_checks)*100:.1f}%")
        print()
        
        # Show issues
        issues = [r for r in self.results if r[2] not in ["OK", "RUNNING", "EXISTS", "SET", "IN_USE", "AVAILABLE"]]
        
        if issues:
            print("🚨 ISSUES FOUND:")
            for category, item, status in issues:
                print(f"   • {category}: {item} - {status}")
            print()
            
            print("💡 SUGGESTED FIXES:")
            self.suggest_fixes(issues)
        else:
            print("🎉 ALL CHECKS PASSED!")
            
    def suggest_fixes(self, issues):
        """แนะนำวิธีแก้ปัญหา"""
        for category, item, status in issues:
            if category == "FILE" and "MISSING" in status:
                print(f"   → Missing file {item}: Re-run the setup script")
                
            elif category == "PACKAGE" and "MISSING" in status:
                print(f"   → Install {item}: pip install {item}")
                
            elif category == "API" and "NOT_RUNNING" in status:
                print("   → Start API server: cd apps/orchestrator && python main.py")
                
            elif category == "DOCKER" and "NOT_AVAILABLE" in status:
                print("   → Install Docker Desktop from docker.com")
                
            elif category == "ENV" and "NOT_SET" in status:
                print(f"   → Set {item} in .env file")
                
    def run_full_check(self):
        """รันการตรวจสอบทั้งหมด"""
        self.print_header()
        
        self.check_files()
        self.check_python_env()
        self.check_docker()
        self.check_environment_vars()
        self.check_ports()
        self.check_api_server()
        
        self.generate_report()

if __name__ == "__main__":
    checker = HealthChecker()
    checker.run_full_check()