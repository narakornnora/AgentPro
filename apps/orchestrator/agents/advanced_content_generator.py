"""
🧠 Advanced Content Generator - AI สร้างเนื้อหาเฉพาะแต่ละประเภทธุรกิจ
"""
import json
import random
from typing import Dict, List, Any, Tuple
from .business_analyzer import business_analyzer

class AdvancedContentGenerator:
    def __init__(self):
        self.content_templates = {
            "coffee_shop": {
                "hero_messages": [
                    "เริ่มต้นวันใหม่ด้วยกาแฟสุดพิเศษ",
                    "กาแฟคุณภาพ บรรยากาศดี บริการจากใจ",
                    "ต้อนรับสู่โลกแห่งกาแฟพรีเมียม",
                    "ความหอมกรุ่นที่ปลุกเซลล์ความรู้สึก"
                ],
                "value_propositions": [
                    "เมล็ดกาแฟคัดสรร จากไร่สูงเฉพาะ",
                    "บาริสต้ามืออาชีพ พร้อมให้คำปรึกษา",
                    "บรรยากาศอบอุ่น เหมาะสำหรับทำงาน",
                    "เปิดเสิร์ฟตั้งแต่เช้าตรู่ถึงดึก"
                ],
                "service_descriptions": {
                    "specialty_coffee": "กาแฟสเปเชียลตี้ จากเมล็ดคัดพิเศษ ปรุงด้วยฝีมือบาริสต้ามืออาชีพ",
                    "food_pairing": "ขนมอบสดใหม่ และอาหารเบาๆ ที่คู่กับกาแฟได้อย่างลงตัว",
                    "workspace": "พื้นที่ทำงาน Wi-Fi เร็ว เต้าเสียบครบ บรรยากาศเอื้อต่อการทำงาน",
                    "events": "พื้นที่จัดงาน workshop การเรียนรู้ และกิจกรรมชุมชน"
                },
                "page_content": {
                    "about": "เราเป็นร้านกาแฟท่ีมุ่งมั่นนำเสนอกาแฟคุณภาพสูงและประสบการณ์ที่ยากลืม",
                    "menu": "เลือกสรรเมล็ดกาแฟจากทั่วโลก ปรุงด้วยความใส่ใจในทุกรายละเอียด",
                    "contact": "เราต้อนรับทุกคนด้วยใจที่อบอุ่น มาสัมผัสประสบการณ์กาแฟสุดพิเศษ"
                }
            },
            
            "restaurant": {
                "hero_messages": [
                    "ประสบการณ์รับประทานอาหารระดับโลก",
                    "อาหารเลิศรส จากเชฟชั้นนำ",
                    "Fine Dining Experience ที่ไม่เหมือนใคร",
                    "ความหรูหราที่สัมผัสได้ในทุกคำ"
                ],
                "value_propositions": [
                    "เชฟมืออาชีพ ประสบการณ์ระดับโลก",
                    "วัตถุดิบคุณภาพสูง นำเข้าพิเศษ",
                    "บรรยากาศหรูหรา เหมาะสำหรับโอกาสพิเศษ",
                    "บริการส่วนตัว ใส่ใจทุกรายละเอียด"
                ],
                "service_descriptions": {
                    "fine_dining": "อาหารระดับมิชลิน จัดเสิร์ฟด้วยศิลปะการนำเสนอที่สวยงาม",
                    "wine_pairing": "การจับคู่ไวน์ที่ลงตัว เสริมรสชาติอาหารให้โดดเด่น",
                    "private_dining": "ห้องส่วนตัวสำหรับงานเลี้ยงพิเศษ การประชุม หรือฉลอง",
                    "chef_table": "Chef's Table ประสบการณ์การรับประทานอาหารใกล้ชิดกับเชฟ"
                },
                "page_content": {
                    "about": "ร้านอาหารของเราก่อตั้งขึ้นด้วยปรัชญาการนำเสนออาหารคุณภาพสูงและประสบการณ์ที่ยอดเยี่ยม",
                    "menu": "เมนูอาหารที่ผสมผสานเทคนิคสมัยใหม่กับรสชาติดั้งเดิม สร้างสรรค์ใหม่ในทุกจาน",
                    "contact": "จองโต๊ะล่วงหน้าเพื่อประสบการณ์ที่ดีที่สุด เราพร้อมต้อนรับด้วยบริการระดับพรีเมียม"
                }
            },
            
            "fashion_boutique": {
                "hero_messages": [
                    "แฟชั่นที่สะท้อนบุคลิกภาพคุณ",
                    "สไตล์ที่ไม่เคยตกยุค เรียบง่ายแต่หรูหรา",
                    "ความมั่นใจเริ่มต้นจากการแต่งตัว",
                    "Fashion Forward สำหรับผู้หญิงยุคใหม่"
                ],
                "value_propositions": [
                    "ดีไซน์เฉพาะตัว ไม่ซ้ำใครในโลก",
                    "ผ้าคุณภาพสูง สัมผัสนุ่มลื่น ใส่สบาย",
                    "เทรนด์แฟชั่นล่าสุด จากรันเวย์สู่ตู้เสื้อผ้า",
                    "บริการส่วนตัว Fashion Stylist มืออาชีพ"
                ],
                "service_descriptions": {
                    "personal_styling": "บริการ Personal Stylist ช่วยเลือกชุดที่เหมาะกับบุคลิกและโอกาส",
                    "custom_tailoring": "บริการตัดเสื้อผ้าพิเศษ ปรับแต่งให้เข้ากับรูปร่างได้อย่างสมบูรณ์แบบ",
                    "seasonal_collection": "คอลเล็กชันตามฤดูกาล ทันเทรนด์แฟชั่นโลก",
                    "vip_membership": "สมาชิก VIP ได้รับสิทธิพิเศษ ส่วนลด และเข้าถึงคอลเล็กชันก่อนใคร"
                },
                "page_content": {
                    "about": "เราเป็นบูทีคแฟชั่นที่มุ่งมั่นสร้างสรรค์เสื้อผ้าที่เสริมความมั่นใจและเปิดเผยบุคลิกภาพเฉพาะตัว",
                    "collection": "คอลเล็กชันล่าสุดที่ผสมผสานความคลาสสิกกับความทันสมัย เหมาะสำหรับผู้หญิงยุคใหม่",
                    "contact": "มาค้นพบสไตล์ที่เป็นคุณ ทีมงานของเรายินดีให้คำปรึกษาแฟชั่นแบบส่วนตัว"
                }
            },
            
            "business_corporate": {
                "hero_messages": [
                    "พาธุรกิจของคุณไปสู่อนาคต",
                    "โซลูชันธุรกิจที่ครบครัน เชี่ยวชาญทุกด้าน",
                    "ความสำเร็จที่เริ่มต้นจากการวางแฝนที่ดี",
                    "พันธมิตรที่เชื่อถือได้ในการเติบโตของธุรกิจ"
                ],
                "value_propositions": [
                    "ทีมงานผู้เชี่ยวชาญ ประสบการณ์หลายสิบปี",
                    "เทคโนโลยีล้ำสมัย นวัตกรรมที่ตอบโจทย์",
                    "ผลงานที่โดดเด่น ลูกค้าชั้นนำทั่วประเทศ",
                    "บริการครบวงจร ตั้งแต่วางแผนถึงดำเนินการ"
                ],
                "service_descriptions": {
                    "consulting": "บริการที่ปรึกษาธุรกิจ วิเคราะห์ วางแผนกลยุทธ์ และพัฒนาองค์กร",
                    "technology": "พัฒนาระบบเทคโนโลยี Digital Transformation เพื่อเพิ่มประสิทธิภาพ",
                    "project_management": "บริหารโครงการขนาดใหญ่ ครบวงจร ตรงเวลา ตรงงบประมาณ",
                    "training": "อบรมและพัฒนาบุคลากร เพิ่มทักษะและความรู้ให้ทันยุคสมัย"
                },
                "page_content": {
                    "about": "บริษัทของเราคือผู้นำด้านการให้คำปรึกษาและโซลูชันทางธุรกิจ ด้วยประสบการณ์และความเชี่ยวชาญ",
                    "services": "เรานำเสนอบริการที่ครอบคลุมทุกด้านของการทำธุรกิจ ตั้งแต่การวางแผนกลยุทธ์ไปจนถึงการดำเนินการ",
                    "contact": "ปรึกษากับผู้เชี่ยวชาญของเราเพื่อหาทางออกที่เหมาะสมกับธุรกิจของคุณ"
                }
            }
        }
        
        self.section_generators = {
            "hero_section": self._generate_hero_content,
            "about_section": self._generate_about_content,
            "services_section": self._generate_services_content,
            "features_section": self._generate_features_content,
            "testimonials_section": self._generate_testimonials_content,
            "cta_section": self._generate_cta_content
        }
        
    def generate_content_strategy(self, business_type: str, complexity_level: str = "medium") -> Dict[str, Any]:
        """สร้างกลยุทธ์เนื้อหาสำหรับธุรกิจ"""
        
        # ได้ข้อมูลการวิเคราะห์ธุรกิจ
        business_analysis = business_analyzer.analyze_business_needs(business_type, complexity_level)
        
        # สร้างเนื้อหาตามประเภทธุรกิจ
        content_templates = self.content_templates.get(business_type, self.content_templates["business_corporate"])
        
        return {
            "business_type": business_type,
            "complexity_level": complexity_level,
            "content_templates": content_templates,
            "business_analysis": business_analysis,
            "page_structure": self._generate_page_structure(business_type, complexity_level),
            "content_sections": self._generate_all_sections(business_type),
            "seo_strategy": self._generate_seo_strategy(business_type),
            "user_journey": self._generate_user_journey(business_type)
        }
    
    def _generate_page_structure(self, business_type: str, complexity_level: str) -> Dict[str, List[str]]:
        """กำหนดโครงสร้างหน้าเว็บ"""
        base_pages = ["index.html", "about.html", "contact.html"]
        
        page_structure = {
            "essential_pages": base_pages.copy(),
            "additional_pages": [],
            "app_pages": []
        }
        
        if business_type == "coffee_shop":
            page_structure["additional_pages"].extend(["menu.html", "gallery.html"])
            if complexity_level in ["medium", "high"]:
                page_structure["app_pages"].extend(["order.html", "booking.html"])
            if complexity_level == "high":
                page_structure["app_pages"].extend(["loyalty.html", "events.html"])
                
        elif business_type == "restaurant":
            page_structure["additional_pages"].extend(["menu.html", "reservations.html", "gallery.html"])
            if complexity_level in ["medium", "high"]:
                page_structure["app_pages"].extend(["booking.html", "events.html"])
            if complexity_level == "high":
                page_structure["app_pages"].extend(["wine.html", "private-dining.html"])
                
        elif business_type == "fashion_boutique":
            page_structure["additional_pages"].extend(["collections.html", "lookbook.html"])
            if complexity_level in ["medium", "high"]:
                page_structure["app_pages"].extend(["shop.html", "cart.html", "wishlist.html"])
            if complexity_level == "high":
                page_structure["app_pages"].extend(["styling.html", "account.html"])
                
        elif business_type == "business_corporate":
            page_structure["additional_pages"].extend(["services.html", "portfolio.html", "team.html"])
            if complexity_level in ["medium", "high"]:
                page_structure["app_pages"].extend(["quote.html", "client-portal.html"])
            if complexity_level == "high":
                page_structure["app_pages"].extend(["dashboard.html", "projects.html"])
        
        return page_structure
    
    def _generate_all_sections(self, business_type: str) -> Dict[str, Dict[str, Any]]:
        """สร้างเนื้อหาทุกส่วนของเว็บไซต์"""
        sections = {}
        
        for section_name, generator_func in self.section_generators.items():
            sections[section_name] = generator_func(business_type)
            
        return sections
    
    def _generate_hero_content(self, business_type: str) -> Dict[str, Any]:
        """สร้างเนื้อหา Hero Section"""
        templates = self.content_templates.get(business_type, self.content_templates["business_corporate"])
        
        return {
            "headline": random.choice(templates["hero_messages"]),
            "subline": random.choice(templates["value_propositions"]),
            "cta_primary": "เริ่มต้นใช้งาน",
            "cta_secondary": "เรียนรู้เพิ่มเติม",
            "background_style": "gradient-overlay"
        }
    
    def _generate_about_content(self, business_type: str) -> Dict[str, Any]:
        """สร้างเนื้อหา About Section"""
        templates = self.content_templates.get(business_type, self.content_templates["business_corporate"])
        
        return {
            "title": "เกี่ยวกับเรา",
            "description": templates["page_content"]["about"],
            "highlights": templates["value_propositions"][:3],
            "stats": self._generate_business_stats(business_type)
        }
    
    def _generate_services_content(self, business_type: str) -> Dict[str, Any]:
        """สร้างเนื้อหา Services Section"""
        templates = self.content_templates.get(business_type, self.content_templates["business_corporate"])
        
        return {
            "title": "บริการของเรา",
            "services": templates["service_descriptions"],
            "features": templates["value_propositions"]
        }
    
    def _generate_features_content(self, business_type: str) -> Dict[str, Any]:
        """สร้างเนื้อหา Features Section"""
        feature_icons = {
            "coffee_shop": ["fas fa-coffee", "fas fa-wifi", "fas fa-clock", "fas fa-heart"],
            "restaurant": ["fas fa-utensils", "fas fa-wine-glass", "fas fa-star", "fas fa-users"],
            "fashion_boutique": ["fas fa-tshirt", "fas fa-gem", "fas fa-palette", "fas fa-shopping-bag"],
            "business_corporate": ["fas fa-chart-line", "fas fa-cogs", "fas fa-handshake", "fas fa-shield-alt"]
        }
        
        templates = self.content_templates.get(business_type, self.content_templates["business_corporate"])
        icons = feature_icons.get(business_type, feature_icons["business_corporate"])
        
        features = []
        for i, (title, desc) in enumerate(list(templates["service_descriptions"].items())[:4]):
            features.append({
                "icon": icons[i] if i < len(icons) else "fas fa-star",
                "title": title.replace("_", " ").title(),
                "description": desc
            })
        
        return {
            "title": "ความเป็นเลิศที่เราภาคภูมิใจ",
            "subtitle": "เราให้บริการที่เหนือกว่าด้วยคุณภาพระดับมาตรฐานสากล",
            "features": features
        }
    
    def _generate_testimonials_content(self, business_type: str) -> Dict[str, Any]:
        """สร้างเนื้อหา Testimonials"""
        testimonials_db = {
            "coffee_shop": [
                {"name": "นางสาวอรุณี ใจดี", "text": "กาแฟที่นี่อร่อยมาก บรรยากาศดี เหมาะสำหรับทำงาน", "rating": 5},
                {"name": "คุณสมชาย รักกาแฟ", "text": "บาริสต้าให้คำแนะนำดี กาแฟทุกแก้วมีคุณภาพ", "rating": 5},
                {"name": "นางสาวมาลี มีสุข", "text": "ร้านโปรดของฉัน มาทุกวันเพราะกาแฟหอมมาก", "rating": 5}
            ],
            "restaurant": [
                {"name": "คุณพิชญา กินดี", "text": "อาหารอร่อยมาก เชฟเก่งจริงๆ บรรยากาศหรูหรา", "rating": 5},
                {"name": "นายวิชัย มีเงิน", "text": "เหมาะสำหรับงานเลี้ยงพิเศษ บริการดีมาก", "rating": 5},
                {"name": "คุณนิรมล อิ่มอร่อย", "text": "ประสบการณ์การกินที่ยอดเยี่ยม คุ้มค่าทุกบาท", "rating": 5}
            ],
            "fashion_boutique": [
                {"name": "คุณสวย มีสไตล์", "text": "เสื้อผ้าสวยมาก ใส่แล้วมั่นใจ คุณภาพดี", "rating": 5},
                {"name": "นางสาวแฟชั่น ทันสมัย", "text": "ดีไซน์ไม่ซ้ำใคร มี Personal Stylist ช่วยเลือก", "rating": 5},
                {"name": "คุณหรูหรา ดูดี", "text": "เป็นร้านประจำของฉัน เสื้อผ้าทุกชิ้นมีคุณภาพ", "rating": 5}
            ],
            "business_corporate": [
                {"name": "คุณสำเร็จ ธุรกิจดี", "text": "ให้คำปรึกษาดีมาก ช่วยธุรกิจเติบโตได้จริง", "rating": 5},
                {"name": "นางมานี มีผล", "text": "ทีมงานมืออาชีพ โซลูชันที่ได้รับตรงความต้องการ", "rating": 5},
                {"name": "คุณเก่ง ทำได้", "text": "พันธมิตรที่เชื่อถือได้ ผลงานออกมาดีเกินคาด", "rating": 5}
            ]
        }
        
        testimonials = testimonials_db.get(business_type, testimonials_db["business_corporate"])
        
        return {
            "title": "ความคิดเห็นจากลูกค้า",
            "subtitle": "ประสบการณ์ที่ดีจากลูกค้าที่ไว้วางใจเรา",
            "testimonials": testimonials
        }
    
    def _generate_cta_content(self, business_type: str) -> Dict[str, Any]:
        """สร้างเนื้อหา Call-to-Action"""
        cta_messages = {
            "coffee_shop": {
                "title": "มาดื่มกาแฟกับเราสิ",
                "subtitle": "เปิดทุกวัน 6:00 - 22:00 น.",
                "button": "ดูเมนู"
            },
            "restaurant": {
                "title": "จองโต๊ะวันนี้",
                "subtitle": "สำหรับประสบการณ์ที่ไม่ลืม",
                "button": "จองโต๊ะ"
            },
            "fashion_boutique": {
                "title": "ค้นพบสไตล์ใหม่",
                "subtitle": "คอลเล็กชันล่าสุดรอคุณอยู่",
                "button": "ช้อปเลย"
            },
            "business_corporate": {
                "title": "ปรึกษาฟรี",
                "subtitle": "รับคำปรึกษาจากผู้เชี่ยวชาญ",
                "button": "ติดต่อเรา"
            }
        }
        
        return cta_messages.get(business_type, cta_messages["business_corporate"])
    
    def _generate_business_stats(self, business_type: str) -> List[Dict[str, str]]:
        """สร้างสถิติธุรกิจ"""
        stats_db = {
            "coffee_shop": [
                {"number": "500+", "label": "แก้วต่อวัน"},
                {"number": "98%", "label": "ลูกค้าพอใจ"},
                {"number": "3", "label": "ปี ประสบการณ์"}
            ],
            "restaurant": [
                {"number": "1000+", "label": "ลูกค้าพอใจ"},
                {"number": "50+", "label": "เมนูพิเศษ"},
                {"number": "5", "label": "ปี ประสบการณ์"}
            ],
            "fashion_boutique": [
                {"number": "2000+", "label": "ลูกค้าทั่วประเทศ"},
                {"number": "100+", "label": "ดีไซน์เฉพาะ"},
                {"number": "10", "label": "ปี ประสบการณ์"}
            ],
            "business_corporate": [
                {"number": "500+", "label": "โครงการสำเร็จ"},
                {"number": "95%", "label": "ลูกค้าพอใจ"},
                {"number": "15", "label": "ปี ประสบการณ์"}
            ]
        }
        
        return stats_db.get(business_type, stats_db["business_corporate"])
    
    def _generate_seo_strategy(self, business_type: str) -> Dict[str, Any]:
        """สร้างกลยุทธ์ SEO"""
        seo_keywords = {
            "coffee_shop": ["ร้านกาแฟ", "กาแฟสด", "บาริสต้า", "เมล็ดกาแฟ", "คาเฟ่"],
            "restaurant": ["ร้านอาหาร", "Fine Dining", "เชฟ", "อาหารเลิศรส", "จองโต๊ะ"],
            "fashion_boutique": ["แฟชั่น", "เสื้อผ้า", "บูทีค", "สไตล์", "ดีไซน์"],
            "business_corporate": ["ที่ปรึกษาธุรกิจ", "โซลูชัน", "บริการธุรกิจ", "ผู้เชี่ยวชาญ"]
        }
        
        return {
            "primary_keywords": seo_keywords.get(business_type, seo_keywords["business_corporate"]),
            "meta_description_template": f"{{business_name}} - {{primary_service}} คุณภาพสูง บริการมืออาชีพ",
            "title_template": "{{page_name}} | {{business_name}} - {{tagline}}"
        }
    
    def _generate_user_journey(self, business_type: str) -> List[Dict[str, str]]:
        """สร้าง User Journey"""
        journeys = {
            "coffee_shop": [
                {"stage": "Awareness", "action": "ค้นหาร้านกาแฟใกล้บ้าน", "touchpoint": "Google Search, Social Media"},
                {"stage": "Interest", "action": "ดูเมนูและรีวิว", "touchpoint": "Website, Facebook"},
                {"stage": "Consideration", "action": "เปรียบเทียบราคาและบรรยากาศ", "touchpoint": "Website Gallery, Google Maps"},
                {"stage": "Purchase", "action": "มาซื้อกาแฟครั้งแรก", "touchpoint": "Physical Store"},
                {"stage": "Retention", "action": "กลับมาซื้อซ้ำ", "touchpoint": "Loyalty Program, Social Media"}
            ],
            "restaurant": [
                {"stage": "Awareness", "action": "หาร้านอาหารสำหรับโอกาสพิเศษ", "touchpoint": "Search Engine, Recommendations"},
                {"stage": "Interest", "action": "ดูเมนูและบรรยากาศร้าน", "touchpoint": "Website, Instagram"},
                {"stage": "Consideration", "action": "อ่านรีวิวและเปรียบเทียบ", "touchpoint": "Review Sites, Website"},
                {"stage": "Purchase", "action": "จองโต๊ะและมาใช้บริการ", "touchpoint": "Booking System, Phone"},
                {"stage": "Retention", "action": "กลับมาใช้บริการซ้ำ", "touchpoint": "Email Marketing, Events"}
            ],
            "fashion_boutique": [
                {"stage": "Awareness", "action": "ค้นหาเสื้อผ้าแฟชั่น", "touchpoint": "Instagram, Fashion Blogs"},
                {"stage": "Interest", "action": "ดูคอลเล็กชันและแต่งตัว", "touchpoint": "Website, Lookbook"},
                {"stage": "Consideration", "action": "เลือกสินค้าและตรวจสอบไซส์", "touchpoint": "Product Pages, Size Guide"},
                {"stage": "Purchase", "action": "สั่งซื้อออนไลน์หรือมาร้าน", "touchpoint": "E-commerce, Physical Store"},
                {"stage": "Retention", "action": "ติดตามคอลเล็กชันใหม่", "touchpoint": "Newsletter, VIP Program"}
            ],
            "business_corporate": [
                {"stage": "Awareness", "action": "มีความต้องการโซลูชันธุรกิจ", "touchpoint": "Search, Referrals"},
                {"stage": "Interest", "action": "ศึกษาบริการและผลงาน", "touchpoint": "Website, Case Studies"},
                {"stage": "Consideration", "action": "เปรียบเทียบและขอใบเสนอราคา", "touchpoint": "Quote System, Sales Call"},
                {"stage": "Purchase", "action": "ตัดสินใจใช้บริการ", "touchpoint": "Contract Signing"},
                {"stage": "Retention", "action": "ใช้บริการต่อเนื่องหรือแนะนำ", "touchpoint": "Account Management, Referral Program"}
            ]
        }
        
        return journeys.get(business_type, journeys["business_corporate"])

# สร้าง instance
advanced_content_generator = AdvancedContentGenerator()

if __name__ == "__main__":
    # ทดสอบการสร้างเนื้อหา
    for business_type in ["coffee_shop", "restaurant", "fashion_boutique", "business_corporate"]:
        print(f"\n🎯 {business_type.replace('_', ' ').title()} Content Strategy")
        print("=" * 60)
        
        strategy = advanced_content_generator.generate_content_strategy(business_type, "high")
        print(f"📄 Pages: {len(strategy['page_structure']['essential_pages']) + len(strategy['page_structure']['additional_pages']) + len(strategy['page_structure']['app_pages'])}")
        print(f"🎨 Sections: {len(strategy['content_sections'])}")
        print(f"📱 App Pages: {len(strategy['page_structure']['app_pages'])}")
        print(f"🔍 SEO Keywords: {', '.join(strategy['seo_strategy']['primary_keywords'][:3])}")
        
        # แสดงตัวอย่าง Hero Content
        hero = strategy['content_sections']['hero_section']
        print(f"💡 Hero: {hero['headline'][:50]}...")