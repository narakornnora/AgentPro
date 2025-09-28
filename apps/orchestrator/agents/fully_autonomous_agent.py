"""
Fully Autonomous Development Agent
Agent ที่สามารถพัฒนาแอพพลิเคชันได้อย่างครบวงจรโดยอัตโนมัติ
- สร้างไฟล์เอง (Code Generation)
- แก้ไฟล์เอง (Self-Editing)
- สร้าง Database เอง (Schema Design)
- ออกแบบเอง (UI/UX Generation) 
- ทดสอบเอง (Quality Assurance)
"""

import os
import json
import asyncio
import time
import uuid
import subprocess
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

from .base_agent import BaseAgent, AgentTask, AgentResult
from .requirement_tracker import RequirementTracker, RequirementStatus

class AppType(Enum):
    WEB_APP = "web_app"
    MOBILE_APP = "mobile_app"
    DESKTOP_APP = "desktop_app"
    API_SERVER = "api_server"
    MICROSERVICE = "microservice"
    STATIC_SITE = "static_site"
    PROGRESSIVE_WEB_APP = "pwa"
    ELECTRON_APP = "electron_app"

class TechStack(Enum):
    # Frontend
    HTML_CSS_JS = "html_css_js"
    REACT = "react"
    VUE = "vue"
    ANGULAR = "angular"
    SVELTE = "svelte"
    
    # Backend
    NODE_EXPRESS = "node_express"
    PYTHON_FLASK = "python_flask"
    PYTHON_DJANGO = "python_django"
    PYTHON_FASTAPI = "python_fastapi"
    PHP_LARAVEL = "php_laravel"
    JAVA_SPRING = "java_spring"
    DOTNET_CORE = "dotnet_core"
    GO_GIN = "go_gin"
    RUBY_RAILS = "ruby_rails"

class DatabaseType(Enum):
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    MONGODB = "mongodb"
    REDIS = "redis"
    FIREBASE = "firebase"
    JSON_FILES = "json_files"

@dataclass
class ProjectStructure:
    app_type: AppType
    tech_stack: TechStack
    database: DatabaseType
    features: List[str]
    file_structure: Dict[str, Any]
    dependencies: List[str]
    build_commands: List[str]
    run_commands: List[str]

