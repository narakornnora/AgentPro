"""
Mobile App Preview System with AI Screen Flow Generation
ระบบ Preview แอพมือถือพร้อม AI สร้างหน้าจออัตโนมัติ
========================================================
🤖 AI คิดเองว่าจะต้องมีหน้าจออะไรให้แอพสมบูرณ์
📱 แสดงผลบนหน้าจอมือถือจริง
✨ สร้างหน้าจอที่ขาดหายไปอัตโนมัติ
"""

import asyncio
import json
import time
from typing import Dict, List, Any, Optional
from pathlib import Path
import re

class MobileAppPreviewSystem:
    """Advanced mobile app preview system with AI screen generation"""
    
    def __init__(self):
        self.supported_devices = {
            "iphone15": {"width": 393, "height": 852, "name": "iPhone 15"},
            "iphone15_plus": {"width": 428, "height": 926, "name": "iPhone 15 Plus"},
            "samsung_s24": {"width": 384, "height": 854, "name": "Samsung Galaxy S24"},
            "pixel8": {"width": 412, "height": 915, "name": "Google Pixel 8"}
        }
        self.current_device = "iphone15"
        
    async def analyze_app_and_generate_screens(self, app_description: str, existing_screens: List[Dict]) -> Dict[str, Any]:
        """Analyze app type and generate complete screen flow"""
        
        print("🤖 AI กำลังวิเคราะห์แอพและคิดหน้าจอที่จำเป็น...")
        
        # AI analysis of app type and required screens
        app_analysis = await self._analyze_app_type(app_description)
        required_screens = await self._generate_required_screens(app_analysis, existing_screens)
        missing_screens = await self._identify_missing_screens(required_screens, existing_screens)
        
        return {
            "app_analysis": app_analysis,
            "required_screens": required_screens,
            "existing_screens": existing_screens,
            "missing_screens": missing_screens,
            "completeness_score": len(existing_screens) / len(required_screens) * 100
        }
    
    async def _analyze_app_type(self, description: str) -> Dict[str, Any]:
        """AI analysis of app type and characteristics"""
        
        # Simulate AI analysis based on keywords and patterns
        app_types = {
            "e-commerce": ["shop", "buy", "sell", "product", "cart", "payment", "ซื้อ", "ขาย", "สินค้า"],
            "social": ["social", "chat", "friend", "follow", "post", "share", "แชท", "เพื่อน", "โพสต์"],
            "productivity": ["task", "todo", "note", "remind", "schedule", "งาน", "จด", "เตือน"],
            "fitness": ["fitness", "health", "workout", "exercise", "ออกกำลัง", "สุขภาพ"],
            "food": ["food", "restaurant", "recipe", "cook", "อาหาร", "ร้าน", "ทำอาหาร"],
            "finance": ["money", "bank", "budget", "payment", "เงิน", "ธนาคาร", "จ่าย"],
            "education": ["learn", "course", "study", "lesson", "เรียน", "หลักสูตร", "บทเรียน"],
            "entertainment": ["game", "music", "video", "movie", "เกม", "เพลง", "หนัง"],
            "travel": ["travel", "hotel", "flight", "trip", "เที่ยว", "โรงแรม", "เครื่องบิน"],
            "business": ["business", "company", "office", "meeting", "ธุรกิจ", "บริษัท", "ประชุม"]
        }
        
        detected_types = []
        for app_type, keywords in app_types.items():
            if any(keyword.lower() in description.lower() for keyword in keywords):
                detected_types.append(app_type)
        
        primary_type = detected_types[0] if detected_types else "general"
        
        return {
            "primary_type": primary_type,
            "detected_types": detected_types,
            "complexity": "high" if len(detected_types) > 2 else "medium" if len(detected_types) > 1 else "simple",
            "user_flow_complexity": self._determine_flow_complexity(primary_type)
        }
    
    def _determine_flow_complexity(self, app_type: str) -> str:
        """Determine user flow complexity based on app type"""
        complex_flows = ["e-commerce", "finance", "business", "education"]
        medium_flows = ["social", "productivity", "food", "travel"]
        
        if app_type in complex_flows:
            return "complex"
        elif app_type in medium_flows:
            return "medium"
        else:
            return "simple"
    
    async def _generate_required_screens(self, app_analysis: Dict, existing_screens: List[Dict]) -> List[Dict[str, Any]]:
        """Generate complete list of required screens based on app type"""
        
        base_screens = [
            {"name": "splash", "title": "Splash Screen", "priority": "essential", "type": "onboarding"},
            {"name": "onboarding", "title": "Welcome/Onboarding", "priority": "essential", "type": "onboarding"},
            {"name": "home", "title": "Home/Dashboard", "priority": "essential", "type": "main"}
        ]
        
        # Type-specific screens
        type_screens = {
            "e-commerce": [
                {"name": "product_list", "title": "Product Listing", "priority": "essential", "type": "main"},
                {"name": "product_detail", "title": "Product Details", "priority": "essential", "type": "detail"},
                {"name": "cart", "title": "Shopping Cart", "priority": "essential", "type": "main"},
                {"name": "checkout", "title": "Checkout", "priority": "essential", "type": "flow"},
                {"name": "payment", "title": "Payment", "priority": "essential", "type": "flow"},
                {"name": "order_confirmation", "title": "Order Confirmation", "priority": "essential", "type": "flow"},
                {"name": "search", "title": "Search Products", "priority": "important", "type": "utility"},
                {"name": "wishlist", "title": "Wishlist", "priority": "nice-to-have", "type": "utility"},
                {"name": "order_history", "title": "Order History", "priority": "important", "type": "account"}
            ],
            "social": [
                {"name": "feed", "title": "Social Feed", "priority": "essential", "type": "main"},
                {"name": "post_create", "title": "Create Post", "priority": "essential", "type": "creation"},
                {"name": "profile", "title": "User Profile", "priority": "essential", "type": "account"},
                {"name": "chat_list", "title": "Messages", "priority": "important", "type": "main"},
                {"name": "chat", "title": "Chat Conversation", "priority": "important", "type": "detail"},
                {"name": "friends", "title": "Friends List", "priority": "important", "type": "social"},
                {"name": "search_users", "title": "Search Users", "priority": "important", "type": "utility"},
                {"name": "notifications", "title": "Notifications", "priority": "important", "type": "utility"}
            ],
            "productivity": [
                {"name": "task_list", "title": "Task List", "priority": "essential", "type": "main"},
                {"name": "task_detail", "title": "Task Details", "priority": "essential", "type": "detail"},
                {"name": "task_create", "title": "Create Task", "priority": "essential", "type": "creation"},
                {"name": "calendar", "title": "Calendar View", "priority": "important", "type": "main"},
                {"name": "categories", "title": "Categories", "priority": "important", "type": "organization"},
                {"name": "search_tasks", "title": "Search Tasks", "priority": "nice-to-have", "type": "utility"},
                {"name": "statistics", "title": "Statistics", "priority": "nice-to-have", "type": "analytics"}
            ],
            "fitness": [
                {"name": "dashboard", "title": "Fitness Dashboard", "priority": "essential", "type": "main"},
                {"name": "workout_list", "title": "Workouts", "priority": "essential", "type": "main"},
                {"name": "workout_detail", "title": "Workout Details", "priority": "essential", "type": "detail"},
                {"name": "exercise_tracker", "title": "Exercise Tracker", "priority": "essential", "type": "active"},
                {"name": "progress", "title": "Progress Tracking", "priority": "important", "type": "analytics"},
                {"name": "goals", "title": "Goals Setting", "priority": "important", "type": "settings"},
                {"name": "nutrition", "title": "Nutrition Log", "priority": "nice-to-have", "type": "utility"}
            ]
        }
        
        # Common utility screens
        utility_screens = [
            {"name": "settings", "title": "Settings", "priority": "important", "type": "account"},
            {"name": "profile_edit", "title": "Edit Profile", "priority": "important", "type": "account"},
            {"name": "help", "title": "Help & Support", "priority": "nice-to-have", "type": "utility"},
            {"name": "about", "title": "About", "priority": "nice-to-have", "type": "utility"},
            {"name": "login", "title": "Login", "priority": "essential", "type": "auth"},
            {"name": "register", "title": "Register", "priority": "essential", "type": "auth"},
            {"name": "forgot_password", "title": "Forgot Password", "priority": "important", "type": "auth"}
        ]
        
        required_screens = base_screens.copy()
        
        # Add type-specific screens
        primary_type = app_analysis["primary_type"]
        if primary_type in type_screens:
            required_screens.extend(type_screens[primary_type])
        
        # Add utility screens
        required_screens.extend(utility_screens)
        
        # Add screens for detected secondary types
        for detected_type in app_analysis["detected_types"]:
            if detected_type != primary_type and detected_type in type_screens:
                # Add key screens from secondary types
                secondary_screens = [screen for screen in type_screens[detected_type] 
                                   if screen["priority"] == "essential"]
                required_screens.extend(secondary_screens)
        
        return required_screens
    
    async def _identify_missing_screens(self, required_screens: List[Dict], existing_screens: List[Dict]) -> List[Dict]:
        """Identify which screens are missing from the current app"""
        
        existing_names = [screen.get("name", "").lower() for screen in existing_screens]
        
        missing_screens = []
        for required_screen in required_screens:
            if required_screen["name"] not in existing_names:
                missing_screens.append(required_screen)
        
        # Sort by priority
        priority_order = {"essential": 1, "important": 2, "nice-to-have": 3}
        missing_screens.sort(key=lambda x: priority_order.get(x["priority"], 4))
        
        return missing_screens
    
    async def generate_missing_screens_html(self, missing_screens: List[Dict], app_type: str) -> Dict[str, str]:
        """Generate HTML for missing screens"""
        
        generated_screens = {}
        
        for screen in missing_screens[:5]:  # Generate top 5 missing screens
            print(f"🎨 สร้างหน้าจอ: {screen['title']}...")
            
            screen_html = await self._generate_screen_html(screen, app_type)
            generated_screens[screen["name"]] = screen_html
            
            await asyncio.sleep(0.2)  # Simulate generation time
        
        return generated_screens
    
    async def _generate_screen_html(self, screen: Dict, app_type: str) -> str:
        """Generate HTML for a specific screen based on its type and purpose"""
        
        screen_templates = {
            "splash": self._generate_splash_screen,
            "onboarding": self._generate_onboarding_screen,
            "home": self._generate_home_screen,
            "login": self._generate_login_screen,
            "register": self._generate_register_screen,
            "product_list": self._generate_product_list_screen,
            "product_detail": self._generate_product_detail_screen,
            "cart": self._generate_cart_screen,
            "checkout": self._generate_checkout_screen,
            "feed": self._generate_social_feed_screen,
            "profile": self._generate_profile_screen,
            "task_list": self._generate_task_list_screen,
            "settings": self._generate_settings_screen
        }
        
        generator = screen_templates.get(screen["name"], self._generate_generic_screen)
        return generator(screen, app_type)
    
    def _generate_splash_screen(self, screen: Dict, app_type: str) -> str:
        """Generate splash screen HTML"""
        return """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Splash Screen</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        .splash-container {
            text-align: center;
            color: white;
        }
        .logo {
            width: 120px;
            height: 120px;
            background: rgba(255,255,255,0.2);
            border-radius: 30px;
            margin: 0 auto 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 60px;
            animation: pulse 2s infinite;
        }
        .app-name {
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 10px;
        }
        .tagline {
            font-size: 16px;
            opacity: 0.8;
        }
        .loading-dots {
            margin-top: 40px;
        }
        .dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: white;
            margin: 0 4px;
            animation: loading 1.4s infinite ease-in-out;
        }
        .dot:nth-child(1) { animation-delay: -0.32s; }
        .dot:nth-child(2) { animation-delay: -0.16s; }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        @keyframes loading {
            0%, 80%, 100% { transform: scale(0); opacity: 0.5; }
            40% { transform: scale(1); opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="splash-container">
        <div class="logo">📱</div>
        <div class="app-name">MyApp</div>
        <div class="tagline">Your Digital Companion</div>
        <div class="loading-dots">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        </div>
    </div>
</body>
</html>
        """
    
    def _generate_onboarding_screen(self, screen: Dict, app_type: str) -> str:
        """Generate onboarding screen HTML"""
        return """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome - เริ่มต้นใช้งาน</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            color: white;
        }
        .onboarding-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 40px 20px;
            text-align: center;
        }
        .feature-icon {
            width: 120px;
            height: 120px;
            background: rgba(255,255,255,0.2);
            border-radius: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 60px;
            margin-bottom: 40px;
            animation: float 3s ease-in-out infinite;
        }
        .welcome-title {
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 15px;
        }
        .welcome-subtitle {
            font-size: 18px;
            opacity: 0.9;
            margin-bottom: 40px;
            line-height: 1.5;
        }
        .features-list {
            margin-bottom: 50px;
        }
        .feature-item {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            padding: 15px 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 12px;
            backdrop-filter: blur(10px);
        }
        .feature-emoji {
            font-size: 24px;
            margin-right: 15px;
        }
        .feature-text {
            font-size: 16px;
            font-weight: 500;
        }
        .navigation-dots {
            display: flex;
            gap: 8px;
            margin-bottom: 30px;
        }
        .dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: rgba(255,255,255,0.3);
            transition: all 0.3s;
        }
        .dot.active {
            background: white;
            transform: scale(1.2);
        }
        .action-buttons {
            display: flex;
            flex-direction: column;
            gap: 15px;
            width: 100%;
            max-width: 300px;
        }
        .btn {
            padding: 15px 30px;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn-primary {
            background: white;
            color: #667eea;
        }
        .btn-secondary {
            background: rgba(255,255,255,0.2);
            color: white;
            border: 2px solid rgba(255,255,255,0.3);
        }
        .btn:hover {
            transform: translateY(-2px);
        }
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
    </style>
</head>
<body>
    <div class="onboarding-container">
        <div class="feature-icon">🌟</div>
        <h1 class="welcome-title">ยินดีต้อนรับ!</h1>
        <p class="welcome-subtitle">
            ค้นพบฟีเจอร์ที่น่าตื่นเต้นและเริ่มต้นประสบการณ์ใหม่ที่ยอดเยี่ยม
        </p>
        
        <div class="features-list">
            <div class="feature-item">
                <span class="feature-emoji">⚡</span>
                <span class="feature-text">ใช้งานง่าย รวดเร็วทันใจ</span>
            </div>
            <div class="feature-item">
                <span class="feature-emoji">🔒</span>
                <span class="feature-text">ความปลอดภัยระดับสูง</span>
            </div>
            <div class="feature-item">
                <span class="feature-emoji">🎯</span>
                <span class="feature-text">ฟีเจอร์ครบครันตอบโจทย์</span>
            </div>
        </div>
        
        <div class="navigation-dots">
            <div class="dot active"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        </div>
        
        <div class="action-buttons">
            <button class="btn btn-primary">เริ่มใช้งาน</button>
            <button class="btn btn-secondary">ข้าม</button>
        </div>
    </div>
</body>
</html>
        """
    
    def _generate_register_screen(self, screen: Dict, app_type: str) -> str:
        """Generate register screen HTML"""
        return """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>สมัครสมาชิก</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .register-container {
            max-width: 350px;
            margin: 20px auto;
            background: white;
            border-radius: 20px;
            padding: 30px 25px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .logo-icon {
            width: 70px;
            height: 70px;
            background: #667eea;
            border-radius: 18px;
            margin: 0 auto 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 35px;
            color: white;
        }
        h1 {
            color: #333;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        .subtitle {
            color: #666;
            font-size: 14px;
        }
        .form-group {
            margin-bottom: 18px;
        }
        label {
            display: block;
            color: #333;
            font-weight: 500;
            margin-bottom: 6px;
            font-size: 14px;
        }
        input[type="text"], input[type="email"], input[type="password"], input[type="tel"] {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            font-size: 15px;
            transition: border-color 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        .checkbox-group {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            margin: 20px 0;
        }
        .checkbox-group input[type="checkbox"] {
            margin-top: 2px;
        }
        .checkbox-group label {
            font-size: 13px;
            line-height: 1.4;
            margin-bottom: 0;
        }
        .checkbox-group a {
            color: #667eea;
            text-decoration: none;
        }
        .register-btn {
            width: 100%;
            padding: 14px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s;
        }
        .register-btn:hover {
            background: #5a67d8;
        }
        .divider {
            text-align: center;
            margin: 25px 0;
            color: #999;
            position: relative;
            font-size: 14px;
        }
        .divider::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            height: 1px;
            background: #e1e5e9;
            z-index: 1;
        }
        .divider span {
            background: white;
            padding: 0 15px;
            position: relative;
            z-index: 2;
        }
        .social-login {
            display: flex;
            gap: 12px;
            margin-bottom: 25px;
        }
        .social-btn {
            flex: 1;
            padding: 10px;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            background: white;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            font-size: 13px;
            color: #333;
        }
        .login-link {
            text-align: center;
            color: #666;
            font-size: 14px;
        }
        .login-link a {
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }
    </style>
</head>
<body>
    <div class="register-container">
        <div class="header">
            <div class="logo-icon">📝</div>
            <h1>สมัครสมาชิก</h1>
            <p class="subtitle">เริ่มต้นใช้งานกับเรา</p>
        </div>
        
        <form>
            <div class="form-group">
                <label for="fullname">ชื่อ-นามสกุล</label>
                <input type="text" id="fullname" placeholder="กรอกชื่อ-นามสกุล">
            </div>
            
            <div class="form-group">
                <label for="email">อีเมล</label>
                <input type="email" id="email" placeholder="กรอกอีเมลของคุณ">
            </div>
            
            <div class="form-group">
                <label for="phone">เบอร์โทรศัพท์</label>
                <input type="tel" id="phone" placeholder="กรอกเบอร์โทรศัพท์">
            </div>
            
            <div class="form-group">
                <label for="password">รหัสผ่าน</label>
                <input type="password" id="password" placeholder="สร้างรหัสผ่าน">
            </div>
            
            <div class="form-group">
                <label for="confirmPassword">ยืนยันรหัสผ่าน</label>
                <input type="password" id="confirmPassword" placeholder="ยืนยันรหัสผ่าน">
            </div>
            
            <div class="checkbox-group">
                <input type="checkbox" id="terms">
                <label for="terms">
                    ฉันยอมรับ <a href="#">ข้อกำหนดและเงื่อนไข</a> และ <a href="#">นโยบายความเป็นส่วนตัว</a>
                </label>
            </div>
            
            <button type="submit" class="register-btn">สมัครสมาชิก</button>
        </form>
        
        <div class="divider">
            <span>หรือ</span>
        </div>
        
        <div class="social-login">
            <button class="social-btn">
                <span>📘</span> Facebook
            </button>
            <button class="social-btn">
                <span>🔍</span> Google
            </button>
        </div>
        
        <div class="login-link">
            มีบัญชีอยู่แล้ว? <a href="#">เข้าสู่ระบบ</a>
        </div>
    </div>
</body>
</html>
        """
    
    def _generate_login_screen(self, screen: Dict, app_type: str) -> str:
        """Generate login screen HTML"""
        return """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>เข้าสู่ระบบ</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .login-container {
            max-width: 350px;
            margin: 60px auto;
            background: white;
            border-radius: 20px;
            padding: 40px 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        .logo {
            text-align: center;
            margin-bottom: 40px;
        }
        .logo-icon {
            width: 80px;
            height: 80px;
            background: #667eea;
            border-radius: 20px;
            margin: 0 auto 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
            color: white;
        }
        h1 {
            text-align: center;
            color: #333;
            font-size: 28px;
            font-weight: 700;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            color: #333;
            font-weight: 500;
            margin-bottom: 8px;
        }
        input[type="email"], input[type="password"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #e1e5e9;
            border-radius: 12px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input[type="email"]:focus, input[type="password"]:focus {
            outline: none;
            border-color: #667eea;
        }
        .forgot-password {
            text-align: right;
            margin-bottom: 30px;
        }
        .forgot-password a {
            color: #667eea;
            text-decoration: none;
            font-size: 14px;
        }
        .login-btn {
            width: 100%;
            padding: 15px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s;
        }
        .login-btn:hover {
            background: #5a67d8;
        }
        .divider {
            text-align: center;
            margin: 30px 0;
            color: #999;
            position: relative;
        }
        .divider::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            height: 1px;
            background: #e1e5e9;
            z-index: 1;
        }
        .divider span {
            background: white;
            padding: 0 15px;
            position: relative;
            z-index: 2;
        }
        .social-login {
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
        }
        .social-btn {
            flex: 1;
            padding: 12px;
            border: 2px solid #e1e5e9;
            border-radius: 12px;
            background: white;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            font-size: 14px;
            color: #333;
        }
        .signup-link {
            text-align: center;
            color: #666;
        }
        .signup-link a {
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">
            <div class="logo-icon">🔐</div>
            <h1>เข้าสู่ระบบ</h1>
            <p class="subtitle">ยินดีต้อนรับกลับมา!</p>
        </div>
        
        <form>
            <div class="form-group">
                <label for="email">อีเมล</label>
                <input type="email" id="email" placeholder="กรอกอีเมลของคุณ">
            </div>
            
            <div class="form-group">
                <label for="password">รหัสผ่าน</label>
                <input type="password" id="password" placeholder="กรอกรหัสผ่าน">
            </div>
            
            <div class="forgot-password">
                <a href="#">ลืมรหัสผ่าน?</a>
            </div>
            
            <button type="submit" class="login-btn">เข้าสู่ระบบ</button>
        </form>
        
        <div class="divider">
            <span>หรือ</span>
        </div>
        
        <div class="social-login">
            <button class="social-btn">
                <span>📘</span> Facebook
            </button>
            <button class="social-btn">
                <span>🔍</span> Google
            </button>
        </div>
        
        <div class="signup-link">
            ยังไม่มีบัญชี? <a href="#">สมัครสมาชิก</a>
        </div>
    </div>
</body>
</html>
        """
    
    def _generate_home_screen(self, screen: Dict, app_type: str) -> str:
        """Generate home screen based on app type"""
        if app_type == "e-commerce":
            return self._generate_ecommerce_home()
        elif app_type == "social":
            return self._generate_social_home()
        elif app_type == "productivity":
            return self._generate_productivity_home()
        else:
            return self._generate_generic_home()
    
    def _generate_ecommerce_home(self) -> str:
        """Generate e-commerce home screen"""
        return """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>หน้าหลัก - ร้านค้าออนไลน์</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8f9fa;
        }
        .header {
            background: white;
            padding: 15px 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .header-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .logo {
            font-size: 24px;
            font-weight: 700;
            color: #333;
        }
        .cart-icon {
            position: relative;
            font-size: 24px;
            color: #667eea;
        }
        .cart-badge {
            position: absolute;
            top: -8px;
            right: -8px;
            background: #ff4757;
            color: white;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            font-size: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .search-bar {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e1e5e9;
            border-radius: 25px;
            font-size: 16px;
            background: #f8f9fa;
        }
        .banner {
            margin: 20px;
            height: 150px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            position: relative;
            overflow: hidden;
        }
        .banner-content {
            text-align: center;
            z-index: 2;
        }
        .banner h2 {
            font-size: 24px;
            margin-bottom: 10px;
        }
        .banner p {
            opacity: 0.9;
        }
        .categories {
            padding: 0 20px;
            margin-bottom: 30px;
        }
        .section-title {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 15px;
            color: #333;
        }
        .category-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
        }
        .category-item {
            background: white;
            padding: 20px 10px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        .category-icon {
            font-size: 32px;
            margin-bottom: 8px;
        }
        .category-name {
            font-size: 12px;
            color: #666;
            font-weight: 500;
        }
        .products {
            padding: 0 20px;
        }
        .product-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }
        .product-card {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        .product-image {
            height: 120px;
            background: #f1f3f4;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
        }
        .product-info {
            padding: 12px;
        }
        .product-name {
            font-size: 14px;
            font-weight: 500;
            margin-bottom: 5px;
            color: #333;
        }
        .product-price {
            font-size: 16px;
            font-weight: 600;
            color: #667eea;
        }
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: white;
            padding: 10px 0;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-around;
        }
        .nav-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            color: #999;
            font-size: 12px;
        }
        .nav-item.active {
            color: #667eea;
        }
        .nav-icon {
            font-size: 20px;
            margin-bottom: 4px;
        }
        .main-content {
            padding-bottom: 80px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-top">
            <div class="logo">ShopApp</div>
            <div class="cart-icon">
                🛒
                <div class="cart-badge">3</div>
            </div>
        </div>
        <input type="text" class="search-bar" placeholder="ค้นหาสินค้า...">
    </div>
    
    <div class="main-content">
        <div class="banner">
            <div class="banner-content">
                <h2>ลดราคาพิเศษ</h2>
                <p>ส่วนลดสูงสุด 50% วันนี้เท่านั้น!</p>
            </div>
        </div>
        
        <div class="categories">
            <h3 class="section-title">หมวดหมู่สินค้า</h3>
            <div class="category-grid">
                <div class="category-item">
                    <div class="category-icon">👕</div>
                    <div class="category-name">เสื้อผ้า</div>
                </div>
                <div class="category-item">
                    <div class="category-icon">📱</div>
                    <div class="category-name">อิเล็กทรอนิกส์</div>
                </div>
                <div class="category-item">
                    <div class="category-icon">🏠</div>
                    <div class="category-name">ของใช้ในบ้าน</div>
                </div>
                <div class="category-item">
                    <div class="category-icon">⚽</div>
                    <div class="category-name">กีฬา</div>
                </div>
            </div>
        </div>
        
        <div class="products">
            <h3 class="section-title">สินค้าแนะนำ</h3>
            <div class="product-grid">
                <div class="product-card">
                    <div class="product-image">👕</div>
                    <div class="product-info">
                        <div class="product-name">เสื้อยืดคุณภาพดี</div>
                        <div class="product-price">฿299</div>
                    </div>
                </div>
                <div class="product-card">
                    <div class="product-image">📱</div>
                    <div class="product-info">
                        <div class="product-name">สมาร์ทโฟนรุ่นใหม่</div>
                        <div class="product-price">฿12,990</div>
                    </div>
                </div>
                <div class="product-card">
                    <div class="product-image">👟</div>
                    <div class="product-info">
                        <div class="product-name">รองเท้าผ้าใบ</div>
                        <div class="product-price">฿1,590</div>
                    </div>
                </div>
                <div class="product-card">
                    <div class="product-image">🎧</div>
                    <div class="product-info">
                        <div class="product-name">หูฟังไร้สาย</div>
                        <div class="product-price">฿2,490</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="bottom-nav">
        <div class="nav-item active">
            <div class="nav-icon">🏠</div>
            <div>หน้าหลัก</div>
        </div>
        <div class="nav-item">
            <div class="nav-icon">🔍</div>
            <div>ค้นหา</div>
        </div>
        <div class="nav-item">
            <div class="nav-icon">❤️</div>
            <div>รายการโปรด</div>
        </div>
        <div class="nav-item">
            <div class="nav-icon">👤</div>
            <div>โปรไฟล์</div>
        </div>
    </div>
</body>
</html>
        """
    
    def _generate_product_list_screen(self, screen: Dict, app_type: str) -> str:
        """Generate product listing screen"""
        return self._generate_ecommerce_home()  # Use the same as home for now
    
    def _generate_product_detail_screen(self, screen: Dict, app_type: str) -> str:
        """Generate product detail screen"""
        return """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>รายละเอียดสินค้า</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8f9fa;
        }
        .header {
            background: white;
            padding: 15px 20px;
            display: flex;
            align-items: center;
            gap: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .back-btn { font-size: 20px; color: #667eea; }
        .title { font-size: 18px; font-weight: 600; color: #333; }
        .product-image {
            width: 100%;
            height: 300px;
            background: #f1f3f4;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 80px;
        }
        .product-info {
            background: white;
            padding: 20px;
            margin-top: -20px;
            border-radius: 20px 20px 0 0;
            position: relative;
        }
        .product-name {
            font-size: 24px;
            font-weight: 700;
            color: #333;
            margin-bottom: 10px;
        }
        .product-price {
            font-size: 28px;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 15px;
        }
        .rating {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 20px;
        }
        .stars { color: #ffc107; }
        .rating-text { color: #666; font-size: 14px; }
        .description {
            color: #666;
            line-height: 1.6;
            margin-bottom: 30px;
        }
        .quantity-selector {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 30px;
        }
        .quantity-controls {
            display: flex;
            align-items: center;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
        }
        .qty-btn {
            width: 40px;
            height: 40px;
            border: none;
            background: none;
            font-size: 18px;
            color: #667eea;
            cursor: pointer;
        }
        .qty-input {
            width: 60px;
            height: 40px;
            border: none;
            text-align: center;
            font-size: 16px;
            font-weight: 600;
        }
        .add-to-cart {
            width: 100%;
            background: #667eea;
            color: white;
            border: none;
            padding: 15px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            margin-bottom: 15px;
        }
        .buy-now {
            width: 100%;
            background: #ff4757;
            color: white;
            border: none;
            padding: 15px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="back-btn">←</div>
        <div class="title">รายละเอียดสินค้า</div>
    </div>
    
    <div class="product-image">📱</div>
    
    <div class="product-info">
        <h1 class="product-name">สมาร์ทโฟนรุ่นใหม่</h1>
        <div class="product-price">฿12,990</div>
        
        <div class="rating">
            <span class="stars">⭐⭐⭐⭐⭐</span>
            <span class="rating-text">4.8 (234 รีวิว)</span>
        </div>
        
        <div class="description">
            สมาร์ทโฟนรุ่นใหม่ล่าสุดที่มาพร้อมกับเทคโนโลยีที่ทันสมัย 
            กล้องความละเอียดสูง แบตเตอรี่ทนทาน และดีไซน์ที่สวยงาม
        </div>
        
        <div class="quantity-selector">
            <span>จำนวน:</span>
            <div class="quantity-controls">
                <button class="qty-btn">-</button>
                <input type="number" class="qty-input" value="1">
                <button class="qty-btn">+</button>
            </div>
        </div>
        
        <button class="add-to-cart">🛒 เพิ่มในตะกร้า</button>
        <button class="buy-now">⚡ ซื้อทันที</button>
    </div>
</body>
</html>
        """
    
    def _generate_cart_screen(self, screen: Dict, app_type: str) -> str:
        """Generate shopping cart screen"""
        return """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ตะกร้าสินค้า</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8f9fa;
            padding-bottom: 100px;
        }
        .header {
            background: white;
            padding: 15px 20px;
            display: flex;
            align-items: center;
            gap: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .back-btn { font-size: 20px; color: #667eea; }
        .title { font-size: 18px; font-weight: 600; color: #333; }
        .cart-items {
            padding: 20px;
        }
        .cart-item {
            background: white;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 15px;
            display: flex;
            gap: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        .item-image {
            width: 80px;
            height: 80px;
            background: #f1f3f4;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
        }
        .item-details {
            flex: 1;
        }
        .item-name {
            font-size: 16px;
            font-weight: 600;
            color: #333;
            margin-bottom: 5px;
        }
        .item-price {
            font-size: 18px;
            font-weight: 600;
            color: #667eea;
            margin-bottom: 10px;
        }
        .item-controls {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .quantity-controls {
            display: flex;
            align-items: center;
            border: 1px solid #e1e5e9;
            border-radius: 6px;
        }
        .qty-btn {
            width: 30px;
            height: 30px;
            border: none;
            background: none;
            font-size: 16px;
            color: #667eea;
            cursor: pointer;
        }
        .qty-display {
            width: 40px;
            text-align: center;
            font-weight: 600;
        }
        .remove-btn {
            color: #ff4757;
            font-size: 16px;
            cursor: pointer;
        }
        .cart-summary {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: white;
            padding: 20px;
            box-shadow: 0 -4px 20px rgba(0,0,0,0.1);
        }
        .summary-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            color: #666;
        }
        .total-row {
            display: flex;
            justify-content: space-between;
            font-size: 18px;
            font-weight: 700;
            color: #333;
            border-top: 1px solid #e1e5e9;
            padding-top: 15px;
            margin-bottom: 20px;
        }
        .checkout-btn {
            width: 100%;
            background: #667eea;
            color: white;
            border: none;
            padding: 15px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="back-btn">←</div>
        <div class="title">ตะกร้าสินค้า (3 รายการ)</div>
    </div>
    
    <div class="cart-items">
        <div class="cart-item">
            <div class="item-image">📱</div>
            <div class="item-details">
                <div class="item-name">สมาร์ทโฟนรุ่นใหม่</div>
                <div class="item-price">฿12,990</div>
                <div class="item-controls">
                    <div class="quantity-controls">
                        <button class="qty-btn">-</button>
                        <div class="qty-display">1</div>
                        <button class="qty-btn">+</button>
                    </div>
                    <div class="remove-btn">🗑️</div>
                </div>
            </div>
        </div>
        
        <div class="cart-item">
            <div class="item-image">🎧</div>
            <div class="item-details">
                <div class="item-name">หูฟังไร้สาย</div>
                <div class="item-price">฿2,490</div>
                <div class="item-controls">
                    <div class="quantity-controls">
                        <button class="qty-btn">-</button>
                        <div class="qty-display">2</div>
                        <button class="qty-btn">+</button>
                    </div>
                    <div class="remove-btn">🗑️</div>
                </div>
            </div>
        </div>
        
        <div class="cart-item">
            <div class="item-image">👕</div>
            <div class="item-details">
                <div class="item-name">เสื้อยืดคุณภาพดี</div>
                <div class="item-price">฿299</div>
                <div class="item-controls">
                    <div class="quantity-controls">
                        <button class="qty-btn">-</button>
                        <div class="qty-display">1</div>
                        <button class="qty-btn">+</button>
                    </div>
                    <div class="remove-btn">🗑️</div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="cart-summary">
        <div class="summary-row">
            <span>ยอดรวมสินค้า</span>
            <span>฿18,269</span>
        </div>
        <div class="summary-row">
            <span>ค่าจัดส่ง</span>
            <span>฿50</span>
        </div>
        <div class="summary-row">
            <span>ส่วนลด</span>
            <span style="color: #4caf50;">-฿200</span>
        </div>
        <div class="total-row">
            <span>ยอดรวมทั้งหมด</span>
            <span>฿18,119</span>
        </div>
        <button class="checkout-btn">ดำเนินการชำระเงิน</button>
    </div>
</body>
</html>
        """
    
    def _generate_checkout_screen(self, screen: Dict, app_type: str) -> str:
        """Generate checkout screen"""
        return """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ชำระเงิน</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8f9fa;
            padding-bottom: 100px;
        }
        .header {
            background: white;
            padding: 15px 20px;
            display: flex;
            align-items: center;
            gap: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .back-btn { font-size: 20px; color: #667eea; }
        .title { font-size: 18px; font-weight: 600; color: #333; }
        .section {
            background: white;
            margin: 15px 20px;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        .section-title {
            font-size: 16px;
            font-weight: 600;
            color: #333;
            margin-bottom: 15px;
        }
        .address-card {
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            padding: 15px;
        }
        .address-name {
            font-weight: 600;
            color: #333;
            margin-bottom: 5px;
        }
        .address-text {
            color: #666;
            line-height: 1.5;
        }
        .payment-methods {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .payment-option {
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            padding: 15px;
            display: flex;
            align-items: center;
            gap: 12px;
            cursor: pointer;
        }
        .payment-option.selected {
            border-color: #667eea;
            background: rgba(102, 126, 234, 0.05);
        }
        .payment-icon {
            font-size: 24px;
        }
        .payment-text {
            font-weight: 500;
            color: #333;
        }
        .order-summary {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: white;
            padding: 20px;
            box-shadow: 0 -4px 20px rgba(0,0,0,0.1);
        }
        .summary-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            color: #666;
        }
        .total-row {
            display: flex;
            justify-content: space-between;
            font-size: 18px;
            font-weight: 700;
            color: #333;
            border-top: 1px solid #e1e5e9;
            padding-top: 15px;
            margin-bottom: 20px;
        }
        .place-order-btn {
            width: 100%;
            background: #4caf50;
            color: white;
            border: none;
            padding: 15px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="back-btn">←</div>
        <div class="title">ชำระเงิน</div>
    </div>
    
    <div class="section">
        <div class="section-title">📍 ที่อยู่จัดส่ง</div>
        <div class="address-card">
            <div class="address-name">คุณสมชาย ใจดี</div>
            <div class="address-text">
                123/45 ถ.สุขุมวิท แขวงคลองตัน เขตคลองตัน<br>
                กรุงเทพมหานคร 10110<br>
                โทร: 081-234-5678
            </div>
        </div>
    </div>
    
    <div class="section">
        <div class="section-title">💳 วิธีการชำระเงิน</div>
        <div class="payment-methods">
            <div class="payment-option selected">
                <span class="payment-icon">💳</span>
                <span class="payment-text">บัตรเครดิต/เดบิต</span>
            </div>
            <div class="payment-option">
                <span class="payment-icon">📱</span>
                <span class="payment-text">Mobile Banking</span>
            </div>
            <div class="payment-option">
                <span class="payment-icon">🏪</span>
                <span class="payment-text">ชำระเงินปลายทาง</span>
            </div>
            <div class="payment-option">
                <span class="payment-icon">💰</span>
                <span class="payment-text">TrueMoney Wallet</span>
            </div>
        </div>
    </div>
    
    <div class="order-summary">
        <div class="summary-row">
            <span>ยอดรวมสินค้า</span>
            <span>฿18,269</span>
        </div>
        <div class="summary-row">
            <span>ค่าจัดส่ง</span>
            <span>฿50</span>
        </div>
        <div class="summary-row">
            <span>ส่วนลด</span>
            <span style="color: #4caf50;">-฿200</span>
        </div>
        <div class="total-row">
            <span>ยอดรวมทั้งหมด</span>
            <span>฿18,119</span>
        </div>
        <button class="place-order-btn">สั่งซื้อสินค้า</button>
    </div>
</body>
</html>
        """
    
    def _generate_social_feed_screen(self, screen: Dict, app_type: str) -> str:
        """Generate social media feed screen"""
        return """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Feed</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8f9fa;
            padding-bottom: 80px;
        }
        .header {
            background: white;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .logo {
            font-size: 24px;
            font-weight: 700;
            color: #667eea;
        }
        .header-icons {
            display: flex;
            gap: 15px;
            font-size: 20px;
            color: #333;
        }
        .post {
            background: white;
            margin: 15px 20px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            overflow: hidden;
        }
        .post-header {
            padding: 15px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .avatar {
            width: 40px;
            height: 40px;
            background: #667eea;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
        }
        .post-info {
            flex: 1;
        }
        .username {
            font-weight: 600;
            color: #333;
        }
        .timestamp {
            font-size: 12px;
            color: #666;
        }
        .post-content {
            padding: 0 15px 15px;
            color: #333;
            line-height: 1.5;
        }
        .post-image {
            width: 100%;
            height: 200px;
            background: #f1f3f4;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 60px;
        }
        .post-actions {
            padding: 15px;
            display: flex;
            justify-content: space-around;
            border-top: 1px solid #f0f0f0;
        }
        .action-btn {
            display: flex;
            align-items: center;
            gap: 8px;
            color: #666;
            font-size: 14px;
            cursor: pointer;
        }
        .action-btn.liked {
            color: #ff4757;
        }
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: white;
            padding: 10px 0;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-around;
        }
        .nav-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            color: #999;
            font-size: 12px;
            cursor: pointer;
        }
        .nav-item.active {
            color: #667eea;
        }
        .nav-icon {
            font-size: 20px;
            margin-bottom: 4px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">SocialApp</div>
        <div class="header-icons">
            <span>💬</span>
            <span>🔔</span>
        </div>
    </div>
    
    <div class="post">
        <div class="post-header">
            <div class="avatar">A</div>
            <div class="post-info">
                <div class="username">อานนท์ สวยงาม</div>
                <div class="timestamp">2 ชั่วโมงที่แล้ว</div>
            </div>
            <span>⋯</span>
        </div>
        <div class="post-content">
            วันนี้ไปเที่ยวทะเลกับเพื่อน ๆ สนุกมาก! อากาศดีมากเลย 🌊☀️
        </div>
        <div class="post-image">🏖️</div>
        <div class="post-actions">
            <div class="action-btn liked">
                <span>❤️</span>
                <span>123</span>
            </div>
            <div class="action-btn">
                <span>💬</span>
                <span>45</span>
            </div>
            <div class="action-btn">
                <span>↗️</span>
                <span>แชร์</span>
            </div>
        </div>
    </div>
    
    <div class="post">
        <div class="post-header">
            <div class="avatar">B</div>
            <div class="post-info">
                <div class="username">บุญชู ใจดี</div>
                <div class="timestamp">5 ชั่วโมงที่แล้ว</div>
            </div>
            <span>⋯</span>
        </div>
        <div class="post-content">
            ทำอาหารใหม่ ใครอยากลองบ้าง? 😋
        </div>
        <div class="post-image">🍝</div>
        <div class="post-actions">
            <div class="action-btn">
                <span>❤️</span>
                <span>89</span>
            </div>
            <div class="action-btn">
                <span>💬</span>
                <span>23</span>
            </div>
            <div class="action-btn">
                <span>↗️</span>
                <span>แชร์</span>
            </div>
        </div>
    </div>
    
    <div class="bottom-nav">
        <div class="nav-item active">
            <div class="nav-icon">🏠</div>
            <div>หน้าหลัก</div>
        </div>
        <div class="nav-item">
            <div class="nav-icon">🔍</div>
            <div>ค้นหา</div>
        </div>
        <div class="nav-item">
            <div class="nav-icon">➕</div>
            <div>โพสต์</div>
        </div>
        <div class="nav-item">
            <div class="nav-icon">❤️</div>
            <div>กิจกรรม</div>
        </div>
        <div class="nav-item">
            <div class="nav-icon">👤</div>
            <div>โปรไฟล์</div>
        </div>
    </div>
</body>
</html>
        """
    
    def _generate_profile_screen(self, screen: Dict, app_type: str) -> str:
        """Generate profile screen"""
        return """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>โปรไฟล์</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8f9fa;
        }
        .header {
            background: white;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .title {
            font-size: 18px;
            font-weight: 600;
            color: #333;
        }
        .settings-btn {
            font-size: 20px;
            color: #667eea;
            cursor: pointer;
        }
        .profile-header {
            background: white;
            padding: 30px 20px;
            text-align: center;
            margin-bottom: 20px;
        }
        .profile-avatar {
            width: 100px;
            height: 100px;
            background: #667eea;
            border-radius: 50%;
            margin: 0 auto 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
            color: white;
            font-weight: 600;
        }
        .profile-name {
            font-size: 24px;
            font-weight: 700;
            color: #333;
            margin-bottom: 8px;
        }
        .profile-email {
            color: #666;
            margin-bottom: 20px;
        }
        .profile-stats {
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
        }
        .stat-item {
            text-align: center;
        }
        .stat-number {
            font-size: 20px;
            font-weight: 700;
            color: #333;
        }
        .stat-label {
            font-size: 12px;
            color: #666;
            margin-top: 4px;
        }
        .menu-section {
            background: white;
            margin: 0 20px 20px;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        .menu-item {
            padding: 15px 20px;
            display: flex;
            align-items: center;
            gap: 15px;
            border-bottom: 1px solid #f0f0f0;
            cursor: pointer;
        }
        .menu-item:last-child {
            border-bottom: none;
        }
        .menu-icon {
            font-size: 20px;
            width: 24px;
        }
        .menu-text {
            flex: 1;
            font-size: 16px;
            color: #333;
        }
        .menu-arrow {
            color: #999;
        }
        .logout-btn {
            background: #ff4757;
            color: white;
            border: none;
            padding: 15px;
            margin: 0 20px 20px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="title">โปรไฟล์</div>
        <div class="settings-btn">⚙️</div>
    </div>
    
    <div class="profile-header">
        <div class="profile-avatar">JD</div>
        <div class="profile-name">จอห์น โด</div>
        <div class="profile-email">john.doe@example.com</div>
        
        <div class="profile-stats">
            <div class="stat-item">
                <div class="stat-number">234</div>
                <div class="stat-label">โพสต์</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">1.2K</div>
                <div class="stat-label">ผู้ติดตาม</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">567</div>
                <div class="stat-label">กำลังติดตาม</div>
            </div>
        </div>
    </div>
    
    <div class="menu-section">
        <div class="menu-item">
            <span class="menu-icon">👤</span>
            <span class="menu-text">แก้ไขโปรไฟล์</span>
            <span class="menu-arrow">›</span>
        </div>
        <div class="menu-item">
            <span class="menu-icon">🔔</span>
            <span class="menu-text">การแจ้งเตือน</span>
            <span class="menu-arrow">›</span>
        </div>
        <div class="menu-item">
            <span class="menu-icon">🔒</span>
            <span class="menu-text">ความเป็นส่วนตัว</span>
            <span class="menu-arrow">›</span>
        </div>
    </div>
    
    <div class="menu-section">
        <div class="menu-item">
            <span class="menu-icon">❤️</span>
            <span class="menu-text">รายการโปรด</span>
            <span class="menu-arrow">›</span>
        </div>
        <div class="menu-item">
            <span class="menu-icon">📊</span>
            <span class="menu-text">สถิติการใช้งาน</span>
            <span class="menu-arrow">›</span>
        </div>
    </div>
    
    <div class="menu-section">
        <div class="menu-item">
            <span class="menu-icon">💬</span>
            <span class="menu-text">ติดต่อเรา</span>
            <span class="menu-arrow">›</span>
        </div>
        <div class="menu-item">
            <span class="menu-icon">ℹ️</span>
            <span class="menu-text">เกี่ยวกับเรา</span>
            <span class="menu-arrow">›</span>
        </div>
    </div>
    
    <button class="logout-btn">ออกจากระบบ</button>
</body>
</html>
        """
    
    def _generate_task_list_screen(self, screen: Dict, app_type: str) -> str:
        """Generate task list screen for productivity apps"""
        return """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>รายการงาน</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8f9fa;
            padding-bottom: 80px;
        }
        .header {
            background: white;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .title {
            font-size: 18px;
            font-weight: 600;
            color: #333;
        }
        .add-btn {
            width: 40px;
            height: 40px;
            background: #667eea;
            border: none;
            border-radius: 50%;
            color: white;
            font-size: 20px;
            cursor: pointer;
        }
        .task-list {
            padding: 20px;
        }
        .task-item {
            background: white;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        .task-checkbox {
            width: 24px;
            height: 24px;
            border: 2px solid #ddd;
            border-radius: 50%;
            cursor: pointer;
        }
        .task-checkbox.completed {
            background: #4caf50;
            border-color: #4caf50;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        .task-content {
            flex: 1;
        }
        .task-title {
            font-size: 16px;
            color: #333;
            margin-bottom: 4px;
        }
        .task-title.completed {
            text-decoration: line-through;
            opacity: 0.6;
        }
        .task-meta {
            display: flex;
            gap: 10px;
            font-size: 12px;
            color: #666;
        }
        .priority {
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 10px;
            font-weight: 600;
        }
        .priority.high { background: #ffebee; color: #d32f2f; }
        .priority.medium { background: #fff3e0; color: #f57c00; }
        .priority.low { background: #e8f5e8; color: #388e3c; }
    </style>
</head>
<body>
    <div class="header">
        <div class="title">รายการงาน</div>
        <button class="add-btn">+</button>
    </div>
    
    <div class="task-list">
        <div class="task-item">
            <div class="task-checkbox"></div>
            <div class="task-content">
                <div class="task-title">ทำรายงานประจำเดือน</div>
                <div class="task-meta">
                    <span class="priority high">สำคัญ</span>
                    <span>📅 วันนี้</span>
                </div>
            </div>
        </div>
        
        <div class="task-item">
            <div class="task-checkbox completed">✓</div>
            <div class="task-content">
                <div class="task-title completed">ซื้อของใช้ในบ้าน</div>
                <div class="task-meta">
                    <span class="priority low">ปกติ</span>
                    <span>✅ เสร็จแล้ว</span>
                </div>
            </div>
        </div>
        
        <div class="task-item">
            <div class="task-checkbox"></div>
            <div class="task-content">
                <div class="task-title">นัดหมายกับลูกค้า</div>
                <div class="task-meta">
                    <span class="priority medium">ปานกลาง</span>
                    <span>📅 พรุ่งนี้ 14:00</span>
                </div>
            </div>
        </div>
        
        <div class="task-item">
            <div class="task-checkbox"></div>
            <div class="task-content">
                <div class="task-title">อ่านหนังสือ 30 หน้า</div>
                <div class="task-meta">
                    <span class="priority low">ปกติ</span>
                    <span>📚 ส่วนตัว</span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
        """
    
    def _generate_settings_screen(self, screen: Dict, app_type: str) -> str:
        """Generate settings screen"""
        return """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ตั้งค่า</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8f9fa;
        }
        .header {
            background: white;
            padding: 15px 20px;
            display: flex;
            align-items: center;
            gap: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .back-btn { font-size: 20px; color: #667eea; cursor: pointer; }
        .title { font-size: 18px; font-weight: 600; color: #333; }
        .settings-section {
            background: white;
            margin: 20px;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        .section-title {
            padding: 15px 20px;
            background: #f8f9fa;
            font-size: 14px;
            font-weight: 600;
            color: #666;
            text-transform: uppercase;
        }
        .setting-item {
            padding: 15px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid #f0f0f0;
        }
        .setting-item:last-child { border-bottom: none; }
        .setting-left {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .setting-icon {
            font-size: 20px;
            width: 24px;
        }
        .setting-text {
            font-size: 16px;
            color: #333;
        }
        .toggle {
            width: 50px;
            height: 28px;
            background: #ddd;
            border-radius: 14px;
            position: relative;
            cursor: pointer;
        }
        .toggle.active {
            background: #667eea;
        }
        .toggle-thumb {
            width: 24px;
            height: 24px;
            background: white;
            border-radius: 50%;
            position: absolute;
            top: 2px;
            left: 2px;
            transition: transform 0.3s;
        }
        .toggle.active .toggle-thumb {
            transform: translateX(22px);
        }
        .setting-arrow {
            color: #999;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="back-btn">←</div>
        <div class="title">ตั้งค่า</div>
    </div>
    
    <div class="settings-section">
        <div class="section-title">บัญชีผู้ใช้</div>
        <div class="setting-item">
            <div class="setting-left">
                <span class="setting-icon">👤</span>
                <span class="setting-text">ข้อมูลส่วนตัว</span>
            </div>
            <span class="setting-arrow">›</span>
        </div>
        <div class="setting-item">
            <div class="setting-left">
                <span class="setting-icon">🔒</span>
                <span class="setting-text">เปลี่ยนรหัสผ่าน</span>
            </div>
            <span class="setting-arrow">›</span>
        </div>
    </div>
    
    <div class="settings-section">
        <div class="section-title">การแจ้งเตือน</div>
        <div class="setting-item">
            <div class="setting-left">
                <span class="setting-icon">🔔</span>
                <span class="setting-text">การแจ้งเตือนทั่วไป</span>
            </div>
            <div class="toggle active">
                <div class="toggle-thumb"></div>
            </div>
        </div>
        <div class="setting-item">
            <div class="setting-left">
                <span class="setting-icon">📧</span>
                <span class="setting-text">การแจ้งเตือนทางอีเมล</span>
            </div>
            <div class="toggle">
                <div class="toggle-thumb"></div>
            </div>
        </div>
    </div>
    
    <div class="settings-section">
        <div class="section-title">ทั่วไป</div>
        <div class="setting-item">
            <div class="setting-left">
                <span class="setting-icon">🌙</span>
                <span class="setting-text">โหมดกลางคืน</span>
            </div>
            <div class="toggle">
                <div class="toggle-thumb"></div>
            </div>
        </div>
        <div class="setting-item">
            <div class="setting-left">
                <span class="setting-icon">🌍</span>
                <span class="setting-text">ภาษา</span>
            </div>
            <span class="setting-arrow">›</span>
        </div>
        <div class="setting-item">
            <div class="setting-left">
                <span class="setting-icon">💾</span>
                <span class="setting-text">การสำรองข้อมูล</span>
            </div>
            <span class="setting-arrow">›</span>
        </div>
    </div>
    
    <div class="settings-section">
        <div class="section-title">การช่วยเหลือ</div>
        <div class="setting-item">
            <div class="setting-left">
                <span class="setting-icon">❓</span>
                <span class="setting-text">ช่วยเหลือและการสนับสนุน</span>
            </div>
            <span class="setting-arrow">›</span>
        </div>
        <div class="setting-item">
            <div class="setting-left">
                <span class="setting-icon">ℹ️</span>
                <span class="setting-text">เกี่ยวกับแอป</span>
            </div>
            <span class="setting-arrow">›</span>
        </div>
    </div>
</body>
</html>
        """

    def _generate_generic_screen(self, screen: Dict, app_type: str) -> str:
        """Generate generic screen template"""
        return f"""
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{screen['title']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8f9fa;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }}
        .header {{
            background: white;
            padding: 15px 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        .back-btn {{
            font-size: 20px;
            color: #667eea;
            cursor: pointer;
        }}
        .title {{
            font-size: 18px;
            font-weight: 600;
            color: #333;
        }}
        .content {{
            flex: 1;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
        }}
        .screen-icon {{
            font-size: 80px;
            margin-bottom: 20px;
            opacity: 0.6;
        }}
        .screen-title {{
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 10px;
            color: #333;
        }}
        .screen-description {{
            color: #666;
            line-height: 1.6;
            margin-bottom: 30px;
        }}
        .placeholder-content {{
            width: 100%;
            max-width: 300px;
            background: white;
            border-radius: 12px;
            padding: 30px 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        }}
        .feature-list {{
            list-style: none;
            text-align: left;
        }}
        .feature-list li {{
            padding: 10px 0;
            border-bottom: 1px solid #f0f0f0;
            color: #666;
        }}
        .feature-list li:last-child {{
            border-bottom: none;
        }}
        .feature-list li::before {{
            content: '✓';
            color: #4caf50;
            font-weight: bold;
            margin-right: 10px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="back-btn">←</div>
        <div class="title">{screen['title']}</div>
    </div>
    
    <div class="content">
        <div class="screen-icon">📱</div>
        <div class="screen-title">{screen['title']}</div>
        <div class="screen-description">
            หน้าจอนี้จะแสดงฟีเจอร์และฟังก์ชันที่เกี่ยวข้องกับ {screen['title']}
        </div>
        
        <div class="placeholder-content">
            <ul class="feature-list">
                <li>ฟีเจอร์หลักของหน้าจอ</li>
                <li>การนำทางที่ใช้งานง่าย</li>
                <li>การตอบสนองที่รวดเร็ว</li>
                <li>ดีไซน์ที่สวยงาม</li>
                <li>ประสบการณ์ผู้ใช้ที่ดี</li>
            </ul>
        </div>
    </div>
</body>
</html>
        """

    async def create_mobile_preview_interface(self, screens_data: Dict) -> str:
        """Create comprehensive mobile preview interface"""
        
        device = self.supported_devices[self.current_device]
        
        return f"""
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mobile App Preview - {device['name']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}
        
        .preview-container {{
            display: flex;
            gap: 40px;
            align-items: flex-start;
            max-width: 1400px;
            width: 100%;
        }}
        
        .device-frame {{
            position: relative;
            width: {device['width'] + 40}px;
            height: {device['height'] + 80}px;
            background: #1a1a1a;
            border-radius: 35px;
            padding: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        
        .device-screen {{
            width: 100%;
            height: 100%;
            background: #000;
            border-radius: 25px;
            overflow: hidden;
            position: relative;
        }}
        
        .device-header {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 30px;
            background: #000;
            z-index: 1000;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        
        .dynamic-island {{
            width: 120px;
            height: 20px;
            background: #1a1a1a;
            border-radius: 10px;
        }}
        
        .screen-content {{
            width: 100%;
            height: calc(100% - 30px);
            margin-top: 30px;
            overflow: hidden;
        }}
        
        .screen-iframe {{
            width: 100%;
            height: 100%;
            border: none;
        }}
        
        .device-controls {{
            flex: 1;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            color: white;
        }}
        
        .controls-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
        }}
        
        .device-selector {{
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 8px;
            padding: 8px 12px;
            color: white;
            font-size: 14px;
        }}
        
        .screen-list {{
            margin-bottom: 30px;
        }}
        
        .section-title {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 15px;
            color: rgba(255,255,255,0.9);
        }}
        
        .screen-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            gap: 12px;
            margin-bottom: 20px;
        }}
        
        .screen-item {{
            background: rgba(255,255,255,0.1);
            border: 2px solid transparent;
            border-radius: 12px;
            padding: 15px 10px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 12px;
        }}
        
        .screen-item:hover {{
            background: rgba(255,255,255,0.2);
            border-color: rgba(255,255,255,0.3);
        }}
        
        .screen-item.active {{
            background: rgba(255,255,255,0.2);
            border-color: #4caf50;
        }}
        
        .screen-item.missing {{
            background: rgba(255,75,75,0.2);
            border-color: rgba(255,75,75,0.5);
        }}
        
        .screen-icon {{
            font-size: 24px;
            margin-bottom: 8px;
        }}
        
        .screen-name {{
            font-size: 11px;
            line-height: 1.3;
        }}
        
        .priority-badge {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            color: white;
            font-size: 10px;
            padding: 2px 6px;
            border-radius: 4px;
            margin-top: 4px;
        }}
        
        .priority-essential {{ background: rgba(255,75,75,0.8); }}
        .priority-important {{ background: rgba(255,165,0,0.8); }}
        .priority-nice-to-have {{ background: rgba(75,75,255,0.8); }}
        
        .app-analysis {{
            background: rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        
        .analysis-item {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            font-size: 14px;
        }}
        
        .completeness-bar {{
            width: 100%;
            height: 8px;
            background: rgba(255,255,255,0.2);
            border-radius: 4px;
            overflow: hidden;
            margin-top: 10px;
        }}
        
        .completeness-fill {{
            height: 100%;
            background: linear-gradient(90deg, #4caf50, #8bc34a);
            border-radius: 4px;
            transition: width 0.3s ease;
        }}
        
        .generate-btn {{
            width: 100%;
            background: linear-gradient(135deg, #4caf50, #45a049);
            border: none;
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s ease;
            margin-top: 15px;
        }}
        
        .generate-btn:hover {{
            transform: translateY(-2px);
        }}
        
        .status-indicator {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            margin-top: 15px;
        }}
        
        .status-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #4caf50;
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}
        
        .device-label {{
            text-align: center;
            margin-top: 15px;
            font-size: 14px;
            color: rgba(255,255,255,0.7);
        }}
    </style>
</head>
<body>
    <div class="preview-container">
        <div class="device-frame">
            <div class="device-screen">
                <div class="device-header">
                    <div class="dynamic-island"></div>
                </div>
                <div class="screen-content">
                    <iframe class="screen-iframe" id="screenFrame" src="about:blank"></iframe>
                </div>
            </div>
            <div class="device-label">{device['name']}</div>
        </div>
        
        <div class="device-controls">
            <div class="controls-header">
                <h2>📱 Mobile App Preview</h2>
                <select class="device-selector" onchange="changeDevice(this.value)">
                    <option value="iphone15">iPhone 15</option>
                    <option value="iphone15_plus">iPhone 15 Plus</option>
                    <option value="samsung_s24">Samsung Galaxy S24</option>
                    <option value="pixel8">Google Pixel 8</option>
                </select>
            </div>
            
            <div class="app-analysis">
                <div class="section-title">🤖 AI Analysis</div>
                <div class="analysis-item">
                    <span>App Type:</span>
                    <span id="appType">{screens_data.get('app_analysis', {}).get('primary_type', 'Unknown')}</span>
                </div>
                <div class="analysis-item">
                    <span>Complexity:</span>
                    <span id="complexity">{screens_data.get('app_analysis', {}).get('complexity', 'Unknown')}</span>
                </div>
                <div class="analysis-item">
                    <span>Completeness:</span>
                    <span id="completeness">{screens_data.get('completeness_score', 0):.0f}%</span>
                </div>
                <div class="completeness-bar">
                    <div class="completeness-fill" style="width: {screens_data.get('completeness_score', 0)}%"></div>
                </div>
            </div>
            
            <div class="screen-list">
                <div class="section-title">✅ Existing Screens ({len(screens_data.get('existing_screens', []))})</div>
                <div class="screen-grid" id="existingScreens"></div>
            </div>
            
            <div class="screen-list">
                <div class="section-title">⚠️ Missing Screens ({len(screens_data.get('missing_screens', []))})</div>
                <div class="screen-grid" id="missingScreens"></div>
                <button class="generate-btn" onclick="generateMissingScreens()">
                    🤖 AI สร้างหน้าจอที่ขาดหายไป
                </button>
            </div>
            
            <div class="status-indicator">
                <div class="status-dot"></div>
                <span>AI พร้อมสร้างแอพสมบูรณ์แบบ</span>
            </div>
        </div>
    </div>
    
    <script>
        const screensData = {json.dumps(screens_data)};
        let currentScreen = '';
        
        function initializeScreens() {{
            displayExistingScreens();
            displayMissingScreens();
        }}
        
        function displayExistingScreens() {{
            const container = document.getElementById('existingScreens');
            const existingScreens = screensData.existing_screens || [];
            
            container.innerHTML = existingScreens.map(screen => `
                <div class="screen-item" onclick="loadScreen('${{screen.name}}')">
                    <div class="screen-icon">${{getScreenIcon(screen.name)}}</div>
                    <div class="screen-name">${{screen.title || screen.name}}</div>
                </div>
            `).join('');
        }}
        
        function displayMissingScreens() {{
            const container = document.getElementById('missingScreens');
            const missingScreens = screensData.missing_screens || [];
            
            container.innerHTML = missingScreens.map(screen => `
                <div class="screen-item missing" onclick="generateScreen('${{screen.name}}')">
                    <div class="screen-icon">${{getScreenIcon(screen.name)}}</div>
                    <div class="screen-name">${{screen.title}}</div>
                    <div class="priority-badge priority-${{screen.priority.replace('-', '-')}}">${{screen.priority}}</div>
                </div>
            `).join('');
        }}
        
        function getScreenIcon(screenName) {{
            const icons = {{
                'splash': '🎯',
                'onboarding': '👋',
                'home': '🏠',
                'login': '🔐',
                'register': '📝',
                'profile': '👤',
                'settings': '⚙️',
                'product_list': '📦',
                'product_detail': '🔍',
                'cart': '🛒',
                'checkout': '💳',
                'feed': '📱',
                'chat': '💬',
                'task_list': '📋',
                'search': '🔍',
                'notifications': '🔔'
            }};
            return icons[screenName] || '📱';
        }}
        
        function loadScreen(screenName) {{
            // ในการใช้งานจริง จะโหลดหน้าจอจากไฟล์หรือ API
            console.log('Loading screen:', screenName);
            currentScreen = screenName;
            
            // อัพเดท active state
            document.querySelectorAll('.screen-item').forEach(item => {{
                item.classList.remove('active');
            }});
            event.target.closest('.screen-item').classList.add('active');
        }}
        
        function generateScreen(screenName) {{
            console.log('Generating screen:', screenName);
            // ในการใช้งานจริง จะเรียก AI API เพื่อสร้างหน้าจอ
            alert(`🤖 AI กำลังสร้างหน้าจอ "${{screenName}}" ให้คุณ...`);
        }}
        
        function generateMissingScreens() {{
            alert('🤖 AI กำลังสร้างหน้าจอทั้งหมดที่ขาดหายไปเพื่อให้แอพสมบูรณ์...');
        }}
        
        function changeDevice(deviceType) {{
            // ในการใช้งานจริง จะเปลี่ยนขนาดและสไตล์ของ device frame
            console.log('Changing device to:', deviceType);
        }}
        
        // Initialize on page load
        initializeScreens();
    </script>
</body>
</html>
        """

