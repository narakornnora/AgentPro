"""
🎨 Professional Design Templates - สร้าง Design Templates แบบมืออาชีพ
"""
import os
from typing import Dict, List, Any

class ProfessionalDesignTemplates:
    def __init__(self):
        self.design_systems = {
            "modern_minimal": {
                "name": "Modern Minimal",
                "description": "ดีไซน์มินิมอล ทันสมัย เรียบหรู",
                "color_schemes": {
                    "primary": "#2563eb",
                    "secondary": "#64748b", 
                    "accent": "#f59e0b",
                    "success": "#10b981",
                    "warning": "#f59e0b",
                    "error": "#ef4444",
                    "background": "#ffffff",
                    "surface": "#f8fafc",
                    "text": "#1e293b"
                },
                "typography": {
                    "heading_font": "Inter, system-ui, sans-serif",
                    "body_font": "Inter, system-ui, sans-serif",
                    "heading_weight": "600",
                    "body_weight": "400"
                },
                "spacing": {
                    "xs": "0.5rem",
                    "sm": "1rem", 
                    "md": "1.5rem",
                    "lg": "2rem",
                    "xl": "3rem"
                }
            },
            
            "elegant_corporate": {
                "name": "Elegant Corporate",
                "description": "ดีไซน์หรูหรา เหมาะสำหรับองค์กรขนาดใหญ่",
                "color_schemes": {
                    "primary": "#1e40af",
                    "secondary": "#374151",
                    "accent": "#d97706", 
                    "success": "#059669",
                    "warning": "#d97706",
                    "error": "#dc2626",
                    "background": "#ffffff",
                    "surface": "#f9fafb",
                    "text": "#111827"
                },
                "typography": {
                    "heading_font": "Playfair Display, serif",
                    "body_font": "Source Sans Pro, sans-serif",
                    "heading_weight": "700",
                    "body_weight": "400"
                },
                "spacing": {
                    "xs": "0.75rem",
                    "sm": "1.25rem",
                    "md": "2rem", 
                    "lg": "2.5rem",
                    "xl": "4rem"
                }
            },
            
            "vibrant_creative": {
                "name": "Vibrant Creative",
                "description": "ดีไซน์สีสันสดใส เหมาะสำหรับธุรกิจสร้างสรรค์",
                "color_schemes": {
                    "primary": "#7c3aed",
                    "secondary": "#ec4899",
                    "accent": "#06b6d4",
                    "success": "#22c55e", 
                    "warning": "#f59e0b",
                    "error": "#ef4444",
                    "background": "#ffffff",
                    "surface": "#fef7ff",
                    "text": "#1f2937"
                },
                "typography": {
                    "heading_font": "Poppins, sans-serif",
                    "body_font": "Open Sans, sans-serif", 
                    "heading_weight": "700",
                    "body_weight": "400"
                },
                "spacing": {
                    "xs": "0.5rem",
                    "sm": "1rem",
                    "md": "1.5rem",
                    "lg": "2.5rem", 
                    "xl": "3.5rem"
                }
            }
        }
        
        self.layout_patterns = {
            "hero_centered": self._generate_hero_centered_css(),
            "hero_split": self._generate_hero_split_css(), 
            "grid_showcase": self._generate_grid_showcase_css(),
            "card_layout": self._generate_card_layout_css(),
            "sidebar_layout": self._generate_sidebar_layout_css()
        }
        
        self.component_library = {
            "buttons": self._generate_button_components(),
            "cards": self._generate_card_components(),
            "navigation": self._generate_nav_components(),
            "forms": self._generate_form_components(),
            "modals": self._generate_modal_components()
        }
    
    def generate_template(self, business_type: str, design_style: str = "modern_minimal") -> Dict[str, Any]:
        """สร้าง design template สำหรับประเภทธุรกิจ"""
        
        # เลือก design system
        design_system = self.design_systems.get(design_style, self.design_systems["modern_minimal"])
        
        # เลือก layout patterns ตามประเภทธุรกิจ
        layouts = self._select_layouts_for_business(business_type)
        
        return {
            "business_type": business_type,
            "design_style": design_style,
            "design_system": design_system,
            "layouts": layouts,
            "components": self.component_library,
            "css_variables": self._generate_css_variables(design_system),
            "responsive_breakpoints": self._generate_responsive_breakpoints(),
            "css_framework": self._generate_complete_css(design_system, layouts),
            "js_interactions": self._generate_interaction_js()
        }
    
    def _select_layouts_for_business(self, business_type: str) -> List[str]:
        """เลือก layout patterns ที่เหมาะสมตามประเภทธุรกิจ"""
        business_layouts = {
            "coffee_shop": ["hero_centered", "grid_showcase", "card_layout"],
            "restaurant": ["hero_split", "grid_showcase", "card_layout"],
            "fashion_boutique": ["hero_centered", "grid_showcase", "sidebar_layout"],
            "business_corporate": ["hero_split", "card_layout", "sidebar_layout"],
            "ecommerce": ["hero_centered", "grid_showcase", "card_layout"]
        }
        
        return business_layouts.get(business_type, ["hero_centered", "card_layout"])
    
    def _generate_css_variables(self, design_system: Dict) -> str:
        """สร้าง CSS Variables จาก design system"""
        colors = design_system["color_schemes"]
        typography = design_system["typography"] 
        spacing = design_system["spacing"]
        
        css_vars = ":root {\n"
        
        # Colors
        for name, value in colors.items():
            css_vars += f"  --color-{name.replace('_', '-')}: {value};\n"
        
        # Typography
        css_vars += f"  --font-heading: {typography['heading_font']};\n"
        css_vars += f"  --font-body: {typography['body_font']};\n"
        css_vars += f"  --weight-heading: {typography['heading_weight']};\n" 
        css_vars += f"  --weight-body: {typography['body_weight']};\n"
        
        # Spacing
        for name, value in spacing.items():
            css_vars += f"  --spacing-{name}: {value};\n"
            
        css_vars += "}\n"
        return css_vars
    
    def _generate_responsive_breakpoints(self) -> Dict[str, str]:
        """สร้าง responsive breakpoints"""
        return {
            "mobile": "480px",
            "tablet": "768px", 
            "desktop": "1024px",
            "wide": "1280px"
        }
    
    def _generate_complete_css(self, design_system: Dict, layouts: List[str]) -> str:
        """สร้าง CSS ครบชุดสำหรับเว็บไซต์"""
        css = self._generate_css_variables(design_system) + "\n"
        
        # Reset & Base Styles
        css += self._generate_base_styles() + "\n"
        
        # Layout Styles
        for layout in layouts:
            if layout in self.layout_patterns:
                css += self.layout_patterns[layout] + "\n"
        
        # Component Styles
        for component_type, styles in self.component_library.items():
            css += styles + "\n"
        
        # Responsive Styles
        css += self._generate_responsive_styles() + "\n"
        
        return css
    
    def _generate_base_styles(self) -> str:
        """สร้าง base styles"""
        return """
/* Base Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: var(--font-body);
    font-weight: var(--weight-body);
    color: var(--color-text);
    background-color: var(--color-background);
    line-height: 1.6;
}

h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-heading);
    font-weight: var(--weight-heading);
    line-height: 1.2;
    margin-bottom: var(--spacing-sm);
}

p {
    margin-bottom: var(--spacing-sm);
}

img {
    max-width: 100%;
    height: auto;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-md);
}

.section {
    padding: var(--spacing-xl) 0;
}

.text-center {
    text-align: center;
}

.mb-0 { margin-bottom: 0; }
.mb-sm { margin-bottom: var(--spacing-sm); }
.mb-md { margin-bottom: var(--spacing-md); }
.mb-lg { margin-bottom: var(--spacing-lg); }

.mt-0 { margin-top: 0; }
.mt-sm { margin-top: var(--spacing-sm); }
.mt-md { margin-top: var(--spacing-md); }
.mt-lg { margin-top: var(--spacing-lg); }
"""
    
    def _generate_hero_centered_css(self) -> str:
        """Hero Section แบบกึ่งกลาง"""
        return """
/* Hero Centered Layout */
.hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
    color: white;
    position: relative;
}

.hero::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.3);
    z-index: 1;
}

.hero-content {
    position: relative;
    z-index: 2;
    max-width: 600px;
    padding: var(--spacing-xl);
}

.hero-title {
    font-size: 3.5rem;
    margin-bottom: var(--spacing-md);
    font-weight: var(--weight-heading);
}

.hero-subtitle {
    font-size: 1.25rem;
    margin-bottom: var(--spacing-lg);
    opacity: 0.9;
}

.hero-buttons {
    display: flex;
    gap: var(--spacing-md);
    justify-content: center;
    flex-wrap: wrap;
}
"""
    
    def _generate_hero_split_css(self) -> str:
        """Hero Section แบบแยกข้าง"""
        return """
/* Hero Split Layout */
.hero-split {
    min-height: 100vh;
    display: grid;
    grid-template-columns: 1fr 1fr;
    align-items: center;
}

.hero-content {
    padding: var(--spacing-xl);
}

.hero-image {
    height: 100vh;
    background-size: cover;
    background-position: center;
}

.hero-title {
    font-size: 3rem;
    margin-bottom: var(--spacing-md);
    color: var(--color-text);
}

.hero-subtitle {
    font-size: 1.125rem;
    margin-bottom: var(--spacing-lg);
    color: var(--color-secondary);
}

@media (max-width: 768px) {
    .hero-split {
        grid-template-columns: 1fr;
        min-height: auto;
    }
    
    .hero-image {
        height: 50vh;
        order: -1;
    }
}
"""
    
    def _generate_grid_showcase_css(self) -> str:
        """Grid Showcase Layout"""
        return """
/* Grid Showcase Layout */
.grid-showcase {
    padding: var(--spacing-xl) 0;
}

.showcase-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: var(--spacing-lg);
    margin-top: var(--spacing-lg);
}

.showcase-item {
    background: var(--color-surface);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.showcase-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.showcase-image {
    height: 200px;
    background-size: cover;
    background-position: center;
}

.showcase-content {
    padding: var(--spacing-md);
}

.showcase-title {
    font-size: 1.25rem;
    margin-bottom: var(--spacing-sm);
    color: var(--color-text);
}

.showcase-description {
    color: var(--color-secondary);
    font-size: 0.95rem;
}
"""
    
    def _generate_card_layout_css(self) -> str:
        """Card Layout CSS"""
        return """
/* Card Layout */
.cards-section {
    padding: var(--spacing-xl) 0;
    background: var(--color-surface);
}

.cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: var(--spacing-md);
}

.card {
    background: white;
    border-radius: 16px;
    padding: var(--spacing-lg);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
    border: 1px solid rgba(0, 0, 0, 0.05);
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.card-icon {
    width: 60px;
    height: 60px;
    background: var(--color-primary);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: var(--spacing-md);
    color: white;
    font-size: 1.5rem;
}

.card-title {
    font-size: 1.25rem;
    margin-bottom: var(--spacing-sm);
    color: var(--color-text);
}

.card-description {
    color: var(--color-secondary);
    line-height: 1.6;
}
"""
    
    def _generate_sidebar_layout_css(self) -> str:
        """Sidebar Layout CSS"""
        return """
/* Sidebar Layout */
.sidebar-layout {
    display: grid;
    grid-template-columns: 300px 1fr;
    gap: var(--spacing-lg);
    min-height: 100vh;
}

.sidebar {
    background: var(--color-surface);
    padding: var(--spacing-lg);
    border-right: 1px solid rgba(0, 0, 0, 0.1);
}

.main-content {
    padding: var(--spacing-lg);
}

.sidebar-menu {
    list-style: none;
}

.sidebar-menu li {
    margin-bottom: var(--spacing-sm);
}

.sidebar-menu a {
    display: block;
    padding: var(--spacing-sm);
    color: var(--color-text);
    text-decoration: none;
    border-radius: 8px;
    transition: background-color 0.2s ease;
}

.sidebar-menu a:hover,
.sidebar-menu a.active {
    background-color: var(--color-primary);
    color: white;
}

@media (max-width: 768px) {
    .sidebar-layout {
        grid-template-columns: 1fr;
    }
    
    .sidebar {
        order: 2;
    }
}
"""
    
    def _generate_button_components(self) -> str:
        """Button Components CSS"""
        return """
/* Button Components */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    font-weight: 500;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 0.95rem;
    line-height: 1.2;
}

.btn-primary {
    background: var(--color-primary);
    color: white;
}

.btn-primary:hover {
    background: color-mix(in srgb, var(--color-primary) 90%, black);
    transform: translateY(-1px);
}

.btn-secondary {
    background: transparent;
    color: var(--color-primary);
    border: 2px solid var(--color-primary);
}

.btn-secondary:hover {
    background: var(--color-primary);
    color: white;
}

.btn-accent {
    background: var(--color-accent);
    color: white;
}

.btn-large {
    padding: 16px 32px;
    font-size: 1.1rem;
}

.btn-small {
    padding: 8px 16px;
    font-size: 0.85rem;
}

.btn-rounded {
    border-radius: 50px;
}

.btn-icon {
    gap: 8px;
}
"""
    
    def _generate_card_components(self) -> str:
        """Card Components CSS"""
        return """
/* Card Components */
.feature-card {
    background: white;
    border-radius: 16px;
    padding: var(--spacing-lg);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.feature-icon {
    width: 70px;
    height: 70px;
    background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: var(--spacing-md);
    color: white;
    font-size: 1.75rem;
}

.feature-title {
    font-size: 1.5rem;
    margin-bottom: var(--spacing-sm);
    color: var(--color-text);
}

.feature-description {
    color: var(--color-secondary);
    flex-grow: 1;
    line-height: 1.6;
}

.product-card {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
}

.product-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.15);
}

.product-image {
    height: 250px;
    background-size: cover;
    background-position: center;
    position: relative;
}

.product-badge {
    position: absolute;
    top: 12px;
    right: 12px;
    background: var(--color-accent);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
}

.product-content {
    padding: var(--spacing-md);
}

.product-title {
    font-size: 1.25rem;
    margin-bottom: var(--spacing-xs);
}

.product-price {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--color-primary);
    margin-bottom: var(--spacing-sm);
}

.product-description {
    color: var(--color-secondary);
    font-size: 0.9rem;
    margin-bottom: var(--spacing-md);
}
"""
    
    def _generate_nav_components(self) -> str:
        """Navigation Components CSS"""
        return """
/* Navigation Components */
.navbar {
    background: white;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    position: sticky;
    top: 0;
    z-index: 100;
}

.nav-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-md) var(--spacing-md);
    max-width: 1200px;
    margin: 0 auto;
}

.nav-logo h2 {
    color: var(--color-primary);
    margin: 0;
    font-size: 1.5rem;
}

.nav-menu {
    display: flex;
    list-style: none;
    gap: var(--spacing-lg);
    margin: 0;
}

.nav-menu a {
    color: var(--color-text);
    text-decoration: none;
    font-weight: 500;
    padding: 8px 16px;
    border-radius: 6px;
    transition: all 0.2s ease;
}

.nav-menu a:hover,
.nav-menu a.active {
    background: var(--color-primary);
    color: white;
}

.hamburger {
    display: none;
    flex-direction: column;
    cursor: pointer;
    gap: 4px;
}

.hamburger span {
    width: 25px;
    height: 3px;
    background: var(--color-text);
    transition: all 0.3s ease;
}

@media (max-width: 768px) {
    .nav-menu {
        position: fixed;
        top: 70px;
        left: -100%;
        width: 100%;
        background: white;
        flex-direction: column;
        padding: var(--spacing-md);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        transition: left 0.3s ease;
    }
    
    .nav-menu.active {
        left: 0;
    }
    
    .hamburger {
        display: flex;
    }
}
"""
    
    def _generate_form_components(self) -> str:
        """Form Components CSS"""
        return """
/* Form Components */
.form-group {
    margin-bottom: var(--spacing-md);
}

.form-label {
    display: block;
    margin-bottom: var(--spacing-xs);
    font-weight: 500;
    color: var(--color-text);
}

.form-input,
.form-textarea,
.form-select {
    width: 100%;
    padding: 12px 16px;
    border: 2px solid #e5e7eb;
    border-radius: 8px;
    font-size: 1rem;
    transition: all 0.2s ease;
    background: white;
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
    outline: none;
    border-color: var(--color-primary);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.form-textarea {
    resize: vertical;
    min-height: 120px;
}

.form-checkbox,
.form-radio {
    margin-right: var(--spacing-xs);
}

.checkbox-label,
.radio-label {
    display: flex;
    align-items: center;
    cursor: pointer;
    margin-bottom: var(--spacing-sm);
}

.form-error {
    color: var(--color-error);
    font-size: 0.875rem;
    margin-top: 4px;
}

.form-success {
    color: var(--color-success);
    font-size: 0.875rem;
    margin-top: 4px;
}

.form-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: var(--spacing-md);
}
"""
    
    def _generate_modal_components(self) -> str:
        """Modal Components CSS"""
        return """
/* Modal Components */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
}

.modal-overlay.active {
    opacity: 1;
    visibility: visible;
}

.modal {
    background: white;
    border-radius: 16px;
    max-width: 500px;
    width: 90%;
    max-height: 90vh;
    overflow-y: auto;
    transform: scale(0.9);
    transition: transform 0.3s ease;
}

.modal-overlay.active .modal {
    transform: scale(1);
}

.modal-header {
    padding: var(--spacing-lg);
    border-bottom: 1px solid #e5e7eb;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.modal-title {
    margin: 0;
    font-size: 1.5rem;
    color: var(--color-text);
}

.modal-close {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: var(--color-secondary);
    padding: 4px;
}

.modal-body {
    padding: var(--spacing-lg);
}

.modal-footer {
    padding: var(--spacing-lg);
    border-top: 1px solid #e5e7eb;
    display: flex;
    gap: var(--spacing-sm);
    justify-content: flex-end;
}
"""
    
    def _generate_responsive_styles(self) -> str:
        """Responsive Styles"""
        return """
/* Responsive Styles */
@media (max-width: 1024px) {
    .container {
        padding: 0 var(--spacing-sm);
    }
    
    .hero-title {
        font-size: 2.5rem;
    }
    
    .cards-grid {
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    }
}

@media (max-width: 768px) {
    .hero-title {
        font-size: 2rem;
    }
    
    .hero-buttons {
        flex-direction: column;
        align-items: center;
    }
    
    .showcase-grid {
        grid-template-columns: 1fr;
    }
    
    .cards-grid {
        grid-template-columns: 1fr;
    }
    
    .section {
        padding: var(--spacing-lg) 0;
    }
}

@media (max-width: 480px) {
    .hero-title {
        font-size: 1.75rem;
    }
    
    .hero-content {
        padding: var(--spacing-md);
    }
    
    .btn {
        width: 100%;
        justify-content: center;
    }
}
"""
    
    def _generate_interaction_js(self) -> str:
        """JavaScript สำหรับ interactions"""
        return """
// Professional Design Template Interactions
class DesignInteractions {
    constructor() {
        this.init();
    }
    
    init() {
        this.setupNavigation();
        this.setupModals();
        this.setupForms();
        this.setupAnimations();
    }
    
    setupNavigation() {
        // Mobile menu toggle
        const hamburger = document.querySelector('.hamburger');
        const navMenu = document.querySelector('.nav-menu');
        
        hamburger?.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            hamburger.classList.toggle('active');
        });
        
        // Smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
    
    setupModals() {
        // Modal functionality
        const modalTriggers = document.querySelectorAll('[data-modal]');
        const modalOverlays = document.querySelectorAll('.modal-overlay');
        const modalCloses = document.querySelectorAll('.modal-close');
        
        modalTriggers.forEach(trigger => {
            trigger.addEventListener('click', () => {
                const modalId = trigger.dataset.modal;
                const modal = document.getElementById(modalId);
                modal?.classList.add('active');
            });
        });
        
        modalCloses.forEach(close => {
            close.addEventListener('click', () => {
                close.closest('.modal-overlay').classList.remove('active');
            });
        });
        
        modalOverlays.forEach(overlay => {
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) {
                    overlay.classList.remove('active');
                }
            });
        });
    }
    
    setupForms() {
        // Form validation and enhancement
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, textarea, select');
            
            inputs.forEach(input => {
                // Real-time validation
                input.addEventListener('blur', () => {
                    this.validateField(input);
                });
                
                // Clear errors on input
                input.addEventListener('input', () => {
                    this.clearFieldError(input);
                });
            });
        });
    }
    
    validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let errorMessage = '';
        
        // Required validation
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            errorMessage = 'กรุณากรอกข้อมูลนี้';
        }
        
        // Email validation
        if (field.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                errorMessage = 'รูปแบบอีเมลไม่ถูกต้อง';
            }
        }
        
        // Phone validation
        if (field.type === 'tel' && value) {
            const phoneRegex = /^[0-9]{10}$/;
            if (!phoneRegex.test(value.replace(/[-\s]/g, ''))) {
                isValid = false;
                errorMessage = 'รูปแบบเบอร์โทรไม่ถูกต้อง';
            }
        }
        
        this.showFieldValidation(field, isValid, errorMessage);
        return isValid;
    }
    
    showFieldValidation(field, isValid, errorMessage) {
        const errorElement = field.parentNode.querySelector('.form-error');
        
        if (errorElement) {
            errorElement.remove();
        }
        
        if (!isValid) {
            const error = document.createElement('div');
            error.className = 'form-error';
            error.textContent = errorMessage;
            field.parentNode.appendChild(error);
            field.style.borderColor = 'var(--color-error)';
        } else {
            field.style.borderColor = 'var(--color-success)';
        }
    }
    
    clearFieldError(field) {
        const errorElement = field.parentNode.querySelector('.form-error');
        if (errorElement) {
            errorElement.remove();
        }
        field.style.borderColor = '#e5e7eb';
    }
    
    setupAnimations() {
        // Intersection Observer for animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);
        
        // Observe elements for animation
        document.querySelectorAll('.card, .feature-card, .showcase-item').forEach(el => {
            observer.observe(el);
        });
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new DesignInteractions();
});

// Animation CSS (add to CSS)
/*
.card, .feature-card, .showcase-item {
    opacity: 0;
    transform: translateY(30px);
    transition: all 0.6s ease;
}

.card.animate-in, .feature-card.animate-in, .showcase-item.animate-in {
    opacity: 1;
    transform: translateY(0);
}
*/
"""

# สร้าง instance
professional_templates = ProfessionalDesignTemplates()

if __name__ == "__main__":
    # ทดสอบการสร้าง template
    business_types = ["coffee_shop", "restaurant", "fashion_boutique", "business_corporate"]
    design_styles = ["modern_minimal", "elegant_corporate", "vibrant_creative"]
    
    for business_type in business_types:
        for design_style in design_styles:
            print(f"\n🎨 {business_type} - {design_style}")
            print("=" * 60)
            
            template = professional_templates.generate_template(business_type, design_style)
            print(f"🎯 Business: {template['business_type']}")
            print(f"🎨 Style: {template['design_style']}")
            print(f"📐 Layouts: {len(template['layouts'])}")
            print(f"🧩 Components: {len(template['components'])}")
            print(f"📱 Responsive: Yes")
            
            # แสดงตัวอย่าง color scheme
            colors = template['design_system']['color_schemes']
            print(f"🎨 Colors: {colors['primary']}, {colors['secondary']}, {colors['accent']}")
            break  # แสดงเฉพาะ style แรกของแต่ละ business