class FullyAutonomousAgent(BaseAgent):
    """Agent ที่สามารถพัฒนาแอพได้อย่างครบวงจรโดยอัตโนมัติ"""
    
    def __init__(self, openai_client, workspace_path: Path):
        super().__init__(
            name="FullyAutonomousAgent",
            capabilities=[
                "autonomous_development",
                "code_generation",
                "database_design",
                "ui_design", 
                "testing",
                "deployment"
            ]
        )
        self.client = openai_client
        self.workspace = workspace_path
        self.workspace.mkdir(parents=True, exist_ok=True)
        
        # Project templates และ patterns
        self.project_templates = self._load_project_templates()
        self.ui_components = self._load_ui_components()
        self.database_schemas = self._load_database_schemas()
        
    def can_handle(self, task: AgentTask) -> bool:
        """ตรวจสอบว่า agent สามารถจัดการงานได้หรือไม่"""
        return task.type in [
            "create_full_application",
            "autonomous_development",
            "generate_complete_project"
        ]
    
    async def execute_task(self, task: AgentTask) -> AgentResult:
        """Execute autonomous development task"""
        
        try:
            user_requirements = task.input_data.get("requirements", "")
            app_preferences = task.input_data.get("preferences", {})
            
            # Phase 1: Autonomous Project Analysis
            project_plan = await self._analyze_and_plan_project(user_requirements, app_preferences)
            
            # Phase 2: Generate Project Structure
            project_path = await self._create_project_structure(project_plan)
            
            # Phase 3: Generate Code Files
            generated_files = await self._generate_all_code_files(project_plan, project_path)
            
            # Phase 4: Setup Database
            database_setup = await self._setup_database(project_plan, project_path)
            
            # Phase 5: Generate UI/UX
            ui_files = await self._generate_ui_design(project_plan, project_path)
            
            # Phase 6: Self-Testing
            test_results = await self._run_autonomous_tests(project_plan, project_path)
            
            # Phase 7: Self-Improvement (if tests fail)
            if test_results.get("pass_rate", 0) < 80:
                improved_files = await self._self_improve_code(project_plan, project_path, test_results)
                # Re-test after improvements
                test_results = await self._run_autonomous_tests(project_plan, project_path)
            
            # Phase 8: Package and Deploy
            deployment_info = await self._prepare_deployment(project_plan, project_path)
            
            return AgentResult(
                success=True,
                data={
                    "project_path": str(project_path),
                    "project_plan": project_plan,
                    "generated_files": generated_files,
                    "database_setup": database_setup,
                    "ui_files": ui_files,
                    "test_results": test_results,
                    "deployment_info": deployment_info,
                    "preview_url": deployment_info.get("preview_url"),
                    "agent_name": self.name
                },
                suggestions=[
                    f"Project generated: {project_plan['app_type']}",
                    f"Tech stack: {project_plan['tech_stack']}",
                    f"Test pass rate: {test_results.get('pass_rate', 0)}%"
                ]
            )
            
        except Exception as e:
            return AgentResult(
                success=False,
                data={},
                issues=[f"Autonomous development failed: {str(e)}"]
            )
    
    async def improve_result(self, result: AgentResult, feedback: Dict[str, Any]) -> AgentResult:
        """Autonomous improvement based on feedback"""
        
        if not result.success:
            return result
            
        project_path = Path(result.data["project_path"])
        project_plan = result.data["project_plan"]
        
        # Analyze feedback and improve
        improvements = await self._analyze_feedback_and_improve(
            feedback, project_plan, project_path
        )
        
        # Update result with improvements
        result.data.update(improvements)
        
        return result
    
    async def _analyze_and_plan_project(self, requirements: str, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """วิเคราะห์และวางแผนโปรเจคแบบอัตโนมัติ"""
        
        analysis_prompt = f"""
        Analyze the following requirements and create a complete project plan:
        
        Requirements: "{requirements}"
        Preferences: {json.dumps(preferences, indent=2)}
        
        Create a comprehensive project plan with:
        1. App type (web_app, mobile_app, api_server, etc.)
        2. Tech stack selection with reasoning
        3. Database requirements
        4. Feature breakdown
        5. File structure
        6. Dependencies
        7. UI/UX requirements
        8. Testing strategy
        
        Return JSON format:
        {{
            "app_type": "web_app|mobile_app|api_server|etc",
            "tech_stack": "react|vue|python_flask|etc",
            "database": "sqlite|postgresql|mongodb|etc", 
            "features": ["feature1", "feature2"],
            "pages": ["page1", "page2"],
            "components": ["comp1", "comp2"],
            "apis": ["api1", "api2"],
            "file_structure": {{
                "folders": ["src", "public", "api"],
                "key_files": ["index.html", "app.js", "api.py"]
            }},
            "dependencies": ["package1", "package2"],
            "ui_theme": "modern|minimal|corporate|creative",
            "color_scheme": ["#primary", "#secondary"],
            "complexity_score": 1-10
        }}
        """
        
        try:
            response = await self.client.chat.completions.acreate(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert software architect. Respond only with valid JSON."},
                    {"role": "user", "content": analysis_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            plan = json.loads(response.choices[0].message.content)
            
            # Add project ID and timestamps
            plan["project_id"] = f"project_{int(time.time())}"
            plan["created_at"] = time.time()
            
            return plan
            
        except Exception as e:
            print(f"Project analysis error: {e}")
            # Fallback plan
            return {
                "app_type": "web_app",
                "tech_stack": "html_css_js",
                "database": "json_files",
                "features": ["home_page", "about", "contact"],
                "pages": ["index", "about", "contact"],
                "components": ["header", "footer", "main_content"],
                "apis": [],
                "file_structure": {
                    "folders": ["assets", "css", "js"],
                    "key_files": ["index.html", "styles.css", "script.js"]
                },
                "dependencies": [],
                "ui_theme": "modern",
                "color_scheme": ["#667eea", "#764ba2"],
                "complexity_score": 3,
                "project_id": f"project_{int(time.time())}",
                "created_at": time.time()
            }
    
    async def _create_project_structure(self, plan: Dict[str, Any]) -> Path:
        """สร้างโครงสร้างโปรเจคอัตโนมัติ"""
        
        project_id = plan["project_id"]
        project_path = self.workspace / project_id
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Create folder structure
        folders = plan["file_structure"].get("folders", [])
        for folder in folders:
            (project_path / folder).mkdir(parents=True, exist_ok=True)
        
        # Create additional standard folders based on app type
        app_type = plan.get("app_type", "web_app")
        
        if app_type in ["web_app", "static_site"]:
            standard_folders = ["assets", "css", "js", "images", "data"]
        elif app_type == "api_server":
            standard_folders = ["routes", "models", "middleware", "utils", "tests"]
        elif app_type == "react":
            standard_folders = ["src", "public", "src/components", "src/pages", "src/utils"]
        else:
            standard_folders = ["src", "assets", "config"]
        
        for folder in standard_folders:
            (project_path / folder).mkdir(parents=True, exist_ok=True)
        
        # Create project configuration files
        await self._create_config_files(plan, project_path)
        
        return project_path
    
    async def _create_config_files(self, plan: Dict[str, Any], project_path: Path):
        """สร้างไฟล์ config อัตโนมัติ"""
        
        # package.json for Node.js projects
        if plan.get("tech_stack") in ["react", "vue", "node_express"]:
            package_json = {
                "name": plan["project_id"],
                "version": "1.0.0",
                "description": "Auto-generated project",
                "main": "index.js",
                "scripts": {
                    "start": "node server.js",
                    "dev": "nodemon server.js",
                    "build": "webpack --mode production",
                    "test": "jest"
                },
                "dependencies": {},
                "devDependencies": {}
            }
            
            (project_path / "package.json").write_text(
                json.dumps(package_json, indent=2)
            )
        
        # requirements.txt for Python projects
        if "python" in plan.get("tech_stack", ""):
            requirements = [
                "flask==2.3.3" if "flask" in plan.get("tech_stack", "") else "",
                "django==4.2.5" if "django" in plan.get("tech_stack", "") else "",
                "fastapi==0.103.1" if "fastapi" in plan.get("tech_stack", "") else "",
                "sqlalchemy==2.0.21",
                "pytest==7.4.2",
                "requests==2.31.0"
            ]
            
            requirements = [req for req in requirements if req]  # Remove empty strings
            
            (project_path / "requirements.txt").write_text("\n".join(requirements))
        
        # README.md
        readme_content = f"""# {plan["project_id"].replace('_', ' ').title()}

Auto-generated project using AgentPro AI Builder

## Project Details
- **Type:** {plan.get("app_type", "N/A")}
- **Tech Stack:** {plan.get("tech_stack", "N/A")}
- **Database:** {plan.get("database", "N/A")}

## Features
{chr(10).join(f"- {feature}" for feature in plan.get("features", []))}

## Getting Started

### Installation
```bash
# Install dependencies
{"npm install" if "node" in plan.get("tech_stack", "") or plan.get("tech_stack") in ["react", "vue"] else "pip install -r requirements.txt"}
```

### Running the Application
```bash
# Start development server
{"npm run dev" if "node" in plan.get("tech_stack", "") or plan.get("tech_stack") in ["react", "vue"] else "python app.py"}
```

## Project Structure
{chr(10).join(f"- `{folder}/`" for folder in plan["file_structure"].get("folders", []))}

Generated by AgentPro AI Builder on {time.strftime("%Y-%m-%d %H:%M:%S")}
"""
        
        (project_path / "README.md").write_text(readme_content)
    
    async def _generate_all_code_files(self, plan: Dict[str, Any], project_path: Path) -> List[str]:
        """Generate all code files autonomously"""
        
        generated_files = []
        
        # Generate based on app type and tech stack
        app_type = plan.get("app_type", "web_app")
        tech_stack = plan.get("tech_stack", "html_css_js")
        
        if tech_stack == "html_css_js":
            generated_files.extend(await self._generate_html_css_js_files(plan, project_path))
        elif tech_stack == "react":
            generated_files.extend(await self._generate_react_files(plan, project_path))
        elif tech_stack == "python_flask":
            generated_files.extend(await self._generate_flask_files(plan, project_path))
        elif tech_stack == "node_express":
            generated_files.extend(await self._generate_express_files(plan, project_path))
        else:
            # Default to HTML/CSS/JS
            generated_files.extend(await self._generate_html_css_js_files(plan, project_path))
        
        return generated_files
    
    async def _generate_html_css_js_files(self, plan: Dict[str, Any], project_path: Path) -> List[str]:
        """Generate HTML, CSS, JS files"""
        
        files_created = []
        
        # Generate HTML files for each page
        pages = plan.get("pages", ["index"])
        for page in pages:
            html_content = await self._generate_html_page(page, plan)
            file_path = project_path / f"{page}.html"
            file_path.write_text(html_content, encoding="utf-8")
            files_created.append(str(file_path))
        
        # Generate CSS file
        css_content = await self._generate_css_styles(plan)
        css_path = project_path / "css" / "styles.css"
        css_path.write_text(css_content, encoding="utf-8")
        files_created.append(str(css_path))
        
        # Generate JavaScript file
        js_content = await self._generate_javascript(plan)
        js_path = project_path / "js" / "script.js"
        js_path.write_text(js_content, encoding="utf-8")
        files_created.append(str(js_path))
        
        return files_created
    
    async def _generate_html_page(self, page_name: str, plan: Dict[str, Any]) -> str:
        """Generate HTML page content"""
        
        prompt = f"""
        Generate a complete HTML page for "{page_name}" with these specifications:
        
        Project: {plan.get("project_id", "Unknown")}
        App Type: {plan.get("app_type", "web_app")}
        Features: {plan.get("features", [])}
        UI Theme: {plan.get("ui_theme", "modern")}
        Color Scheme: {plan.get("color_scheme", ["#667eea", "#764ba2"])}
        
        Requirements:
        - Modern, responsive HTML5 structure
        - Semantic HTML elements
        - Proper meta tags for SEO
        - Link to ./css/styles.css
        - Link to ./js/script.js
        - Include navigation to other pages: {plan.get("pages", [])}
        - Content appropriate for {page_name} page
        - Accessibility attributes
        - Mobile-first approach
        
        Generate ONLY the HTML content, no explanations.
        """
        
        try:
            response = await self.client.chat.completions.acreate(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert frontend developer. Generate clean, semantic HTML5 code."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"HTML generation error: {e}")
            # Fallback HTML
            return self._get_fallback_html(page_name, plan)
    
    def _get_fallback_html(self, page_name: str, plan: Dict[str, Any]) -> str:
        """Fallback HTML template"""
        
        return f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_name.title()} - {plan.get("project_id", "My App").replace("_", " ").title()}</title>
    <meta name="description" content="Auto-generated {page_name} page">
    <link rel="stylesheet" href="./css/styles.css">
</head>
<body>
    <header>
        <nav>
            <div class="nav-container">
                <div class="logo">
                    <h1>{plan.get("project_id", "My App").replace("_", " ").title()}</h1>
                </div>
                <ul class="nav-menu">
                    {chr(10).join(f'<li><a href="./{page}.html">{page.title()}</a></li>' for page in plan.get("pages", []))}
                </ul>
            </div>
        </nav>
    </header>

    <main>
        <section class="hero">
            <div class="container">
                <h1>Welcome to {page_name.title()} Page</h1>
                <p>This page was auto-generated by AgentPro AI Builder</p>
            </div>
        </section>

        <section class="content">
            <div class="container">
                <h2>Features</h2>
                <div class="features-grid">
                    {chr(10).join(f'<div class="feature-card"><h3>{feature}</h3><p>Description for {feature}</p></div>' for feature in plan.get("features", []))}
                </div>
            </div>
        </section>
    </main>

    <footer>
        <div class="container">
            <p>&copy; {time.strftime("%Y")} {plan.get("project_id", "My App").replace("_", " ").title()}. Generated by AgentPro AI Builder.</p>
        </div>
    </footer>

    <script src="./js/script.js"></script>
</body>
</html>"""
    
    async def _generate_css_styles(self, plan: Dict[str, Any]) -> str:
        """Generate CSS styles autonomously"""
        
        prompt = f"""
        Generate comprehensive CSS styles for this project:
        
        Project: {plan.get("project_id", "Unknown")}
        UI Theme: {plan.get("ui_theme", "modern")}
        Color Scheme: {plan.get("color_scheme", ["#667eea", "#764ba2"])}
        Features: {plan.get("features", [])}
        Pages: {plan.get("pages", [])}
        
        Generate modern, responsive CSS with:
        - CSS Variables for colors and spacing
        - Mobile-first responsive design
        - Flexbox and CSS Grid layouts
        - Smooth animations and transitions
        - Modern typography
        - Accessibility considerations
        - Beautiful gradients and shadows
        - Hover effects and interactions
        - Print styles
        
        Include styles for:
        - Navigation menu
        - Hero sections
        - Feature cards/grids
        - Forms and buttons
        - Footer
        - Utility classes
        
        Generate ONLY CSS code, no explanations.
        """
        
        try:
            response = await self.client.chat.completions.acreate(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert CSS developer. Generate modern, clean CSS code."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"CSS generation error: {e}")
            return self._get_fallback_css(plan)
    
    def _get_fallback_css(self, plan: Dict[str, Any]) -> str:
        """Fallback CSS styles"""
        
        colors = plan.get("color_scheme", ["#667eea", "#764ba2"])
        primary_color = colors[0] if colors else "#667eea"
        secondary_color = colors[1] if len(colors) > 1 else "#764ba2"
        
        return f"""/* Auto-generated CSS by AgentPro AI Builder */

:root {{
    --primary-color: {primary_color};
    --secondary-color: {secondary_color};
    --text-color: #333;
    --bg-color: #ffffff;
    --light-gray: #f8f9fa;
    --border-color: #e0e0e0;
    --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    --border-radius: 8px;
    --transition: all 0.3s ease;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background-color: var(--bg-color);
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}}

/* Header and Navigation */
header {{
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    padding: 1rem 0;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: var(--shadow);
}}

.nav-container {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}}

.logo h1 {{
    font-size: 1.8rem;
    font-weight: 700;
}}

.nav-menu {{
    display: flex;
    list-style: none;
    gap: 2rem;
}}

.nav-menu a {{
    color: white;
    text-decoration: none;
    font-weight: 500;
    transition: var(--transition);
    padding: 0.5rem 1rem;
    border-radius: var(--border-radius);
}}

.nav-menu a:hover {{
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
}}

/* Main Content */
main {{
    min-height: calc(100vh - 120px);
}}

.hero {{
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    padding: 4rem 0;
    text-align: center;
}}

.hero h1 {{
    font-size: 3rem;
    margin-bottom: 1rem;
    font-weight: 700;
}}

.hero p {{
    font-size: 1.2rem;
    opacity: 0.9;
    max-width: 600px;
    margin: 0 auto;
}}

.content {{
    padding: 4rem 0;
}}

.content h2 {{
    text-align: center;
    margin-bottom: 3rem;
    font-size: 2.5rem;
    color: var(--text-color);
}}

/* Features Grid */
.features-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}}

