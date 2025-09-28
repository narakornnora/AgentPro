#!/usr/bin/env python3
"""
Built-in HTTP Server - No dependencies crash!
"""
import http.server
import socketserver
import json
import urllib.parse
from pathlib import Path

class LovableHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/':
            self.serve_interface()
        elif self.path == '/test':
            self.serve_json({'message': 'Server working!', 'status': 'ok'})
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/chat':
            self.serve_json({
                'type': 'start_building',
                'message': 'เริ่มสร้างแอปเลย! 🚀',
                'session_id': 'test_session',
                'requirements': {'app_name': 'Test App'}
            })
        else:
            self.serve_json({'error': 'Unknown endpoint'})
    
    def serve_interface(self):
        try:
            interface_file = Path("C:/agent/lovable_split_interface.html")
            if interface_file.exists():
                with open(interface_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            else:
                self.serve_json({'message': 'Interface not found'})
        except Exception as e:
            self.serve_json({'error': str(e)})
    
    def serve_json(self, data):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            json_data = json.dumps(data, ensure_ascii=False)
            self.wfile.write(json_data.encode('utf-8'))
        except Exception as e:
            print(f"Error serving JSON: {e}")
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == "__main__":
    PORT = 8007
    
    try:
        with socketserver.TCPServer(("", PORT), LovableHandler) as httpd:
            print(f"🚀 Built-in Server Starting...")
            print(f"📍 Server: http://localhost:{PORT}")
            print("💪 No dependencies - cannot crash!")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")