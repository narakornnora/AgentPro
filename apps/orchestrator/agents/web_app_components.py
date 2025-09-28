"""
⚙️ Web App Component System - ระบบสร้าง Web App Components
"""
import os
import json
from typing import Dict, List, Any

class WebAppComponentSystem:
    def __init__(self):
        self.component_templates = {
            "shopping_cart": {
                "description": "ระบบตะกร้าสินค้าครบครัน",
                "files": {
                    "cart.html": self._generate_cart_html(),
                    "cart.js": self._generate_cart_js(),
                    "cart.css": self._generate_cart_css(),
                    "cart_api.py": self._generate_cart_api()
                },
                "database_schema": {
                    "cart_items": {
                        "id": "INTEGER PRIMARY KEY",
                        "session_id": "TEXT",
                        "product_id": "INTEGER", 
                        "product_name": "TEXT",
                        "price": "REAL",
                        "quantity": "INTEGER",
                        "total": "REAL",
                        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
                    },
                    "products": {
                        "id": "INTEGER PRIMARY KEY",
                        "name": "TEXT NOT NULL",
                        "description": "TEXT",
                        "price": "REAL NOT NULL",
                        "image_url": "TEXT",
                        "category": "TEXT",
                        "stock": "INTEGER DEFAULT 0",
                        "active": "BOOLEAN DEFAULT 1"
                    }
                },
                "integration_code": self._generate_cart_integration()
            },
            
            "chatbot": {
                "description": "ระบบแชทบอทอัจฉริยะ",
                "files": {
                    "chatbot.html": self._generate_chatbot_html(),
                    "chatbot.js": self._generate_chatbot_js(),
                    "chatbot.css": self._generate_chatbot_css(),
                    "chatbot_api.py": self._generate_chatbot_api()
                },
                "database_schema": {
                    "conversations": {
                        "id": "INTEGER PRIMARY KEY",
                        "session_id": "TEXT",
                        "user_message": "TEXT",
                        "bot_response": "TEXT",
                        "timestamp": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
                    },
                    "faq_data": {
                        "id": "INTEGER PRIMARY KEY",
                        "question": "TEXT",
                        "answer": "TEXT",
                        "keywords": "TEXT",
                        "category": "TEXT"
                    }
                },
                "integration_code": self._generate_chatbot_integration()
            },
            
            "user_registration": {
                "description": "ระบบสมาชิกและการลงทะเบียน",
                "files": {
                    "register.html": self._generate_register_html(),
                    "login.html": self._generate_login_html(),
                    "profile.html": self._generate_profile_html(),
                    "auth.js": self._generate_auth_js(),
                    "auth.css": self._generate_auth_css(),
                    "auth_api.py": self._generate_auth_api()
                },
                "database_schema": {
                    "users": {
                        "id": "INTEGER PRIMARY KEY",
                        "email": "TEXT UNIQUE NOT NULL",
                        "password_hash": "TEXT NOT NULL",
                        "first_name": "TEXT",
                        "last_name": "TEXT",
                        "phone": "TEXT",
                        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                        "last_login": "TIMESTAMP",
                        "active": "BOOLEAN DEFAULT 1"
                    },
                    "user_sessions": {
                        "id": "INTEGER PRIMARY KEY",
                        "user_id": "INTEGER",
                        "session_token": "TEXT UNIQUE",
                        "expires_at": "TIMESTAMP",
                        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
                    }
                },
                "integration_code": self._generate_auth_integration()
            },
            
            "booking_system": {
                "description": "ระบบจองโต๊ะ/นัดหมาย",
                "files": {
                    "booking.html": self._generate_booking_html(),
                    "calendar.js": self._generate_calendar_js(),
                    "booking.css": self._generate_booking_css(),
                    "booking_api.py": self._generate_booking_api()
                },
                "database_schema": {
                    "bookings": {
                        "id": "INTEGER PRIMARY KEY",
                        "customer_name": "TEXT NOT NULL",
                        "customer_email": "TEXT",
                        "customer_phone": "TEXT",
                        "booking_date": "DATE",
                        "booking_time": "TIME",
                        "party_size": "INTEGER",
                        "special_requests": "TEXT",
                        "status": "TEXT DEFAULT 'confirmed'",
                        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
                    },
                    "availability": {
                        "id": "INTEGER PRIMARY KEY",
                        "date": "DATE",
                        "time_slot": "TIME",
                        "max_capacity": "INTEGER",
                        "current_bookings": "INTEGER DEFAULT 0",
                        "available": "BOOLEAN DEFAULT 1"
                    }
                },
                "integration_code": self._generate_booking_integration()
            },
            
            "payment_system": {
                "description": "ระบบชำระเงินออนไลน์",
                "files": {
                    "payment.html": self._generate_payment_html(),
                    "payment.js": self._generate_payment_js(),
                    "payment.css": self._generate_payment_css(),
                    "payment_api.py": self._generate_payment_api()
                },
                "database_schema": {
                    "orders": {
                        "id": "INTEGER PRIMARY KEY",
                        "order_number": "TEXT UNIQUE",
                        "customer_id": "INTEGER",
                        "total_amount": "REAL",
                        "payment_status": "TEXT DEFAULT 'pending'",
                        "payment_method": "TEXT",
                        "transaction_id": "TEXT",
                        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
                    },
                    "order_items": {
                        "id": "INTEGER PRIMARY KEY",
                        "order_id": "INTEGER",
                        "product_id": "INTEGER",
                        "quantity": "INTEGER",
                        "unit_price": "REAL",
                        "total_price": "REAL"
                    }
                },
                "integration_code": self._generate_payment_integration()
            }
        }
    
    def generate_component(self, component_type: str, business_type: str = "general") -> Dict[str, Any]:
        """สร้าง component ตามประเภทที่ระบุ"""
        if component_type not in self.component_templates:
            raise ValueError(f"Component type '{component_type}' not supported")
        
        template = self.component_templates[component_type]
        
        # ปรับแต่ง component ตามประเภทธุรกิจ
        customized_template = self._customize_for_business(template, business_type, component_type)
        
        return {
            "component_type": component_type,
            "business_type": business_type,
            "description": customized_template["description"],
            "files": customized_template["files"],
            "database_schema": customized_template["database_schema"],
            "integration_code": customized_template["integration_code"],
            "setup_instructions": self._generate_setup_instructions(component_type)
        }
    
    def _customize_for_business(self, template: Dict, business_type: str, component_type: str) -> Dict:
        """ปรับแต่ง template ตามประเภทธุรกิจ"""
        customized = template.copy()
        
        # ปรับแต่งเนื้อหาตามประเภทธุรกิจ
        if component_type == "chatbot" and business_type == "coffee_shop":
            # เพิ่ม FAQ เฉพาะร้านกาแฟ
            customized["files"]["chatbot_faq.json"] = json.dumps({
                "faq": [
                    {"q": "เปิดกี่โมง", "a": "เราเปิดทุกวัน 6:00-22:00 น."},
                    {"q": "มีกาแฟอะไรบ้าง", "a": "เรามีเอสเปรสโซ่ ลาเต้ คาปูชิโน่ และกาแฟพิเศษอื่นๆ"},
                    {"q": "สั่งกาแฟล่วงหน้าได้ไหม", "a": "ได้ครับ สามารถสั่งผ่านระบบออนไลน์ได้เลย"},
                    {"q": "มี Wi-Fi ไหม", "a": "มีครับ Wi-Fi ฟรีสำหรับลูกค้า รหัส: CoffeeLovers"},
                    {"q": "จอดรถได้ที่ไหน", "a": "มีลานจอดรถของร้าน และสามารถจอดริมถนนได้"}
                ]
            }, indent=2, ensure_ascii=False)
            
        elif component_type == "booking_system" and business_type == "restaurant":
            # ปรับแต่งระบบจองสำหรับร้านอาหาร
            customized["database_schema"]["bookings"]["table_preference"] = "TEXT"
            customized["database_schema"]["bookings"]["dietary_requirements"] = "TEXT"
            
        elif component_type == "shopping_cart" and business_type == "fashion_boutique":
            # เพิ่มฟีเจอร์สำหรับแฟชั่น
            customized["database_schema"]["products"]["size"] = "TEXT"
            customized["database_schema"]["products"]["color"] = "TEXT"
            customized["database_schema"]["products"]["material"] = "TEXT"
        
        return customized
    
    def _generate_setup_instructions(self, component_type: str) -> List[str]:
        """สร้างคำแนะนำการติดตั้ง"""
        instructions = {
            "shopping_cart": [
                "1. สร้างตารางฐานข้อมูล cart_items และ products",
                "2. เพิ่มไฟล์ cart.html, cart.js, cart.css ในโฟลเดอร์เว็บไซต์",
                "3. เพิ่ม cart_api.py ในส่วน backend",
                "4. เพิ่ม session management สำหรับจัดการตะกร้า",
                "5. ทดสอบการเพิ่ม/ลบสินค้าในตะกร้า"
            ],
            "chatbot": [
                "1. สร้างตารางฐานข้อมูล conversations และ faq_data",
                "2. เพิ่มไฟล์ chatbot.html, chatbot.js, chatbot.css",
                "3. ตั้งค่า chatbot_api.py พร้อม AI response system",
                "4. เพิ่มข้อมูล FAQ เบื้องต้น",
                "5. ทดสอบการสนทนากับบอท"
            ],
            "user_registration": [
                "1. สร้างตารางฐานข้อมูล users และ user_sessions",
                "2. เพิ่มหน้า register.html, login.html, profile.html",
                "3. ติดตั้ง auth_api.py พร้อมระบบ authentication",
                "4. ตั้งค่า session management และ password hashing",
                "5. ทดสอบการสมัครสมาชิกและเข้าสู่ระบบ"
            ],
            "booking_system": [
                "1. สร้างตารางฐานข้อมูล bookings และ availability",
                "2. เพิ่มไฟล์ booking.html, calendar.js, booking.css",
                "3. ติดตั้ง booking_api.py พร้อมระบบจัดการนัดหมาย",
                "4. ตั้งค่าข้อมูล availability เบื้องต้น",
                "5. ทดสอบการจองและยกเลิก"
            ],
            "payment_system": [
                "1. สร้างตารางฐานข้อมูล orders และ order_items",
                "2. เพิ่มไฟล์ payment.html, payment.js, payment.css",
                "3. ติดตั้ง payment_api.py พร้อม payment gateway",
                "4. ตั้งค่า API keys สำหรับ payment provider",
                "5. ทดสอบการชำระเงินในโหมด sandbox"
            ]
        }
        
        return instructions.get(component_type, ["ไม่พบคำแนะนำสำหรับ component นี้"])
    
    # HTML Templates
    def _generate_cart_html(self) -> str:
        return '''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ตะกร้าสินค้า</title>
    <link rel="stylesheet" href="cart.css">
</head>
<body>
    <div class="cart-container">
        <h2>ตะกร้าสินค้าของคุณ</h2>
        <div id="cart-items"></div>
        <div class="cart-summary">
            <div class="total-amount">
                <span>รวม: ฿<span id="cart-total">0.00</span></span>
            </div>
            <div class="cart-actions">
                <button id="clear-cart" class="btn-secondary">ล้างตะกร้า</button>
                <button id="checkout" class="btn-primary">ชำระเงิน</button>
            </div>
        </div>
    </div>
    <script src="cart.js"></script>
</body>
</html>'''
    
    def _generate_chatbot_html(self) -> str:
        return '''<div id="chatbot-widget" class="chatbot-widget">
    <div class="chatbot-header" onclick="toggleChat()">
        <i class="fas fa-comments"></i>
        <span>ช่วยเหลือ</span>
        <div class="chat-status online"></div>
    </div>
    <div id="chatbot-body" class="chatbot-body">
        <div class="chat-messages" id="chat-messages">
            <div class="bot-message">
                <div class="message-content">สวัสดีครับ! มีอะไรให้ช่วยไหมครับ?</div>
            </div>
        </div>
        <div class="chat-input-container">
            <input type="text" id="chat-input" placeholder="พิมพ์ข้อความ..." onkeypress="handleEnter(event)">
            <button onclick="sendMessage()" class="send-btn">
                <i class="fas fa-paper-plane"></i>
            </button>
        </div>
    </div>
</div>'''
    
    def _generate_register_html(self) -> str:
        return '''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>สมัครสมาชิก</title>
    <link rel="stylesheet" href="auth.css">
</head>
<body>
    <div class="auth-container">
        <form id="register-form" class="auth-form">
            <h2>สมัครสมาชิก</h2>
            <div class="form-group">
                <input type="text" id="first_name" placeholder="ชื่อ" required>
            </div>
            <div class="form-group">
                <input type="text" id="last_name" placeholder="นามสกุล" required>
            </div>
            <div class="form-group">
                <input type="email" id="email" placeholder="อีเมล" required>
            </div>
            <div class="form-group">
                <input type="tel" id="phone" placeholder="เบอร์โทรศัพท์">
            </div>
            <div class="form-group">
                <input type="password" id="password" placeholder="รหัสผ่าน" required>
            </div>
            <div class="form-group">
                <input type="password" id="confirm_password" placeholder="ยืนยันรหัสผ่าน" required>
            </div>
            <button type="submit" class="btn-primary">สมัครสมาชิก</button>
            <p class="auth-link">มีบัญชีแล้ว? <a href="login.html">เข้าสู่ระบบ</a></p>
        </form>
    </div>
    <script src="auth.js"></script>
</body>
</html>'''
    
    def _generate_booking_html(self) -> str:
        return '''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>จองโต๊ะ</title>
    <link rel="stylesheet" href="booking.css">
</head>
<body>
    <div class="booking-container">
        <h2>จองโต๊ะ</h2>
        <form id="booking-form">
            <div class="form-row">
                <div class="form-group">
                    <label>วันที่</label>
                    <input type="date" id="booking_date" required>
                </div>
                <div class="form-group">
                    <label>เวลา</label>
                    <select id="booking_time" required>
                        <option value="">เลือกเวลา</option>
                        <option value="11:00">11:00</option>
                        <option value="12:00">12:00</option>
                        <option value="13:00">13:00</option>
                        <option value="14:00">14:00</option>
                        <option value="18:00">18:00</option>
                        <option value="19:00">19:00</option>
                        <option value="20:00">20:00</option>
                    </select>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>จำนวนท่าน</label>
                    <select id="party_size" required>
                        <option value="">เลือกจำนวน</option>
                        <option value="1">1 ท่าน</option>
                        <option value="2">2 ท่าน</option>
                        <option value="4">4 ท่าน</option>
                        <option value="6">6 ท่าน</option>
                        <option value="8">8 ท่าน</option>
                    </select>
                </div>
            </div>
            <div class="form-group">
                <label>ชื่อ</label>
                <input type="text" id="customer_name" required>
            </div>
            <div class="form-group">
                <label>อีเมล</label>
                <input type="email" id="customer_email" required>
            </div>
            <div class="form-group">
                <label>เบอร์โทรศัพท์</label>
                <input type="tel" id="customer_phone" required>
            </div>
            <div class="form-group">
                <label>ความต้องการพิเศษ</label>
                <textarea id="special_requests" rows="3" placeholder="เช่น อาหารพิเศษ หรือ การเฉลิมฉลอง"></textarea>
            </div>
            <button type="submit" class="btn-primary">จองโต๊ะ</button>
        </form>
    </div>
    <script src="calendar.js"></script>
</body>
</html>'''
    
    def _generate_payment_html(self) -> str:
        return '''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ชำระเงิน</title>
    <link rel="stylesheet" href="payment.css">
</head>
<body>
    <div class="payment-container">
        <h2>ชำระเงิน</h2>
        <div class="order-summary">
            <h3>สรุปคำสั่งซื้อ</h3>
            <div id="order-items"></div>
            <div class="total-amount">
                <strong>รวม: ฿<span id="total-amount">0.00</span></strong>
            </div>
        </div>
        
        <form id="payment-form">
            <h3>วิธีการชำระเงิน</h3>
            <div class="payment-methods">
                <label class="payment-method">
                    <input type="radio" name="payment_method" value="credit_card" checked>
                    <span>บัตรเครดิต/เดบิต</span>
                </label>
                <label class="payment-method">
                    <input type="radio" name="payment_method" value="promptpay">
                    <span>พร้อมเพย์</span>
                </label>
                <label class="payment-method">
                    <input type="radio" name="payment_method" value="bank_transfer">
                    <span>โอนเงิน</span>
                </label>
            </div>
            
            <div id="credit-card-form" class="payment-form-section">
                <div class="form-group">
                    <input type="text" placeholder="หมายเลขบัตร" maxlength="19">
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <input type="text" placeholder="MM/YY" maxlength="5">
                    </div>
                    <div class="form-group">
                        <input type="text" placeholder="CVV" maxlength="4">
                    </div>
                </div>
                <div class="form-group">
                    <input type="text" placeholder="ชื่อบนบัตร">
                </div>
            </div>
            
            <button type="submit" class="btn-primary">ชำระเงิน</button>
        </form>
    </div>
    <script src="payment.js"></script>
</body>
</html>'''
    
    # JavaScript Templates
    def _generate_cart_js(self) -> str:
        return '''class ShoppingCart {
    constructor() {
        this.items = JSON.parse(localStorage.getItem('cart')) || [];
        this.init();
    }
    
    init() {
        this.renderCart();
        this.setupEventListeners();
    }
    
    addItem(product) {
        const existingItem = this.items.find(item => item.id === product.id);
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            this.items.push({...product, quantity: 1});
        }
        this.saveCart();
        this.renderCart();
    }
    
    removeItem(productId) {
        this.items = this.items.filter(item => item.id !== productId);
        this.saveCart();
        this.renderCart();
    }
    
    updateQuantity(productId, quantity) {
        const item = this.items.find(item => item.id === productId);
        if (item) {
            item.quantity = Math.max(0, quantity);
            if (item.quantity === 0) {
                this.removeItem(productId);
            }
        }
        this.saveCart();
        this.renderCart();
    }
    
    clearCart() {
        this.items = [];
        this.saveCart();
        this.renderCart();
    }
    
    getTotal() {
        return this.items.reduce((total, item) => total + (item.price * item.quantity), 0);
    }
    
    saveCart() {
        localStorage.setItem('cart', JSON.stringify(this.items));
    }
    
    renderCart() {
        const container = document.getElementById('cart-items');
        const totalElement = document.getElementById('cart-total');
        
        if (this.items.length === 0) {
            container.innerHTML = '<p class="empty-cart">ตะกร้าว่าง</p>';
        } else {
            container.innerHTML = this.items.map(item => `
                <div class="cart-item" data-id="${item.id}">
                    <img src="${item.image}" alt="${item.name}" class="item-image">
                    <div class="item-details">
                        <h4>${item.name}</h4>
                        <p class="item-price">฿${item.price.toFixed(2)}</p>
                    </div>
                    <div class="quantity-controls">
                        <button onclick="cart.updateQuantity(${item.id}, ${item.quantity - 1})">-</button>
                        <span>${item.quantity}</span>
                        <button onclick="cart.updateQuantity(${item.id}, ${item.quantity + 1})">+</button>
                    </div>
                    <div class="item-total">
                        ฿${(item.price * item.quantity).toFixed(2)}
                    </div>
                    <button onclick="cart.removeItem(${item.id})" class="remove-btn">×</button>
                </div>
            `).join('');
        }
        
        totalElement.textContent = this.getTotal().toFixed(2);
    }
    
    setupEventListeners() {
        document.getElementById('clear-cart')?.addEventListener('click', () => {
            if (confirm('คุณต้องการล้างตะกร้าทั้งหมดหรือไม่?')) {
                this.clearCart();
            }
        });
        
        document.getElementById('checkout')?.addEventListener('click', () => {
            if (this.items.length === 0) {
                alert('กรุณาเพิ่มสินค้าในตะกร้าก่อน');
                return;
            }
            window.location.href = 'payment.html';
        });
    }
}

// สร้าง instance
const cart = new ShoppingCart();

// ฟังก์ชันสำหรับเพิ่มสินค้าจากหน้าอื่น
window.addToCart = function(product) {
    cart.addItem(product);
    // แสดงการแจ้งเตือน
    showNotification('เพิ่มสินค้าในตะกร้าแล้ว');
};

function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'cart-notification';
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}'''
    
    def _generate_chatbot_js(self) -> str:
        return '''class Chatbot {
    constructor() {
        this.isOpen = false;
        this.messages = [];
        this.init();
    }
    
    init() {
        this.createWidget();
        this.loadFAQ();
    }
    
    createWidget() {
        if (document.getElementById('chatbot-widget')) return;
        
        const widget = document.createElement('div');
        widget.innerHTML = `
            <div id="chatbot-widget" class="chatbot-widget">
                <div class="chatbot-header" onclick="chatbot.toggle()">
                    <i class="fas fa-comments"></i>
                    <span>ช่วยเหลือ</span>
                    <div class="chat-status online"></div>
                </div>
                <div id="chatbot-body" class="chatbot-body">
                    <div class="chat-messages" id="chat-messages">
                        <div class="bot-message">
                            <div class="message-content">สวัสดีครับ! มีอะไรให้ช่วยไหมครับ?</div>
                        </div>
                    </div>
                    <div class="chat-input-container">
                        <input type="text" id="chat-input" placeholder="พิมพ์ข้อความ..." onkeypress="chatbot.handleEnter(event)">
                        <button onclick="chatbot.sendMessage()" class="send-btn">
                            <i class="fas fa-paper-plane"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(widget.firstElementChild);
    }
    
    toggle() {
        this.isOpen = !this.isOpen;
        const body = document.getElementById('chatbot-body');
        body.style.display = this.isOpen ? 'flex' : 'none';
    }
    
    handleEnter(event) {
        if (event.key === 'Enter') {
            this.sendMessage();
        }
    }
    
    sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        
        if (!message) return;
        
        this.addMessage(message, 'user');
        input.value = '';
        
        // หาคำตอบ
        setTimeout(() => {
            const response = this.findResponse(message);
            this.addMessage(response, 'bot');
        }, 500);
    }
    
    addMessage(text, sender) {
        const messages = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = sender === 'user' ? 'user-message' : 'bot-message';
        messageDiv.innerHTML = `<div class="message-content">${text}</div>`;
        
        messages.appendChild(messageDiv);
        messages.scrollTop = messages.scrollHeight;
    }
    
    findResponse(message) {
        const lowerMessage = message.toLowerCase();
        
        // ตรวจสอบ FAQ
        for (const faq of this.faqData) {
            if (faq.keywords.some(keyword => lowerMessage.includes(keyword.toLowerCase()))) {
                return faq.answer;
            }
        }
        
        // คำตอบทั่วไป
        if (lowerMessage.includes('สวัสดี') || lowerMessage.includes('hello')) {
            return 'สวัสดีครับ! ยินดีต้อนรับ มีอะไรให้ช่วยไหมครับ?';
        }
        
        if (lowerMessage.includes('ขอบคุณ') || lowerMessage.includes('thank')) {
            return 'ยินดีครับ! หากมีคำถามอื่นสามารถสอบถามได้เสมอนะครับ';
        }
        
        return 'ขออภัยครับ ผมไม่เข้าใจคำถามของคุณ กรุณาลองถามใหม่หรือติดต่อทีมงานของเราได้เลยครับ';
    }
    
    loadFAQ() {
        // ข้อมูล FAQ เบื้องต้น
        this.faqData = [
            {
                keywords: ['เปิด', 'ปิด', 'เวลา', 'กี่โมง'],
                answer: 'เราเปิดบริการทุกวัน 09:00-20:00 น. ครับ'
            },
            {
                keywords: ['ที่อยู่', 'แผนที่', 'location'],
                answer: 'เราอยู่ที่ 123 ถนนสุขุมวิท เขตวัฒนา กรุงเทพฯ 10110'
            },
            {
                keywords: ['โทร', 'ติดต่อ', 'เบอร์'],
                answer: 'สามารถติดต่อเราได้ที่ 02-123-4567 หรือ contact@example.com'
            }
        ];
    }
}

// สร้าง instance
const chatbot = new Chatbot();

// ฟังก์ชันสำหรับเรียกใช้จากภายนอก
window.toggleChat = () => chatbot.toggle();
window.sendMessage = () => chatbot.sendMessage();
window.handleEnter = (event) => chatbot.handleEnter(event);'''
    
    # CSS Templates
    def _generate_cart_css(self) -> str:
        return '''.cart-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.cart-item {
    display: flex;
    align-items: center;
    padding: 15px;
    border: 1px solid #e0e0e0;
    margin-bottom: 10px;
    border-radius: 8px;
}

.item-image {
    width: 80px;
    height: 80px;
    object-fit: cover;
    border-radius: 4px;
    margin-right: 15px;
}

.item-details {
    flex: 1;
    margin-right: 15px;
}

.item-details h4 {
    margin: 0 0 5px 0;
    font-size: 16px;
}

.item-price {
    color: #666;
    margin: 0;
}

.quantity-controls {
    display: flex;
    align-items: center;
    margin-right: 15px;
}

.quantity-controls button {
    width: 30px;
    height: 30px;
    border: 1px solid #ddd;
    background: #f5f5f5;
    cursor: pointer;
    border-radius: 4px;
}

.quantity-controls span {
    margin: 0 10px;
    min-width: 20px;
    text-align: center;
}

.item-total {
    font-weight: bold;
    min-width: 80px;
    text-align: right;
    margin-right: 15px;
}

.remove-btn {
    width: 30px;
    height: 30px;
    border: none;
    background: #ff4444;
    color: white;
    cursor: pointer;
    border-radius: 50%;
    font-size: 18px;
}

.cart-summary {
    margin-top: 30px;
    padding: 20px;
    background: #f9f9f9;
    border-radius: 8px;
}

.total-amount {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 15px;
}

.cart-actions {
    display: flex;
    gap: 10px;
}

.btn-primary, .btn-secondary {
    padding: 12px 24px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 16px;
}

.btn-primary {
    background: #007bff;
    color: white;
}

.btn-secondary {
    background: #6c757d;
    color: white;
}

.empty-cart {
    text-align: center;
    color: #666;
    font-style: italic;
    padding: 40px;
}

.cart-notification {
    position: fixed;
    top: 20px;
    right: 20px;
    background: #28a745;
    color: white;
    padding: 12px 20px;
    border-radius: 6px;
    z-index: 1000;
}'''
    
    def _generate_chatbot_css(self) -> str:
        return '''.chatbot-widget {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 350px;
    max-width: 90vw;
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    z-index: 1000;
    font-family: Arial, sans-serif;
}

.chatbot-header {
    background: #007bff;
    color: white;
    padding: 15px 20px;
    border-radius: 12px 12px 0 0;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 10px;
}

.chat-status {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-left: auto;
}

.chat-status.online {
    background: #28a745;
}

.chatbot-body {
    height: 400px;
    display: none;
    flex-direction: column;
}

.chat-messages {
    flex: 1;
    padding: 15px;
    overflow-y: auto;
    max-height: 320px;
}

.user-message, .bot-message {
    margin-bottom: 15px;
}

.user-message .message-content {
    background: #007bff;
    color: white;
    padding: 10px 15px;
    border-radius: 18px 18px 4px 18px;
    margin-left: 50px;
    text-align: right;
}

.bot-message .message-content {
    background: #f1f3f4;
    color: #333;
    padding: 10px 15px;
    border-radius: 18px 18px 18px 4px;
    margin-right: 50px;
}

.chat-input-container {
    display: flex;
    padding: 15px;
    border-top: 1px solid #e0e0e0;
    gap: 10px;
}

#chat-input {
    flex: 1;
    border: 1px solid #ddd;
    border-radius: 20px;
    padding: 8px 15px;
    outline: none;
}

.send-btn {
    width: 40px;
    height: 40px;
    border: none;
    background: #007bff;
    color: white;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}

@media (max-width: 480px) {
    .chatbot-widget {
        width: 100%;
        bottom: 0;
        right: 0;
        border-radius: 12px 12px 0 0;
    }
}'''
    
    # API Templates (Python)
    def _generate_cart_api(self) -> str:
        return '''"""
Flask API for Shopping Cart System

from flask import Flask, request, jsonify, session
import sqlite3
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

def init_db():
    conn = sqlite3.connect('cart.db')
    conn.execute(CREATE_TABLE_CART_ITEMS)
    conn.execute(CREATE_TABLE_PRODUCTS)
    conn.commit()
    conn.close()

# SQL Queries
CREATE_TABLE_CART_ITEMS = '''
    CREATE TABLE IF NOT EXISTS cart_items (
        id INTEGER PRIMARY KEY,
        session_id TEXT,
        product_id INTEGER,
        product_name TEXT,
        price REAL,
        quantity INTEGER,
        total REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
'''

CREATE_TABLE_PRODUCTS = '''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        image_url TEXT,
        category TEXT,
        stock INTEGER DEFAULT 0,
        active BOOLEAN DEFAULT 1
    )
