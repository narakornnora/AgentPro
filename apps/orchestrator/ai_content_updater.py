"""
🤖 AI Content Updater - อัพเดทเนื้อหาเว็บไซต์ด้วย AI อัตโนมัติ
"""
import os
import json
import re
from pathlib import Path

class AIContentUpdater:
    def __init__(self):
        self.updated_files = []
        
    def load_content_suggestions(self, site_path):
        """โหลดข้อเสนอแนะเนื้อหาจากไฟล์ JSON"""
        content_file = os.path.join(site_path, "content_suggestions.json")
        
        if not os.path.exists(content_file):
            return None
            
        with open(content_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def update_alt_texts(self, html_file, content_data):
        """อัพเดท alt text ของรูปภาพ"""
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated = False
        
        for img_data in content_data:
            filename = img_data['filename']
            new_alt_text = img_data['alt_text']
            
            # หาและแทนที่ alt text
            patterns = [
                rf'<img([^>]*?)src="[^"]*{re.escape(filename)}"([^>]*?)alt="([^"]*?)"([^>]*?)>',
                rf'<img([^>]*?)alt="([^"]*?)"([^>]*?)src="[^"]*{re.escape(filename)}"([^>]*?)>'
            ]
            
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    old_alt = match.group(3) if len(match.groups()) >= 3 else ""
                    if old_alt != new_alt_text:
                        # แทนที่ alt text เก่าด้วยใหม่
                        old_img_tag = match.group(0)
                        new_img_tag = re.sub(r'alt="[^"]*"', f'alt="{new_alt_text}"', old_img_tag)
                        content = content.replace(old_img_tag, new_img_tag)
                        updated = True
                        print(f"    📝 อัพเดท alt: {filename}")
        
        if updated:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
        return updated
    
    def enhance_image_descriptions(self, html_file, content_data, project_type):
        """เพิ่มคำอธิบายรูปภาพในส่วน gallery"""
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated = False
        
        # หา gallery items และเพิ่มเนื้อหา
        gallery_pattern = r'<div class="gallery-item"[^>]*>(.*?)</div>'
        matches = re.finditer(gallery_pattern, content, re.DOTALL | re.IGNORECASE)
        
        for match in matches:
            gallery_item = match.group(0)
            gallery_content = match.group(1)
            
            # หารูปภาพใน gallery item นี้
            img_match = re.search(r'src="[^"]*([^/]*\.(jpg|png|jpeg))"', gallery_content)
            if img_match:
                img_filename = img_match.group(1)
                
                # หาข้อมูลรูปภาพ
                img_data = next((item for item in content_data if item['filename'] == img_filename), None)
                if img_data and img_data['related_content']:
                    # ตรวจสอบว่ามี overlay หรือไม่
                    if 'gallery-overlay' in gallery_content:
                        # อัพเดทเนื้อหาใน overlay
                        overlay_match = re.search(r'<div class="gallery-overlay">(.*?)</div>', gallery_content, re.DOTALL)
                        if overlay_match:
                            overlay_content = overlay_match.group(1)
                            
                            # เพิ่มเนื้อหาใหม่
                            if len(img_data['related_content']) > 0:
                                new_description = img_data['related_content'][0]
                                
                                # ตรวจสอบว่ามี <p> อยู่แล้วหรือไม่
                                if not re.search(r'<p[^>]*>.*?</p>', overlay_content, re.DOTALL):
                                    # เพิ่ม paragraph ใหม่
                                    h4_match = re.search(r'(<h4[^>]*>.*?</h4>)', overlay_content)
                                    if h4_match:
                                        new_overlay = overlay_content.replace(
                                            h4_match.group(1),
                                            h4_match.group(1) + f'\\n                        <p>{new_description}</p>'
                                        )
                                        
                                        new_gallery_item = gallery_item.replace(overlay_content, new_overlay)
                                        content = content.replace(gallery_item, new_gallery_item)
                                        updated = True
                                        print(f"    ✨ เพิ่มคำอธิบาย: {img_filename}")
        
        if updated:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
        return updated
    
    def update_hero_content(self, html_file, suggestions):
        """อัพเดทเนื้อหาในส่วน Hero"""
        if not suggestions.get('hero_suggestions'):
            return False
            
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated = False
        hero_texts = suggestions['hero_suggestions']
        
        # หา hero subtitle และอัพเดท
        subtitle_pattern = r'<p class="hero-subtitle"[^>]*>(.*?)</p>'
        subtitle_match = re.search(subtitle_pattern, content, re.DOTALL)
        
        if subtitle_match and len(hero_texts) > 1:
            current_subtitle = subtitle_match.group(1).strip()
            new_subtitle = hero_texts[1]  # ใช้ข้อความที่ 2
            
            if current_subtitle != new_subtitle:
                new_subtitle_tag = f'<p class="hero-subtitle">{new_subtitle}</p>'
                content = content.replace(subtitle_match.group(0), new_subtitle_tag)
                updated = True
                print(f"    🎯 อัพเดท Hero subtitle")
        
        if updated:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
        return updated
    
    def add_content_metadata(self, html_file, suggestions):
        """เพิ่ม metadata สำหรับ SEO"""
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated = False
        
        # เพิ่ม meta description
        if not re.search(r'<meta name="description"', content):
            if suggestions.get('hero_suggestions'):
                description = suggestions['hero_suggestions'][0]
                meta_description = f'    <meta name="description" content="{description}">'
                
                # หาตำแหน่งที่เหมาะสมใน <head>
                head_match = re.search(r'(<title>.*?</title>)', content, re.DOTALL)
                if head_match:
                    new_head = head_match.group(0) + '\\n' + meta_description
                    content = content.replace(head_match.group(0), new_head)
                    updated = True
                    print(f"    🔍 เพิ่ม SEO meta description")
        
        if updated:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
        return updated
    
    def update_website_content(self, site_path):
        """อัพเดทเนื้อหาทั้งเว็บไซต์"""
        site_name = os.path.basename(site_path)
        print(f"🤖 อัพเดทเนื้อหา {site_name}...")
        
        # โหลดข้อเสนอแนะ
        suggestions = self.load_content_suggestions(site_path)
        if not suggestions:
            print(f"  ❌ ไม่พบไฟล์ content suggestions")
            return False
        
        # หาไฟล์ HTML ทั้งหมด
        html_files = []
        for root, dirs, files in os.walk(site_path):
            for file in files:
                if file.endswith('.html'):
                    html_files.append(os.path.join(root, file))
        
        total_updates = 0
        content_data = suggestions.get('content_data', [])
        
        for html_file in html_files:
            file_updates = 0
            filename = os.path.basename(html_file)
            
            print(f"  📄 ปรับปรุง {filename}...")
            
            # อัพเดท alt texts
            if self.update_alt_texts(html_file, content_data):
                file_updates += 1
            
            # เสริมคำอธิบายรูปภาพ
            if self.enhance_image_descriptions(html_file, content_data, suggestions['project_type']):
                file_updates += 1
                
            # อัพเดท hero content (เฉพาะ index.html)
            if filename == 'index.html':
                if self.update_hero_content(html_file, suggestions):
                    file_updates += 1
                    
                if self.add_content_metadata(html_file, suggestions):
                    file_updates += 1
            
            if file_updates > 0:
                total_updates += file_updates
                self.updated_files.append(html_file)
        
        print(f"  ✅ อัพเดทเสร็จสิ้น: {total_updates} การเปลี่ยนแปลง")
        return total_updates > 0
    
    def update_all_websites(self):
        """อัพเดทเนื้อหาทุกเว็บไซต์"""
        workspace_path = "C:/agent/workspace"
        print("🚀 เริ่มอัพเดทเนื้อหาด้วย AI...\n")
        
        updated_sites = 0
        total_changes = 0
        
        for item in os.listdir(workspace_path):
            site_path = os.path.join(workspace_path, item)
            
            if os.path.isdir(site_path) and not item.startswith('.'):
                has_html = any(f.endswith('.html') for f in os.listdir(site_path))
                if has_html:
                    if self.update_website_content(site_path):
                        updated_sites += 1
                    print()
        
        print(f"🎉 อัพเดทเสร็จสิ้น!")
        print(f"📊 เว็บไซต์ที่อัพเดท: {updated_sites} เว็บไซต์")
        print(f"📄 ไฟล์ที่เปลี่ยนแปลง: {len(self.updated_files)} ไฟล์")
        
        return updated_sites

if __name__ == "__main__":
    updater = AIContentUpdater()
    updater.update_all_websites()