.feature-card {{
    background: white;
    padding: 2rem;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    text-align: center;
    transition: var(--transition);
    border: 1px solid var(--border-color);
}}

.feature-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}}

.feature-card h3 {{
    color: var(--primary-color);
    margin-bottom: 1rem;
    font-size: 1.5rem;
}}

/* Buttons */
.btn {{
    display: inline-block;
    padding: 12px 24px;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    text-decoration: none;
    border-radius: var(--border-radius);
    font-weight: 500;
    transition: var(--transition);
    border: none;
    cursor: pointer;
}}

.btn:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}}

/* Footer */
footer {{
    background: var(--light-gray);
    padding: 2rem 0;
    text-align: center;
    border-top: 1px solid var(--border-color);
}}

/* Responsive Design */
@media (max-width: 768px) {{
    .nav-container {{
        flex-direction: column;
        gap: 1rem;
    }}
    
    .nav-menu {{
        gap: 1rem;
    }}
    
    .hero h1 {{
        font-size: 2rem;
    }}
    
    .content h2 {{
        font-size: 2rem;
    }}
    
    .features-grid {{
        grid-template-columns: 1fr;
        gap: 1rem;
    }}
}}

/* Utility Classes */
.text-center {{ text-align: center; }}
.mt-1 {{ margin-top: 1rem; }}
.mt-2 {{ margin-top: 2rem; }}
.mb-1 {{ margin-bottom: 1rem; }}
.mb-2 {{ margin-bottom: 2rem; }}
.p-1 {{ padding: 1rem; }}
.p-2 {{ padding: 2rem; }}