'''
"""
    
    # Integration Code Templates
    def _generate_cart_integration(self) -> str:
        return '''// การเชื่อมต่อ Shopping Cart กับหน้าเว็บหลัก

// 1. เพิ่ม CSS และ JS ในหน้าเว็บหลัก
<link rel="stylesheet" href="cart.css">
<script src="cart.js"></script>

// 2. เพิ่มปุ่มเพิ่มสินค้าในหน้าสินค้า
<button onclick="addToCart({
    id: 1,
    name: 'ชื่อสินค้า',
    price: 100.00,
    image: 'path/to/image.jpg'
})" class="add-to-cart-btn">
    เพิ่มในตะกร้า
</button>

// 3. แสดงจำนวนสินค้าในตะกร้า
<div class="cart-icon">
    <i class="fas fa-shopping-cart"></i>
    <span id="cart-count">0</span>
</div>

// 4. อัพเดทจำนวนสินค้าในตะกร้า
function updateCartCount() {
    const count = cart.items.reduce((total, item) => total + item.quantity, 0);
    document.getElementById('cart-count').textContent = count;
}

// เรียกใช้เมื่อโหลดหน้าเว็บ
document.addEventListener('DOMContentLoaded', updateCartCount);'''
    
    def _generate_chatbot_integration(self) -> str:
        return '''// การเชื่อมต่อ Chatbot กับเว็บไซต์

