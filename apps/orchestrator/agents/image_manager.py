"""
🖼️ Image Management System - จัดการรูปภาพสำหรับเว็บไซต์ Professional
"""

import os
import json
import random
from pathlib import Path
from typing import Dict, List, Any, Optional

class ImageManager:
    def __init__(self, base_path: str = "C:/agent/data"):
        self.base_path = Path(base_path)
        self.image_cache = {}
        self.group_mappings = {
            # Business & Corporate
            "professional_website": ["business", "tech", "general"],
            "corporate": ["business", "technology", "general"],
            "company": ["business", "tech", "general"],
            
            # E-commerce & Retail
            "ecommerce": ["fashion", "electronics", "general"],
            "shop": ["fashion", "electronics", "bag", "man-shoes", "woman-shoes"],
            "store": ["fashion", "electronics", "beauty"],
            "retail": ["fashion", "electronics", "beauty"],
            
            # Food & Beverage
            "restaurant": ["restaurant", "thai-food", "coffee"],
            "cafe": ["coffee", "restaurant"],
            "coffee": ["coffee", "beverage"],
            "food": ["restaurant", "thai-food", "coffee"],
            "bakery": ["bakery", "coffee"],
            
            # Health & Beauty
            "beauty": ["beauty", "beauty-clinic", "spa", "salon"],
            "health": ["clinic", "beauty-clinic", "spa"],
            "spa": ["spa", "beauty", "salon"],
            "clinic": ["clinic", "beauty-clinic"],
            "salon": ["salon", "beauty", "spa"],
            
            # Travel & Hospitality
            "travel": ["travel", "travel-tour", "resort", "hotel"],
            "hotel": ["hotel", "resort", "travel"],
            "resort": ["resort", "hotel", "travel"],
            "tourism": ["travel-tour", "travel", "resort"],
            
            # Automotive
            "car": ["automotive", "car-rental"],
            "automotive": ["automotive", "car-rental"],
            
            # Education & Learning
            "education": ["education", "school", "course", "music-school"],
            "school": ["school", "education", "course"],
            "learning": ["education", "course", "music-school"],
            
            # Fitness & Sports
            "fitness": ["fitness", "sport-shoes", "yoga"],
            "gym": ["fitness", "sport-shoes"],
            "yoga": ["yoga", "fitness", "spa"],
            "sports": ["fitness", "sport-shoes", "yoga"],
            
            # Events & Entertainment
            "event": ["event", "wedding", "music-school"],
            "wedding": ["wedding", "event", "beauty"],
            "entertainment": ["event", "music-school"],
            
            # Fashion & Accessories
            "fashion": ["fashion", "bag", "man-shoes", "woman-shoes"],
            "accessories": ["bag", "man-watch", "lady-watch", "man-watch-expensive", "lady-watch-expensive"],
            "watches": ["man-watch", "lady-watch", "man-watch-expensive", "lady-watch-expensive"],
            
            # Real Estate & Construction
            "real_estate": ["real-estate", "construction", "interior-design"],
            "construction": ["construction", "real-estate", "interior-design"],
            "interior": ["interior-design", "real-estate"],
            
            # Pets & Animals
            "pet": ["pet-shop", "vet"],
            "veterinary": ["vet", "pet-shop"],
            
            # Flowers & Plants
            "flower": ["flower-shop", "wedding", "beauty"],
        }

    def scan_available_images(self) -> Dict[str, List[str]]:
        """สแกนรูปภาพที่มีอยู่ทั้งหมด"""
        
        available_images = {}
        
        for group_folder in self.base_path.iterdir():
            if group_folder.is_dir():
                raw_folder = group_folder / "raw"
                if raw_folder.exists():
                    images = []
                    for img_file in raw_folder.iterdir():
                        if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                            images.append(img_file.name)
                    
                    if images:
                        available_images[group_folder.name] = images
        
        self.image_cache = available_images
        return available_images

    def get_images_for_project(self, project_type: str, count: int = 10) -> Dict[str, Any]:
        """เลือกรูปภาพที่เหมาะสมสำหรับ project type"""
        
        if not self.image_cache:
            self.scan_available_images()
        
        # หาก group ที่เหมาะสม
        relevant_groups = self.group_mappings.get(project_type.lower(), ["general", "business"])
        
        selected_images = []
        image_info = {}
        
        for group in relevant_groups:
            if group in self.image_cache and len(selected_images) < count:
                available = self.image_cache[group]
                needed = min(count - len(selected_images), len(available))
                
                # เลือกแบบสุ่ม
                selected = random.sample(available, needed)
                
                for img_name in selected:
                    img_path = f"data/{group}/raw/{img_name}"
                    selected_images.append({
                        "filename": img_name,
                        "path": img_path,
                        "full_path": str(self.base_path / group / "raw" / img_name),
                        "group": group,
                        "url": f"./data/{group}/raw/{img_name}",
                        "description": self._generate_description(img_name, group)
                    })
        
        # หากยังไม่พอ ให้เลือกจาก general
        if len(selected_images) < count and "general" in self.image_cache:
            remaining = count - len(selected_images)
            general_images = self.image_cache["general"]
            additional = random.sample(general_images, min(remaining, len(general_images)))
            
            for img_name in additional:
                selected_images.append({
                    "filename": img_name,
                    "path": f"data/general/raw/{img_name}",
                    "full_path": str(self.base_path / "general" / "raw" / img_name),
                    "group": "general",
                    "url": f"./data/general/raw/{img_name}",
                    "description": self._generate_description(img_name, "general")
                })
        
        return {
            "project_type": project_type,
            "total_images": len(selected_images),
            "relevant_groups": relevant_groups,
            "images": selected_images,
            "css_urls": [img["url"] for img in selected_images]
        }

    def get_hero_image(self, project_type: str) -> Optional[Dict[str, Any]]:
        """เลือกรูปหลักสำหรับ Hero Section"""
        
        images = self.get_images_for_project(project_type, 5)
        if images["images"]:
            hero = random.choice(images["images"])
            hero["is_hero"] = True
            return hero
        return None

    def get_gallery_images(self, project_type: str, count: int = 6) -> List[Dict[str, Any]]:
        """เลือกรูปสำหรับ Gallery/Portfolio"""
        
        images = self.get_images_for_project(project_type, count)
        return images["images"]

    def _generate_description(self, filename: str, group: str) -> str:
        """สร้างคำอธิบายรูปภาพ"""
        
        # ลบเลขและนามสกุลออก
        base_name = filename.split('-', 1)[-1] if '-' in filename else filename
        base_name = base_name.rsplit('.', 1)[0]
        
        # แทนที่ - ด้วย space
        description = base_name.replace('-', ' ').title()
        
        # เพิ่ม context ตาม group
        group_contexts = {
            "coffee": "Professional coffee shop atmosphere",
            "restaurant": "Fine dining restaurant experience", 
            "business": "Modern business environment",
            "technology": "Cutting-edge technology solutions",
            "fashion": "Latest fashion trends and style",
            "beauty": "Premium beauty and wellness services",
            "travel": "Amazing travel destinations and experiences",
            "fitness": "Professional fitness and health services",
            "real-estate": "Premium real estate properties"
        }
        
        context = group_contexts.get(group, "Professional business image")
        return f"{description} - {context}"

    def generate_css_with_images(self, project_type: str) -> str:
        """สร้าง CSS ที่ใช้รูปภาพจริง"""
        
        images = self.get_images_for_project(project_type, 8)
        hero_img = self.get_hero_image(project_type)
        
        css = """/* Generated CSS with Real Images */
"""
        
        if hero_img:
            css += f"""
.hero-section {{
    background-image: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('{hero_img["url"]}');
    background-size: cover;
    background-position: center;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
}}
"""
        
        # Gallery Images
        for i, img in enumerate(images["images"][:6]):
            css += f"""
.gallery-item-{i+1} {{
    background-image: url('{img["url"]}');
    background-size: cover;
    background-position: center;
}}
"""
        
        # Card backgrounds
        for i, img in enumerate(images["images"][:4]):
            css += f"""
.feature-card-{i+1}::before {{
    background-image: url('{img["url"]}');
    background-size: cover;
    background-position: center;
    opacity: 0.1;
}}
"""
        
        return css

    def copy_images_to_project(self, project_path: str, project_type: str) -> Dict[str, Any]:
        """คัดลอกรูปภาพไปยัง project folder"""
        
        import shutil
        
        project_path = Path(project_path)
        assets_path = project_path / "assets" / "images"
        assets_path.mkdir(parents=True, exist_ok=True)
        
        images = self.get_images_for_project(project_type, 10)
        copied_files = []
        
        for img in images["images"]:
            src_path = Path(img["full_path"])
            dest_path = assets_path / img["filename"]
            
            if src_path.exists():
                shutil.copy2(src_path, dest_path)
                copied_files.append({
                    "original": str(src_path),
                    "copied": str(dest_path),
                    "relative_url": f"./assets/images/{img['filename']}",
                    "description": img["description"]
                })
        
        return {
            "success": True,
            "copied_count": len(copied_files),
            "copied_files": copied_files,
            "assets_path": str(assets_path)
        }

# Global instance
image_manager = ImageManager()