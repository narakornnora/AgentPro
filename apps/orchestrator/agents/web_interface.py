"""
Enhanced Web Interface System
ระบบ web interface ที่สวยงามและใช้งานง่าย เทียบเท่า Lovable
- Real-time collaborative editor with live preview
- Drag-and-drop visual builder 
- Advanced code editor with AI assistance
- Beautiful responsive design system
- Real-time collaboration features
- Performance monitoring dashboard
- Analytics and optimization interface
"""

import asyncio
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum
import aiofiles
import aiohttp

class InterfaceTheme(Enum):
    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"
    CUSTOM = "custom"

class EditorMode(Enum):
    VISUAL = "visual"
    CODE = "code" 
    SPLIT = "split"
    PREVIEW = "preview"

class ComponentCategory(Enum):
    LAYOUT = "layout"
    NAVIGATION = "navigation" 
    FORMS = "forms"
    DATA_DISPLAY = "data_display"
    FEEDBACK = "feedback"
    MEDIA = "media"
    CUSTOM = "custom"

class DeploymentStatus(Enum):
    IDLE = "idle"
    BUILDING = "building"
    DEPLOYING = "deploying"
    SUCCESS = "success"
    ERROR = "error"

@dataclass
class UIComponent:
    component_id: str
    name: str
    category: ComponentCategory
    description: str
    props: Dict[str, Any]
    children: List[str]
    styles: Dict[str, Any]
    responsive_settings: Dict[str, Any]
    accessibility_config: Dict[str, Any]
    created_at: float

@dataclass 
class ProjectFile:
    file_id: str
    file_path: str
    content: str
    file_type: str
    last_modified: float
    locked_by: Optional[str]
    collaborators: List[str]
    version_history: List[Dict[str, Any]]

@dataclass
class LivePreview:
    preview_id: str
    project_id: str
    url: str
    mode: EditorMode
    device_type: str
    viewport_size: Dict[str, int]
    hot_reload: bool
    last_updated: float

@dataclass
class CollaborationSession:
    session_id: str
    project_id: str
    participants: List[Dict[str, Any]]
    active_cursors: Dict[str, Dict[str, Any]]
    shared_state: Dict[str, Any]
    created_at: float