// 1. เพิ่ม CSS และ JS ในหน้าเว็บ
<link rel="stylesheet" href="chatbot.css">
<script src="chatbot.js"></script>

// 2. Chatbot จะสร้างตัวเองอัตโนมัติ
// ไม่จำเป็นต้องเพิ่ม HTML

// 3. ปรับแต่ง FAQ ตามธุรกิจ
// แก้ไขในไฟล์ chatbot.js ส่วน loadFAQ()

// 4. เชื่อมต่อกับ API สำหรับคำตอบที่ซับซ้อน
async function getAIResponse(message) {
    try {
        const response = await fetch('/api/chatbot/message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });
        return await response.json();
    } catch (error) {
        return { response: 'ขออภัย ระบบมีปัญหา กรุณาลองใหม่อีกครั้ง' };
    }
}'''
    
    def _generate_auth_integration(self) -> str:
        return '''// การเชื่อมต่อ Authentication System

// 1. เพิ่มลิงก์สมัครสมาชิกและเข้าสู่ระบบ
<nav>
    <a href="register.html">สมัครสมาชิก</a>
    <a href="login.html">เข้าสู่ระบบ</a>
    <div id="user-menu" style="display: none;">
        <span id="user-name"></span>
        <a href="profile.html">โปรไฟล์</a>
        <button onclick="logout()">ออกจากระบบ</button>
    </div>
</nav>

// 2. ตรวจสอบสถานะการเข้าสู่ระบบ
function checkAuthStatus() {
    const token = localStorage.getItem('auth_token');
    if (token) {
        // แสดงเมนูผู้ใช้
        showUserMenu();
    } else {
        // แสดงปุ่มเข้าสู่ระบบ
        showLoginButtons();
    }
}

// 3. ป้องกันหน้าที่ต้องเข้าสู่ระบบ
function requireAuth() {
    const token = localStorage.getItem('auth_token');
    if (!token) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

// เรียกใช้เมื่อโหลดหน้าเว็บ
document.addEventListener('DOMContentLoaded', checkAuthStatus);'''
    
    def _generate_booking_integration(self) -> str:
        return '''// การเชื่อมต่อ Booking System

// 1. เพิ่มปุ่มจองในหน้าหลัก
<button onclick="window.location.href='booking.html'" class="booking-btn">
    จองโต๊ะ
</button>

// 2. ตรวจสอบช่วงเวลาที่ว่าง
async function checkAvailability(date, time) {
    const response = await fetch('/api/booking/availability', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ date, time })
    });
    return await response.json();
}

