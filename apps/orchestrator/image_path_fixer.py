"""
🔧 Image Path Fixer - แก้ไขปัญหา path รูปภาพในเว็บไซต์
"""
import os
import re
import shutil
from pathlib import Path

class ImagePathFixer:
    def __init__(self, workspace_path="C:/agent/workspace"):
        self.workspace_path = workspace_path
        
    def scan_broken_images(self, site_path):
        """สแกนหารูปภาพที่ path ไม่ถูกต้อง"""
        broken_images = []
        html_files = []
        
        # หาไฟล์ HTML ทั้งหมด
        for root, dirs, files in os.walk(site_path):
            for file in files:
                if file.endswith('.html'):
                    html_files.append(os.path.join(root, file))
        
        # ตรวจสอบ path รูปภาพในแต่ละไฟล์
        for html_file in html_files:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # หา img src และ background-image
            img_patterns = [
                r'src="([^"]*\.(jpg|jpeg|png|gif|webp))"',
                r"src='([^']*\.(jpg|jpeg|png|gif|webp))'",
                r'url\([\'"]?([^\'")]*\.(jpg|jpeg|png|gif|webp))[\'"]?\)',
                r'data-bg="([^"]*\.(jpg|jpeg|png|gif|webp))"'
            ]
            
            for pattern in img_patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    img_path = match.group(1)
                    full_path = os.path.join(site_path, img_path.lstrip('./'))
                    
                    if not os.path.exists(full_path):
                        broken_images.append({
                            'file': html_file,
                            'path': img_path,
                            'full_path': full_path,
                            'pattern': match.group(0)
                        })
        
        return broken_images
    
    def get_available_images(self, site_path):
        """ได้รายชื่อรูปภาพที่มีอยู่จริง"""
        assets_images = os.path.join(site_path, 'assets', 'images')
        available_images = []
        
        if os.path.exists(assets_images):
            for file in os.listdir(assets_images):
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    available_images.append(file)
                    
        return sorted(available_images)
    
    def fix_broken_images(self, site_path):
        """แก้ไขรูปภาพที่เสีย"""
        print(f"🔧 แก้ไข {os.path.basename(site_path)}...")
        
        broken_images = self.scan_broken_images(site_path)
        available_images = self.get_available_images(site_path)
        
        if not available_images:
            print(f"  ❌ ไม่พบรูปภาพใน assets/images")
            return False
            
        print(f"  📊 รูปภาพเสีย: {len(broken_images)} รูป")
        print(f"  📊 รูปภาพที่มี: {len(available_images)} รูป")
        
        if not broken_images:
            print(f"  ✅ ไม่พบปัญหารูปภาพ")
            return True
            
        # แก้ไขรูปภาพเสียโดยใช้รูปที่มี
        fixed_files = set()
        replacement_idx = 0
        
        for broken in broken_images:
            # เลือกรูปทดแทน
            if replacement_idx < len(available_images):
                replacement_img = available_images[replacement_idx]
                replacement_idx = (replacement_idx + 1) % len(available_images)
            else:
                replacement_img = available_images[0]
            
            # อ่านไฟล์และแทนที่
            try:
                with open(broken['file'], 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # แทนที่ path เก่าด้วยใหม่
                old_path = broken['path']
                new_path = f"./assets/images/{replacement_img}"
                
                content = content.replace(old_path, new_path)
                
                with open(broken['file'], 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                fixed_files.add(broken['file'])
                print(f"    🔄 แทนที่: {os.path.basename(old_path)} → {replacement_img}")
                
            except Exception as e:
                print(f"    ❌ ข้อผิดพลาด: {e}")
        
        print(f"  ✅ แก้ไขไฟล์: {len(fixed_files)} ไฟล์")
        return True
    
    def fix_all_websites(self):
        """แก้ไขทุกเว็บไซต์ใน workspace"""
        print("🚀 เริ่มแก้ไขปัญหารูปภาพในทุกเว็บไซต์...\n")
        
        sites_fixed = 0
        for item in os.listdir(self.workspace_path):
            site_path = os.path.join(self.workspace_path, item)
            
            if os.path.isdir(site_path) and not item.startswith('.'):
                # ตรวจสอบว่าเป็นเว็บไซต์ (มี index.html หรือ assets)
                has_html = any(f.endswith('.html') for f in os.listdir(site_path))
                has_assets = os.path.exists(os.path.join(site_path, 'assets'))
                
                if has_html or has_assets:
                    if self.fix_broken_images(site_path):
                        sites_fixed += 1
                    print()
        
        print(f"🎉 แก้ไขเสร็จสิ้น! เว็บไซต์ที่แก้ไข: {sites_fixed} เว็บไซต์")
        return sites_fixed

if __name__ == "__main__":
    fixer = ImagePathFixer()
    fixer.fix_all_websites()