/* Animations */
@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.animate-fade-in {{
    animation: fadeIn 0.6s ease-out;
}}"""
    
    async def _generate_javascript(self, plan: Dict[str, Any]) -> str:
        """Generate JavaScript functionality"""
        
        prompt = f"""
        Generate comprehensive JavaScript for this project:
        
        Project: {plan.get("project_id", "Unknown")}
        Features: {plan.get("features", [])}
        Pages: {plan.get("pages", [])}
        
        Generate modern JavaScript that includes:
        - DOM manipulation
        - Event listeners
        - Smooth scrolling navigation
        - Interactive animations
        - Form validation (if forms exist)
        - Mobile menu toggle
        - Loading animations
        - Error handling
        - Accessibility improvements
        - Performance optimizations
        
        Use modern ES6+ syntax with:
        - Arrow functions
        - Template literals
        - Async/await
        - Destructuring
        - Modules pattern
        
        Generate ONLY JavaScript code, no explanations.
        """
        
        try:
            response = await self.client.chat.completions.acreate(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert JavaScript developer. Generate modern, clean JS code."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"JavaScript generation error: {e}")
            return self._get_fallback_javascript(plan)
    
    def _get_fallback_javascript(self, plan: Dict[str, Any]) -> str:
        """Fallback JavaScript code"""
        
        return f"""// Auto-generated JavaScript by AgentPro AI Builder