// 3. ส่งอีเมลยืนยัน
function sendConfirmationEmail(bookingData) {
    // เชื่อมต่อกับระบบส่งอีเมล
    fetch('/api/booking/confirm', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bookingData)
    });
}

// 4. แสดงปฏิทินที่ว่าง
function loadAvailableSlots() {
    // โหลดช่วงเวลาที่ว่างและแสดงในปฏิทิน
}'''
    
    def _generate_payment_integration(self) -> str:
        return '''// การเชื่อมต่อ Payment System

// 1. เชื่อมต่อกับ Payment Gateway
// ตัวอย่างสำหรับ Stripe
const stripe = Stripe('pk_test_your_key_here');

// 2. ประมวลผลการชำระเงิน
async function processPayment(paymentMethod, amount) {
    const response = await fetch('/api/payment/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            payment_method: paymentMethod,
            amount: amount
        })
    });
    return await response.json();
}

// 3. รับการแจ้งเตือนสำเร็จ
function handlePaymentSuccess(result) {
    // ล้างตะกร้า
    cart.clearCart();
    // แสดงหน้าขอบคุณ
    window.location.href = 'thank-you.html';
}

// 4. จัดการข้อผิดพลาด
function handlePaymentError(error) {
    alert('เกิดข้อผิดพลาดในการชำระเงิน: ' + error.message);
}'''
    
    # เพิ่มเมธอดอื่นๆ ตามต้องการ...
    
    def _generate_login_html(self) -> str:
        return '''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>เข้าสู่ระบบ</title>
    <link rel="stylesheet" href="auth.css">
