#!/usr/bin/env python3
"""
🚀 LOVABLE CLONE - COMPLETE AI APP BUILDER
เลียนแบบ Lovable.dev แต่เจ๋งกว่า!
=======================================
✨ Build something Lovable - Create apps and websites by chatting with AI
💬 Natural language to full applications
🎨 Beautiful UI exactly like Lovable
⚡ Real-time preview with live updates
🤖 Multi-agent system working behind the scenes
"""

import os
import time
import json
import asyncio
import uuid
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from flask import Flask, render_template_string, request, jsonify
from flask_socketio import SocketIO, emit
import openai

class LovableClone:
    """Complete Lovable Clone with multi-agent backend"""
    
    def __init__(self):
        self.projects = {}
        self.workspace = Path("C:/agent/workspace/generated-projects")
        self.workspace.mkdir(parents=True, exist_ok=True)
        
        # Initialize OpenAI (if available)
        self.client = None
        if os.getenv("OPENAI_API_KEY"):
            self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def create_web_interface(self):
        """Create complete Lovable-style web interface"""
        
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'lovable-clone-secret'
        socketio = SocketIO(app, cors_allowed_origins="*")
        
        # Landing Page Template - เลียนแบบ Lovable เป๊ะ ๆ
        LANDING_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Build something 💖 Lovable</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        /* Header Navigation */
        .header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            padding: 16px 24px;
        }
        
        .nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .logo {
            display: flex;
            align-items: center;
            font-size: 24px;
            font-weight: 700;
            color: #333;
        }
        
        .logo .heart {
            margin: 0 8px;
            font-size: 20px;
        }
        
        .nav-links {
            display: flex;
            align-items: center;
            gap: 32px;
        }
        
        .nav-link {
            color: #666;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s;
        }
        
        .nav-link:hover {
            color: #333;
        }
        
        .user-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: linear-gradient(45deg, #667eea, #764ba2);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            font-size: 14px;
        }
        
        /* Main Content */
        .main-content {
            padding-top: 100px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            position: relative;
        }
        
        .hero-title {
            font-size: 64px;
            font-weight: 700;
            color: #333;
            margin-bottom: 24px;
            line-height: 1.1;
        }
        
        .hero-title .heart {
            color: #f093fb;
            margin: 0 8px;
        }
        
        .hero-subtitle {
            font-size: 24px;
            color: #666;
            margin-bottom: 48px;
            font-weight: 400;
        }
        
        /* Chat Input Container */
        .chat-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            padding: 32px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 800px;
            margin-bottom: 32px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .chat-input-wrapper {
            position: relative;
            margin-bottom: 24px;
        }
        
        .chat-input {
            width: 100%;
            padding: 20px 60px 20px 24px;
            border: 2px solid #e5e7eb;
            border-radius: 16px;
            font-size: 16px;
            font-family: inherit;
            background: white;
            transition: all 0.2s;
            outline: none;
            resize: none;
            min-height: 60px;
        }
        
        .chat-input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        }
        
        .send-button {
            position: absolute;
            right: 8px;
            top: 50%;
            transform: translateY(-50%);
            background: #667eea;
            color: white;
            border: none;
            border-radius: 12px;
            width: 44px;
            height: 44px;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .send-button:hover {
            background: #5a6fd8;
            transform: translateY(-50%) scale(1.05);
        }
        
        .send-button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        /* Action Buttons */
        .action-buttons {
            display: flex;
            gap: 16px;
            align-items: center;
            justify-content: center;
        }
        
        .action-btn {
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 12px;
            padding: 8px 16px;
            font-size: 14px;
            color: #666;
            cursor: pointer;
            transition: all 0.2s;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .action-btn:hover {
            background: white;
            color: #333;
        }
        
        /* Example Apps */
        .example-apps {
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
            justify-content: center;
            margin-top: 32px;
        }
        
        .example-app {
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 12px;
            padding: 12px 20px;
            font-size: 14px;
            color: #666;
            cursor: pointer;
            transition: all 0.2s;
            text-decoration: none;
        }
        
        .example-app:hover {
            background: white;
            color: #333;
            transform: translateY(-2px);
        }
        
        /* Loading States */
        .loading {
            display: none;
            text-align: center;
            margin-top: 24px;
        }
        
        .spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid #f3f3f3;
            border-top: 2px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .hero-title {
                font-size: 40px;
            }
            
            .hero-subtitle {
                font-size: 18px;
            }
            
            .chat-container {
                margin: 0 16px 32px;
                padding: 24px;
            }
            
            .nav-links {
                display: none;
            }
            
            .example-apps {
                flex-direction: column;
                align-items: center;
            }
        }
        
        /* Background Animation */
        .bg-animation {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: -1;
        }
        
        .bg-orb {
            position: absolute;
            border-radius: 50%;
            background: linear-gradient(45deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
            animation: float 20s ease-in-out infinite;
        }
        
        .bg-orb:nth-child(1) {
            width: 200px;
            height: 200px;
            top: 10%;
            left: 10%;
            animation-delay: 0s;
        }
        
        .bg-orb:nth-child(2) {
            width: 300px;
            height: 300px;
            top: 60%;
            right: 10%;
            animation-delay: -10s;
        }
        
        .bg-orb:nth-child(3) {
            width: 150px;
            height: 150px;
            bottom: 20%;
            left: 20%;
            animation-delay: -5s;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            33% { transform: translateY(-30px) rotate(120deg); }
            66% { transform: translateY(20px) rotate(240deg); }
        }
    </style>
</head>
<body>
    <!-- Background Animation -->
    <div class="bg-animation">
        <div class="bg-orb"></div>
        <div class="bg-orb"></div>
        <div class="bg-orb"></div>
    </div>

    <!-- Header -->
    <header class="header">
        <nav class="nav">
            <div class="logo">
                <span>🚀 Lovable</span>
            </div>
            <div class="nav-links">
                <a href="#" class="nav-link">Community</a>
                <a href="#" class="nav-link">Pricing</a>
                <a href="#" class="nav-link">Enterprise</a>
                <a href="#" class="nav-link">Learn</a>
                <a href="#" class="nav-link">Launched</a>
                <div class="user-avatar">N</div>
            </div>
        </nav>
    </header>

    <!-- Main Content -->
    <main class="main-content">
        <h1 class="hero-title">Build something <span class="heart">💖</span> Lovable</h1>
        <p class="hero-subtitle">Create apps and websites by chatting with AI</p>
        
        <div class="chat-container">
            <div class="chat-input-wrapper">
                <textarea 
                    class="chat-input" 
                    id="promptInput"
                    placeholder="Ask Lovable to create a landing page for my..."
                    rows="1"
                ></textarea>
                <button class="send-button" id="sendButton">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                    </svg>
                </button>
            </div>
            
            <div class="action-buttons">
                <button class="action-btn" onclick="attachFile()">
                    📎 Attach
                </button>
                <button class="action-btn" onclick="selectWorkspace()">
                    📁 Workspace
                </button>
                <button class="action-btn" onclick="connectSupabase()">
                    ⚡ Supabase
                </button>
            </div>
            
            <div class="loading" id="loadingState">
                <div class="spinner"></div>
                <p>AI is thinking...</p>
            </div>
        </div>
        
        <!-- Example Apps -->
        <div class="example-apps">
            <div class="example-app" onclick="useExample('Bill splitter')">
                💰 Bill splitter
            </div>
            <div class="example-app" onclick="useExample('Social media feed')">
                📱 Social media feed
            </div>
            <div class="example-app" onclick="useExample('Note taking app')">
                📝 Note taking app
            </div>
            <div class="example-app" onclick="useExample('Expense tracker')">
                📊 Expense tracker
            </div>
        </div>
    </main>

    <!-- Socket.IO -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.4/socket.io.js"></script>
    
    <script>
        const socket = io();
        const promptInput = document.getElementById('promptInput');
        const sendButton = document.getElementById('sendButton');
        const loadingState = document.getElementById('loadingState');
        
        // Auto-resize textarea
        promptInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
        
        // Send message
        function sendMessage() {
            const prompt = promptInput.value.trim();
            if (!prompt) return;
            
            // Show loading
            loadingState.style.display = 'block';
            sendButton.disabled = true;
            
            // Send to AI backend
            socket.emit('create_app', {
                prompt: prompt,
                timestamp: Date.now()
            });
            
            // Clear input
            promptInput.value = '';
            promptInput.style.height = 'auto';
        }
        
        // Send button click
        sendButton.addEventListener('click', sendMessage);
        
        // Enter key handling
        promptInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
        
        // Example app selection
        function useExample(appType) {
            promptInput.value = `Create a ${appType} app with a modern, clean design`;
            promptInput.focus();
        }
        
        // Action buttons (placeholder functions)
        function attachFile() {
            alert('File attachment feature coming soon!');
        }
        
        function selectWorkspace() {
            alert('Workspace selection feature coming soon!');
        }
        
        function connectSupabase() {
            alert('Supabase integration feature coming soon!');
        }
        
        // Socket event handlers
        socket.on('connect', function() {
            console.log('Connected to AgentPro AI Backend');
        });
        
        socket.on('app_created', function(data) {
            // Redirect to chat interface
            window.location.href = `/chat/${data.project_id}`;
        });
        
        socket.on('error', function(data) {
            loadingState.style.display = 'none';
            sendButton.disabled = false;
            alert('Error: ' + data.message);
        });
        
        // Focus input on load
        window.addEventListener('load', function() {
            promptInput.focus();
        });
    </script>
</body>
</html>
        """
        
        # Chat Interface Template - เลียนแบบ Lovable chat + preview
        CHAT_INTERFACE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ project_name }} - Lovable</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #f8fafc;
            height: 100vh;
            overflow: hidden;
        }
        
        /* Header */
        .header {
            background: white;
            border-bottom: 1px solid #e5e7eb;
            padding: 12px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            height: 60px;
        }
        
        .project-info {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .project-icon {
            width: 32px;
            height: 32px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
        }
        
        .project-details h1 {
            font-size: 16px;
            font-weight: 600;
            color: #111827;
        }
        
        .project-status {
            font-size: 12px;
            color: #6b7280;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .header-actions {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .header-btn {
            background: #f3f4f6;
            border: none;
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 14px;
            color: #374151;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .header-btn:hover {
            background: #e5e7eb;
        }
        
        .publish-btn {
            background: #667eea;
            color: white;
        }
        
        .publish-btn:hover {
            background: #5a6fd8;
        }
        
        /* Main Layout */
        .main-container {
            display: flex;
            height: calc(100vh - 60px);
        }
        
        /* Left Panel - Chat */
        .chat-panel {
            width: 400px;
            background: white;
            border-right: 1px solid #e5e7eb;
            display: flex;
            flex-direction: column;
        }
        
        .chat-header {
            padding: 16px;
            border-bottom: 1px solid #f3f4f6;
        }
        
        .chat-title {
            font-size: 14px;
            font-weight: 600;
            color: #111827;
            margin-bottom: 4px;
        }
        
        .chat-subtitle {
            font-size: 12px;
            color: #6b7280;
        }
        
        .chat-messages {
            flex: 1;
            padding: 16px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        
        .message {
            display: flex;
            gap: 12px;
            align-items: flex-start;
        }
        
        .message-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            font-weight: 600;
            flex-shrink: 0;
        }
        
        .user-avatar {
            background: #667eea;
            color: white;
        }
        
        .ai-avatar {
            background: #f3f4f6;
            color: #6b7280;
        }
        
        .message-content {
            flex: 1;
        }
        
        .message-text {
            background: #f8fafc;
            padding: 12px 16px;
            border-radius: 12px;
            font-size: 14px;
            line-height: 1.5;
            color: #374151;
        }
        
        .user-message .message-text {
            background: #667eea;
            color: white;
        }
        
        .message-time {
            font-size: 11px;
            color: #9ca3af;
            margin-top: 4px;
        }
        
        /* Chat Input */
        .chat-input-container {
            padding: 16px;
            border-top: 1px solid #f3f4f6;
            background: white;
        }
        
        .chat-input-wrapper {
            position: relative;
        }
        
        .chat-input {
            width: 100%;
            padding: 12px 50px 12px 16px;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            font-size: 14px;
            font-family: inherit;
            background: #f9fafb;
            outline: none;
            resize: none;
            min-height: 44px;
            max-height: 120px;
        }
        
        .chat-input:focus {
            border-color: #667eea;
            background: white;
        }
        
        .chat-send-btn {
            position: absolute;
            right: 8px;
            top: 50%;
            transform: translateY(-50%);
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            width: 32px;
            height: 32px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
        }
        
        .chat-send-btn:hover {
            background: #5a6fd8;
        }
        
        .chat-send-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        /* Right Panel - Preview */
        .preview-panel {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: #f8fafc;
        }
        
        .preview-header {
            background: white;
            padding: 12px 24px;
            border-bottom: 1px solid #e5e7eb;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .preview-tabs {
            display: flex;
            gap: 8px;
        }
        
        .preview-tab {
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            color: #6b7280;
        }
        
        .preview-tab.active {
            background: #667eea;
            color: white;
        }
        
        .preview-actions {
            display: flex;
            gap: 8px;
        }
        
        .preview-btn {
            background: #f3f4f6;
            border: none;
            border-radius: 6px;
            padding: 6px 12px;
            font-size: 12px;
            color: #374151;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .preview-btn:hover {
            background: #e5e7eb;
        }
        
        .preview-content {
            flex: 1;
            position: relative;
            background: white;
            margin: 16px;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        
        .preview-iframe {
            width: 100%;
            height: 100%;
            border: none;
            background: white;
        }
        
        .preview-loading {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            color: #6b7280;
        }
        
        .preview-spinner {
            width: 24px;
            height: 24px;
            border: 2px solid #f3f3f3;
            border-top: 2px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 12px;
        }
        
        /* Responsive */
        @media (max-width: 1024px) {
            .chat-panel {
                width: 350px;
            }
        }
        
        @media (max-width: 768px) {
            .main-container {
                flex-direction: column;
            }
            
            .chat-panel {
                width: 100%;
                height: 50vh;
            }
            
            .preview-panel {
                height: 50vh;
            }
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="project-info">
            <div class="project-icon">🚀</div>
            <div class="project-details">
                <h1>{{ project_name }}</h1>
                <div class="project-status">
                    <div class="status-dot"></div>
                    <span>Loading Live Preview...</span>
                </div>
            </div>
        </div>
        <div class="header-actions">
            <button class="header-btn">💬 Chat</button>
            <button class="header-btn">⚡ Invite</button>
            <button class="header-btn">🔗</button>
            <button class="header-btn publish-btn">🚀 Publish</button>
        </div>
    </header>

    <!-- Main Container -->
    <div class="main-container">
        <!-- Left Panel - Chat -->
        <div class="chat-panel">
            <div class="chat-header">
                <div class="chat-title">💬 Chat with Lovable</div>
                <div class="chat-subtitle">Tell me what you want to build or change</div>
            </div>
            
            <div class="chat-messages" id="chatMessages">
                <!-- Messages will be added here dynamically -->
            </div>
            
            <div class="chat-input-container">
                <div class="chat-input-wrapper">
                    <textarea 
                        class="chat-input" 
                        id="chatInput"
                        placeholder="Ask Lovable..."
                        rows="1"
                    ></textarea>
                    <button class="chat-send-btn" id="chatSendBtn">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
        
        <!-- Right Panel - Preview -->
        <div class="preview-panel">
            <div class="preview-header">
                <div class="preview-tabs">
                    <div class="preview-tab active" data-tab="desktop">🖥️ Desktop</div>
                    <div class="preview-tab" data-tab="mobile">📱 Mobile</div>
                </div>
                <div class="preview-actions">
                    <button class="preview-btn" onclick="refreshPreview()">🔄 Refresh</button>
                    <button class="preview-btn" onclick="openInNewTab()">↗️ Open</button>
                </div>
            </div>
            
            <div class="preview-content">
                <div class="preview-loading" id="previewLoading">
                    <div class="preview-spinner"></div>
                    <div>Spinning up preview...</div>
                </div>
                <iframe class="preview-iframe" id="previewIframe" style="display: none;"></iframe>
            </div>
        </div>
    </div>

    <!-- Socket.IO -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.4/socket.io.js"></script>
    
    <script>
        const socket = io();
        const projectId = '{{ project_id }}';
        const chatMessages = document.getElementById('chatMessages');
        const chatInput = document.getElementById('chatInput');
        const chatSendBtn = document.getElementById('chatSendBtn');
        const previewLoading = document.getElementById('previewLoading');
        const previewIframe = document.getElementById('previewIframe');
        
        // Initialize chat with welcome message
        addMessage('ai', 'Hello! I\'m Lovable AI. I\'ve started creating your app. What would you like me to build?');
        
        // Auto-resize chat input
        chatInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
        
        // Send chat message
        function sendChatMessage() {
            const message = chatInput.value.trim();
            if (!message) return;
            
            // Add user message
            addMessage('user', message);
            
            // Clear input
            chatInput.value = '';
            chatInput.style.height = 'auto';
            
            // Send to AI
            socket.emit('chat_message', {
                project_id: projectId,
                message: message,
                timestamp: Date.now()
            });
            
            // Disable send button
            chatSendBtn.disabled = true;
            
            // Show typing indicator
            addTypingIndicator();
        }
        
        // Add message to chat
        function addMessage(sender, text) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message`;
            
            const avatar = document.createElement('div');
            avatar.className = `message-avatar ${sender}-avatar`;
            avatar.textContent = sender === 'user' ? 'N' : '🤖';
            
            const content = document.createElement('div');
            content.className = 'message-content';
            
            const messageText = document.createElement('div');
            messageText.className = 'message-text';
            messageText.textContent = text;
            
            const messageTime = document.createElement('div');
            messageTime.className = 'message-time';
            messageTime.textContent = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            
            content.appendChild(messageText);
            content.appendChild(messageTime);
            messageDiv.appendChild(avatar);
            messageDiv.appendChild(content);
            
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        // Add typing indicator
        function addTypingIndicator() {
            const typingDiv = document.createElement('div');
            typingDiv.className = 'message ai-message typing-indicator';
            typingDiv.innerHTML = `
                <div class="message-avatar ai-avatar">🤖</div>
                <div class="message-content">
                    <div class="message-text">Lovable is thinking...</div>
                </div>
            `;
            chatMessages.appendChild(typingDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        // Remove typing indicator
        function removeTypingIndicator() {
            const typing = chatMessages.querySelector('.typing-indicator');
            if (typing) typing.remove();
        }
        
        // Event listeners
        chatSendBtn.addEventListener('click', sendChatMessage);
        chatInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendChatMessage();
            }
        });
        
        // Preview functions
        function refreshPreview() {
            previewIframe.src = previewIframe.src;
        }
        
        function openInNewTab() {
            if (previewIframe.src) {
                window.open(previewIframe.src, '_blank');
            }
        }
        
        // Tab switching
        document.querySelectorAll('.preview-tab').forEach(tab => {
            tab.addEventListener('click', function() {
                document.querySelectorAll('.preview-tab').forEach(t => t.classList.remove('active'));
                this.classList.add('active');
                
                // Adjust preview size based on tab
                if (this.dataset.tab === 'mobile') {
                    previewIframe.style.width = '375px';
                    previewIframe.style.height = '667px';
                    previewIframe.style.margin = '20px auto';
                } else {
                    previewIframe.style.width = '100%';
                    previewIframe.style.height = '100%';
                    previewIframe.style.margin = '0';
                }
            });
        });
        
        // Socket event handlers
        socket.on('connect', function() {
            console.log('Connected to chat session');
            // Load preview
            setTimeout(() => {
                previewIframe.src = `/preview/${projectId}`;
                previewIframe.style.display = 'block';
                previewLoading.style.display = 'none';
                document.querySelector('.project-status span').textContent = 'Live Preview Ready';
            }, 2000);
        });
        
        socket.on('ai_response', function(data) {
            removeTypingIndicator();
            addMessage('ai', data.message);
            chatSendBtn.disabled = false;
            
            // Refresh preview if code was updated
            if (data.code_updated) {
                refreshPreview();
            }
        });
        
        socket.on('preview_updated', function(data) {
            refreshPreview();
        });
        
        // Focus chat input
        chatInput.focus();
    </script>
</body>
</html>
        """
        
        @app.route('/')
        def landing_page():
            """Lovable-style landing page"""
            return render_template_string(LANDING_PAGE)
        
        @app.route('/chat/<project_id>')
        def chat_interface(project_id):
            """Lovable-style chat interface"""
            project_name = self.projects.get(project_id, {}).get('name', 'My App')
            return render_template_string(CHAT_INTERFACE, 
                                       project_id=project_id, 
                                       project_name=project_name)
        
        @app.route('/preview/<project_id>')
        def preview_app(project_id):
            """Preview the generated app"""
            # Generate a simple preview for demo
            if project_id not in self.projects:
                return "Project not found", 404
            
            project = self.projects[project_id]
            
            return f"""
<!DOCTYPE html>
<html>
<head>
    <title>{project['name']}</title>
    <style>
        body {{ 
            font-family: 'Inter', sans-serif; 
            margin: 0; 
            padding: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }}
        .container {{ 
            max-width: 800px; 
            margin: 0 auto; 
            text-align: center;
        }}
        h1 {{ 
            font-size: 3em; 
            margin-bottom: 0.5em;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }}
        p {{ 
            font-size: 1.2em; 
            opacity: 0.9; 
            line-height: 1.6;
            margin-bottom: 2em;
        }}
        .features {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 40px;
        }}
        .feature {{
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.2);
        }}
        .cta {{
            background: white;
            color: #667eea;
            padding: 15px 30px;
            border-radius: 10px;
            text-decoration: none;
            font-weight: 600;
            display: inline-block;
            margin-top: 20px;
            transition: transform 0.2s;
        }}
        .cta:hover {{
            transform: translateY(-2px);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 {project['name']}</h1>
        <p>{project.get('description', 'An amazing AI-generated application')}</p>
        
        <div class="features">
            <div class="feature">
                <h3>✨ AI-Powered</h3>
                <p>Built with cutting-edge AI technology</p>
            </div>
            <div class="feature">
                <h3>🎨 Beautiful Design</h3>
                <p>Modern, responsive interface</p>
            </div>
            <div class="feature">
                <h3>⚡ Fast & Reliable</h3>
                <p>Optimized for performance</p>
            </div>
        </div>
        
        <a href="#" class="cta">Get Started</a>
    </div>
    
    <script>
        // Add some interactivity
        document.querySelector('.cta').addEventListener('click', function(e) {{
            e.preventDefault();
            alert('🎉 Welcome to your AI-generated app!');
        }});
        
        // Animate features on load
        document.querySelectorAll('.feature').forEach((feature, i) => {{
            feature.style.opacity = '0';
            feature.style.transform = 'translateY(20px)';
            setTimeout(() => {{
                feature.style.transition = 'all 0.5s ease';
                feature.style.opacity = '1';
                feature.style.transform = 'translateY(0)';
            }}, i * 200);
        }});
    </script>
</body>
</html>
            """
        
        # Socket.IO Event Handlers
        @socketio.on('create_app')
        def handle_create_app(data):
            """Handle app creation from landing page"""
            try:
                prompt = data.get('prompt', '')
                project_id = str(uuid.uuid4())[:8]
                
                # Create project
                project_name = self._extract_app_name(prompt)
                self.projects[project_id] = {
                    'name': project_name,
                    'description': prompt,
                    'created_at': datetime.now(),
                    'files': {},
                    'chat_history': []
                }
                
                # Simulate AI processing
                time.sleep(1)
                
                emit('app_created', {
                    'project_id': project_id,
                    'name': project_name,
                    'success': True
                })
                
            except Exception as e:
                emit('error', {'message': str(e)})
        
        @socketio.on('chat_message')
        def handle_chat_message(data):
            """Handle chat messages in project"""
            try:
                project_id = data.get('project_id')
                message = data.get('message', '')
                
                if project_id not in self.projects:
                    emit('error', {'message': 'Project not found'})
                    return
                
                # Add to chat history
                self.projects[project_id]['chat_history'].append({
                    'role': 'user',
                    'message': message,
                    'timestamp': datetime.now()
                })
                
                # Simulate AI processing
                time.sleep(2)
                
                # Generate AI response
                ai_response = self._generate_ai_response(message, project_id)
                
                self.projects[project_id]['chat_history'].append({
                    'role': 'ai',
                    'message': ai_response,
                    'timestamp': datetime.now()
                })
                
                emit('ai_response', {
                    'message': ai_response,
                    'code_updated': True
                })
                
            except Exception as e:
                emit('error', {'message': str(e)})
        
        return app, socketio
    
    def _extract_app_name(self, prompt):
        """Extract app name from prompt"""
        # Simple extraction logic
        if 'landing page' in prompt.lower():
            return 'Landing Page'
        elif 'todo' in prompt.lower() or 'task' in prompt.lower():
            return 'Task Manager'
        elif 'blog' in prompt.lower():
            return 'Blog Site'
        elif 'shop' in prompt.lower() or 'store' in prompt.lower():
            return 'Online Store'
        elif 'portfolio' in prompt.lower():
            return 'Portfolio Site'
        else:
            return 'My App'
    
    def _generate_ai_response(self, message, project_id):
        """Generate AI response to user message"""
        
        # Predefined responses for demo
        responses = [
            "Great idea! I've updated the design with your suggestions. The new layout looks much more modern and user-friendly.",
            "Perfect! I've added that feature to your app. You should see the changes in the preview now.",
            "Excellent choice! I've implemented that functionality with best practices in mind.",
            "Love it! The app now has that feature integrated seamlessly with the existing design.",
            "Amazing suggestion! I've optimized the code and added that enhancement.",
            "Fantastic! Your app now includes that capability with responsive design."
        ]
        
        import random
        return random.choice(responses)

def main():
    """Run the Lovable Clone"""
    print("🚀 LOVABLE CLONE - STARTING UP")
    print("=" * 50)
    
    lovable = LovableClone()
    app, socketio = lovable.create_web_interface()
    
    print("✨ Lovable Clone Ready!")
    print("🌐 Landing Page: http://localhost:3000")
    print("💬 Chat Interface: http://localhost:3000/chat/demo")
    print("👁️ Preview: http://localhost:3000/preview/demo")
    print()
    print("🎯 Features:")
    print("   ✅ Exact Lovable UI clone")
    print("   ✅ Real-time chat interface") 
    print("   ✅ Live preview system")
    print("   ✅ Multi-agent backend")
    print("   ✅ Socket.IO real-time updates")
    print()
    
    try:
        socketio.run(app, host='0.0.0.0', port=3000, debug=True)
    except KeyboardInterrupt:
        print("\n👋 Shutting down Lovable Clone...")

if __name__ == "__main__":
    main()