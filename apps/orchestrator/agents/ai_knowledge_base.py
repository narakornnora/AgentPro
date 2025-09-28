"""
🧠 AI Knowledge Base - ความรู้ลึกสำหรับการพัฒนา Complex Applications
"""

class AIKnowledgeBase:
    def __init__(self):
        self.architecture_patterns = {
            "mvc": {
                "description": "Model-View-Controller Pattern",
                "complexity": "medium",
                "best_for": ["web_applications", "desktop_apps"],
                "structure": {
                    "models": "Data and business logic",
                    "views": "User interface components", 
                    "controllers": "Handle user input and coordinate"
                },
                "files_needed": [
                    "models/User.js", "models/Product.js", "models/Order.js",
                    "views/HomePage.js", "views/ProductPage.js", "views/Dashboard.js",
                    "controllers/AuthController.js", "controllers/ProductController.js",
                    "routes/api.js", "routes/web.js", "middleware/auth.js"
                ]
            },
            
            "microservices": {
                "description": "Microservices Architecture",
                "complexity": "high", 
                "best_for": ["large_applications", "scalable_systems"],
                "structure": {
                    "user_service": "Handle user management",
                    "product_service": "Manage products and inventory",
                    "payment_service": "Process payments",
                    "notification_service": "Send notifications",
                    "api_gateway": "Route requests to services"
                },
                "files_needed": [
                    "services/user-service/app.js", "services/user-service/models/User.js",
                    "services/product-service/app.js", "services/product-service/models/Product.js", 
                    "services/payment-service/app.js", "services/payment-service/controllers/PaymentController.js",
                    "api-gateway/gateway.js", "api-gateway/routes.js",
                    "docker-compose.yml", "nginx.conf"
                ]
            },

            "component_architecture": {
                "description": "Component-Based Frontend Architecture", 
                "complexity": "medium",
                "best_for": ["react_apps", "vue_apps", "angular_apps"],
                "structure": {
                    "components": "Reusable UI components",
                    "containers": "Smart components with state",
                    "services": "API and business logic",
                    "store": "Global state management"
                },
                "files_needed": [
                    "src/components/Header/Header.jsx", "src/components/Footer/Footer.jsx",
                    "src/components/Button/Button.jsx", "src/components/Modal/Modal.jsx",
                    "src/containers/HomePage/HomePage.jsx", "src/containers/Dashboard/Dashboard.jsx",
                    "src/services/api.js", "src/services/auth.js",
                    "src/store/index.js", "src/store/reducers.js", "src/store/actions.js"
                ]
            },

            "jamstack": {
                "description": "JAMstack (JavaScript, APIs, Markup)",
                "complexity": "medium",
                "best_for": ["static_sites", "blogs", "portfolios", "e_commerce"],
                "structure": {
                    "static_site": "Pre-built HTML/CSS/JS",
                    "apis": "Third-party or custom APIs",
                    "cdn": "Content Delivery Network"
                },
                "files_needed": [
                    "src/pages/index.js", "src/pages/about.js", "src/pages/blog/[slug].js",
                    "src/components/Layout.js", "src/components/SEO.js",
                    "src/lib/api.js", "src/lib/utils.js",
                    "public/manifest.json", "next.config.js", "package.json"
                ]
            }
        }

        self.technology_stacks = {
            "react_fullstack": {
                "frontend": ["React", "TypeScript", "Tailwind CSS", "React Router"],
                "backend": ["Node.js", "Express", "JWT", "bcrypt"],
                "database": ["MongoDB", "Mongoose"],
                "deployment": ["Docker", "AWS", "Nginx"],
                "testing": ["Jest", "React Testing Library", "Supertest"],
                "files": {
                    "frontend": [
                        "src/App.tsx", "src/components/Layout/Layout.tsx",
                        "src/pages/HomePage.tsx", "src/pages/LoginPage.tsx",
                        "src/hooks/useAuth.ts", "src/context/AuthContext.tsx",
                        "src/services/api.ts", "src/utils/helpers.ts",
                        "package.json", "tsconfig.json", "tailwind.config.js"
                    ],
                    "backend": [
                        "src/app.js", "src/routes/auth.js", "src/routes/api.js",
                        "src/models/User.js", "src/models/Product.js",
                        "src/middleware/auth.js", "src/controllers/AuthController.js",
                        "src/config/database.js", "src/utils/helpers.js",
                        "package.json", "Dockerfile", ".env.example"
                    ]
                }
            },

            "vue_nuxt": {
                "frontend": ["Vue 3", "Nuxt 3", "TypeScript", "Pinia", "Vuetify"],
                "backend": ["Node.js", "Fastify", "Prisma"],
                "database": ["PostgreSQL", "Redis"],
                "deployment": ["Vercel", "Railway", "Docker"],
                "files": {
                    "frontend": [
                        "nuxt.config.ts", "app.vue", 
                        "pages/index.vue", "pages/login.vue", "pages/dashboard.vue",
                        "components/Header.vue", "components/Sidebar.vue",
                        "composables/useAuth.ts", "stores/auth.ts",
                        "plugins/api.ts", "middleware/auth.ts"
                    ],
                    "backend": [
                        "src/app.ts", "src/routes/auth.ts", "src/routes/users.ts",
                        "src/models/User.ts", "src/services/AuthService.ts",
                        "prisma/schema.prisma", "prisma/seed.ts",
                        "src/config/database.ts", "package.json"
                    ]
                }
            },

            "nextjs_fullstack": {
                "framework": ["Next.js 14", "TypeScript", "App Router"],
                "ui": ["Tailwind CSS", "shadcn/ui", "Framer Motion"],
                "database": ["Prisma", "PostgreSQL", "Supabase"],
                "auth": ["NextAuth.js", "Clerk"],
                "deployment": ["Vercel", "AWS", "Docker"],
                "files": [
                    "app/layout.tsx", "app/page.tsx", "app/globals.css",
                    "app/(auth)/login/page.tsx", "app/(dashboard)/dashboard/page.tsx",
                    "components/ui/button.tsx", "components/ui/input.tsx",
                    "components/Header.tsx", "components/Sidebar.tsx",
                    "lib/auth.ts", "lib/db.ts", "lib/utils.ts",
                    "prisma/schema.prisma", "next.config.js", "tailwind.config.ts"
                ]
            }
        }

        self.complex_features = {
            "authentication": {
                "basic": ["login", "register", "logout"],
                "advanced": ["2FA", "OAuth", "JWT refresh", "password_reset", "email_verification"],
                "files": [
                    "auth/AuthService.js", "auth/middleware.js", "auth/strategies/jwt.js",
                    "auth/strategies/oauth.js", "auth/controllers/AuthController.js",
                    "auth/models/User.js", "auth/routes/auth.js"
                ]
            },

            "real_time": {
                "features": ["chat", "notifications", "live_updates", "collaborative_editing"],
                "technologies": ["Socket.IO", "WebRTC", "Server-Sent Events"],
                "files": [
                    "realtime/SocketServer.js", "realtime/ChatHandler.js",
                    "realtime/NotificationHandler.js", "realtime/RoomManager.js",
                    "client/socket.js", "client/chat.js"
                ]
            },

            "payment_system": {
                "providers": ["Stripe", "PayPal", "Square"],
                "features": ["subscriptions", "one_time_payments", "refunds", "webhooks"],
                "files": [
                    "payments/StripeService.js", "payments/PaymentController.js",
                    "payments/models/Payment.js", "payments/webhooks/stripe.js",
                    "payments/routes/payments.js"
                ]
            },

            "file_management": {
                "features": ["upload", "resize", "cloud_storage", "cdn"],
                "technologies": ["AWS S3", "Cloudinary", "Firebase Storage"],
                "files": [
                    "storage/FileService.js", "storage/ImageProcessor.js",
                    "storage/CloudUploader.js", "storage/controllers/FileController.js"
                ]
            }
        }

        self.database_patterns = {
            "relational": {
                "databases": ["PostgreSQL", "MySQL", "SQLite"],
                "patterns": ["Repository Pattern", "Active Record", "Data Mapper"],
                "files": [
                    "database/migrations/001_create_users.sql",
                    "database/models/User.js", "database/repositories/UserRepository.js",
                    "database/config/connection.js", "database/seeders/UserSeeder.js"
                ]
            },

            "nosql": {
                "databases": ["MongoDB", "DynamoDB", "Firebase"],
                "patterns": ["Document Store", "Collection Pattern"],
                "files": [
                    "database/models/User.js", "database/services/MongoService.js",
                    "database/config/mongodb.js", "database/schemas/userSchema.js"
                ]
            }
        }

    def get_architecture_recommendation(self, project_type: str, complexity: str, team_size: int) -> dict:
        """แนะนำ Architecture ที่เหมาะสม"""
        
        if complexity == "simple" and team_size <= 2:
            return {
                "architecture": "mvc",
                "stack": "react_fullstack",
                "reasoning": "MVC pattern เหมาะสำหรับโปรเจกต์เล็ก ทีมน้อย"
            }
        
        elif complexity == "medium" and team_size <= 5:
            return {
                "architecture": "component_architecture", 
                "stack": "nextjs_fullstack",
                "reasoning": "Component architecture เหมาะสำหรับโปรเจกต์ขนาดกลาง"
            }
        
        elif complexity == "high" or team_size > 5:
            return {
                "architecture": "microservices",
                "stack": "react_fullstack",
                "reasoning": "Microservices เหมาะสำหรับโปรเจกต์ใหญ่ ทีมหลายคน"
            }
        
        else:
            return {
                "architecture": "jamstack",
                "stack": "nextjs_fullstack", 
                "reasoning": "JAMstack เหมาะสำหรับเว็บไซต์ทั่วไป"
            }

    def generate_file_structure(self, architecture: str, features: list) -> dict:
        """สร้างโครงสร้างไฟล์ที่ซับซ้อน"""
        
        base_files = self.architecture_patterns[architecture]["files_needed"]
        feature_files = []
        
        for feature in features:
            if feature in self.complex_features:
                feature_files.extend(self.complex_features[feature]["files"])
        
        return {
            "base_files": base_files,
            "feature_files": feature_files,
            "total_files": len(base_files) + len(feature_files),
            "complexity_score": self._calculate_complexity(architecture, features)
        }

    def _calculate_complexity(self, architecture: str, features: list) -> int:
        """คำนวณคะแนนความซับซ้อน"""
        
        base_score = {
            "mvc": 3,
            "component_architecture": 5,
            "microservices": 8,
            "jamstack": 4
        }.get(architecture, 3)
        
        feature_score = len(features) * 2
        
        return min(base_score + feature_score, 10)

# Global instance
ai_knowledge = AIKnowledgeBase()