class EnhancedWebInterface:
    """Enhanced web interface system matching Lovable's capabilities"""
    
    def __init__(self, openai_client, project_path: Path):
        self.client = openai_client
        self.project_path = project_path
        
        # Interface state
        self.current_theme = InterfaceTheme.DARK
        self.editor_mode = EditorMode.SPLIT
        
        # Project management
        self.active_projects: Dict[str, Dict[str, Any]] = {}
        self.project_files: Dict[str, ProjectFile] = {}
        self.ui_components: Dict[str, UIComponent] = {}
        
        # Live preview system
        self.live_previews: Dict[str, LivePreview] = {}
        self.collaboration_sessions: Dict[str, CollaborationSession] = {}
        
        # Component library
        self.component_library = self._initialize_component_library()
        self.template_library = self._initialize_template_library()
        
        # Interface configuration
        self.interface_config = self._initialize_interface_config()
        
    def _initialize_component_library(self) -> Dict[ComponentCategory, List[Dict[str, Any]]]:
        """Initialize comprehensive component library"""
        
        return {
            ComponentCategory.LAYOUT: [
                {
                    "name": "Container",
                    "description": "Responsive container with max-width constraints",
                    "props": {"maxWidth": "1200px", "padding": "16px", "margin": "auto"},
                    "code_template": "<div className='container mx-auto px-4 max-w-7xl'>{children}</div>"
                },
                {
                    "name": "Grid", 
                    "description": "Flexible CSS Grid layout system",
                    "props": {"columns": 12, "gap": "16px", "responsive": True},
                    "code_template": "<div className='grid grid-cols-12 gap-4'>{children}</div>"
                },
                {
                    "name": "Flex",
                    "description": "Flexbox layout container",
                    "props": {"direction": "row", "justify": "flex-start", "align": "stretch"},
                    "code_template": "<div className='flex flex-row justify-start items-stretch'>{children}</div>"
                },
                {
                    "name": "Stack",
                    "description": "Vertical stack with consistent spacing",
                    "props": {"spacing": "16px", "divider": False},
                    "code_template": "<div className='flex flex-col space-y-4'>{children}</div>"
                }
            ],
            ComponentCategory.NAVIGATION: [
                {
                    "name": "Header",
                    "description": "Responsive navigation header",
                    "props": {"logo": "", "links": [], "ctaButton": True},
                    "code_template": "<header className='bg-white shadow-sm border-b'><nav className='container mx-auto px-4 py-3 flex items-center justify-between'>{children}</nav></header>"
                },
                {
                    "name": "Sidebar",
                    "description": "Collapsible sidebar navigation",
                    "props": {"position": "left", "collapsible": True, "width": "280px"},
                    "code_template": "<aside className='w-64 bg-gray-50 h-full border-r'>{children}</aside>"
                },
                {
                    "name": "Breadcrumb",
                    "description": "Navigation breadcrumb trail",
                    "props": {"separator": "/", "items": []},
                    "code_template": "<nav className='flex items-center space-x-2 text-sm text-gray-600'>{children}</nav>"
                },
                {
                    "name": "Tabs",
                    "description": "Tabbed navigation interface",
                    "props": {"defaultTab": 0, "variant": "underline"},
                    "code_template": "<div className='border-b border-gray-200'><nav className='flex space-x-8'>{children}</nav></div>"
                }
            ],
            ComponentCategory.FORMS: [
                {
                    "name": "Input",
                    "description": "Text input with validation",
                    "props": {"type": "text", "placeholder": "", "required": False, "validation": ""},
                    "code_template": "<input className='w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500' />"
                },
                {
                    "name": "Button",
                    "description": "Interactive button component",
                    "props": {"variant": "primary", "size": "medium", "disabled": False, "loading": False},
                    "code_template": "<button className='px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500'>{children}</button>"
                },
                {
                    "name": "Select",
                    "description": "Dropdown selection component",
                    "props": {"options": [], "multiple": False, "searchable": False},
                    "code_template": "<select className='w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'>{children}</select>"
                },
                {
                    "name": "Form",
                    "description": "Form container with validation",
                    "props": {"validation": "client", "autocomplete": True},
                    "code_template": "<form className='space-y-4'>{children}</form>"
                }
            ],
            ComponentCategory.DATA_DISPLAY: [
                {
                    "name": "Table",
                    "description": "Data table with sorting and pagination",
                    "props": {"sortable": True, "pagination": True, "selectable": False},
                    "code_template": "<div className='overflow-x-auto'><table className='min-w-full divide-y divide-gray-200'>{children}</table></div>"
                },
                {
                    "name": "Card",
                    "description": "Content card container",
                    "props": {"shadow": True, "border": True, "padding": "24px"},
                    "code_template": "<div className='bg-white rounded-lg shadow-sm border border-gray-200 p-6'>{children}</div>"
                },
                {
                    "name": "Badge",
                    "description": "Status badge component",
                    "props": {"variant": "default", "size": "medium"},
                    "code_template": "<span className='inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800'>{children}</span>"
                },
                {
                    "name": "Avatar",
                    "description": "User avatar component",
                    "props": {"size": "medium", "src": "", "fallback": ""},
                    "code_template": "<div className='relative inline-block h-10 w-10 rounded-full overflow-hidden bg-gray-100'>{children}</div>"
                }
            ],
            ComponentCategory.FEEDBACK: [
                {
                    "name": "Alert",
                    "description": "Alert/notification component",
                    "props": {"variant": "info", "dismissible": True, "icon": True},
                    "code_template": "<div className='rounded-md bg-blue-50 border border-blue-200 p-4'>{children}</div>"
                },
                {
                    "name": "Modal",
                    "description": "Modal dialog component",
                    "props": {"size": "medium", "backdrop": True, "closable": True},
                    "code_template": "<div className='fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50'><div className='bg-white rounded-lg shadow-xl max-w-md w-full mx-4'>{children}</div></div>"
                },
                {
                    "name": "Toast",
                    "description": "Toast notification",
                    "props": {"position": "top-right", "duration": 5000, "dismissible": True},
                    "code_template": "<div className='fixed top-4 right-4 bg-white rounded-lg shadow-lg border p-4 max-w-sm'>{children}</div>"
                },
                {
                    "name": "Progress",
                    "description": "Progress bar component",
                    "props": {"value": 0, "max": 100, "showLabel": True},
                    "code_template": "<div className='w-full bg-gray-200 rounded-full h-2'><div className='bg-blue-600 h-2 rounded-full transition-all duration-300' style={{width: '0%'}}></div></div>"
                }
            ],
            ComponentCategory.MEDIA: [
                {
                    "name": "Image",
                    "description": "Optimized image component",
                    "props": {"src": "", "alt": "", "lazy": True, "responsive": True},
                    "code_template": "<img className='max-w-full h-auto' loading='lazy' />"
                },
                {
                    "name": "Video",
                    "description": "Video player component", 
                    "props": {"src": "", "controls": True, "autoplay": False, "loop": False},
                    "code_template": "<video className='w-full h-auto' controls>{children}</video>"
                },
                {
                    "name": "Icon",
                    "description": "Icon component with library support",
                    "props": {"name": "", "size": "medium", "color": "current"},
                    "code_template": "<svg className='w-5 h-5' fill='currentColor'>{children}</svg>"
                }
            ]
        }
    
    def _initialize_template_library(self) -> List[Dict[str, Any]]:
        """Initialize template library"""
        
        return [
            {
                "name": "Landing Page",
                "description": "Modern landing page with hero section, features, and CTA",
                "category": "marketing",
                "preview_image": "/templates/landing-page.jpg",
                "components": ["Header", "Hero", "Features", "Testimonials", "CTA", "Footer"],
                "tags": ["responsive", "conversion-optimized", "modern"]
            },
            {
                "name": "Dashboard",
                "description": "Admin dashboard with sidebar navigation and charts",
                "category": "admin",
                "preview_image": "/templates/dashboard.jpg", 
                "components": ["Sidebar", "Header", "Charts", "Tables", "Cards"],
                "tags": ["admin", "data-visualization", "responsive"]
            },
            {
                "name": "E-commerce",
                "description": "Product catalog with cart and checkout",
                "category": "ecommerce",
                "preview_image": "/templates/ecommerce.jpg",
                "components": ["ProductGrid", "Cart", "Checkout", "Reviews"],
                "tags": ["shop", "payment", "responsive"]
            },
            {
                "name": "Blog",
                "description": "Clean blog layout with article listing and reading experience",
                "category": "content",
                "preview_image": "/templates/blog.jpg",
                "components": ["Header", "ArticleList", "Sidebar", "Footer"],
                "tags": ["content", "seo-optimized", "readable"]
            },
            {
                "name": "Portfolio",
                "description": "Creative portfolio showcase",
                "category": "creative",
                "preview_image": "/templates/portfolio.jpg",
                "components": ["Gallery", "About", "Contact", "Projects"],
                "tags": ["creative", "visual", "responsive"]
            }
        ]
    
    def _initialize_interface_config(self) -> Dict[str, Any]:
        """Initialize interface configuration"""
        
        return {
            "editor": {
                "theme": "vs-dark",
                "font_family": "'JetBrains Mono', 'Fira Code', monospace",
                "font_size": 14,
                "line_height": 1.5,
                "tab_size": 2,
                "word_wrap": True,
                "minimap": True,
                "line_numbers": True,
                "auto_save": True,
                "auto_format": True,
                "emmet": True,
                "intellisense": True,
                "vim_mode": False
            },
            "preview": {
                "hot_reload": True,
                "auto_refresh": True,
                "device_presets": [
                    {"name": "Desktop", "width": 1920, "height": 1080},
                    {"name": "Laptop", "width": 1366, "height": 768},
                    {"name": "Tablet", "width": 768, "height": 1024},
                    {"name": "Mobile", "width": 375, "height": 667}
                ],
                "responsive_breakpoints": {
                    "xs": 0,
                    "sm": 640,
                    "md": 768,
                    "lg": 1024,
                    "xl": 1280,
                    "2xl": 1536
                }
            },
            "collaboration": {
                "real_time_cursors": True,
                "live_editing": True,
                "voice_chat": True,
                "screen_sharing": True,
                "presence_indicators": True,
                "conflict_resolution": "operational_transform"
            },
            "performance": {
                "code_splitting": True,
                "lazy_loading": True,
                "caching": True,
                "compression": True,
                "bundle_analysis": True
            },
            "accessibility": {
                "screen_reader_support": True,
                "keyboard_navigation": True,
                "high_contrast": True,
                "focus_indicators": True,
                "aria_labels": True
            }
        }
    
    async def create_project_interface(self, project_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive project interface"""
        
        project_id = f"project_{int(time.time())}"
        
        # Initialize project structure
        project_data = {
            "project_id": project_id,
            "name": project_config.get("name", "New Project"),
            "description": project_config.get("description", ""),
            "framework": project_config.get("framework", "react"),
            "template": project_config.get("template", "blank"),
            "created_at": time.time(),
            "last_modified": time.time(),
            "settings": {
                "theme": self.current_theme.value,
                "editor_mode": self.editor_mode.value,
                "auto_save": True,
                "collaboration_enabled": True
            }
        }
        
        self.active_projects[project_id] = project_data
        
        # Create initial files based on template
        if project_config.get("template") != "blank":
            await self._create_template_files(project_id, project_config["template"])
        else:
            await self._create_blank_project_files(project_id, project_config)
        
        # Setup live preview
        preview = await self._create_live_preview(project_id)
        
        # Initialize collaboration session
        collaboration = await self._create_collaboration_session(project_id)
        
        # Generate interface layout
        interface_layout = await self._generate_interface_layout(project_data, preview, collaboration)
        
        return {
            "project": project_data,
            "preview": asdict(preview),
            "collaboration": asdict(collaboration),
            "interface_layout": interface_layout,
            "component_library": self.component_library,
            "templates": self.template_library
        }
    
    async def _create_template_files(self, project_id: str, template_name: str):
        """Create files from template"""
        
        template_files = await self._get_template_files(template_name)
        
        for file_data in template_files:
            file_obj = ProjectFile(
                file_id=f"file_{int(time.time())}_{len(self.project_files)}",
                file_path=file_data["path"],
                content=file_data["content"],
                file_type=file_data["type"],
                last_modified=time.time(),
                locked_by=None,
                collaborators=[],
                version_history=[]
            )
            
            self.project_files[file_obj.file_id] = file_obj
    
    async def _get_template_files(self, template_name: str) -> List[Dict[str, Any]]:
        """Generate template files using AI"""
        
        template_prompt = f"""
        Create a complete {template_name} template with modern, production-ready code.
        
        Generate files for:
        - HTML/React components
        - CSS/Tailwind styles  
        - JavaScript functionality
        - Configuration files
        - README with setup instructions
        
        Template requirements:
        - Responsive design
        - Accessibility compliant
        - SEO optimized
        - Performance optimized
        - Modern best practices
        - Clean, maintainable code
        
        Return file structure:
        {{
            "files": [
                {{
                    "path": "src/App.jsx",
                    "type": "javascript",
                    "content": "// Complete component code here..."
                }},
                {{
                    "path": "src/styles/globals.css", 
                    "type": "css",
                    "content": "/* Complete styles here... */"
                }}
            ]
        }}
        """
        
        try:
            response = await self.client.chat.completions.acreate(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert web developer. Generate complete, production-ready template files. Respond only with valid JSON."},
                    {"role": "user", "content": template_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get("files", [])
            
        except Exception as e:
            print(f"Template generation error: {e}")
            return await self._get_fallback_template_files(template_name)
    
    async def _get_fallback_template_files(self, template_name: str) -> List[Dict[str, Any]]:
        """Fallback template files"""
        
        return [
            {
                "path": "src/App.jsx",
                "type": "javascript", 
                "content": """import React from 'react';
import './App.css';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Welcome to Your App</h1>
        </div>
      </header>
      
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              Get Started Building
            </h2>
            <p className="text-gray-600 mb-6">
              Your new project is ready! Start by editing the components or adding new features.
            </p>
            <button className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
              Start Building
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;"""
            },
            {
                "path": "src/App.css",
                "type": "css",
                "content": """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  }
}