// Project: {plan.get("project_id", "Unknown")}

class AppController {{
    constructor() {{
        this.init();
    }}

    init() {{
        this.setupEventListeners();
        this.setupAnimations();
        this.setupNavigation();
        this.setupAccessibility();
        console.log('🤖 AgentPro AI Builder - App initialized successfully!');
    }}

    setupEventListeners() {{
        // Wait for DOM to be fully loaded
        document.addEventListener('DOMContentLoaded', () => {{
            this.handlePageLoad();
        }});

        // Handle window resize
        window.addEventListener('resize', this.debounce(() => {{
            this.handleResize();
        }}, 250));

        // Handle scroll events
        window.addEventListener('scroll', this.throttle(() => {{
            this.handleScroll();
        }}, 16));
    }}

    setupNavigation() {{
        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', (e) => {{
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{
                        behavior: 'smooth',
                        block: 'start'
                    }});
                }}
            }});
        }});

        // Mobile menu toggle (if exists)
        const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
        const navMenu = document.querySelector('.nav-menu');
        
        if (mobileMenuBtn && navMenu) {{
            mobileMenuBtn.addEventListener('click', () => {{
                navMenu.classList.toggle('active');
                mobileMenuBtn.classList.toggle('active');
            }});
        }}
    }}

    setupAnimations() {{
        // Intersection Observer for animations
        const observerOptions = {{
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        }};

        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('animate-fade-in');
                    observer.unobserve(entry.target);
                }}
            }});
        }}, observerOptions);

        // Observe elements for animation
        document.querySelectorAll('.feature-card, .content section').forEach(el => {{
            observer.observe(el);
        }});
    }}

    setupAccessibility() {{
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Tab') {{
                document.body.classList.add('keyboard-nav');
            }}
        }});

        document.addEventListener('mousedown', () => {{
            document.body.classList.remove('keyboard-nav');
        }});

        // Skip to main content link
        const skipLink = document.createElement('a');
        skipLink.href = '#main';
        skipLink.textContent = 'Skip to main content';
        skipLink.className = 'skip-link';
        skipLink.style.cssText = `
            position: absolute;
            top: -40px;
            left: 6px;
            background: var(--primary-color);
            color: white;
            padding: 8px;
            border-radius: 4px;
            text-decoration: none;
            transition: top 0.3s;
            z-index: 1000;
        `;
        
        skipLink.addEventListener('focus', () => {{
            skipLink.style.top = '6px';
        }});
        
        skipLink.addEventListener('blur', () => {{
            skipLink.style.top = '-40px';
        }});

        document.body.insertBefore(skipLink, document.body.firstChild);
    }}

    handlePageLoad() {{
        // Add loading complete class
        document.body.classList.add('loaded');
        
        // Initialize any page-specific functionality
        this.initializeForms();
        this.initializeInteractiveElements();
    }}

    handleResize() {{
        // Handle responsive adjustments
        console.log('Window resized:', window.innerWidth);
    }}

    handleScroll() {{
        // Handle scroll-based animations or effects
        const scrolled = window.pageYOffset;
        const header = document.querySelector('header');
        
        if (header) {{
            if (scrolled > 100) {{
                header.classList.add('scrolled');
            }} else {{
                header.classList.remove('scrolled');
            }}
        }}
    }}

    initializeForms() {{
        // Form validation and handling
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {{
            form.addEventListener('submit', (e) => {{
                if (!this.validateForm(form)) {{
                    e.preventDefault();
                }}
            }});
        }});
    }}

    validateForm(form) {{
        let isValid = true;
        const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
        
        inputs.forEach(input => {{
            if (!input.value.trim()) {{
                this.showError(input, 'This field is required');
                isValid = false;
            }} else {{
                this.clearError(input);
            }}
        }});
        
        return isValid;
    }}

    showError(input, message) {{
        input.classList.add('error');
        
        let errorEl = input.parentNode.querySelector('.error-message');
        if (!errorEl) {{
            errorEl = document.createElement('div');
            errorEl.className = 'error-message';
            errorEl.style.cssText = 'color: #e74c3c; font-size: 0.9rem; margin-top: 5px;';
            input.parentNode.appendChild(errorEl);
        }}
        
        errorEl.textContent = message;
    }}

    clearError(input) {{
        input.classList.remove('error');
        const errorEl = input.parentNode.querySelector('.error-message');
        if (errorEl) {{
            errorEl.remove();
        }}
    }}

    initializeInteractiveElements() {{
        // Add hover effects and interactions
        document.querySelectorAll('.feature-card').forEach(card => {{
            card.addEventListener('mouseenter', () => {{
                card.style.transform = 'translateY(-5px) scale(1.02)';
            }});
            
            card.addEventListener('mouseleave', () => {{
                card.style.transform = 'translateY(0) scale(1)';
            }});
        }});

        // Add click animations to buttons
        document.querySelectorAll('.btn').forEach(btn => {{
            btn.addEventListener('click', function(e) {{
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.cssText = `
                    position: absolute;
                    width: ${{size}}px;
                    height: ${{size}}px;
                    left: ${{x}}px;
                    top: ${{y}}px;
                    background: rgba(255, 255, 255, 0.3);
                    border-radius: 50%;
                    transform: scale(0);
                    animation: ripple 0.6s linear;
                    pointer-events: none;
                `;
                
                this.style.position = 'relative';
                this.style.overflow = 'hidden';
                this.appendChild(ripple);
                
                setTimeout(() => ripple.remove(), 600);
            }});
        }});
    }}

    // Utility functions
    debounce(func, wait) {{
        let timeout;
        return function executedFunction(...args) {{
            const later = () => {{
                clearTimeout(timeout);
                func(...args);
            }};
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        }};
    }}

    throttle(func, limit) {{
        let inThrottle;
        return function() {{
            const args = arguments;
            const context = this;
            if (!inThrottle) {{
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }}
        }};
    }}
}}

