"""
🎯 Business Type Analyzer - วิเคราะห์ความต้องการแต่ละประเภทธุรกิจ
"""
import json
from typing import Dict, List, Any

class BusinessTypeAnalyzer:
    def __init__(self):
        self.business_profiles = {
            "coffee_shop": {
                "name": "Coffee Shop / Cafe",
                "target_audience": ["นักเรียน/นักศึกษา", "ผู้ทำงาน", "คู่รัก", "กลุ่มเพื่อน"],
                "key_features": {
                    "essential": ["menu_showcase", "location_info", "opening_hours", "contact_form"],
                    "recommended": ["online_ordering", "loyalty_program", "event_booking", "photo_gallery"],
                    "advanced": ["mobile_app", "chatbot", "delivery_tracking", "pos_integration"]
                },
                "content_focus": {
                    "primary": ["คุณภาพกาแฟ", "บรรยากาศร้าน", "บริการที่ดี", "ราคาเหมาะสม"],
                    "secondary": ["เมนูหลากหลาย", "วัตถุดิบคุณภาพ", "เชฟ/บาริสต้า", "โปรโมชั่น"],
                    "storytelling": ["ต้นกำเนิดเมล็ดกาแฟ", "กระบวนการคั่ว", "เรื่องราวเจ้าของ", "ชุมชนลูกค้า"]
                },
                "web_app_features": {
                    "shopping_cart": "สำหรับสั่งกาแฟออนไลน์",
                    "booking_system": "จองโต๊ะ/ห้องประชุม",
                    "loyalty_program": "สะสมแต้ม แลกของรางวัล",
                    "chatbot": "ตอบคำถามเมนู และรับออเดอร์"
                }
            },
            
            "restaurant": {
                "name": "Fine Dining Restaurant",
                "target_audience": ["คู่รัก", "ครอบครื้ว", "นักธุรกิจ", "นักท่องเที่ยว"],
                "key_features": {
                    "essential": ["menu_catalog", "chef_profile", "reservation_system", "location_map"],
                    "recommended": ["virtual_tour", "wine_pairing", "private_dining", "event_hosting"],
                    "advanced": ["table_management", "pos_system", "inventory_tracking", "crm_system"]
                },
                "content_focus": {
                    "primary": ["คุณภาพอาหาร", "เชฟมืออาชีพ", "บรรยากาศหรูหรา", "บริการพิเศษ"],
                    "secondary": ["วัตถุดิบพรีเมียม", "เทคนิคการปรุง", "ประวัติร้าน", "รางวัลที่ได้รับ"],
                    "storytelling": ["ปรัชญาการทำอาหาร", "แรงบันดาลใจเชฟ", "วัฒนธรรมอาหาร", "ประสบการณ์ลูกค้า"]
                },
                "web_app_features": {
                    "reservation_system": "จองโต๊ะ เลือกเวลา และจำนวนคน",
                    "menu_ordering": "พรีออเดอร์ ชำระเงินล่วงหน้า",
                    "event_booking": "จองงานเลี้ยง ปาร์ตี้",
                    "loyalty_program": "สมาชิก VIP พิเศษ"
                }
            },
            
            "fashion_boutique": {
                "name": "Fashion Boutique",
                "target_audience": ["ผู้หญิงวัยทำงาน", "แฟชั่นนิสต้า", "นักช้อปปิ้ง", "เซเลบริตี้"],
                "key_features": {
                    "essential": ["product_showcase", "size_guide", "shopping_cart", "wishlist"],
                    "recommended": ["virtual_try_on", "style_advisor", "personal_shopping", "fashion_blog"],
                    "advanced": ["ar_fitting", "ai_recommendation", "social_commerce", "influencer_program"]
                },
                "content_focus": {
                    "primary": ["ไตล์แฟชั่น", "คุณภาพผ้า", "ดีไซน์เฉพาะ", "เทรนด์ล่าสุด"],
                    "secondary": ["แบรนด์ดัง", "ราคาเหมาะสม", "บริการส่วนตัว", "การดูแลลูกค้า"],
                    "storytelling": ["แรงบันดาลใจดีไซน์", "เรื่องราวแบรนด์", "ไลฟ์สไตล์ลูกค้า", "sustainable fashion"]
                },
                "web_app_features": {
                    "shopping_cart": "เต็มรูปแบบ พร้อมระบบชำระเงิน",
                    "wishlist": "รายการสินค้าที่ชอบ",
                    "size_advisor": "AI แนะนำไซส์ที่เหมาะสม",
                    "style_matching": "แมทช์ชุดและแนะนำไอเทม"
                }
            },
            
            "business_corporate": {
                "name": "Corporate Business",
                "target_audience": ["ผู้บริหาร", "นักลงทุน", "พันธมิตรธุรกิจ", "ลูกค้าองค์กร"],
                "key_features": {
                    "essential": ["company_profile", "service_portfolio", "contact_system", "testimonials"],
                    "recommended": ["case_studies", "team_profiles", "news_updates", "client_portal"],
                    "advanced": ["crm_integration", "project_management", "analytics_dashboard", "api_services"]
                },
                "content_focus": {
                    "primary": ["ความเชี่ยวชาญ", "ประสบการณ์", "ผลงานที่โดดเด่น", "ความน่าเชื่อถือ"],
                    "secondary": ["ทีมงานคุณภาพ", "เทคโนโลยี", "นวัตกรรม", "มาตรฐานสากล"],
                    "storytelling": ["วิสัยทัศน์บริษัท", "ความสำเร็จลูกค้า", "การเติบโต", "การพัฒนาอย่างยั่งยืน"]
                },
                "web_app_features": {
                    "client_portal": "ระบบลูกค้าเข้าดูโปรเจกต์",
                    "quote_system": "ขอใบเสนอราคาออนไลน์",
                    "project_tracking": "ติดตามความคืบหน้า",
                    "support_system": "ระบบแจ้งปัญหา/ช่วยเหลือ"
                }
            },
            
            "ecommerce": {
                "name": "E-commerce Store",
                "target_audience": ["นักช้อปออนไลน์", "ครอบครัว", "นักธุรกิจ", "รีเซลเลอร์"],
                "key_features": {
                    "essential": ["product_catalog", "shopping_cart", "payment_gateway", "order_tracking"],
                    "recommended": ["user_accounts", "review_system", "recommendation_engine", "mobile_app"],
                    "advanced": ["ai_chatbot", "inventory_management", "multi_vendor", "analytics"]
                },
                "content_focus": {
                    "primary": ["ความหลากหลายสินค้า", "ราคาดี", "บริการส่งเร็ว", "ความปลอดภัย"],
                    "secondary": ["คุณภาพสินค้า", "การรับประกัน", "บริการหลังการขาย", "โปรโมชั่น"],
                    "storytelling": ["คัดสรรสินค้าคุณภาพ", "เรื่องราวแบรนด์", "ชุมชนลูกค้า", "การดูแลสิ่งแวดล้อม"]
                },
                "web_app_features": {
                    "shopping_cart": "ระบบสั่งซื้อครบวงจร",
                    "user_registration": "สมาชิก พร้อมประวัติการสั่งซื้อ",
                    "payment_system": "รองรับหลายช่องทาง",
                    "chatbot": "ช่วยเหลือลูกค้า 24/7"
                }
            }
        }
        
        self.feature_requirements = {
            "shopping_cart": {
                "files": ["cart.html", "cart.js", "cart.css"],
                "database": ["products", "cart_items", "orders"],
                "apis": ["add_to_cart", "update_cart", "checkout"],
                "dependencies": ["payment_gateway", "inventory_system"]
            },
            "chatbot": {
                "files": ["chatbot.html", "chatbot.js", "chatbot.css"],
                "database": ["conversations", "faq", "responses"],
                "apis": ["send_message", "get_response", "save_conversation"],
                "dependencies": ["ai_service", "websocket"]
            },
            "user_registration": {
                "files": ["register.html", "login.html", "profile.html", "auth.js"],
                "database": ["users", "sessions", "user_preferences"],
                "apis": ["register", "login", "logout", "profile_update"],
                "dependencies": ["authentication", "session_management"]
            },
            "booking_system": {
                "files": ["booking.html", "calendar.js", "booking.css"],
                "database": ["bookings", "availability", "customers"],
                "apis": ["check_availability", "make_booking", "cancel_booking"],
                "dependencies": ["calendar_system", "notification_system"]
            }
        }
    
    def analyze_business_needs(self, business_type: str, complexity_level: str = "medium") -> Dict[str, Any]:
        """วิเคราะห์ความต้องการของธุรกิจ"""
        if business_type not in self.business_profiles:
            business_type = "business_corporate"  # default
            
        profile = self.business_profiles[business_type]
        
        # กำหนด features ตาม complexity level
        features = profile["key_features"]["essential"].copy()
        
        if complexity_level in ["medium", "high"]:
            features.extend(profile["key_features"]["recommended"])
        
        if complexity_level == "high":
            features.extend(profile["key_features"]["advanced"])
        
        return {
            "business_profile": profile,
            "required_features": features,
            "web_app_features": profile["web_app_features"],
            "content_strategy": profile["content_focus"],
            "target_audience": profile["target_audience"],
            "complexity_level": complexity_level
        }
    
    def get_feature_specifications(self, features: List[str]) -> Dict[str, Any]:
        """ดูรายละเอียดของ features ที่ต้องการ"""
        specifications = {}
        
        for feature in features:
            if feature in self.feature_requirements:
                specifications[feature] = self.feature_requirements[feature]
            else:
                # สร้าง spec พื้นฐานสำหรับ feature ที่ไม่มีในระบบ
                specifications[feature] = {
                    "files": [f"{feature}.html", f"{feature}.js", f"{feature}.css"],
                    "database": [f"{feature}_data"],
                    "apis": [f"get_{feature}", f"update_{feature}"],
                    "dependencies": ["basic_framework"]
                }
        
        return specifications
    
    def generate_project_structure(self, business_type: str, complexity_level: str = "medium") -> Dict[str, Any]:
        """สร้างโครงสร้างโปรเจกต์ตามประเภทธุรกิจ"""
        analysis = self.analyze_business_needs(business_type, complexity_level)
        feature_specs = self.get_feature_specifications(analysis["required_features"])
        
        # สร้าง file structure
        file_structure = {
            "html_files": ["index.html", "about.html", "contact.html"],
            "css_files": ["style.css", "responsive.css"],
            "js_files": ["main.js", "utils.js"],
            "database_files": ["database.db"],
            "api_files": ["api.py", "routes.py"],
            "assets": ["images/", "fonts/", "icons/"]
        }
        
        # เพิ่ม files จาก features
        for feature, spec in feature_specs.items():
            file_structure["html_files"].extend(spec.get("files", []))
            if "database" in spec:
                file_structure["database_files"].extend([f"{db}.db" for db in spec["database"]])
            if "apis" in spec:
                file_structure["api_files"].extend([f"{api}.py" for api in spec["apis"]])
        
        return {
            "business_analysis": analysis,
            "feature_specifications": feature_specs,
            "file_structure": file_structure,
            "estimated_files": sum(len(files) for files in file_structure.values() if isinstance(files, list)),
            "development_priority": self._get_development_priority(analysis["required_features"])
        }
    
    def _get_development_priority(self, features: List[str]) -> List[str]:
        """กำหนดลำดับความสำคัญในการพัฒนา"""
        priority_map = {
            "menu_showcase": 1,
            "product_showcase": 1,
            "company_profile": 1,
            "shopping_cart": 2,
            "booking_system": 2,
            "user_registration": 2,
            "chatbot": 3,
            "payment_system": 3,
            "analytics": 4
        }
        
        # เรียงตามความสำคัญ
        prioritized = sorted(features, key=lambda x: priority_map.get(x, 5))
        return prioritized

# สร้าง instance
business_analyzer = BusinessTypeAnalyzer()

if __name__ == "__main__":
    # ทดสอบการวิเคราะห์
    for business_type in ["coffee_shop", "restaurant", "fashion_boutique", "business_corporate"]:
        print(f"\n🏢 {business_type.replace('_', ' ').title()}")
        print("=" * 50)
        
        analysis = business_analyzer.generate_project_structure(business_type, "high")
        print(f"📊 Features: {len(analysis['business_analysis']['required_features'])}")
        print(f"📁 Files: {analysis['estimated_files']}")
        print(f"🎯 Target: {', '.join(analysis['business_analysis']['target_audience'][:2])}")
        print(f"⚡ Web Apps: {', '.join(analysis['business_analysis']['web_app_features'].keys())}")