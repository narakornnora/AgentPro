"""
AI-Powered UI/UX Design System
สำหรับการสร้าง UI/UX อัตโนมัติที่สวยงามและใช้งานได้จริง
เทียบเท่าหรือดีกว่า Lovable ในด้านการออกแบบ
"""

import json
import asyncio
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum
import colorsys
import math

class DesignStyle(Enum):
    MODERN_MINIMAL = "modern_minimal"
    GLASSMORPHISM = "glassmorphism"
    NEUMORPHISM = "neumorphism"
    MATERIAL_DESIGN = "material_design"
    BRUTALIST = "brutalist"
    GRADIENT_COSMIC = "gradient_cosmic"
    DARK_MODE_PRO = "dark_mode_pro"
    RETRO_FUTURISTIC = "retro_futuristic"

class ComponentType(Enum):
    BUTTON = "button"
    CARD = "card"
    MODAL = "modal"
    NAVIGATION = "navigation"
    FORM = "form"
    HERO_SECTION = "hero_section"
    FEATURE_GRID = "feature_grid"
    TESTIMONIAL = "testimonial"
    PRICING = "pricing"
    FOOTER = "footer"

class AnimationType(Enum):
    FADE_IN = "fade_in"
    SLIDE_UP = "slide_up"
    SCALE_IN = "scale_in"
    BOUNCE = "bounce"
    PARALLAX = "parallax"
    MORPHING = "morphing"
    PARTICLE_EFFECT = "particle_effect"
    LIQUID_MOTION = "liquid_motion"

@dataclass
class ColorPalette:
    name: str
    primary: str
    secondary: str
    accent: str
    neutral: str
    background: str
    surface: str
    text_primary: str
    text_secondary: str
    success: str
    warning: str
    error: str
    gradients: List[str]

@dataclass
class Typography:
    font_family: str
    font_weights: List[int]
    font_sizes: Dict[str, str]
    line_heights: Dict[str, str]
    letter_spacing: Dict[str, str]

@dataclass
class Spacing:
    scale: str  # "linear", "geometric", "custom"
    base_unit: int
    values: Dict[str, str]

@dataclass
class ComponentDesign:
    component_type: ComponentType
    style: DesignStyle
    html_structure: str
    css_styles: str
    javascript_behavior: Optional[str]
    accessibility_features: List[str]
    responsive_breakpoints: Dict[str, str]
    animations: List[AnimationType]
    micro_interactions: List[str]

@dataclass
class DesignSystem:
    name: str
    style: DesignStyle
    colors: ColorPalette
    typography: Typography
    spacing: Spacing
    components: List[ComponentDesign]
    layout_patterns: List[str]
    design_tokens: Dict[str, Any]