// Add ripple animation CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {{
        to {{
            transform: scale(4);
            opacity: 0;
        }}
    }}
    
    .keyboard-nav *:focus {{
        outline: 2px solid var(--primary-color);
        outline-offset: 2px;
    }}
    
    body:not(.keyboard-nav) *:focus {{
        outline: none;
    }}
`;
document.head.appendChild(style);

// Initialize the app
const app = new AppController();

// Export for use in other scripts
window.AgentProApp = app;"""
    
    async def _setup_database(self, plan: Dict[str, Any], project_path: Path) -> Dict[str, Any]:
        """Setup database autonomously"""
        
        database_type = plan.get("database", "json_files")
        
        if database_type == "json_files":
            return await self._setup_json_database(plan, project_path)
        elif database_type == "sqlite":
            return await self._setup_sqlite_database(plan, project_path)
        elif database_type == "postgresql":
            return await self._setup_postgresql_database(plan, project_path)
        else:
            return await self._setup_json_database(plan, project_path)  # Fallback
    
    async def _setup_json_database(self, plan: Dict[str, Any], project_path: Path) -> Dict[str, Any]:
        """Setup JSON file-based database"""
        
        data_dir = project_path / "data"
        data_dir.mkdir(exist_ok=True)
        
        # Create sample data files based on features
        features = plan.get("features", [])
        created_files = []
        
        # Default data structure
        default_data = {
            "users": [
                {"id": 1, "name": "John Doe", "email": "john@example.com"},
                {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
            ],
            "settings": {
                "app_name": plan.get("project_id", "My App"),
                "version": "1.0.0",
                "theme": plan.get("ui_theme", "modern")
            }
        }
        
        # Feature-specific data
        if "products" in str(features).lower() or "shop" in str(features).lower():
            default_data["products"] = [
                {"id": 1, "name": "Product 1", "price": 299, "category": "Category A"},
                {"id": 2, "name": "Product 2", "price": 399, "category": "Category B"}
            ]
        
        if "blog" in str(features).lower() or "articles" in str(features).lower():
            default_data["articles"] = [
                {
                    "id": 1,
                    "title": "Welcome to Our Blog",
                    "content": "This is a sample blog post.",
                    "author": "Admin",
                    "date": time.strftime("%Y-%m-%d")
                }
            ]
        
        # Write data files
        for data_type, data in default_data.items():
            file_path = data_dir / f"{data_type}.json"
            file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
            created_files.append(str(file_path))
        
        return {
            "type": "json_files",
            "location": str(data_dir),
            "files": created_files,
            "structure": list(default_data.keys())
        }
    
    def _load_project_templates(self) -> Dict[str, Any]:
        """Load project templates"""
        return {
            "web_app": {},
            "api_server": {},
            "mobile_app": {}
        }
    
    def _load_ui_components(self) -> Dict[str, Any]:
        """Load UI component templates"""
        return {
            "header": {},
            "footer": {},
            "button": {},
            "card": {}
        }
    
    def _load_database_schemas(self) -> Dict[str, Any]:
        """Load database schema templates"""
        return {
            "user": {},
            "product": {},
            "order": {}
        }
    
    async def _generate_ui_design(self, plan: Dict[str, Any], project_path: Path) -> List[str]:
        """Generate UI design files"""
        # This method will be expanded to generate additional UI assets
        return []
    
    async def _run_autonomous_tests(self, plan: Dict[str, Any], project_path: Path) -> Dict[str, Any]:
        """Run autonomous tests"""
        
        # Simple file existence tests
        tests_passed = 0
        total_tests = 0
        
        # Test if key files exist
        key_files = ["index.html", "css/styles.css", "js/script.js"]
        
        for file_path in key_files:
            total_tests += 1
            if (project_path / file_path).exists():
                tests_passed += 1
        
        pass_rate = (tests_passed / total_tests * 100) if total_tests > 0 else 0
        
        return {
            "total_tests": total_tests,
            "passed": tests_passed,
            "failed": total_tests - tests_passed,
            "pass_rate": pass_rate,
            "details": "Basic file structure validation"
        }
    
    async def _self_improve_code(self, plan: Dict[str, Any], project_path: Path, test_results: Dict[str, Any]) -> List[str]:
        """Self-improve code based on test results"""
        
        improved_files = []
        
        # Analyze failed tests and improve
        failed_count = test_results.get("failed", 0)
        
        if failed_count > 0:
            # Re-generate missing files
            key_files = ["index.html", "css/styles.css", "js/script.js"]
            
            for file_path in key_files:
                full_path = project_path / file_path
                if not full_path.exists():
                    # Re-generate missing file
                    if file_path == "index.html":
                        content = await self._generate_html_page("index", plan)
                        full_path.write_text(content, encoding="utf-8")
                    elif file_path == "css/styles.css":
                        content = await self._generate_css_styles(plan)
                        full_path.write_text(content, encoding="utf-8")
                    elif file_path == "js/script.js":
                        content = await self._generate_javascript(plan)
                        full_path.write_text(content, encoding="utf-8")
                    
                    improved_files.append(str(full_path))
        
        return improved_files
    
    async def _prepare_deployment(self, plan: Dict[str, Any], project_path: Path) -> Dict[str, Any]:
        """Prepare for deployment"""
        
        # Create deployment package
        return {
            "ready_for_deployment": True,
            "preview_url": f"/app/{plan['project_id']}/index.html",
            "deployment_path": str(project_path),
            "entry_point": "index.html"
        }
    
    async def _analyze_feedback_and_improve(self, feedback: Dict[str, Any], plan: Dict[str, Any], project_path: Path) -> Dict[str, Any]:
        """Analyze feedback and make improvements"""
        
        improvements = {}
        
        # Process feedback and make improvements
        if feedback.get("ui_feedback"):
            # Improve UI based on feedback
            pass
        
        if feedback.get("functionality_feedback"):
            # Improve functionality
            pass
        
        return improvements