</head>
<body>
    <div class="auth-container">
        <form id="login-form" class="auth-form">
            <h2>เข้าสู่ระบบ</h2>
            <div class="form-group">
                <input type="email" id="email" placeholder="อีเมล" required>
            </div>
            <div class="form-group">
                <input type="password" id="password" placeholder="รหัสผ่าน" required>
            </div>
            <div class="form-group">
                <label class="checkbox-label">
                    <input type="checkbox" id="remember"> จำการเข้าสู่ระบบ
                </label>
            </div>
            <button type="submit" class="btn-primary">เข้าสู่ระบบ</button>
            <p class="auth-link">ยังไม่มีบัญชี? <a href="register.html">สมัครสมาชิก</a></p>
            <p class="auth-link"><a href="forgot-password.html">ลืมรหัสผ่าน?</a></p>
        </form>
    </div>
    <script src="auth.js"></script>
</body>
</html>'''

# สร้าง instance
web_app_components = WebAppComponentSystem()

if __name__ == "__main__":
    # ทดสอบการสร้าง component
    components = ["shopping_cart", "chatbot", "user_registration", "booking_system", "payment_system"]
    
    for component_type in components:
        print(f"\n⚙️ {component_type.replace('_', ' ').title()}")
        print("=" * 50)
        
        component = web_app_components.generate_component(component_type, "coffee_shop")
        print(f"📄 Files: {len(component['files'])}")
        print(f"🗄️ Tables: {len(component['database_schema'])}")
        print(f"📋 Setup Steps: {len(component['setup_instructions'])}")
        print(f"💡 Description: {component['description']}")