async def main():
    """Main function to demonstrate mobile preview system"""
    
    print("📱 MOBILE APP PREVIEW SYSTEM WITH AI SCREEN GENERATION")
    print("=" * 80)
    print()
    
    # Initialize the system
    preview_system = MobileAppPreviewSystem()
    
    # Example app analysis
    app_description = "แอพขายของออนไลน์ ที่มีระบบตะกร้าสินค้า การชำระเงิน และการติดตามคำสั่งซื้อ"
    existing_screens = [
        {"name": "home", "title": "หน้าหลัก"},
        {"name": "login", "title": "เข้าสู่ระบบ"},
        {"name": "product_list", "title": "รายการสินค้า"}
    ]
    
    print("🤖 AI กำลังวิเคราะห์แอพและสร้างหน้าจอที่จำเป็น...")
    analysis = await preview_system.analyze_app_and_generate_screens(app_description, existing_screens)
    
    print(f"\n📊 ผลการวิเคราะห์:")
    print(f"   🎯 ประเภทแอพ: {analysis['app_analysis']['primary_type']}")
    print(f"   📈 ความซับซ้อน: {analysis['app_analysis']['complexity']}")
    print(f"   ✅ หน้าจอที่มี: {len(analysis['existing_screens'])}")
    print(f"   ⚠️ หน้าจอที่ขาด: {len(analysis['missing_screens'])}")
    print(f"   📊 ความสมบูรณ์: {analysis['completeness_score']:.0f}%")
    
    print(f"\n⚠️ หน้าจอที่ AI แนะนำให้เพิ่ม:")
    for screen in analysis['missing_screens'][:8]:  # Show top 8
        priority_emoji = {"essential": "🔴", "important": "🟡", "nice-to-have": "🔵"}
        emoji = priority_emoji.get(screen['priority'], '⚪')
        print(f"   {emoji} {screen['title']} ({screen['priority']})")
    
    print(f"\n🎨 AI กำลังสร้างหน้าจอที่ขาดหายไป...")
    generated_screens = await preview_system.generate_missing_screens_html(
        analysis['missing_screens'], 
        analysis['app_analysis']['primary_type']
    )
    
    print(f"✅ สร้างหน้าจอสำเร็จ {len(generated_screens)} หน้า:")
    for screen_name in generated_screens.keys():
        print(f"   📱 {screen_name}.html")
    
    # Create mobile preview interface
    print(f"\n📱 สร้าง Mobile Preview Interface...")
    preview_html = await preview_system.create_mobile_preview_interface(analysis)
    
    return {
        "analysis": analysis,
        "generated_screens": generated_screens,
        "preview_interface": preview_html
    }

if __name__ == "__main__":
    asyncio.run(main())