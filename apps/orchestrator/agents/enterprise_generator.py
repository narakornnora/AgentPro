"""
🏗️ Enterprise Project Generator - สร้างโปรเจ็กต์ Professional จริงๆ
"""

import asyncio
import json
import os
import sqlite3
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from openai import AsyncOpenAI
from .ai_knowledge_base import ai_knowledge
from .image_manager import image_manager

class EnterpriseProjectGenerator:
    def __init__(self):
        self.client = AsyncOpenAI()
        self.project_templates = {
            "professional_website": {
                "structure": ["home", "about", "services", "portfolio", "contact", "blog"],
                "features": ["contact_form", "newsletter", "cms", "analytics", "seo"],
                "technologies": ["html5", "css3", "javascript", "php", "mysql"]
            },
            "ecommerce_platform": {
                "structure": ["homepage", "products", "cart", "checkout", "account", "admin"],
                "features": ["payment_gateway", "inventory", "orders", "reviews", "shipping"],
                "technologies": ["react", "nodejs", "mongodb", "stripe", "aws"]
            },
            "mobile_app": {
                "structure": ["splash", "login", "dashboard", "features", "profile", "settings"],
                "features": ["authentication", "push_notifications", "offline_mode", "camera"],
                "technologies": ["react_native", "firebase", "redux", "expo"]
            },
            "saas_platform": {
                "structure": ["landing", "dashboard", "analytics", "settings", "billing", "api"],
                "features": ["multi_tenant", "subscriptions", "api_keys", "webhooks", "admin"],
                "technologies": ["nextjs", "postgresql", "redis", "docker", "kubernetes"]
            }
        }
        
    def create_complex_architecture(self, project_name: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """สร้าง Complex Architecture ที่ซับซ้อนจริงๆ"""
        
        try:
            # วิเคราะห์ความซับซ้อนและแนะนำ Architecture
            complexity = requirements.get("estimated_complexity", "medium")
            team_size = requirements.get("team_size", 3)
            project_type = requirements.get("project_type", "professional_website")
            
            # ได้รับคำแนะนำจาก AI Knowledge Base
            recommendation = ai_knowledge.get_architecture_recommendation(
                project_type, complexity, team_size
            )
            
            architecture = recommendation["architecture"]
            stack = recommendation["stack"]
            
            # สร้างโครงสร้างโปรเจกต์
            project_path = Path("C:/agent/workspace") / project_name
            project_path.mkdir(parents=True, exist_ok=True)
            
            # สร้างไฟล์ตาม Architecture Pattern
            architecture_info = ai_knowledge.architecture_patterns[architecture]
            stack_info = ai_knowledge.technology_stacks[stack]
            
            created_files = []
            created_folders = set()
            
            # สร้างโครงสร้างโฟลเดอร์พื้นฐาน
            if architecture == "microservices":
                base_folders = [
                    "services/user-service", "services/product-service", "services/payment-service",
                    "api-gateway", "shared/models", "shared/utils", "docker", "nginx"
                ]
            elif architecture == "component_architecture":
                base_folders = [
                    "src/components", "src/containers", "src/pages", "src/hooks",
                    "src/services", "src/store", "src/utils", "src/assets", "public"
                ]
            elif architecture == "nextjs_fullstack":
                base_folders = [
                    "app/(auth)", "app/(dashboard)", "app/api/auth", "app/api/users",
                    "components/ui", "lib", "prisma", "public", "styles"
                ]
            else:  # MVC
                base_folders = [
                    "models", "views", "controllers", "routes", "middleware", 
                    "public/css", "public/js", "public/images", "config"
                ]
            
            # สร้างโฟลเดอร์
            for folder in base_folders:
                folder_path = project_path / folder
                folder_path.mkdir(parents=True, exist_ok=True)
                created_folders.add(str(folder_path))
            
            # สร้างไฟล์ตาม Pattern
            files_to_create = architecture_info["files_needed"]
            
            # เพิ่ม features ที่ซับซ้อน
            requested_features = requirements.get("features", [])
            feature_structure = ai_knowledge.generate_file_structure(architecture, requested_features)
            files_to_create.extend(feature_structure["feature_files"])
            
            # สร้างไฟล์จริงๆ
            for file_path in files_to_create:
                full_path = project_path / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                
                # สร้างเนื้อหาไฟล์ตาม type
                content = self._generate_file_content(file_path, architecture, stack)
                
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                created_files.append(str(full_path))
            
            # สร้าง package.json และ config files
            self._create_config_files(project_path, architecture, stack)
            
            return {
                "success": True,
                "project_path": str(project_path),
                "architecture": architecture,
                "stack": stack,
                "created_files": created_files,
                "created_folders": list(created_folders),
                "complexity_score": feature_structure.get("complexity_score", 5),
                "recommendation_reason": recommendation["reasoning"],
                "total_files": len(created_files),
                "message": f"สร้าง {architecture} architecture สำหรับ {project_name} เรียบร้อยแล้ว"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"เกิดข้อผิดพลาดในการสร้าง Complex Architecture: {e}"
            }

    def _generate_file_content(self, file_path: str, architecture: str, stack: str) -> str:
        """สร้างเนื้อหาไฟล์ที่มีคุณภาพสูง"""
        
        file_name = Path(file_path).name
        file_ext = Path(file_path).suffix
        
        # React/TypeScript Components
        if file_ext in ['.tsx', '.jsx'] and 'components' in file_path:
            component_name = file_name.replace('.tsx', '').replace('.jsx', '')
            return f"""import React from 'react';
import {{ cn }} from '@/lib/utils';

interface {component_name}Props {{
  className?: string;
  children?: React.ReactNode;
}}

export const {component_name}: React.FC<{component_name}Props> = ({{
  className,
  children,
  ...props
}}) => {{
  return (
    <div className={{cn('', className)}} {{...props}}>
      {{{component_name} Component}}
      {{children}}
    </div>
  );
}};

export default {component_name};
"""

        # Node.js Controllers
        elif 'controller' in file_path.lower() or 'Controller' in file_path:
            controller_name = file_name.replace('.js', '')
            return f"""const {{ asyncHandler }} = require('express-async-handler');

class {controller_name} {{
  // @desc    Get all items
  // @route   GET /api/items
  // @access  Public
  static getAll = asyncHandler(async (req, res) => {{
    try {{
      // Implementation here
      res.status(200).json({{
        success: true,
        data: [],
        message: 'Data retrieved successfully'
      }});
    }} catch (error) {{
      res.status(400).json({{
        success: false,
        message: error.message
      }});
    }}
  }});

  // @desc    Create new item
  // @route   POST /api/items
  // @access  Private
  static create = asyncHandler(async (req, res) => {{
    try {{
      // Implementation here
      res.status(201).json({{
        success: true,
        data: {{}},
        message: 'Item created successfully'
      }});
    }} catch (error) {{
      res.status(400).json({{
        success: false,
        message: error.message
      }});
    }}
  }});
}}

module.exports = {controller_name};
"""

        # API Routes
        elif 'routes' in file_path or 'api' in file_path:
            return """const express = require('express');
const router = express.Router();
const { protect, authorize } = require('../middleware/auth');

// @route   GET /api/v1/resource
router.get('/', (req, res) => {
  res.status(200).json({
    success: true,
    data: []
  });
});

// @route   POST /api/v1/resource
router.post('/', protect, (req, res) => {
  res.status(201).json({
    success: true,
    data: {}
  });
});

module.exports = router;
"""

        # Database Models
        elif 'model' in file_path.lower():
            model_name = file_name.replace('.js', '')
            return f"""const mongoose = require('mongoose');

const {model_name}Schema = new mongoose.Schema({{
  name: {{
    type: String,
    required: [true, 'Name is required'],
    trim: true,
    maxlength: [100, 'Name cannot be more than 100 characters']
  }},
  description: {{
    type: String,
    maxlength: [500, 'Description cannot be more than 500 characters']
  }},
  status: {{
    type: String,
    enum: ['active', 'inactive'],
    default: 'active'
  }},
  createdAt: {{
    type: Date,
    default: Date.now
  }},
  updatedAt: {{
    type: Date,
    default: Date.now
  }}
}});

// Update the updatedAt field before saving
{model_name}Schema.pre('save', function() {{
  this.updatedAt = Date.now();
}});

module.exports = mongoose.model('{model_name}', {model_name}Schema);
"""

        # Package.json
        elif file_name == 'package.json':
            if 'nextjs' in stack:
                return """{
  "name": "nextjs-professional-app",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build", 
    "start": "next start",
    "lint": "next lint",
    "test": "jest",
    "test:watch": "jest --watch"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@prisma/client": "^5.0.0",
    "next-auth": "^4.22.0",
    "tailwindcss": "^3.3.0",
    "framer-motion": "^10.0.0",
    "lucide-react": "^0.268.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "typescript": "^5.0.0",
    "prisma": "^5.0.0",
    "jest": "^29.0.0",
    "@testing-library/react": "^13.0.0"
  }
}"""
            else:
                return """{
  "name": "professional-fullstack-app",
  "version": "1.0.0",
  "main": "src/app.js",
  "scripts": {
    "start": "node src/app.js",
    "dev": "nodemon src/app.js",
    "test": "jest",
    "build": "webpack --mode=production"
  },
  "dependencies": {
    "express": "^4.18.2",
    "mongoose": "^7.4.0",
    "jsonwebtoken": "^9.0.0",
    "bcryptjs": "^2.4.3",
    "cors": "^2.8.5",
    "helmet": "^7.0.0",
    "express-rate-limit": "^6.8.0"
  },
  "devDependencies": {
    "nodemon": "^3.0.0",
    "jest": "^29.6.0",
    "supertest": "^6.3.0"
  }
}"""

        # Default content
        else:
            return f"""/*
 * {file_name}
 * Generated by AgentPro AI Enterprise Generator
 * Architecture: {architecture}
 * Stack: {stack}
 */

// TODO: Implement functionality for {file_name}

console.log('🚀 {file_name} loaded successfully');
"""

    def _create_config_files(self, project_path: Path, architecture: str, stack: str):
        """สร้าง Config Files ที่สำคัญ"""
        
        # Docker Compose สำหรับ Microservices
        if architecture == "microservices":
            docker_compose = """version: '3.8'
services:
  user-service:
    build: ./services/user-service
    ports:
      - "3001:3000"
    environment:
      - NODE_ENV=production
      - DB_HOST=mongodb
    depends_on:
      - mongodb

  product-service:
    build: ./services/product-service
    ports:
      - "3002:3000"
    depends_on:
      - mongodb

  api-gateway:
    build: ./api-gateway
    ports:
      - "8080:3000"
    depends_on:
      - user-service
      - product-service

  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

volumes:
  mongodb_data:
"""
            with open(project_path / "docker-compose.yml", 'w') as f:
                f.write(docker_compose)

        # Next.js Config
        if 'nextjs' in stack:
            nextjs_config = """/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  images: {
    domains: ['localhost'],
  },
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
  },
}

module.exports = nextConfig
"""
            with open(project_path / "next.config.js", 'w') as f:
                f.write(nextjs_config)

        # Tailwind Config
        tailwind_config = """/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
"""
        with open(project_path / "tailwind.config.js", 'w') as f:
            f.write(tailwind_config)

    async def analyze_requirements_thoroughly(self, user_input: str) -> Dict[str, Any]:
        """วิเคราะห์ความต้องการอย่างละเอียดครบถ้วน"""
        
        analysis_prompt = f"""
        วิเคราะห์คำขอนี้อย่างละเอียดเพื่อสร้างโปรเจ็กต์ Professional:
        
        คำขอ: "{user_input}"
        
        กรุณาวิเคราะห์:
        
        1. PROJECT_TYPE: 
           - professional_website (เว็บไซต์องค์กร/บริษัท)
           - ecommerce_platform (ร้านค้าออนไลน์) 
           - mobile_app (แอพมือถือ)
           - saas_platform (ระบบ SaaS)
           - crm_system (ระบบ CRM)
           - learning_platform (ระบบเรียนออนไลน์)
        
        2. BUSINESS_REQUIREMENTS:
           - target_audience (กลุ่มเป้าหมาย)
           - main_objectives (วัตถุประสงค์หลัก)
           - key_features (ฟีเจอร์สำคัญ)
           - business_model (รูปแบบธุรกิจ)
        
        3. TECHNICAL_SPECIFICATIONS:
           - required_pages (หน้าที่ต้องมี)
           - functionality (ฟังก์ชันการทำงาน)
           - integrations (ระบบที่ต้องเชื่อมต่อ)
           - performance_requirements (ความต้องการด้านประสิทธิภาพ)
        
        4. USER_EXPERIENCE:
           - user_journey (เส้นทางผู้ใช้)
           - interaction_flow (การโต้ตอบ)
           - responsive_design (การตอบสนองอุปกรณ์)
           - accessibility (การเข้าถึง)
        
        5. MISSING_INFORMATION:
           - ข้อมูลที่ยังขาดหายไป
           - คำถามที่ควรถามเพิ่มเติม
        
        ตอบในรูปแบบ JSON:
        {{
            "project_type": "",
            "confidence": 0.0,
            "business_requirements": {{}},
            "technical_specifications": {{}},
            "user_experience": {{}},
            "estimated_complexity": "simple|medium|complex|enterprise",
            "estimated_timeline": "1-2 weeks|2-4 weeks|1-3 months|3-6 months",
            "missing_information": [],
            "follow_up_questions": []
        }}
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": analysis_prompt}],
                temperature=0.1
            )
            
            analysis_text = response.choices[0].message.content
            
            # Extract JSON
            import re
            json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
                
        except Exception as e:
            print(f"Analysis error: {e}")
        
        # Fallback analysis
        return {
            "project_type": "professional_website",
            "confidence": 0.7,
            "business_requirements": {"target_audience": "General public"},
            "technical_specifications": {"required_pages": ["home", "about", "contact"]},
            "user_experience": {"responsive_design": True},
            "estimated_complexity": "medium",
            "estimated_timeline": "2-4 weeks",
            "missing_information": ["Brand guidelines", "Content strategy"],
            "follow_up_questions": ["What is your budget range?", "Do you need e-commerce functionality?"]
        }
    
    async def generate_website_with_real_images(self, requirements: Dict) -> Dict[str, Any]:
        """สร้างเว็บไซต์ Professional พร้อมรูปภาพจริง"""
        
        try:
            project_type = requirements.get("project_type", "professional_website")
            project_name = requirements.get("project_name", f"{project_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            # สร้างโครงสร้างโปรเจกต์
            project_result = self.create_complex_architecture(project_name, requirements)
            
            if not project_result["success"]:
                return project_result
            
            project_path = Path(project_result["project_path"])
            
            # เลือกรูปภาพสำหรับโปรเจกต์
            project_images = image_manager.get_images_for_project(project_type, 15)
            hero_image = image_manager.get_hero_image(project_type)
            gallery_images = image_manager.get_gallery_images(project_type, 8)
            
            # คัดลอกรูปภาพไป project
            copy_result = image_manager.copy_images_to_project(str(project_path), project_type)
            
            # สร้างหน้าเว็บหลักด้วยรูปภาพจริง
            pages_created = []
            
            # Homepage
            homepage_html = self._create_homepage_with_images(
                project_type, hero_image, gallery_images, requirements
            )
            homepage_path = project_path / "index.html"
            with open(homepage_path, 'w', encoding='utf-8') as f:
                f.write(homepage_html)
            pages_created.append(str(homepage_path))
            
            # About Page
            about_html = self._create_about_page_with_images(project_type, gallery_images[:4])
            about_path = project_path / "about.html"
            with open(about_path, 'w', encoding='utf-8') as f:
                f.write(about_html)
            pages_created.append(str(about_path))
            
            # Services/Products Page
            services_html = self._create_services_page_with_images(project_type, gallery_images[2:6])
            services_path = project_path / "services.html"
            with open(services_path, 'w', encoding='utf-8') as f:
                f.write(services_html)
            pages_created.append(str(services_path))
            
            # Gallery Page
            gallery_html = self._create_gallery_page_with_images(project_type, gallery_images)
            gallery_path = project_path / "gallery.html"
            with open(gallery_path, 'w', encoding='utf-8') as f:
                f.write(gallery_html)
            pages_created.append(str(gallery_path))
            
            # CSS with Real Images
            css_content = self._create_professional_css_with_images(project_type, project_images, hero_image)
            css_path = project_path / "assets" / "css" / "style.css"
            css_path.parent.mkdir(parents=True, exist_ok=True)
            with open(css_path, 'w', encoding='utf-8') as f:
                f.write(css_content)
            
            # JavaScript
            js_content = self._create_interactive_js()
            js_path = project_path / "assets" / "js" / "main.js"
            js_path.parent.mkdir(parents=True, exist_ok=True)
            with open(js_path, 'w', encoding='utf-8') as f:
                f.write(js_content)
            
            return {
                "success": True,
                "project_path": str(project_path),
                "project_name": project_name,
                "project_type": project_type,
                "pages_created": pages_created,
                "images_used": len(project_images["images"]),
                "hero_image": hero_image["filename"] if hero_image else None,
                "gallery_count": len(gallery_images),
                "copied_images": copy_result["copied_count"],
                "architecture": project_result["architecture"],
                "complexity_score": project_result["complexity_score"],
                "total_files": len(pages_created) + copy_result["copied_count"] + 2,  # +2 for CSS/JS
                "message": f"🎉 สร้างเว็บไซต์ {project_type} พร้อมรูปภาพจริง {copy_result['copied_count']} รูป เรียบร้อยแล้ว!"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"เกิดข้อผิดพลาดในการสร้างเว็บไซต์: {e}"
            }

    def _create_homepage_with_images(self, project_type: str, hero_image: dict, gallery_images: list, requirements: dict) -> str:
        """สร้างหน้าแรกที่ใช้รูปภาพจริง"""
        
        project_title = requirements.get("business_name", f"Professional {project_type.replace('_', ' ').title()}")
        project_description = requirements.get("description", f"Modern {project_type} solution with cutting-edge technology")
        
        hero_bg = f"./assets/images/{hero_image['filename']}" if hero_image else "./assets/images/default-bg.jpg"
        
        html = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_title}</title>
    <link rel="stylesheet" href="./assets/css/style.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo">
                <h2>{project_title}</h2>
            </div>
            <ul class="nav-menu">
                <li><a href="index.html" class="active">หน้าแรก</a></li>
                <li><a href="about.html">เกี่ยวกับเรา</a></li>
                <li><a href="services.html">บริการ</a></li>
                <li><a href="gallery.html">ผลงาน</a></li>
                <li><a href="#contact">ติดต่อ</a></li>
            </ul>
            <div class="hamburger">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero" style="background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{hero_bg}');">
        <div class="hero-content">
            <h1 class="hero-title">{project_title}</h1>
            <p class="hero-subtitle">{project_description}</p>
            <div class="hero-buttons">
                <a href="#services" class="btn btn-primary">เริ่มต้นใช้งาน</a>
                <a href="#about" class="btn btn-secondary">เรียนรู้เพิ่มเติม</a>
            </div>
        </div>
        <div class="hero-scroll">
            <i class="fas fa-chevron-down"></i>
        </div>
    </section>

    <!-- Features Section -->
    <section class="features" id="features">
        <div class="container">
            <div class="section-header">
                <h2>ความเป็นเลิศที่เราภาคภูมิใจ</h2>
                <p>เราให้บริการที่เหนือกว่าด้วยคุณภาพระดับมาตรฐานสากล</p>
            </div>
            <div class="features-grid">"""

        # เพิ่ม Feature Cards พร้อมรูปภาพ
        features = [
            {"icon": "fas fa-rocket", "title": "นวัตกรรมล้ำสมัย", "desc": "เทคโนโลジีที่ทันสมัยและการออกแบบที่โดดเด่น"},
            {"icon": "fas fa-shield-alt", "title": "ความปลอดภัยสูง", "desc": "มาตรฐานความปลอดภัยระดับองค์กรและการรักษาความลับ"},
            {"icon": "fas fa-headset", "title": "สนับสนุน 24/7", "desc": "ทีมงานผู้เชี่ยวชาญพร้อมให้บริการตลอด 24 ชั่วโมง"},
            {"icon": "fas fa-chart-line", "title": "ประสิทธิภาพสูง", "desc": "ผลลัพธ์ที่วัดได้และการปรับปรุงอย่างต่อเนื่อง"}
        ]
        
        for i, feature in enumerate(features):
            bg_img = f"./assets/images/{gallery_images[i]['filename']}" if i < len(gallery_images) else ""
            html += f"""
                <div class="feature-card" data-bg="{bg_img}">
                    <div class="feature-icon">
                        <i class="{feature['icon']}"></i>
                    </div>
                    <h3>{feature['title']}</h3>
                    <p>{feature['desc']}</p>
                </div>"""

        html += """
            </div>
        </div>
    </section>

    <!-- Gallery Preview -->
    <section class="gallery-preview" id="gallery-preview">
        <div class="container">
            <div class="section-header">
                <h2>ผลงานที่น่าประทับใจ</h2>
                <p>ชมผลงานและความสำเร็จของเราที่ผ่านมา</p>
            </div>
            <div class="gallery-grid">"""

        # เพิ่ม Gallery Images
        for i, img in enumerate(gallery_images[:6]):
            html += f"""
                <div class="gallery-item" data-aos="fade-up" data-aos-delay="{i*100}">
                    <img src="./assets/images/{img['filename']}" alt="{img['description']}" loading="lazy">
                    <div class="gallery-overlay">
                        <h4>โปรเจกต์ที่ {i+1}</h4>
                        <p>{img['description']}</p>
                        <a href="gallery.html" class="gallery-link">ดูเพิ่มเติม</a>
                    </div>
                </div>"""

        html += f"""
            </div>
            <div class="text-center">
                <a href="gallery.html" class="btn btn-outline">ดูผลงานทั้งหมด</a>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section class="contact" id="contact">
        <div class="container">
            <div class="contact-content">
                <div class="contact-info">
                    <h2>ติดต่อเรา</h2>
                    <p>พร้อมให้บริการและตอบคำถามของคุณ</p>
                    <div class="contact-details">
                        <div class="contact-item">
                            <i class="fas fa-phone"></i>
                            <span>02-123-4567</span>
                        </div>
                        <div class="contact-item">
                            <i class="fas fa-envelope"></i>
                            <span>info@{project_title.lower().replace(' ', '')}.com</span>
                        </div>
                        <div class="contact-item">
                            <i class="fas fa-map-marker-alt"></i>
                            <span>กรุงเทพมหานคร, ประเทศไทย</span>
                        </div>
                    </div>
                </div>
                <div class="contact-form">
                    <form class="form">
                        <div class="form-group">
                            <input type="text" placeholder="ชื่อของคุณ" required>
                        </div>
                        <div class="form-group">
                            <input type="email" placeholder="อีเมลของคุณ" required>
                        </div>
                        <div class="form-group">
                            <textarea placeholder="ข้อความของคุณ" rows="5" required></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary">ส่งข้อความ</button>
                    </form>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>{project_title}</h3>
                    <p>มุ่งมั่นสร้างสรรค์นวัตกรรมเพื่อการเติบโตที่ยั่งยืน</p>
                </div>
                <div class="footer-section">
                    <h4>บริการ</h4>
                    <ul>
                        <li><a href="#">บริการหลัก</a></li>
                        <li><a href="#">บริการพิเศษ</a></li>
                        <li><a href="#">การปรึกษา</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>ติดตาม</h4>
                    <div class="social-links">
                        <a href="#"><i class="fab fa-facebook"></i></a>
                        <a href="#"><i class="fab fa-twitter"></i></a>
                        <a href="#"><i class="fab fa-linkedin"></i></a>
                        <a href="#"><i class="fab fa-instagram"></i></a>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2025 {project_title}. สร้างโดย AgentPro AI Enterprise Generator</p>
            </div>
        </div>
    </footer>

    <script src="./assets/js/main.js"></script>
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    <script>AOS.init();</script>
</body>
</html>"""

        return html

    def _create_professional_css_with_images(self, project_type: str, project_images: dict, hero_image: dict) -> str:
        """สร้าง CSS Professional พร้อมรูปภาพจริง"""
        
        css = """/* Professional Website CSS with Real Images */
/* Generated by AgentPro AI Enterprise Generator */

:root {
    --primary-color: #2563eb;
    --secondary-color: #1e40af;
    --accent-color: #f59e0b;
    --text-dark: #1f2937;
    --text-light: #6b7280;
    --bg-light: #f9fafb;
    --white: #ffffff;
    --shadow: 0 10px 25px rgba(0,0,0,0.1);
    --border-radius: 12px;
    --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    line-height: 1.6;
    color: var(--text-dark);
    overflow-x: hidden;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Navigation */
.navbar {
    position: fixed;
    top: 0;
    width: 100%;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    z-index: 1000;
    transition: var(--transition);
    border-bottom: 1px solid rgba(0,0,0,0.1);
}

.navbar.scrolled {
    background: rgba(255, 255, 255, 0.98);
    box-shadow: var(--shadow);
}

.nav-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.nav-logo h2 {
    color: var(--primary-color);
    font-weight: 700;
    font-size: 1.5rem;
}

.nav-menu {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-menu a {
    text-decoration: none;
    color: var(--text-dark);
    font-weight: 500;
    transition: var(--transition);
    position: relative;
}

.nav-menu a:hover,
.nav-menu a.active {
    color: var(--primary-color);
}

.nav-menu a::after {
    content: '';
    position: absolute;
    bottom: -5px;
    left: 0;
    width: 0;
    height: 2px;
    background: var(--primary-color);
    transition: var(--transition);
}

.nav-menu a:hover::after,
.nav-menu a.active::after {
    width: 100%;
}

.hamburger {
    display: none;
    flex-direction: column;
    cursor: pointer;
    gap: 4px;
}

.hamburger span {
    width: 25px;
    height: 3px;
    background: var(--text-dark);
    transition: var(--transition);
}

/* Hero Section */
.hero {
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    position: relative;
    color: white;
    text-align: center;
}

.hero::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.4);
}

.hero-content {
    position: relative;
    z-index: 2;
    max-width: 800px;
    margin: 0 auto;
    padding: 0 2rem;
}

.hero-title {
    font-size: clamp(2.5rem, 6vw, 4rem);
    font-weight: 700;
    margin-bottom: 1.5rem;
    line-height: 1.1;
}

.hero-subtitle {
    font-size: clamp(1.1rem, 2vw, 1.3rem);
    margin-bottom: 2.5rem;
    opacity: 0.9;
    line-height: 1.5;
}

.hero-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}

.btn {
    display: inline-flex;
    align-items: center;
    padding: 1rem 2rem;
    border-radius: var(--border-radius);
    text-decoration: none;
    font-weight: 600;
    transition: var(--transition);
    border: 2px solid transparent;
    cursor: pointer;
    font-size: 1rem;
}

.btn-primary {
    background: var(--primary-color);
    color: white;
}

.btn-primary:hover {
    background: var(--secondary-color);
    transform: translateY(-2px);
    box-shadow: var(--shadow);
}

.btn-secondary {
    background: transparent;
    color: white;
    border-color: white;
}

.btn-secondary:hover {
    background: white;
    color: var(--primary-color);
}

.btn-outline {
    background: transparent;
    color: var(--primary-color);
    border-color: var(--primary-color);
}

.btn-outline:hover {
    background: var(--primary-color);
    color: white;
}

.hero-scroll {
    position: absolute;
    bottom: 2rem;
    left: 50%;
    transform: translateX(-50%);
    font-size: 1.5rem;
    animation: bounce 2s infinite;
}

/* Features Section */
.features {
    padding: 6rem 0;
    background: var(--bg-light);
}

.section-header {
    text-align: center;
    margin-bottom: 4rem;
}

.section-header h2 {
    font-size: clamp(2rem, 4vw, 2.5rem);
    margin-bottom: 1rem;
    color: var(--text-dark);
}

.section-header p {
    font-size: 1.1rem;
    color: var(--text-light);
    max-width: 600px;
    margin: 0 auto;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
}

.feature-card {
    background: white;
    padding: 2.5rem 2rem;
    border-radius: var(--border-radius);
    text-align: center;
    box-shadow: var(--shadow);
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}

.feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-size: cover;
    background-position: center;
    opacity: 0.05;
    z-index: 1;
}

.feature-card > * {
    position: relative;
    z-index: 2;
}

.feature-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}

.feature-icon {
    width: 80px;
    height: 80px;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1.5rem;
    font-size: 2rem;
    color: white;
}

.feature-card h3 {
    font-size: 1.3rem;
    margin-bottom: 1rem;
    color: var(--text-dark);
}

.feature-card p {
    color: var(--text-light);
    line-height: 1.6;
}

/* Gallery Section */
.gallery-preview {
    padding: 6rem 0;
    background: white;
}

.gallery-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-bottom: 3rem;
}

.gallery-item {
    position: relative;
    border-radius: var(--border-radius);
    overflow: hidden;
    aspect-ratio: 4/3;
    box-shadow: var(--shadow);
    transition: var(--transition);
}

.gallery-item:hover {
    transform: scale(1.05);
}

.gallery-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: var(--transition);
}

.gallery-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(to bottom, transparent, rgba(0,0,0,0.8));
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: 1.5rem;
    color: white;
    opacity: 0;
    transition: var(--transition);
}

.gallery-item:hover .gallery-overlay {
    opacity: 1;
}

.gallery-overlay h4 {
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
}

.gallery-overlay p {
    font-size: 0.9rem;
    opacity: 0.9;
    margin-bottom: 1rem;
}

.gallery-link {
    color: var(--accent-color);
    text-decoration: none;
    font-weight: 600;
}

/* Contact Section */
.contact {
    padding: 6rem 0;
    background: var(--bg-light);
}

.contact-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    align-items: center;
}

.contact-info h2 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color: var(--text-dark);
}

.contact-info p {
    font-size: 1.1rem;
    color: var(--text-light);
    margin-bottom: 2rem;
}

.contact-details {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.contact-item {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.contact-item i {
    width: 50px;
    height: 50px;
    background: var(--primary-color);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 1.2rem;
}

.contact-form {
    background: white;
    padding: 2.5rem;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 1rem;
    border: 2px solid #e5e7eb;
    border-radius: 8px;
    font-size: 1rem;
    transition: var(--transition);
    font-family: inherit;
}

.form-group input:focus,
.form-group textarea:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

/* Footer */
.footer {
    background: var(--text-dark);
    color: white;
    padding: 3rem 0 1rem;
}

.footer-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.footer-section h3,
.footer-section h4 {
    margin-bottom: 1rem;
    color: white;
}

.footer-section ul {
    list-style: none;
}

.footer-section ul li {
    margin-bottom: 0.5rem;
}

.footer-section ul li a {
    color: #d1d5db;
    text-decoration: none;
    transition: var(--transition);
}

.footer-section ul li a:hover {
    color: white;
}

.social-links {
    display: flex;
    gap: 1rem;
}

.social-links a {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    background: var(--primary-color);
    color: white;
    border-radius: 50%;
    text-decoration: none;
    transition: var(--transition);
}

.social-links a:hover {
    background: var(--accent-color);
    transform: translateY(-2px);
}

.footer-bottom {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid #374151;
    color: #9ca3af;
}

.text-center {
    text-align: center;
}

/* Animations */
@keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
        transform: translateY(0) translateX(-50%);
    }
    40% {
        transform: translateY(-10px) translateX(-50%);
    }
    60% {
        transform: translateY(-5px) translateX(-50%);
    }
}

/* Responsive Design */
@media (max-width: 768px) {
    .hamburger {
        display: flex;
    }
    
    .nav-menu {
        position: fixed;
        left: -100%;
        top: 70px;
        flex-direction: column;
        background-color: white;
        width: 100%;
        text-align: center;
        transition: 0.3s;
        box-shadow: var(--shadow);
        padding: 2rem 0;
    }
    
    .nav-menu.active {
        left: 0;
    }
    
    .hero-buttons {
        flex-direction: column;
        align-items: center;
    }
    
    .contact-content {
        grid-template-columns: 1fr;
        gap: 2rem;
    }
    
    .features-grid {
        grid-template-columns: 1fr;
    }
    
    .gallery-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 480px) {
    .nav-container {
        padding: 1rem;
    }
    
    .hero-content {
        padding: 0 1rem;
    }
    
    .container {
        padding: 0 1rem;
    }
    
    .features,
    .gallery-preview,
    .contact {
        padding: 4rem 0;
    }
}"""

        return css

    def _create_interactive_js(self) -> str:
        """สร้าง JavaScript สำหรับ Interactive Features"""
        
        js = """// Professional Website JavaScript
// Generated by AgentPro AI Enterprise Generator

document.addEventListener('DOMContentLoaded', function() {
    // Mobile Navigation
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
        
        // Close mobile menu when clicking on a link
        document.querySelectorAll('.nav-menu a').forEach(link => {
            link.addEventListener('click', () => {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });
    }
    
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Form submission
    const contactForm = document.querySelector('.contact-form form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(this);
            const name = this.querySelector('input[type="text"]').value;
            const email = this.querySelector('input[type="email"]').value;
            const message = this.querySelector('textarea').value;
            
            // Simple validation
            if (!name || !email || !message) {
                showNotification('กรุณากรอกข้อมูลให้ครบถ้วน', 'error');
                return;
            }
            
            // Simulate form submission
            showNotification('ขอบคุณ! เราได้รับข้อความของคุณแล้ว', 'success');
            this.reset();
        });
    }
    
    // Gallery image lazy loading
    const galleryImages = document.querySelectorAll('.gallery-item img');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.src;
                img.classList.add('loaded');
                observer.unobserve(img);
            }
        });
    });
    
    galleryImages.forEach(img => {
        imageObserver.observe(img);
    });
    
    // Feature cards background images
    const featureCards = document.querySelectorAll('.feature-card');
    
    featureCards.forEach(card => {
        const bgImage = card.getAttribute('data-bg');
        if (bgImage) {
            card.style.backgroundImage = `url('${bgImage}')`;
        }
    });
    
    // Parallax effect for hero section
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const hero = document.querySelector('.hero');
        
        if (hero) {
            const rate = scrolled * -0.5;
            hero.style.transform = `translateY(${rate}px)`;
        }
    });
    
    // Loading animation
    window.addEventListener('load', function() {
        document.body.classList.add('loaded');
        
        // Animate elements on scroll
        const animateOnScroll = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate');
                }
            });
        }, {
            threshold: 0.1
        });
        
        document.querySelectorAll('.feature-card, .gallery-item').forEach(el => {
            animateOnScroll.observe(el);
        });
    });
    
    // Statistics counter animation
    const counters = document.querySelectorAll('.counter');
    
    counters.forEach(counter => {
        const updateCount = () => {
            const target = +counter.getAttribute('data-target');
            const count = +counter.innerText;
            const inc = target / 100;
            
            if (count < target) {
                counter.innerText = Math.ceil(count + inc);
                setTimeout(updateCount, 20);
            } else {
                counter.innerText = target;
            }
        };
        
        // Trigger animation when element is visible
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    updateCount();
                    counterObserver.unobserve(counter);
                }
            });
        });
        
        counterObserver.observe(counter);
    });
});

// Utility Functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span>${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        z-index: 10000;
        transform: translateX(400px);
        transition: transform 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto remove
    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 5000);
    
    // Manual close
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    });
}

// Initialize when page loads
console.log('🚀 Professional website loaded successfully');
console.log('✨ Powered by AgentPro AI Enterprise Generator');"""

        return js

    def _create_about_page_with_images(self, project_type: str, images: list) -> str:
        """สร้างหน้า About พร้อมรูปภาพ"""
        
        html = """<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>เกี่ยวกับเรา - Premium Coffee House</title>
    <link rel="stylesheet" href="./assets/css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo"><h2>Premium Coffee House</h2></div>
            <ul class="nav-menu">
                <li><a href="index.html">หน้าแรก</a></li>
                <li><a href="about.html" class="active">เกี่ยวกับเรา</a></li>
                <li><a href="services.html">บริการ</a></li>
                <li><a href="gallery.html">ผลงาน</a></li>
            </ul>
        </div>
    </nav>

    <section class="page-hero" style="margin-top: 80px; padding: 4rem 0; background: var(--bg-light);">
        <div class="container">
            <h1>เกี่ยวกับเรา</h1>
            <p>เรื่องราวและปรัชญาของเรา</p>
        </div>
    </section>

    <section class="about-content" style="padding: 4rem 0;">
        <div class="container">
            <div class="about-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; align-items: center;">
                <div class="about-text">
                    <h2>ความเป็นมาของเรา</h2>
                    <p>เราเป็นร้านกาแฟที่มุ่งมั่นในการนำเสนอกาแฟคุณภาพสูงและประสบการณ์ที่ไม่เหมือนใคร</p>
                </div>
                <div class="about-image">
"""
        if images:
            html += f'<img src="./assets/images/{images[0]["filename"]}" alt="About us" style="width: 100%; border-radius: 12px;">'
        
        html += """
                </div>
            </div>
        </div>
    </section>
    <script src="./assets/js/main.js"></script>
</body>
</html>"""
        return html

    def _create_services_page_with_images(self, project_type: str, images: list) -> str:
        """สร้างหน้า Services พร้อมรูปภาพ"""
        
        html = """<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>บริการ - Premium Coffee House</title>
    <link rel="stylesheet" href="./assets/css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo"><h2>Premium Coffee House</h2></div>
            <ul class="nav-menu">
                <li><a href="index.html">หน้าแรก</a></li>
                <li><a href="about.html">เกี่ยวกับเรา</a></li>
                <li><a href="services.html" class="active">บริการ</a></li>
                <li><a href="gallery.html">ผลงาน</a></li>
            </ul>
        </div>
    </nav>

    <section class="services-content" style="margin-top: 80px; padding: 4rem 0;">
        <div class="container">
            <h1>บริการของเรา</h1>
            <div class="services-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
"""

        services = [
            {"title": "กาแฟสด", "desc": "กาแฟคุณภาพสูงจากเมล็ดคั่วสด"},
            {"title": "ขนมอบ", "desc": "ขนมอบสดใหม่ทุกวัน"},
            {"title": "บรรยากาศ", "desc": "พื้นที่สวยงามเหมาะสำหรับพักผ่อน"},
            {"title": "Wi-Fi ฟรี", "desc": "อินเทอร์เน็ตความเร็วสูงสำหรับทำงาน"}
        ]

        for i, service in enumerate(services):
            img_src = f"./assets/images/{images[i]['filename']}" if i < len(images) else ""
            html += f"""
                <div class="service-card" style="background: white; padding: 2rem; border-radius: 12px; box-shadow: var(--shadow);">
                    <img src="{img_src}" alt="{service['title']}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 8px; margin-bottom: 1rem;">
                    <h3>{service['title']}</h3>
                    <p>{service['desc']}</p>
                </div>"""

        html += """
            </div>
        </div>
    </section>
    <script src="./assets/js/main.js"></script>
</body>
</html>"""
        return html

    def _create_gallery_page_with_images(self, project_type: str, images: list) -> str:
        """สร้างหน้า Gallery พร้อมรูปภาพ"""
        
        html = """<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ผลงาน - Premium Coffee House</title>
    <link rel="stylesheet" href="./assets/css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo"><h2>Premium Coffee House</h2></div>
            <ul class="nav-menu">
                <li><a href="index.html">หน้าแรก</a></li>
                <li><a href="about.html">เกี่ยวกับเรา</a></li>
                <li><a href="services.html">บริการ</a></li>
                <li><a href="gallery.html" class="active">ผลงาน</a></li>
            </ul>
        </div>
    </nav>

    <section class="gallery-full" style="margin-top: 80px; padding: 4rem 0;">
        <div class="container">
            <h1>แกลเลอรี่</h1>
            <div class="gallery-grid">
"""

        for img in images:
            html += f"""
                <div class="gallery-item">
                    <img src="./assets/images/{img['filename']}" alt="{img['description']}" loading="lazy">
                    <div class="gallery-overlay">
                        <h4>{img['description']}</h4>
                    </div>
                </div>"""

        html += """
            </div>
        </div>
    </section>
    <script src="./assets/js/main.js"></script>
</body>
</html>"""
        return html

    async def generate_professional_website(self, requirements: Dict) -> Dict[str, Any]:
        """สร้างเว็บไซต์ Professional ครบระบบ"""
        
        project_structure = {
            "pages": {},
            "assets": {},
            "config": {},
            "documentation": {}
        }
        
        # สร้างหน้าหลัก
        pages_to_create = requirements.get("technical_specifications", {}).get("required_pages", 
                                         ["home", "about", "services", "contact"])
        
        for page_name in pages_to_create:
            page_content = await self._generate_page_content(page_name, requirements)
            project_structure["pages"][f"{page_name}.html"] = page_content
        
        # สร้าง CSS Framework
        css_framework = await self._generate_css_framework(requirements)
        project_structure["assets"]["styles.css"] = css_framework
        
        # สร้าง JavaScript Components
        js_components = await self._generate_js_components(requirements)
        project_structure["assets"]["app.js"] = js_components
        
        # สร้าง Backend API (ถ้าต้องการ)
        if self._needs_backend(requirements):
            backend_code = await self._generate_backend_api(requirements)
            project_structure["backend"] = backend_code
        
        # สร้าง Database Schema
        if self._needs_database(requirements):
            database_schema = await self._generate_database_schema(requirements)
            project_structure["database"] = database_schema
        
        return project_structure
    
    async def generate_mobile_app(self, requirements: Dict) -> Dict[str, Any]:
        """สร้างแอพมือถือที่คลิกได้จริง"""
        
        app_structure = {
            "screens": {},
            "components": {},
            "navigation": {},
            "services": {},
            "config": {}
        }
        
        # สร้างหน้าจอต่างๆ
        screens = ["SplashScreen", "LoginScreen", "HomeScreen", "ProfileScreen"]
        for screen in screens:
            screen_code = await self._generate_react_native_screen(screen, requirements)
            app_structure["screens"][f"{screen}.js"] = screen_code
        
        # สร้าง Navigation
        navigation_code = await self._generate_navigation_system(requirements)
        app_structure["navigation"]["AppNavigator.js"] = navigation_code
        
        # สร้าง Services
        services = ["AuthService", "APIService", "StorageService"]
        for service in services:
            service_code = await self._generate_service(service, requirements)
            app_structure["services"][f"{service}.js"] = service_code
        
        return app_structure
    
    async def _generate_page_content(self, page_name: str, requirements: Dict) -> str:
        """สร้างเนื้อหาหน้าเว็บที่มี Professional Quality"""
        
        prompt = f"""
        สร้างหน้า {page_name} สำหรับเว็บไซต์ Professional:
        
        Requirements: {json.dumps(requirements, indent=2)}
        
        สร้าง HTML5 ที่มี:
        - Semantic HTML structure
        - SEO optimization
        - Accessibility features
        - Modern design patterns
        - Interactive elements
        - Responsive layout
        - Professional content
        
        รวม CSS และ JavaScript inline สำหรับหน้านี้
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=4000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return self._get_fallback_page(page_name)
    
    async def _generate_react_native_screen(self, screen_name: str, requirements: Dict) -> str:
        """สร้างหน้าจอ React Native ที่ใช้งานได้จริง"""
        
        prompt = f"""
        สร้าง React Native Screen: {screen_name}
        
        Requirements: {json.dumps(requirements, indent=2)}
        
        สร้างโค้ดที่มี:
        - Functional component with hooks
        - Navigation integration
        - State management
        - Interactive buttons and inputs
        - Animations
        - Error handling
        - Professional UI/UX
        
        รวม imports ที่จำเป็นทั้งหมด
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=3000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return self._get_fallback_screen(screen_name)
    
    async def _generate_backend_api(self, requirements: Dict) -> Dict[str, str]:
        """สร้าง Backend API ที่ทำงานได้จริง"""
        
        api_endpoints = {
            "server.js": await self._generate_server_code(requirements),
            "routes/auth.js": await self._generate_auth_routes(),
            "routes/api.js": await self._generate_api_routes(),
            "models/User.js": await self._generate_user_model(),
            "middleware/auth.js": await self._generate_auth_middleware(),
            "config/database.js": await self._generate_db_config(),
            "package.json": self._generate_package_json()
        }
        
        return api_endpoints
    
    def _needs_backend(self, requirements: Dict) -> bool:
        """ตรวจสอบว่าต้องการ Backend หรือไม่"""
        features = requirements.get("technical_specifications", {}).get("functionality", [])
        backend_features = ["login", "database", "api", "payment", "user_management"]
        
        return any(feature in str(features).lower() for feature in backend_features)
    
    def _needs_database(self, requirements: Dict) -> bool:
        """ตรวจสอบว่าต้องการ Database หรือไม่"""
        return self._needs_backend(requirements)
    
    def _get_fallback_page(self, page_name: str) -> str:
        """หน้า Fallback เมื่อ AI ล้มเหลว"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_name.title()} - Professional Website</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Arial', sans-serif; line-height: 1.6; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #333; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{page_name.title()} Page</h1>
        <p>Professional {page_name} content will be generated here.</p>
    </div>
</body>
</html>"""
    
    async def deploy_project(self, project_structure: Dict, project_name: str) -> Dict[str, str]:
        """Deploy โปรเจ็กต์ไปยัง environment จริง"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_dir = Path(f"/app/workspace/{project_name}_{timestamp}")
        
        deployment_info = {
            "project_path": str(project_dir),
            "urls": {},
            "status": "deployed"
        }
        
        # สร้าง directory structure
        project_dir.mkdir(parents=True, exist_ok=True)
        
        # เขียนไฟล์ทั้งหมด
        for category, files in project_structure.items():
            if isinstance(files, dict):
                category_dir = project_dir / category
                category_dir.mkdir(exist_ok=True)
                
                for filename, content in files.items():
                    file_path = category_dir / filename
                    if isinstance(content, str):
                        file_path.write_text(content, encoding="utf-8")
                    else:
                        file_path.write_text(json.dumps(content, indent=2), encoding="utf-8")
        
        # สร้าง URLs สำหรับเข้าถึง
        if "pages" in project_structure:
            for page_file in project_structure["pages"].keys():
                page_name = page_file.replace(".html", "")
                deployment_info["urls"][page_name] = f"http://localhost:8001/projects/{project_name}_{timestamp}/pages/{page_file}"
        
        return deployment_info

# Singleton instance
enterprise_generator = EnterpriseProjectGenerator()