class AIDesignEngine:
    """AI engine สำหรับการสร้าง UI/UX อัตโนมัติ"""
    
    def __init__(self, openai_client):
        self.client = openai_client
        
        # Pre-defined design systems
        self.design_systems = self._initialize_design_systems()
        self.color_harmonies = self._initialize_color_harmonies()
        self.component_templates = self._initialize_component_templates()
        self.animation_libraries = self._initialize_animation_libraries()
        
    def _initialize_design_systems(self) -> Dict[str, DesignSystem]:
        """Initialize pre-built design systems"""
        
        return {
            "modern_minimal": DesignSystem(
                name="Modern Minimal",
                style=DesignStyle.MODERN_MINIMAL,
                colors=ColorPalette(
                    name="Clean Minimal",
                    primary="#000000",
                    secondary="#666666",
                    accent="#0070f3",
                    neutral="#f5f5f5",
                    background="#ffffff",
                    surface="#fafafa",
                    text_primary="#000000",
                    text_secondary="#666666",
                    success="#00d084",
                    warning="#f5a623",
                    error="#e60000",
                    gradients=["linear-gradient(135deg, #667eea 0%, #764ba2 100%)"]
                ),
                typography=Typography(
                    font_family="'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
                    font_weights=[400, 500, 600, 700],
                    font_sizes={
                        "xs": "0.75rem",
                        "sm": "0.875rem", 
                        "base": "1rem",
                        "lg": "1.125rem",
                        "xl": "1.25rem",
                        "2xl": "1.5rem",
                        "3xl": "1.875rem",
                        "4xl": "2.25rem"
                    },
                    line_heights={
                        "tight": "1.25",
                        "normal": "1.5",
                        "relaxed": "1.75"
                    },
                    letter_spacing={
                        "tight": "-0.025em",
                        "normal": "0",
                        "wide": "0.025em"
                    }
                ),
                spacing=Spacing(
                    scale="geometric",
                    base_unit=4,
                    values={
                        "0": "0",
                        "1": "0.25rem",
                        "2": "0.5rem",
                        "3": "0.75rem",
                        "4": "1rem",
                        "6": "1.5rem",
                        "8": "2rem",
                        "12": "3rem",
                        "16": "4rem",
                        "24": "6rem"
                    }
                ),
                components=[],
                layout_patterns=["container_max_width", "grid_system", "flexbox_utils"],
                design_tokens={}
            ),
            
            "glassmorphism": DesignSystem(
                name="Glassmorphism",
                style=DesignStyle.GLASSMORPHISM,
                colors=ColorPalette(
                    name="Glass Effect",
                    primary="#ffffff",
                    secondary="rgba(255, 255, 255, 0.25)",
                    accent="#6366f1",
                    neutral="rgba(255, 255, 255, 0.1)",
                    background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    surface="rgba(255, 255, 255, 0.15)",
                    text_primary="#ffffff",
                    text_secondary="rgba(255, 255, 255, 0.8)",
                    success="#10b981",
                    warning="#f59e0b",
                    error="#ef4444",
                    gradients=[
                        "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
                        "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
                    ]
                ),
                typography=Typography(
                    font_family="'Poppins', -apple-system, BlinkMacSystemFont, sans-serif",
                    font_weights=[300, 400, 500, 600, 700],
                    font_sizes={
                        "xs": "0.75rem",
                        "sm": "0.875rem",
                        "base": "1rem", 
                        "lg": "1.125rem",
                        "xl": "1.25rem",
                        "2xl": "1.5rem",
                        "3xl": "1.875rem",
                        "4xl": "2.25rem"
                    },
                    line_heights={"tight": "1.25", "normal": "1.5", "relaxed": "1.75"},
                    letter_spacing={"tight": "-0.025em", "normal": "0", "wide": "0.025em"}
                ),
                spacing=Spacing(
                    scale="geometric",
                    base_unit=4,
                    values={
                        "0": "0", "1": "0.25rem", "2": "0.5rem", "3": "0.75rem",
                        "4": "1rem", "6": "1.5rem", "8": "2rem", "12": "3rem", "16": "4rem"
                    }
                ),
                components=[],
                layout_patterns=["blur_backgrounds", "transparent_overlays", "frosted_glass"],
                design_tokens={
                    "blur": "backdrop-filter: blur(10px)",
                    "glass_border": "border: 1px solid rgba(255, 255, 255, 0.18)",
                    "glass_shadow": "box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37)"
                }
            )
        }
    
    def _initialize_color_harmonies(self) -> Dict[str, Any]:
        """Initialize color harmony algorithms"""
        
        return {
            "complementary": self._complementary_colors,
            "triadic": self._triadic_colors,
            "analogous": self._analogous_colors,
            "split_complementary": self._split_complementary_colors,
            "tetradic": self._tetradic_colors
        }
    
    def _initialize_component_templates(self) -> Dict[ComponentType, Dict[str, str]]:
        """Initialize component templates for different styles"""
        
        return {
            ComponentType.BUTTON: {
                "modern_minimal": """
                <button class="btn btn-primary">
                    <span class="btn-content">{text}</span>
                </button>
                """,
                "glassmorphism": """
                <button class="btn-glass">
                    <span class="btn-text">{text}</span>
                    <div class="btn-glow"></div>
                </button>
                """
            },
            ComponentType.CARD: {
                "modern_minimal": """
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">{title}</h3>
                    </div>
                    <div class="card-content">
                        {content}
                    </div>
                </div>
                """,
                "glassmorphism": """
                <div class="glass-card">
                    <div class="glass-card-header">
                        <h3 class="glass-card-title">{title}</h3>
                    </div>
                    <div class="glass-card-content">
                        {content}
                    </div>
                </div>
                """
            }
        }
    
    def _initialize_animation_libraries(self) -> Dict[str, Dict[str, str]]:
        """Initialize animation libraries"""
        
        return {
            "css_animations": {
                "fadeIn": """
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(20px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                .fade-in { animation: fadeIn 0.6s ease-out forwards; }
                """,
                "slideUp": """
                @keyframes slideUp {
                    from { transform: translateY(100%); }
                    to { transform: translateY(0); }
                }
                .slide-up { animation: slideUp 0.5s ease-out forwards; }
                """,
                "scaleIn": """
                @keyframes scaleIn {
                    from { transform: scale(0.8); opacity: 0; }
                    to { transform: scale(1); opacity: 1; }
                }
                .scale-in { animation: scaleIn 0.4s ease-out forwards; }
                """
            },
            "framer_motion": {
                "fadeIn": """
                const fadeInVariants = {
                    initial: { opacity: 0, y: 20 },
                    animate: { opacity: 1, y: 0 },
                    transition: { duration: 0.6, ease: "easeOut" }
                };
                """,
                "slideUp": """
                const slideUpVariants = {
                    initial: { y: "100%" },
                    animate: { y: 0 },
                    transition: { duration: 0.5, ease: "easeOut" }
                };
                """
            }
        }
    
    async def generate_intelligent_design(self, requirements: str, preferences: Dict[str, Any]) -> DesignSystem:
        """Generate intelligent design system based on requirements"""
        
        # AI analysis of design requirements
        design_analysis = await self._analyze_design_requirements(requirements, preferences)
        
        # Select optimal design style
        optimal_style = await self._select_optimal_style(design_analysis)
        
        # Generate color palette
        color_palette = await self._generate_intelligent_colors(design_analysis, optimal_style)
        
        # Generate typography
        typography = await self._generate_intelligent_typography(design_analysis, optimal_style)
        
        # Generate spacing system
        spacing = await self._generate_intelligent_spacing(design_analysis)
        
        # Generate components
        components = await self._generate_intelligent_components(design_analysis, optimal_style)
        
        # Create complete design system
        design_system = DesignSystem(
            name=f"AI Generated {optimal_style.value.title()}",
            style=optimal_style,
            colors=color_palette,
            typography=typography,
            spacing=spacing,
            components=components,
            layout_patterns=await self._generate_layout_patterns(design_analysis),
            design_tokens=await self._generate_design_tokens(optimal_style, color_palette)
        )
        
        return design_system
    
    async def _analyze_design_requirements(self, requirements: str, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """AI analysis of design requirements"""
        
        analysis_prompt = f"""
        Analyze the following design requirements and preferences to create an optimal UI/UX design:
        
        Requirements: "{requirements}"
        Preferences: {json.dumps(preferences, indent=2)}
        
        Analyze and provide insights on:
        1. Target audience and user behavior
        2. Brand personality and tone
        3. Industry conventions and expectations
        4. Accessibility requirements
        5. Device and platform considerations
        6. Color psychology and emotional impact
        7. Typography mood and readability
        8. Layout patterns and user flow
        9. Animation and interaction style
        10. Performance and technical constraints
        
        Return detailed JSON analysis:
        {{
            "target_audience": {{
                "demographics": "description",
                "tech_savviness": "beginner|intermediate|advanced",
                "device_preferences": ["desktop", "mobile", "tablet"],
                "accessibility_needs": ["screen_readers", "high_contrast", "large_text"]
            }},
            "brand_personality": {{
                "tone": "professional|playful|elegant|modern|traditional",
                "values": ["trustworthy", "innovative", "accessible"],
                "industry": "tech|healthcare|finance|creative|ecommerce",
                "competitive_position": "premium|affordable|innovative"
            }},
            "design_direction": {{
                "style_preference": "modern_minimal|glassmorphism|material_design|brutalist",
                "color_mood": "calm|energetic|trustworthy|creative|professional",
                "layout_complexity": "simple|moderate|complex",
                "animation_level": "minimal|moderate|rich",
                "content_density": "sparse|balanced|dense"
            }},
            "technical_requirements": {{
                "performance_priority": "high|medium|low",
                "browser_support": ["modern", "legacy"],
                "framework_preference": "react|vue|vanilla",
                "responsive_strategy": "mobile_first|desktop_first|adaptive"
            }},
            "accessibility_level": "basic|aa|aaa",
            "innovation_factor": 1-10
        }}
        """
        
        try:
            response = await self.client.chat.completions.acreate(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert UI/UX designer and design system architect. Respond only with valid JSON."},
                    {"role": "user", "content": analysis_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Design analysis error: {e}")
            # Fallback analysis
            return {
                "target_audience": {
                    "demographics": "general users",
                    "tech_savviness": "intermediate",
                    "device_preferences": ["desktop", "mobile"],
                    "accessibility_needs": ["screen_readers"]
                },
                "brand_personality": {
                    "tone": "modern",
                    "values": ["innovative", "accessible"],
                    "industry": "tech"
                },
                "design_direction": {
                    "style_preference": "modern_minimal",
                    "color_mood": "professional",
                    "layout_complexity": "moderate",
                    "animation_level": "moderate"
                },
                "technical_requirements": {
                    "performance_priority": "high",
                    "browser_support": ["modern"],
                    "framework_preference": "react"
                },
                "accessibility_level": "aa",
                "innovation_factor": 7
            }
    
    async def _select_optimal_style(self, analysis: Dict[str, Any]) -> DesignStyle:
        """Select optimal design style based on analysis"""
        
        style_preference = analysis.get("design_direction", {}).get("style_preference", "modern_minimal")
        
        # Map preferences to design styles
        style_mapping = {
            "modern_minimal": DesignStyle.MODERN_MINIMAL,
            "glassmorphism": DesignStyle.GLASSMORPHISM,
            "material_design": DesignStyle.MATERIAL_DESIGN,
            "neumorphism": DesignStyle.NEUMORPHISM,
            "brutalist": DesignStyle.BRUTALIST,
            "gradient_cosmic": DesignStyle.GRADIENT_COSMIC,
            "dark_mode_pro": DesignStyle.DARK_MODE_PRO,
            "retro_futuristic": DesignStyle.RETRO_FUTURISTIC
        }
        
        return style_mapping.get(style_preference, DesignStyle.MODERN_MINIMAL)
    
    async def _generate_intelligent_colors(self, analysis: Dict[str, Any], style: DesignStyle) -> ColorPalette:
        """Generate intelligent color palette using AI and color theory"""
        
        color_mood = analysis.get("design_direction", {}).get("color_mood", "professional")
        industry = analysis.get("brand_personality", {}).get("industry", "tech")
        
        # Generate base color using AI
        color_prompt = f"""
        Generate a professional color palette for a {industry} application with {color_mood} mood.
        
        Requirements:
        - Style: {style.value}
        - Mood: {color_mood}
        - Industry: {industry}
        - Accessibility: WCAG AA compliant
        - Modern and appealing
        
        Return hex colors only:
        {{
            "primary": "#hexcolor",
            "secondary": "#hexcolor", 
            "accent": "#hexcolor",
            "neutral": "#hexcolor",
            "background": "#hexcolor",
            "surface": "#hexcolor",
            "text_primary": "#hexcolor",
            "text_secondary": "#hexcolor",
            "success": "#hexcolor",
            "warning": "#hexcolor",
            "error": "#hexcolor"
        }}
        """
        
        try:
            response = await self.client.chat.completions.acreate(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a color theory expert. Generate accessible, beautiful color palettes. Respond only with valid JSON."},
                    {"role": "user", "content": color_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.4
            )
            
            colors = json.loads(response.choices[0].message.content)
            
            # Generate gradients based on primary colors
            gradients = self._generate_gradients(colors["primary"], colors["secondary"], colors["accent"])
            
            return ColorPalette(
                name=f"AI {color_mood.title()} Palette",
                primary=colors["primary"],
                secondary=colors["secondary"],
                accent=colors["accent"],
                neutral=colors["neutral"],
                background=colors["background"],
                surface=colors["surface"],
                text_primary=colors["text_primary"],
                text_secondary=colors["text_secondary"],
                success=colors["success"],
                warning=colors["warning"],
                error=colors["error"],
                gradients=gradients
            )
            
        except Exception as e:
            print(f"Color generation error: {e}")
            # Fallback to modern minimal palette
            return self.design_systems["modern_minimal"].colors
    
    def _generate_gradients(self, primary: str, secondary: str, accent: str) -> List[str]:
        """Generate beautiful gradients from color palette"""
        
        return [
            f"linear-gradient(135deg, {primary} 0%, {secondary} 100%)",
            f"linear-gradient(45deg, {primary} 0%, {accent} 100%)",
            f"linear-gradient(180deg, {secondary} 0%, {accent} 100%)",
            f"radial-gradient(circle, {primary} 0%, {secondary} 100%)"
        ]
    
    async def _generate_intelligent_typography(self, analysis: Dict[str, Any], style: DesignStyle) -> Typography:
        """Generate intelligent typography system"""
        
        tone = analysis.get("brand_personality", {}).get("tone", "modern")
        readability_priority = analysis.get("accessibility_level", "aa")
        
        # Font selection based on style and tone
        font_families = {
            DesignStyle.MODERN_MINIMAL: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
            DesignStyle.GLASSMORPHISM: "'Poppins', -apple-system, BlinkMacSystemFont, sans-serif",
            DesignStyle.MATERIAL_DESIGN: "'Roboto', -apple-system, BlinkMacSystemFont, sans-serif",
            DesignStyle.NEUMORPHISM: "'Nunito', -apple-system, BlinkMacSystemFont, sans-serif",
            DesignStyle.BRUTALIST: "'JetBrains Mono', 'Courier New', monospace"
        }
        
        return Typography(
            font_family=font_families.get(style, "'Inter', sans-serif"),
            font_weights=[300, 400, 500, 600, 700, 800],
            font_sizes={
                "xs": "0.75rem",   # 12px
                "sm": "0.875rem",  # 14px
                "base": "1rem",    # 16px
                "lg": "1.125rem",  # 18px
                "xl": "1.25rem",   # 20px
                "2xl": "1.5rem",   # 24px
                "3xl": "1.875rem", # 30px
                "4xl": "2.25rem",  # 36px
                "5xl": "3rem",     # 48px
                "6xl": "3.75rem"   # 60px
            },
            line_heights={
                "tight": "1.25",
                "snug": "1.375", 
                "normal": "1.5",
                "relaxed": "1.625",
                "loose": "2"
            },
            letter_spacing={
                "tighter": "-0.05em",
                "tight": "-0.025em",
                "normal": "0",
                "wide": "0.025em",
                "wider": "0.05em",
                "widest": "0.1em"
            }
        )
    
    async def _generate_intelligent_spacing(self, analysis: Dict[str, Any]) -> Spacing:
        """Generate intelligent spacing system"""
        
        layout_complexity = analysis.get("design_direction", {}).get("layout_complexity", "moderate")
        
        # Adjust spacing based on complexity
        if layout_complexity == "simple":
            base_unit = 8
        elif layout_complexity == "complex":
            base_unit = 4
        else:  # moderate
            base_unit = 6
        
        return Spacing(
            scale="geometric",
            base_unit=base_unit,
            values={
                "0": "0",
                "px": "1px",
                "0.5": f"{base_unit * 0.5 / 4}rem",
                "1": f"{base_unit * 1 / 4}rem",
                "1.5": f"{base_unit * 1.5 / 4}rem",
                "2": f"{base_unit * 2 / 4}rem",
                "2.5": f"{base_unit * 2.5 / 4}rem",
                "3": f"{base_unit * 3 / 4}rem",
                "3.5": f"{base_unit * 3.5 / 4}rem",
                "4": f"{base_unit * 4 / 4}rem",
                "5": f"{base_unit * 5 / 4}rem",
                "6": f"{base_unit * 6 / 4}rem",
                "7": f"{base_unit * 7 / 4}rem",
                "8": f"{base_unit * 8 / 4}rem",
                "9": f"{base_unit * 9 / 4}rem",
                "10": f"{base_unit * 10 / 4}rem",
                "12": f"{base_unit * 12 / 4}rem",
                "14": f"{base_unit * 14 / 4}rem",
                "16": f"{base_unit * 16 / 4}rem",
                "20": f"{base_unit * 20 / 4}rem",
                "24": f"{base_unit * 24 / 4}rem",
                "28": f"{base_unit * 28 / 4}rem",
                "32": f"{base_unit * 32 / 4}rem"
            }
        )
    
    async def _generate_intelligent_components(self, analysis: Dict[str, Any], style: DesignStyle) -> List[ComponentDesign]:
        """Generate intelligent component designs"""
        
        components = []
        
        # Generate button component
        button_design = await self._generate_button_component(analysis, style)
        components.append(button_design)
        
        # Generate card component
        card_design = await self._generate_card_component(analysis, style)
        components.append(card_design)
        
        # Generate navigation component
        nav_design = await self._generate_navigation_component(analysis, style)
        components.append(nav_design)
        
        # Generate form component
        form_design = await self._generate_form_component(analysis, style)
        components.append(form_design)
        
        # Generate hero section
        hero_design = await self._generate_hero_component(analysis, style)
        components.append(hero_design)
        
        return components
    
    async def _generate_button_component(self, analysis: Dict[str, Any], style: DesignStyle) -> ComponentDesign:
        """Generate intelligent button component"""
        
        if style == DesignStyle.GLASSMORPHISM:
            html = """
            <button class="btn-glass" type="button">
                <span class="btn-content">{text}</span>
                <div class="btn-backdrop"></div>
            </button>
            """
            
            css = """
            .btn-glass {
                position: relative;
                padding: 12px 24px;
                border: 1px solid rgba(255, 255, 255, 0.18);
                border-radius: 12px;
                background: rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(10px);
                color: white;
                font-weight: 500;
                cursor: pointer;
                overflow: hidden;
                transition: all 0.3s ease;
            }
            
            .btn-glass:hover {
                background: rgba(255, 255, 255, 0.25);
                transform: translateY(-2px);
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            }
            
            .btn-content {
                position: relative;
                z-index: 2;
            }
            
            .btn-backdrop {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(45deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .btn-glass:hover .btn-backdrop {
                opacity: 1;
            }
            """
        
        else:  # Default modern minimal
            html = """
            <button class="btn btn-primary" type="button">
                <span class="btn-text">{text}</span>
            </button>
            """
            
            css = """
            .btn {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                font-weight: 500;
                font-size: 1rem;
                line-height: 1.5;
                cursor: pointer;
                transition: all 0.2s ease;
                text-decoration: none;
            }
            
            .btn-primary {
                background: #0070f3;
                color: white;
            }
            
            .btn-primary:hover {
                background: #0051cc;
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(0, 112, 243, 0.4);
            }
            
            .btn:focus {
                outline: 2px solid #0070f3;
                outline-offset: 2px;
            }
            """
        
        return ComponentDesign(
            component_type=ComponentType.BUTTON,
            style=style,
            html_structure=html,
            css_styles=css,
            javascript_behavior=None,
            accessibility_features=["keyboard_navigation", "focus_indicators", "screen_reader_support"],
            responsive_breakpoints={
                "mobile": "padding: 10px 20px; font-size: 0.875rem;",
                "tablet": "padding: 12px 24px; font-size: 1rem;",
                "desktop": "padding: 12px 24px; font-size: 1rem;"
            },
            animations=[AnimationType.FADE_IN, AnimationType.SCALE_IN],
            micro_interactions=["hover_lift", "click_ripple", "focus_glow"]
        )
    
    # Color harmony functions
    def _complementary_colors(self, base_color: str) -> List[str]:
        """Generate complementary color harmony"""
        # Implementation for complementary colors
        return [base_color, "#opposite_color"]
    
    def _triadic_colors(self, base_color: str) -> List[str]:
        """Generate triadic color harmony"""
        # Implementation for triadic colors
        return [base_color, "#triadic1", "#triadic2"]
    
    def _analogous_colors(self, base_color: str) -> List[str]:
        """Generate analogous color harmony"""
        # Implementation for analogous colors
        return [base_color, "#analogous1", "#analogous2"]
    
    def _split_complementary_colors(self, base_color: str) -> List[str]:
        """Generate split complementary harmony"""
        # Implementation for split complementary colors
        return [base_color, "#split1", "#split2"]
    
    def _tetradic_colors(self, base_color: str) -> List[str]:
        """Generate tetradic color harmony"""
        # Implementation for tetradic colors
        return [base_color, "#tetradic1", "#tetradic2", "#tetradic3"]
    
    async def _generate_layout_patterns(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate layout patterns based on analysis"""
        
        return [
            "responsive_grid",
            "flexbox_layouts", 
            "container_queries",
            "css_grid_areas",
            "sticky_navigation",
            "hero_sections",
            "card_layouts",
            "sidebar_layouts"
        ]
    
    async def _generate_design_tokens(self, style: DesignStyle, colors: ColorPalette) -> Dict[str, Any]:
        """Generate design tokens for the system"""
        
        return {
            "colors": asdict(colors),
            "shadows": {
                "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
                "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1)",
                "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1)"
            },
            "borders": {
                "radius": {
                    "sm": "4px",
                    "md": "8px", 
                    "lg": "12px",
                    "xl": "16px",
                    "full": "9999px"
                }
            },
            "transitions": {
                "fast": "0.15s ease",
                "normal": "0.3s ease",
                "slow": "0.5s ease"
            }
        }

# Factory function
def create_ai_design_engine(openai_client) -> AIDesignEngine:
    """Create AI design engine instance"""
    return AIDesignEngine(openai_client)