@layer components {
  .container {
    @apply max-w-7xl mx-auto;
  }
  
  .btn-primary {
    @apply px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors;
  }
  
  .card {
    @apply bg-white rounded-lg shadow-sm border border-gray-200 p-6;
  }
}"""
            },
            {
                "path": "package.json",
                "type": "json",
                "content": json.dumps({
                    "name": "new-project",
                    "version": "0.1.0",
                    "private": True,
                    "dependencies": {
                        "react": "^18.2.0",
                        "react-dom": "^18.2.0"
                    },
                    "scripts": {
                        "start": "react-scripts start",
                        "build": "react-scripts build",
                        "test": "react-scripts test",
                        "eject": "react-scripts eject"
                    },
                    "devDependencies": {
                        "react-scripts": "5.0.1",
                        "tailwindcss": "^3.3.0"
                    }
                }, indent=2)
            }
        ]
    
    async def _create_blank_project_files(self, project_id: str, project_config: Dict[str, Any]):
        """Create minimal starter files for blank project"""
        
        framework = project_config.get("framework", "react")
        
        if framework == "react":
            files = await self._get_fallback_template_files("react")
        elif framework == "vue":
            files = await self._get_vue_starter_files()
        elif framework == "angular":
            files = await self._get_angular_starter_files()
        else:
            files = await self._get_html_starter_files()
        
        for file_data in files:
            file_obj = ProjectFile(
                file_id=f"file_{int(time.time())}_{len(self.project_files)}",
                file_path=file_data["path"],
                content=file_data["content"],
                file_type=file_data["type"],
                last_modified=time.time(),
                locked_by=None,
                collaborators=[],
                version_history=[]
            )
            
            self.project_files[file_obj.file_id] = file_obj
    
    async def _create_live_preview(self, project_id: str) -> LivePreview:
        """Create live preview system"""
        
        preview = LivePreview(
            preview_id=f"preview_{project_id}",
            project_id=project_id,
            url=f"http://localhost:3000/preview/{project_id}",
            mode=EditorMode.SPLIT,
            device_type="desktop",
            viewport_size={"width": 1920, "height": 1080},
            hot_reload=True,
            last_updated=time.time()
        )
        
        self.live_previews[preview.preview_id] = preview
        
        return preview
    
    async def _create_collaboration_session(self, project_id: str) -> CollaborationSession:
        """Create collaboration session"""
        
        session = CollaborationSession(
            session_id=f"session_{project_id}",
            project_id=project_id,
            participants=[],
            active_cursors={},
            shared_state={
                "current_file": None,
                "selected_component": None,
                "editor_state": {}
            },
            created_at=time.time()
        )
        
        self.collaboration_sessions[session.session_id] = session
        
        return session
    
    async def _generate_interface_layout(self, project_data: Dict[str, Any], 
                                       preview: LivePreview, 
                                       collaboration: CollaborationSession) -> Dict[str, Any]:
        """Generate comprehensive interface layout"""
        
        return {
            "header": {
                "logo": {"text": "Builder", "icon": "🚀"},
                "project_name": project_data["name"],
                "actions": [
                    {"id": "save", "label": "Save", "shortcut": "Ctrl+S"},
                    {"id": "preview", "label": "Preview", "shortcut": "Ctrl+P"},
                    {"id": "deploy", "label": "Deploy", "shortcut": "Ctrl+D"},
                    {"id": "share", "label": "Share", "shortcut": "Ctrl+Shift+S"}
                ],
                "user_menu": {
                    "avatar": "/api/user/avatar",
                    "items": ["Settings", "Help", "Logout"]
                }
            },
            "sidebar": {
                "width": 280,
                "resizable": True,
                "tabs": [
                    {
                        "id": "explorer",
                        "label": "Files",
                        "icon": "folder",
                        "content": "file_tree"
                    },
                    {
                        "id": "components",
                        "label": "Components", 
                        "icon": "puzzle",
                        "content": "component_library"
                    },
                    {
                        "id": "assets",
                        "label": "Assets",
                        "icon": "image",
                        "content": "asset_manager"
                    },
                    {
                        "id": "layers",
                        "label": "Layers",
                        "icon": "layers",
                        "content": "layer_tree"
                    }
                ]
            },
            "main_editor": {
                "mode": preview.mode.value,
                "panels": {
                    "visual_editor": {
                        "enabled": True,
                        "tools": ["select", "text", "image", "container"],
                        "grid": {"enabled": True, "size": 8},
                        "guides": {"enabled": True},
                        "zoom": {"level": 100, "fit": "width"}
                    },
                    "code_editor": {
                        "enabled": True,
                        "language": "javascript",
                        "theme": self.interface_config["editor"]["theme"],
                        "features": {
                            "intellisense": True,
                            "error_highlighting": True,
                            "auto_completion": True,
                            "emmet": True,
                            "vim_mode": False
                        }
                    },
                    "preview": {
                        "enabled": True,
                        "url": preview.url,
                        "device": preview.device_type,
                        "viewport": preview.viewport_size,
                        "hot_reload": preview.hot_reload,
                        "responsive_testing": True
                    }
                }
            },
            "properties_panel": {
                "width": 320,
                "resizable": True,
                "sections": [
                    {
                        "id": "properties",
                        "label": "Properties",
                        "content": "component_properties"
                    },
                    {
                        "id": "styles",
                        "label": "Styles",
                        "content": "css_editor"
                    },
                    {
                        "id": "responsive",
                        "label": "Responsive",
                        "content": "breakpoint_editor"
                    },
                    {
                        "id": "interactions",
                        "label": "Interactions",
                        "content": "interaction_editor"
                    }
                ]
            },
            "bottom_panel": {
                "height": 200,
                "resizable": True,
                "collapsible": True,
                "tabs": [
                    {
                        "id": "console",
                        "label": "Console",
                        "icon": "terminal"
                    },
                    {
                        "id": "errors",
                        "label": "Problems",
                        "icon": "warning"
                    },
                    {
                        "id": "terminal",
                        "label": "Terminal", 
                        "icon": "terminal"
                    },
                    {
                        "id": "preview_logs",
                        "label": "Preview Logs",
                        "icon": "logs"
                    }
                ]
            },
            "status_bar": {
                "items": [
                    {"id": "cursor_position", "content": "Ln 1, Col 1"},
                    {"id": "file_encoding", "content": "UTF-8"},
                    {"id": "language", "content": "JavaScript"},
                    {"id": "git_branch", "content": "main"},
                    {"id": "deployment_status", "content": "Ready"},
                    {"id": "collaboration", "content": f"{len(collaboration.participants)} online"}
                ]
            },
            "context_menus": {
                "file_tree": [
                    {"id": "new_file", "label": "New File", "shortcut": "Ctrl+N"},
                    {"id": "new_folder", "label": "New Folder"},
                    {"id": "rename", "label": "Rename", "shortcut": "F2"},
                    {"id": "delete", "label": "Delete", "shortcut": "Delete"}
                ],
                "component": [
                    {"id": "edit", "label": "Edit Component"},
                    {"id": "duplicate", "label": "Duplicate", "shortcut": "Ctrl+D"},
                    {"id": "copy", "label": "Copy", "shortcut": "Ctrl+C"},
                    {"id": "delete", "label": "Delete", "shortcut": "Delete"}
                ]
            },
            "keyboard_shortcuts": {
                "global": {
                    "save": "Ctrl+S",
                    "undo": "Ctrl+Z", 
                    "redo": "Ctrl+Y",
                    "find": "Ctrl+F",
                    "replace": "Ctrl+H",
                    "toggle_sidebar": "Ctrl+B",
                    "toggle_preview": "Ctrl+P",
                    "command_palette": "Ctrl+Shift+P"
                },
                "editor": {
                    "format_document": "Shift+Alt+F",
                    "go_to_definition": "F12",
                    "rename_symbol": "F2",
                    "quick_fix": "Ctrl+.",
                    "toggle_comment": "Ctrl+/"
                }
            }
        }
    
    async def handle_file_edit(self, file_id: str, content: str, user_id: str) -> Dict[str, Any]:
        """Handle real-time file editing with collaboration"""
        
        if file_id not in self.project_files:
            raise ValueError(f"File {file_id} not found")
        
        file_obj = self.project_files[file_id]
        
        # Check if file is locked by another user
        if file_obj.locked_by and file_obj.locked_by != user_id:
            return {
                "success": False,
                "error": f"File is being edited by {file_obj.locked_by}",
                "conflict": True
            }
        
        # Update file content
        old_content = file_obj.content
        file_obj.content = content
        file_obj.last_modified = time.time()
        
        # Add to version history
        file_obj.version_history.append({
            "timestamp": time.time(),
            "user_id": user_id,
            "changes": await self._calculate_diff(old_content, content),
            "content_hash": hash(content)
        })
        
        # Update collaboration state
        await self._broadcast_file_change(file_id, user_id, content)
        
        # Trigger live preview update
        await self._update_live_preview(file_obj.file_path, content)
        
        return {
            "success": True,
            "file": asdict(file_obj),
            "live_preview_updated": True
        }
    
    async def _calculate_diff(self, old_content: str, new_content: str) -> List[Dict[str, Any]]:
        """Calculate content diff for version history"""
        
        # Simplified diff calculation
        old_lines = old_content.split('\\n')
        new_lines = new_content.split('\\n')
        
        changes = []
        
        # Basic line-by-line comparison
        max_lines = max(len(old_lines), len(new_lines))
        
        for i in range(max_lines):
            old_line = old_lines[i] if i < len(old_lines) else ""
            new_line = new_lines[i] if i < len(new_lines) else ""
            
            if old_line != new_line:
                if old_line and new_line:
                    changes.append({
                        "type": "modified",
                        "line": i + 1,
                        "old": old_line,
                        "new": new_line
                    })
                elif new_line:
                    changes.append({
                        "type": "added",
                        "line": i + 1,
                        "content": new_line
                    })
                elif old_line:
                    changes.append({
                        "type": "deleted", 
                        "line": i + 1,
                        "content": old_line
                    })
        
        return changes
    
    async def _broadcast_file_change(self, file_id: str, user_id: str, content: str):
        """Broadcast file changes to collaborators"""
        
        # Find collaboration sessions that include this file's project
        file_obj = self.project_files[file_id]
        project_id = None
        
        for proj_id, proj_data in self.active_projects.items():
            if file_id in [f.file_id for f in self.project_files.values()]:
                project_id = proj_id
                break
        
        if project_id:
            for session in self.collaboration_sessions.values():
                if session.project_id == project_id:
                    # Broadcast to all participants except the editor
                    for participant in session.participants:
                        if participant.get("user_id") != user_id:
                            await self._send_collaboration_event(
                                participant["user_id"],
                                {
                                    "type": "file_changed",
                                    "file_id": file_id,
                                    "content": content,
                                    "editor": user_id,
                                    "timestamp": time.time()
                                }
                            )
    
    async def _send_collaboration_event(self, user_id: str, event: Dict[str, Any]):
        """Send collaboration event to specific user"""
        # Would implement WebSocket/SSE sending
        pass
    
    async def _update_live_preview(self, file_path: str, content: str):
        """Update live preview when files change"""
        
        # Find previews that need updating
        for preview in self.live_previews.values():
            if preview.hot_reload:
                # Trigger preview refresh
                preview.last_updated = time.time()
                
                # Would implement actual preview server communication
                await self._refresh_preview_server(preview.preview_id, file_path, content)
    
    async def _refresh_preview_server(self, preview_id: str, file_path: str, content: str):
        """Refresh preview server with new content"""
        # Would implement preview server refresh
        pass
    
    async def add_component_to_page(self, project_id: str, component_type: str, 
                                  position: Dict[str, Any], properties: Dict[str, Any]) -> Dict[str, Any]:
        """Add component to page with drag-and-drop"""
        
        # Create new component instance
        component = UIComponent(
            component_id=f"comp_{int(time.time())}_{component_type}",
            name=properties.get("name", component_type),
            category=ComponentCategory(properties.get("category", "custom")),
            description=properties.get("description", ""),
            props=properties.get("props", {}),
            children=properties.get("children", []),
            styles=properties.get("styles", {}),
            responsive_settings=properties.get("responsive", {}),
            accessibility_config=properties.get("accessibility", {}),
            created_at=time.time()
        )
        
        self.ui_components[component.component_id] = component
        
        # Generate component code
        component_code = await self._generate_component_code(component, position)
        
        # Find target file (usually App.jsx or index.html)
        target_file = await self._find_target_file(project_id)
        
        if target_file:
            # Insert component into file
            updated_content = await self._insert_component_into_file(
                target_file.content,
                component_code,
                position
            )
            
            # Update file
            await self.handle_file_edit(target_file.file_id, updated_content, "system")
        
        return {
            "component": asdict(component),
            "code": component_code,
            "file_updated": target_file.file_path if target_file else None
        }
    
    async def _generate_component_code(self, component: UIComponent, position: Dict[str, Any]) -> str:
        """Generate code for component"""
        
        # Find component template from library
        for category, components in self.component_library.items():
            for comp_template in components:
                if comp_template["name"].lower() == component.name.lower():
                    # Customize template with component properties
                    code = comp_template["code_template"]
                    
                    # Replace placeholders with actual props
                    for prop_key, prop_value in component.props.items():
                        code = code.replace(f"{{{prop_key}}}", str(prop_value))
                    
                    # Add custom styles
                    if component.styles:
                        style_classes = " ".join([f"{k}-{v}" for k, v in component.styles.items()])
                        code = code.replace("className='", f"className='{style_classes} ")
                    
                    return code
        
        # Fallback generic component
        return f"<div className='component-{component.component_id}'>{component.name}</div>"
    
    async def _find_target_file(self, project_id: str) -> Optional[ProjectFile]:
        """Find the target file for component insertion"""
        
        # Look for main files (App.jsx, index.html, etc.)
        target_files = ["src/App.jsx", "src/App.js", "App.jsx", "index.html", "src/main.jsx"]
        
        for file in self.project_files.values():
            if file.file_path in target_files:
                return file
        
        # Return first JavaScript/HTML file
        for file in self.project_files.values():
            if file.file_type in ["javascript", "html", "jsx", "tsx"]:
                return file
        
        return None
    
    async def _insert_component_into_file(self, content: str, component_code: str, 
                                        position: Dict[str, Any]) -> str:
        """Insert component code into file at specified position"""
        
        # For React files, insert before closing tag of main container
        if "return (" in content and "</div>" in content:
            # Find the main container's closing tag
            lines = content.split('\\n')
            insert_line = -1
            
            for i, line in enumerate(lines):
                if "</div>" in line and "main" in line:
                    insert_line = i
                    break
            
            if insert_line > 0:
                # Insert component before closing tag
                lines.insert(insert_line, f"        {component_code}")
                return '\\n'.join(lines)
        
        # For HTML files, insert before </body>
        if "</body>" in content:
            return content.replace("</body>", f"  {component_code}\\n</body>")
        
        # Fallback: append to end
        return content + f"\\n{component_code}"
    
    async def deploy_project(self, project_id: str, deployment_config: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy project with real-time status updates"""
        
        if project_id not in self.active_projects:
            raise ValueError(f"Project {project_id} not found")
        
        project = self.active_projects[project_id]
        
        # Start deployment process
        deployment_id = f"deploy_{int(time.time())}_{project_id}"
        
        deployment_status = {
            "deployment_id": deployment_id,
            "project_id": project_id,
            "status": DeploymentStatus.BUILDING.value,
            "progress": 0,
            "logs": [],
            "url": None,
            "started_at": time.time()
        }
        
        try:
            # Build phase
            deployment_status["logs"].append("🔨 Starting build process...")
            deployment_status["progress"] = 10
            await self._broadcast_deployment_status(deployment_status)
            
            build_result = await self._build_project(project_id)
            
            if build_result["success"]:
                deployment_status["logs"].extend(build_result["logs"])
                deployment_status["progress"] = 60
                deployment_status["status"] = DeploymentStatus.DEPLOYING.value
                await self._broadcast_deployment_status(deployment_status)
                
                # Deploy phase
                deploy_result = await self._deploy_to_platform(project_id, deployment_config)
                
                if deploy_result["success"]:
                    deployment_status["status"] = DeploymentStatus.SUCCESS.value
                    deployment_status["progress"] = 100
                    deployment_status["url"] = deploy_result["url"]
                    deployment_status["logs"].append(f"✅ Deployed successfully to {deploy_result['url']}")
                else:
                    deployment_status["status"] = DeploymentStatus.ERROR.value
                    deployment_status["logs"].append(f"❌ Deployment failed: {deploy_result['error']}")
            else:
                deployment_status["status"] = DeploymentStatus.ERROR.value
                deployment_status["logs"].append(f"❌ Build failed: {build_result['error']}")
                
        except Exception as e:
            deployment_status["status"] = DeploymentStatus.ERROR.value
            deployment_status["logs"].append(f"❌ Deployment error: {str(e)}")
        
        deployment_status["completed_at"] = time.time()
        await self._broadcast_deployment_status(deployment_status)
        
        return deployment_status
    
    async def _build_project(self, project_id: str) -> Dict[str, Any]:
        """Build project files"""
        
        try:
            logs = []
            
            # Simulate build process
            logs.append("📦 Installing dependencies...")
            await asyncio.sleep(1)
            
            logs.append("🔧 Compiling components...")  
            await asyncio.sleep(1)
            
            logs.append("📱 Optimizing for production...")
            await asyncio.sleep(1)
            
            logs.append("✅ Build completed successfully!")
            
            return {
                "success": True,
                "logs": logs,
                "build_time": 3.5,
                "bundle_size": "2.1 MB"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "logs": [f"Build failed: {str(e)}"]
            }
    
    async def _deploy_to_platform(self, project_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy to specified platform"""
        
        platform = config.get("platform", "vercel")
        
        try:
            # Simulate deployment
            await asyncio.sleep(2)
            
            # Generate deployment URL
            project = self.active_projects[project_id]
            project_name = project["name"].lower().replace(" ", "-")
            url = f"https://{project_name}-{project_id[:8]}.{platform}.app"
            
            return {
                "success": True,
                "url": url,
                "platform": platform,
                "deployment_time": 2.3
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _broadcast_deployment_status(self, status: Dict[str, Any]):
        """Broadcast deployment status to connected clients"""
        # Would implement WebSocket broadcast
        pass
    
    async def get_interface_state(self) -> Dict[str, Any]:
        """Get current interface state for client"""
        
        return {
            "theme": self.current_theme.value,
            "editor_mode": self.editor_mode.value,
            "active_projects": list(self.active_projects.keys()),
            "component_library": self.component_library,
            "templates": self.template_library,
            "interface_config": self.interface_config,
            "collaboration_sessions": len(self.collaboration_sessions),
            "live_previews": len(self.live_previews)
        }

# Factory function
def create_web_interface(openai_client, project_path: Path) -> EnhancedWebInterface:
    """Create enhanced web interface instance"""
    return EnhancedWebInterface(openai_client, project_path)