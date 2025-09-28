"""
🎨 Smart Content Generator - ตัวช่วย AI สำหรับสร้างและเติมเนื้อหาที่เกี่ยวข้องกับรูปภาพ
"""
import os
import json
import asyncio
from pathlib import Path

class SmartContentGenerator:
    def __init__(self):
        self.image_descriptions = {
            # Coffee Shop Images
            "cafe-drink-menu": "เมนูเครื่องดื่มสำหรับร้านกาแฟ พร้อมรายการกาแฟหลากหลายชนิด",
            "espresso-bar": "บาร์เอสเปรสโซ่แสดงความเป็นมืออาชีพ",
            "coffee-latte-art": "ลาเต้อาร์ตสวยงาม แสดงฝีมือบาริสต้า",
            "coffee-beans": "เมล็ดกาแฟคุณภาพสูง อบใหม่หอมกรุ่น",
            "graffiti-wall": "ผนังศิลปะในร้านกาแฟ สร้างบรรยากาศแปลกใหม่",
            
            # Restaurant Images
            "dish-ceramic-plate": "จานอาหารระดับมิชลิน จัดเสิร์ฟอย่างมีศิลปะ",
            "brown-themed-bar": "บาร์สไตล์คลาสสิก บรรยากาศอบอุ่น",
            "wooden-tables-chairs": "โต๊ะไม้และเก้าอี้ สไตล์ร่วมสมัย",
            "chef-plating": "เชฟมืออาชีพจัดจานอาหารด้วยความประณีต",
            
            # Business Images  
            "jigsaw-puzzle": "การทำงานเป็นทีม การแก้ปัญหาร่วมกัน",
            "sea-waves": "ความสงบและความมั่นคงในการดำเนินธุรกิจ",
            "mountain-range": "วิสัยทัศน์ระยะไกล การมองการณ์ไกล",
            "port-cranes": "โครงสร้างพื้นฐาน การขนส่งและโลจิสติกส์",
            
            # Fashion Images
            "white-black-sneakers": "รองเท้าผ้าใบแฟชั่น สไตล์มินิมอล",
            "afro-hair-woman": "ผู้หญิงสมัยใหม่ มั่นใจในตัวเอง",
            "stylish-woman": "แฟชั่นผู้หญิง ความเป็นเลิศทางสไตล์",
            "red-stilettos": "รองเท้าส้นสูงสีแดง สัญลักษณ์ความมั่นใจ"
        }
        
        self.content_templates = {
            "hero_text": {
                "coffee": [
                    "ต้อนรับสู่โลกแห่งกาแฟพรีเมียม",
                    "กาแฟคุณภาพสูง บรรยากาศดี บริการจากใจ",
                    "เริ่มต้นวันใหม่ด้วยกาแฟสุดพิเศษ"
                ],
                "restaurant": [
                    "ประสบการณ์รับประทานอาหารระดับโลก",
                    "อาหารเลิศรส จากเชฟชั้นนำ",
                    "Fine Dining Experience ที่ไม่เหมือนใคร"
                ],
                "business": [
                    "พาธุรกิจของคุณไปสู่อนาคต",
                    "โซลูชันธุรกิจที่ครบครัน",
                    "ความสำเร็จที่เริ่มต้นจากการวางแผนที่ดี"
                ],
                "fashion": [
                    "แฟชั่นที่สะท้อนบุคลิกภาพคุณ",
                    "สไตล์ที่ไม่เคยตกยุค",
                    "ความมั่นใจเริ่มต้นจากการแต่งตัว"
                ]
            },
            "feature_descriptions": {
                "coffee": {
                    "quality": "เมล็ดกาแฟคัดสรรจากแหล่งปลูกชั้นนำ อบใหม่ทุกวัน",
                    "atmosphere": "บรรยากาศอบอุ่น เหมาะสำหรับทำงาน พบปะเพื่อน",
                    "service": "บาริสต้ามืออาชีญ พร้อมให้คำแนะนำเครื่องดื่ม",
                    "location": "ทำเลสะดวก จอดรถง่าย เข้าถึงได้ทุกขนส่ง"
                },
                "restaurant": {
                    "cuisine": "อาหารนานาชาติ ปรุงด้วยวัตถุดิบคุณภาพสูง",
                    "ambiance": "การตกแต่งหรูหรา บรรยากาศโรแมนติก",
                    "chef": "เชฟมืออาชีพ ประสบการณ์ระดับโลก",
                    "service": "บริการระดับพรีเมียม ใส่ใจทุกรายละเอียด"
                },
                "business": {
                    "innovation": "เทคโนโลยีล้ำสมัย นวัตกรรมที่ตอบโจทย์",
                    "efficiency": "เพิ่มประสิทธิภาพ ลดต้นทุน เพิ่มผลกำไร",
                    "support": "ทีมงานมืออาชีพ สนับสนุน 24/7",
                    "growth": "การเติบโตที่ยั่งยืน วิสัยทัศน์ระยะยาว"
                },
                "fashion": {
                    "style": "แฟชั่นทันสมัย ไม่เคยตกยุค",
                    "quality": "วัสดุคุณภาพสูง ความทนทาน",
                    "variety": "หลากหลายสไตล์ เหมาะทุกโอกาส",
                    "confidence": "เสริมความมั่นใจ สะท้อนบุคลิกภาพ"
                }
            }
        }
    
    def generate_image_alt_text(self, image_filename):
        """สร้าง alt text ที่เหมาะสมสำหรับรูปภาพ"""
        filename = image_filename.lower()
        
        # วิเคราะห์ชื่อไฟล์เพื่อสร้าง alt text
        keywords = []
        
        if "coffee" in filename or "cafe" in filename:
            keywords.append("กาแฟ")
        if "latte" in filename:
            keywords.append("ลาเต้")
        if "espresso" in filename:
            keywords.append("เอสเปรสโซ่")
        if "menu" in filename:
            keywords.append("เมนู")
        if "dish" in filename or "plate" in filename:
            keywords.append("อาหาร")
        if "chef" in filename:
            keywords.append("เชฟ")
        if "woman" in filename or "fashion" in filename:
            keywords.append("แฟชั่น")
        if "business" in filename:
            keywords.append("ธุรกิจ")
            
        if keywords:
            return f"รูปภาพ{' '.join(keywords)} - บรรยากาศมืออาชีพ"
        else:
            return f"รูปภาพคุณภาพสูง - {image_filename.split('.')[0]}"
    
    def generate_content_for_image(self, image_filename, project_type):
        """สร้างเนื้อหาที่เกี่ยวข้องกับรูปภาพ"""
        alt_text = self.generate_image_alt_text(image_filename)
        
        content = {
            "filename": image_filename,
            "alt_text": alt_text,
            "suggested_usage": [],
            "related_content": []
        }
        
        # เสนอการใช้งานตามประเภทโปรเจกต์
        if project_type in ["coffee", "cafe"]:
            if "menu" in image_filename.lower():
                content["suggested_usage"] = ["หน้าเมนู", "ส่วนผลิตภัณฑ์", "แกลเลอรี่"]
                content["related_content"] = [
                    "เมนูเครื่องดื่มหลากหลาย",
                    "กาแฟคุณภาพพรีเมียม",
                    "ราคาเหมาะสม คุ้มค่า"
                ]
            elif "coffee" in image_filename.lower():
                content["suggested_usage"] = ["หน้าแรก Hero", "เกี่ยวกับเรา", "แกลเลอรี่"]
                content["related_content"] = [
                    "กาแฟสด อบใหม่ทุกวัน",
                    "บาริสต้ามืออาชีพ",
                    "บรรยากาศอบอุ่น"
                ]
                
        elif project_type == "restaurant":
            if "dish" in image_filename.lower():
                content["suggested_usage"] = ["เมนูอาหาร", "หน้าแรก", "แกลเลอรี่"]
                content["related_content"] = [
                    "อาหารนานาชาติ คุณภาพพรีเมียม",
                    "วัตถุดิบสด นำเข้าคุณภาพ",
                    "การจัดจานที่สวยงาม"
                ]
            elif "chef" in image_filename.lower():
                content["suggested_usage"] = ["เกี่ยวกับเรา", "ทีมงาน", "หน้าแรก"]
                content["related_content"] = [
                    "เชฟมืออาชีพ ประสบการณ์สูง",
                    "ฝีมือระดับมิชลิน",
                    "ความใส่ใจในทุกรายละเอียด"
                ]
                
        return content
    
    async def enhance_website_content(self, site_path):
        """เสริมเนื้อหาเว็บไซต์ด้วย AI"""
        print(f"🎨 เสริมเนื้อหา {os.path.basename(site_path)}...")
        
        # ตรวจสอบประเภทเว็บไซต์
        site_name = os.path.basename(site_path).lower()
        if "coffee" in site_name:
            project_type = "coffee"
        elif "restaurant" in site_name:
            project_type = "restaurant"
        elif "business" in site_name:
            project_type = "business"
        elif "fashion" in site_name:
            project_type = "fashion"
        else:
            project_type = "general"
        
        # วิเคราะห์รูปภาพที่มี
        assets_path = os.path.join(site_path, "assets", "images")
        if not os.path.exists(assets_path):
            print(f"  ❌ ไม่พบโฟลเดอร์ assets/images")
            return False
            
        images = [f for f in os.listdir(assets_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        
        # สร้างเนื้อหาสำหรับแต่ละรูป
        content_data = []
        for img in images:
            content = self.generate_content_for_image(img, project_type)
            content_data.append(content)
            
        # บันทึกข้อมูลเนื้อหา
        content_file = os.path.join(site_path, "content_suggestions.json")
        with open(content_file, 'w', encoding='utf-8') as f:
            json.dump({
                "project_type": project_type,
                "total_images": len(images),
                "content_data": content_data,
                "hero_suggestions": self.content_templates["hero_text"].get(project_type, []),
                "feature_suggestions": self.content_templates["feature_descriptions"].get(project_type, {})
            }, f, ensure_ascii=False, indent=2)
            
        print(f"  ✅ สร้างเนื้อหา: {len(images)} รูปภาพ")
        print(f"  📝 บันทึก: content_suggestions.json")
        
        return True
    
    async def enhance_all_websites(self):
        """เสริมเนื้อหาทุกเว็บไซต์"""
        workspace_path = "C:/agent/workspace"
        print("🚀 เริ่มสร้างเนื้อหาอัจฉริยะ...\n")
        
        enhanced_count = 0
        for item in os.listdir(workspace_path):
            site_path = os.path.join(workspace_path, item)
            
            if os.path.isdir(site_path) and not item.startswith('.'):
                has_html = any(f.endswith('.html') for f in os.listdir(site_path))
                if has_html:
                    success = await self.enhance_website_content(site_path)
                    if success:
                        enhanced_count += 1
                    print()
        
        print(f"🎉 เสร็จสิ้น! เว็บไซต์ที่เสริมเนื้อหา: {enhanced_count} เว็บไซต์")
        return enhanced_count

if __name__ == "__main__":
    generator = SmartContentGenerator()
    asyncio.run(generator.enhance_all_websites())