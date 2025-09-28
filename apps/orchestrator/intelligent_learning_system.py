"""
Intelligent Learning System
AI system that learns from user interactions, remembers preferences, 
adapts to coding patterns, and provides personalized app generation experiences.
"""

import asyncio
import json
import pickle
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import sqlite3
import hashlib
from collections import defaultdict, Counter
import re
import time

@dataclass
class UserInteraction:
    """Records user interaction data"""
    user_id: str
    session_id: str
    interaction_type: str  # 'app_request', 'modification', 'preference', 'feedback'
    timestamp: datetime
    data: Dict[str, Any]
    context: Dict[str, Any]

@dataclass
class UserProfile:
    """Comprehensive user profile with preferences and patterns"""
    user_id: str
    preferences: Dict[str, Any]
    coding_patterns: Dict[str, Any]
    app_history: List[Dict[str, Any]]
    interaction_stats: Dict[str, int]
    learning_weights: Dict[str, float]
    last_updated: datetime

@dataclass
class LearningInsight:
    """AI-generated insights about user behavior"""
    insight_type: str
    confidence: float
    description: str
    suggested_action: str
    evidence: List[str]
    created_at: datetime

class UserBehaviorAnalyzer:
    """Analyzes user behavior patterns and preferences"""
    
    def __init__(self):
        self.pattern_weights = {
            'app_type_preference': 1.0,
            'ui_style_preference': 0.8,
            'feature_preference': 0.9,
            'complexity_preference': 0.7,
            'technology_preference': 0.6,
            'color_scheme_preference': 0.5,
            'layout_preference': 0.8,
            'interaction_pattern': 0.9
        }

    async def analyze_user_patterns(self, interactions: List[UserInteraction]) -> Dict[str, Any]:
        """Analyze user behavior patterns from interactions"""
        patterns = {
            'app_types': self._analyze_app_type_patterns(interactions),
            'ui_preferences': self._analyze_ui_preferences(interactions),
            'feature_preferences': self._analyze_feature_preferences(interactions),
            'timing_patterns': self._analyze_timing_patterns(interactions),
            'modification_patterns': self._analyze_modification_patterns(interactions),
            'complexity_preferences': self._analyze_complexity_preferences(interactions),
            'technology_stack_preferences': self._analyze_tech_preferences(interactions)
        }
        
        return patterns

    def _analyze_app_type_patterns(self, interactions: List[UserInteraction]) -> Dict[str, float]:
        """Analyze preferred app types"""
        app_type_counts = Counter()
        
        for interaction in interactions:
            if interaction.interaction_type == 'app_request':
                app_type = interaction.data.get('app_type', 'unknown')
                app_type_counts[app_type] += 1
        
        total = sum(app_type_counts.values())
        if total == 0:
            return {}
        
        return {app_type: count/total for app_type, count in app_type_counts.items()}

    def _analyze_ui_preferences(self, interactions: List[UserInteraction]) -> Dict[str, Any]:
        """Analyze UI/UX preferences from modifications and feedback"""
        ui_prefs = {
            'color_schemes': defaultdict(int),
            'layout_types': defaultdict(int),
            'component_preferences': defaultdict(int),
            'design_styles': defaultdict(int)
        }
        
        for interaction in interactions:
            if interaction.interaction_type == 'modification':
                # Extract UI-related modifications
                mod_data = interaction.data
                if 'color' in str(mod_data).lower():
                    ui_prefs['color_schemes']['custom'] += 1
                if 'layout' in str(mod_data).lower():
                    ui_prefs['layout_types']['custom'] += 1
        
        return dict(ui_prefs)

    def _analyze_feature_preferences(self, interactions: List[UserInteraction]) -> Dict[str, float]:
        """Analyze preferred features and functionalities"""
        feature_mentions = defaultdict(int)
        
        for interaction in interactions:
            text_data = str(interaction.data).lower()
            
            # Common features to look for
            features = [
                'authentication', 'database', 'api', 'search', 'chat', 'payment',
                'notification', 'social', 'analytics', 'admin', 'mobile', 'responsive',
                'dashboard', 'reporting', 'export', 'import', 'security'
            ]
            
            for feature in features:
                if feature in text_data:
                    feature_mentions[feature] += 1
        
        total = sum(feature_mentions.values())
        if total == 0:
            return {}
        
        return {feature: count/total for feature, count in feature_mentions.items()}

    def _analyze_timing_patterns(self, interactions: List[UserInteraction]) -> Dict[str, Any]:
        """Analyze when user is most active and productive"""
        hourly_activity = defaultdict(int)
        daily_activity = defaultdict(int)
        session_durations = []
        
        sessions = defaultdict(list)
        for interaction in interactions:
            sessions[interaction.session_id].append(interaction.timestamp)
        
        for session_times in sessions.values():
            if len(session_times) > 1:
                duration = (max(session_times) - min(session_times)).total_seconds() / 60
                session_durations.append(duration)
        
        for interaction in interactions:
            hour = interaction.timestamp.hour
            day = interaction.timestamp.strftime('%A')
            hourly_activity[hour] += 1
            daily_activity[day] += 1
        
        return {
            'peak_hours': dict(hourly_activity),
            'peak_days': dict(daily_activity),
            'avg_session_duration': np.mean(session_durations) if session_durations else 0,
            'session_count': len(sessions)
        }

    def _analyze_modification_patterns(self, interactions: List[UserInteraction]) -> Dict[str, Any]:
        """Analyze how users typically modify generated apps"""
        modification_types = defaultdict(int)
        modification_frequency = 0
        
        for interaction in interactions:
            if interaction.interaction_type == 'modification':
                modification_frequency += 1
                
                # Categorize modification types
                mod_text = str(interaction.data).lower()
                if any(word in mod_text for word in ['color', 'style', 'design']):
                    modification_types['visual'] += 1
                elif any(word in mod_text for word in ['function', 'feature', 'logic']):
                    modification_types['functional'] += 1
                elif any(word in mod_text for word in ['text', 'content', 'copy']):
                    modification_types['content'] += 1
                elif any(word in mod_text for word in ['layout', 'position', 'arrange']):
                    modification_types['layout'] += 1
        
        total_requests = len([i for i in interactions if i.interaction_type == 'app_request'])
        avg_modifications = modification_frequency / max(1, total_requests)
        
        return {
            'modification_types': dict(modification_types),
            'average_modifications_per_app': avg_modifications,
            'modification_frequency': modification_frequency
        }

    def _analyze_complexity_preferences(self, interactions: List[UserInteraction]) -> Dict[str, float]:
        """Analyze preferred complexity levels"""
        complexity_indicators = {
            'simple': ['simple', 'basic', 'minimal', 'clean'],
            'moderate': ['standard', 'normal', 'typical', 'regular'],
            'complex': ['advanced', 'complex', 'sophisticated', 'comprehensive', 'full-featured']
        }
        
        complexity_scores = defaultdict(int)
        
        for interaction in interactions:
            text_data = str(interaction.data).lower()
            
            for level, keywords in complexity_indicators.items():
                for keyword in keywords:
                    if keyword in text_data:
                        complexity_scores[level] += 1
        
        total = sum(complexity_scores.values())
        if total == 0:
            return {'moderate': 1.0}  # Default to moderate
        
        return {level: score/total for level, score in complexity_scores.items()}

    def _analyze_tech_preferences(self, interactions: List[UserInteraction]) -> Dict[str, float]:
        """Analyze technology stack preferences"""
        tech_mentions = defaultdict(int)
        
        technologies = [
            'react', 'vue', 'angular', 'javascript', 'typescript', 'python',
            'node.js', 'express', 'django', 'flask', 'mongodb', 'mysql',
            'postgresql', 'redis', 'docker', 'aws', 'firebase', 'bootstrap',
            'tailwind', 'scss', 'sass', 'webpack', 'vite'
        ]
        
        for interaction in interactions:
            text_data = str(interaction.data).lower()
            
            for tech in technologies:
                if tech in text_data:
                    tech_mentions[tech] += 1
        
        total = sum(tech_mentions.values())
        if total == 0:
            return {}
        
        return {tech: count/total for tech, count in tech_mentions.items()}

class PersonalizationEngine:
    """Provides personalized recommendations and adaptations"""
    
    def __init__(self):
        self.recommendation_weights = {
            'recent_preferences': 1.5,
            'frequent_patterns': 1.0,
            'seasonal_trends': 0.3,
            'similar_users': 0.7,
            'global_trends': 0.2
        }

    async def generate_personalized_suggestions(self, user_profile: UserProfile, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate personalized suggestions based on user profile"""
        suggestions = []
        
        # App type suggestions
        app_type_suggestions = self._suggest_app_types(user_profile, context)
        suggestions.extend(app_type_suggestions)
        
        # Feature suggestions
        feature_suggestions = self._suggest_features(user_profile, context)
        suggestions.extend(feature_suggestions)
        
        # UI/UX suggestions
        ui_suggestions = self._suggest_ui_elements(user_profile, context)
        suggestions.extend(ui_suggestions)
        
        # Technology stack suggestions
        tech_suggestions = self._suggest_tech_stack(user_profile, context)
        suggestions.extend(tech_suggestions)
        
        # Workflow suggestions
        workflow_suggestions = self._suggest_workflow_improvements(user_profile, context)
        suggestions.extend(workflow_suggestions)
        
        # Sort by relevance score
        suggestions.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return suggestions[:10]  # Return top 10 suggestions

    def _suggest_app_types(self, user_profile: UserProfile, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest app types based on user patterns"""
        suggestions = []
        app_patterns = user_profile.coding_patterns.get('app_types', {})
        
        # Suggest most used app types
        for app_type, frequency in app_patterns.items():
            if frequency > 0.2:  # Used more than 20% of the time
                suggestions.append({
                    'type': 'app_type',
                    'suggestion': f"Based on your history, you might want to create another {app_type}",
                    'action': f"suggest_app_type:{app_type}",
                    'relevance_score': frequency * 0.8,
                    'reasoning': f"You've created {app_type} apps {frequency:.1%} of the time"
                })
        
        # Suggest complementary app types
        if 'website' in app_patterns and app_patterns['website'] > 0.3:
            suggestions.append({
                'type': 'app_type',
                'suggestion': "Consider creating a mobile app to complement your websites",
                'action': "suggest_app_type:mobile_app",
                'relevance_score': 0.6,
                'reasoning': "Mobile apps often complement websites well"
            })
        
        return suggestions

    def _suggest_features(self, user_profile: UserProfile, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest features based on user preferences"""
        suggestions = []
        feature_prefs = user_profile.coding_patterns.get('feature_preferences', {})
        
        for feature, frequency in feature_prefs.items():
            if frequency > 0.1:  # Mentioned more than 10% of the time
                suggestions.append({
                    'type': 'feature',
                    'suggestion': f"Consider adding {feature} functionality",
                    'action': f"suggest_feature:{feature}",
                    'relevance_score': frequency * 0.7,
                    'reasoning': f"You frequently use {feature} features ({frequency:.1%})"
                })
        
        return suggestions

    def _suggest_ui_elements(self, user_profile: UserProfile, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest UI/UX elements based on preferences"""
        suggestions = []
        ui_prefs = user_profile.coding_patterns.get('ui_preferences', {})
        
        # Suggest based on modification patterns
        mod_patterns = user_profile.coding_patterns.get('modification_patterns', {})
        if mod_patterns.get('average_modifications_per_app', 0) > 3:
            suggestions.append({
                'type': 'ui_improvement',
                'suggestion': "Pre-configure UI elements based on your typical modifications",
                'action': "auto_configure_ui",
                'relevance_score': 0.8,
                'reasoning': f"You typically make {mod_patterns['average_modifications_per_app']:.1f} modifications per app"
            })
        
        return suggestions

    def _suggest_tech_stack(self, user_profile: UserProfile, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest technology stack based on preferences"""
        suggestions = []
        tech_prefs = user_profile.coding_patterns.get('technology_stack_preferences', {})
        
        for tech, frequency in tech_prefs.items():
            if frequency > 0.15:
                suggestions.append({
                    'type': 'technology',
                    'suggestion': f"Use {tech} as it matches your preferences",
                    'action': f"suggest_tech:{tech}",
                    'relevance_score': frequency * 0.6,
                    'reasoning': f"You've shown preference for {tech} ({frequency:.1%})"
                })
        
        return suggestions

    def _suggest_workflow_improvements(self, user_profile: UserProfile, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest workflow improvements"""
        suggestions = []
        timing_patterns = user_profile.coding_patterns.get('timing_patterns', {})
        
        # Suggest optimal working times
        peak_hours = timing_patterns.get('peak_hours', {})
        if peak_hours:
            best_hour = max(peak_hours, key=peak_hours.get)
            suggestions.append({
                'type': 'workflow',
                'suggestion': f"Your most productive time appears to be around {best_hour}:00",
                'action': f"suggest_schedule:{best_hour}",
                'relevance_score': 0.4,
                'reasoning': f"You're most active at {best_hour}:00 based on your history"
            })
        
        return suggestions

class AdaptiveCodeGenerator:
    """Generates code that adapts to user preferences and patterns"""
    
    def __init__(self):
        self.adaptation_strategies = {
            'template_selection': self._select_adaptive_template,
            'feature_integration': self._integrate_preferred_features,
            'ui_customization': self._apply_ui_preferences,
            'code_style': self._adapt_code_style,
            'architecture_pattern': self._select_architecture_pattern
        }

    async def generate_adaptive_code(self, requirements: str, user_profile: UserProfile, app_type: str) -> Dict[str, Any]:
        """Generate code adapted to user preferences"""
        
        # Base code generation
        base_code = await self._generate_base_code(requirements, app_type)
        
        # Apply adaptations
        adapted_code = base_code.copy()
        
        for strategy_name, strategy_func in self.adaptation_strategies.items():
            try:
                adapted_code = await strategy_func(adapted_code, user_profile, requirements)
            except Exception as e:
                print(f"Adaptation strategy {strategy_name} failed: {e}")
                # Continue with other strategies
        
        # Add personalization metadata
        adapted_code['personalization_applied'] = {
            'user_id': user_profile.user_id,
            'adaptations': list(self.adaptation_strategies.keys()),
            'confidence_score': self._calculate_adaptation_confidence(user_profile),
            'timestamp': datetime.now().isoformat()
        }
        
        return adapted_code

    async def _generate_base_code(self, requirements: str, app_type: str) -> Dict[str, str]:
        """Generate base code structure"""
        # This would integrate with existing code generation systems
        # For now, return a basic structure
        
        base_templates = {
            'website': {
                'html': self._get_website_html_template(requirements),
                'css': self._get_website_css_template(),
                'js': self._get_website_js_template()
            },
            'web_app': {
                'html': self._get_webapp_html_template(requirements),
                'css': self._get_webapp_css_template(),
                'js': self._get_webapp_js_template()
            },
            'mobile_app': {
                'html': self._get_mobile_html_template(requirements),
                'css': self._get_mobile_css_template(),
                'js': self._get_mobile_js_template()
            }
        }
        
        return base_templates.get(app_type, base_templates['website'])

    async def _select_adaptive_template(self, code: Dict[str, str], user_profile: UserProfile, requirements: str) -> Dict[str, str]:
        """Select template based on user preferences"""
        complexity_prefs = user_profile.coding_patterns.get('complexity_preferences', {})
        
        # Adjust template complexity
        if complexity_prefs.get('simple', 0) > 0.5:
            # Use simpler templates
            code['css'] = self._simplify_css(code['css'])
            code['js'] = self._simplify_js(code['js'])
        elif complexity_prefs.get('complex', 0) > 0.5:
            # Add more advanced features
            code['js'] = self._enhance_js(code['js'])
            code['css'] = self._enhance_css(code['css'])
        
        return code

    async def _integrate_preferred_features(self, code: Dict[str, str], user_profile: UserProfile, requirements: str) -> Dict[str, str]:
        """Integrate frequently used features"""
        feature_prefs = user_profile.coding_patterns.get('feature_preferences', {})
        
        # Add authentication if frequently used
        if feature_prefs.get('authentication', 0) > 0.3:
            code['html'] = self._add_auth_components(code['html'])
            code['js'] = self._add_auth_logic(code['js'])
        
        # Add search if frequently used
        if feature_prefs.get('search', 0) > 0.25:
            code['html'] = self._add_search_components(code['html'])
            code['js'] = self._add_search_logic(code['js'])
        
        return code

    async def _apply_ui_preferences(self, code: Dict[str, str], user_profile: UserProfile, requirements: str) -> Dict[str, str]:
        """Apply UI preferences from user history"""
        ui_prefs = user_profile.coding_patterns.get('ui_preferences', {})
        
        # Apply color scheme preferences
        color_schemes = ui_prefs.get('color_schemes', {})
        if color_schemes:
            code['css'] = self._apply_preferred_colors(code['css'], color_schemes)
        
        # Apply layout preferences
        layout_prefs = ui_prefs.get('layout_types', {})
        if layout_prefs:
            code['css'] = self._apply_preferred_layout(code['css'], layout_prefs)
        
        return code

    async def _adapt_code_style(self, code: Dict[str, str], user_profile: UserProfile, requirements: str) -> Dict[str, str]:
        """Adapt code style to user preferences"""
        # This could adapt naming conventions, indentation, etc.
        # For now, apply basic style preferences
        
        modification_patterns = user_profile.coding_patterns.get('modification_patterns', {})
        
        # If user frequently modifies styling, add more CSS classes
        if modification_patterns.get('modification_types', {}).get('visual', 0) > 3:
            code['css'] = self._add_utility_classes(code['css'])
        
        return code

    async def _select_architecture_pattern(self, code: Dict[str, str], user_profile: UserProfile, requirements: str) -> Dict[str, str]:
        """Select architecture pattern based on user history"""
        tech_prefs = user_profile.coding_patterns.get('technology_stack_preferences', {})
        
        # If user prefers React-like patterns, structure accordingly
        if tech_prefs.get('react', 0) > 0.2:
            code['js'] = self._apply_component_pattern(code['js'])
        
        return code

    def _calculate_adaptation_confidence(self, user_profile: UserProfile) -> float:
        """Calculate confidence in applied adaptations"""
        interactions_count = len(user_profile.app_history)
        
        if interactions_count < 3:
            return 0.3  # Low confidence
        elif interactions_count < 10:
            return 0.6  # Medium confidence
        else:
            return 0.9  # High confidence

    # Template helper methods (simplified versions)
    def _get_website_html_template(self, requirements: str) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Website</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header class="site-header">
        <nav class="main-nav">
            <h1>My Website</h1>
            <!-- Navigation will be added based on requirements -->
        </nav>
    </header>
    <main class="main-content">
        <section class="hero-section">
            <h2>Welcome</h2>
            <p>Based on: {requirements}</p>
        </section>
    </main>
    <footer class="site-footer">
        <p>&copy; 2024 Generated Website</p>
    </footer>
    <script src="script.js"></script>
</body>
</html>"""

    def _get_website_css_template(self) -> str:
        return """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: #333;
}

.site-header {
    background: #2c3e50;
    color: white;
    padding: 1rem 0;
}

.main-nav {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}

.main-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

.hero-section {
    text-align: center;
    padding: 3rem 0;
}

.site-footer {
    background: #34495e;
    color: white;
    text-align: center;
    padding: 2rem 0;
}"""

    def _get_website_js_template(self) -> str:
        return """document.addEventListener('DOMContentLoaded', function() {
    console.log('Website loaded successfully');
    
    // Basic interactivity
    const header = document.querySelector('.site-header');
    if (header) {
        header.addEventListener('click', function() {
            console.log('Header clicked');
        });
    }
});"""

    # Simplified adaptation methods
    def _simplify_css(self, css: str) -> str:
        # Remove complex animations and effects
        return css.replace('@keyframes', '/* @keyframes')
    
    def _simplify_js(self, js: str) -> str:
        # Keep only essential functionality
        return js
    
    def _enhance_css(self, css: str) -> str:
        # Add advanced CSS features
        enhanced = css + "\n\n/* Enhanced animations */\n"
        enhanced += "@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }\n"
        enhanced += ".fade-in { animation: fadeIn 0.5s ease-in; }"
        return enhanced
    
    def _enhance_js(self, js: str) -> str:
        # Add advanced JavaScript features
        enhanced = js + "\n\n// Enhanced functionality\n"
        enhanced += "// Add intersection observer for animations\n"
        enhanced += "const observer = new IntersectionObserver((entries) => {\n"
        enhanced += "    entries.forEach(entry => {\n"
        enhanced += "        if (entry.isIntersecting) {\n"
        enhanced += "            entry.target.classList.add('fade-in');\n"
        enhanced += "        }\n"
        enhanced += "    });\n"
        enhanced += "});\n"
        return enhanced
    
    def _add_auth_components(self, html: str) -> str:
        auth_html = """
    <div class="auth-section">
        <button id="login-btn">Login</button>
        <button id="signup-btn">Sign Up</button>
    </div>"""
        return html.replace('</nav>', auth_html + '</nav>')
    
    def _add_auth_logic(self, js: str) -> str:
        auth_js = """
// Authentication functionality
document.getElementById('login-btn')?.addEventListener('click', function() {
    console.log('Login clicked');
    // Add login logic
});

document.getElementById('signup-btn')?.addEventListener('click', function() {
    console.log('Sign up clicked');
    // Add signup logic
});"""
        return js + "\n" + auth_js
    
    def _add_search_components(self, html: str) -> str:
        search_html = """
    <div class="search-section">
        <input type="text" id="search-input" placeholder="Search...">
        <button id="search-btn">Search</button>
    </div>"""
        return html.replace('</nav>', search_html + '</nav>')
    
    def _add_search_logic(self, js: str) -> str:
        search_js = """
// Search functionality
document.getElementById('search-btn')?.addEventListener('click', function() {
    const query = document.getElementById('search-input').value;
    console.log('Search query:', query);
    // Add search logic
});"""
        return js + "\n" + search_js
    
    def _apply_preferred_colors(self, css: str, color_prefs: Dict) -> str:
        # Apply user's preferred colors
        if 'dark' in color_prefs:
            css += "\n/* Dark theme preferences */\nbody { background: #1a1a1a; color: #fff; }"
        return css
    
    def _apply_preferred_layout(self, css: str, layout_prefs: Dict) -> str:
        # Apply layout preferences
        if 'grid' in layout_prefs:
            css += "\n/* Grid layout preferences */\n.main-content { display: grid; gap: 2rem; }"
        return css
    
    def _add_utility_classes(self, css: str) -> str:
        utilities = """
/* Utility classes for easy customization */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }
.mt-1 { margin-top: 1rem; }
.mt-2 { margin-top: 2rem; }
.mb-1 { margin-bottom: 1rem; }
.mb-2 { margin-bottom: 2rem; }
.p-1 { padding: 1rem; }
.p-2 { padding: 2rem; }"""
        return css + "\n" + utilities
    
    def _apply_component_pattern(self, js: str) -> str:
        component_js = """
// Component-like pattern
class Component {
    constructor(element) {
        this.element = element;
        this.init();
    }
    
    init() {
        console.log('Component initialized');
    }
}"""
        return component_js + "\n" + js

class IntelligentLearningSystem:
    """Main intelligent learning system"""
    
    def __init__(self, db_path: str = "learning_system.db"):
        self.db_path = db_path
        self.behavior_analyzer = UserBehaviorAnalyzer()
        self.personalization_engine = PersonalizationEngine()
        self.adaptive_generator = AdaptiveCodeGenerator()
        
        self.user_profiles = {}
        self.global_insights = []
        
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database for storing learning data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            session_id TEXT NOT NULL,
            interaction_type TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            data TEXT NOT NULL,
            context TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id TEXT PRIMARY KEY,
            preferences TEXT NOT NULL,
            coding_patterns TEXT NOT NULL,
            app_history TEXT NOT NULL,
            interaction_stats TEXT NOT NULL,
            learning_weights TEXT NOT NULL,
            last_updated DATETIME NOT NULL
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS learning_insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            insight_type TEXT NOT NULL,
            confidence REAL NOT NULL,
            description TEXT NOT NULL,
            suggested_action TEXT NOT NULL,
            evidence TEXT NOT NULL,
            created_at DATETIME NOT NULL
        )
        ''')
        
        conn.commit()
        conn.close()

    async def record_interaction(self, user_id: str, session_id: str, interaction_type: str, 
                               data: Dict[str, Any], context: Dict[str, Any] = None):
        """Record user interaction for learning"""
        interaction = UserInteraction(
            user_id=user_id,
            session_id=session_id,
            interaction_type=interaction_type,
            timestamp=datetime.now(),
            data=data,
            context=context or {}
        )
        
        # Store in database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO user_interactions (user_id, session_id, interaction_type, timestamp, data, context)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            interaction.user_id,
            interaction.session_id,
            interaction.interaction_type,
            interaction.timestamp.isoformat(),
            json.dumps(interaction.data),
            json.dumps(interaction.context)
        ))
        
        conn.commit()
        conn.close()
        
        # Update user profile asynchronously
        await self._update_user_profile(user_id)

    async def _update_user_profile(self, user_id: str):
        """Update user profile based on recent interactions"""
        # Load user interactions
        interactions = await self._load_user_interactions(user_id)
        
        if not interactions:
            return
        
        # Analyze patterns
        patterns = await self.behavior_analyzer.analyze_user_patterns(interactions)
        
        # Update or create profile
        if user_id in self.user_profiles:
            profile = self.user_profiles[user_id]
            profile.coding_patterns.update(patterns)
            profile.last_updated = datetime.now()
        else:
            profile = UserProfile(
                user_id=user_id,
                preferences={},
                coding_patterns=patterns,
                app_history=[],
                interaction_stats={},
                learning_weights={},
                last_updated=datetime.now()
            )
            self.user_profiles[user_id] = profile
        
        # Save to database
        await self._save_user_profile(profile)

    async def _load_user_interactions(self, user_id: str, limit: int = 100) -> List[UserInteraction]:
        """Load user interactions from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT user_id, session_id, interaction_type, timestamp, data, context
        FROM user_interactions
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
        ''', (user_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        interactions = []
        for row in rows:
            interactions.append(UserInteraction(
                user_id=row[0],
                session_id=row[1],
                interaction_type=row[2],
                timestamp=datetime.fromisoformat(row[3]),
                data=json.loads(row[4]),
                context=json.loads(row[5]) if row[5] else {}
            ))
        
        return interactions

    async def _save_user_profile(self, profile: UserProfile):
        """Save user profile to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT OR REPLACE INTO user_profiles 
        (user_id, preferences, coding_patterns, app_history, interaction_stats, learning_weights, last_updated)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            profile.user_id,
            json.dumps(profile.preferences),
            json.dumps(profile.coding_patterns),
            json.dumps(profile.app_history),
            json.dumps(profile.interaction_stats),
            json.dumps(profile.learning_weights),
            profile.last_updated.isoformat()
        ))
        
        conn.commit()
        conn.close()

    async def get_personalized_recommendations(self, user_id: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Get personalized recommendations for user"""
        if user_id not in self.user_profiles:
            await self._update_user_profile(user_id)
        
        if user_id not in self.user_profiles:
            return []  # No profile available yet
        
        profile = self.user_profiles[user_id]
        recommendations = await self.personalization_engine.generate_personalized_suggestions(
            profile, context or {}
        )
        
        return recommendations

    async def generate_personalized_app(self, user_id: str, requirements: str, app_type: str) -> Dict[str, Any]:
        """Generate app personalized for user"""
        if user_id not in self.user_profiles:
            await self._update_user_profile(user_id)
        
        if user_id in self.user_profiles:
            profile = self.user_profiles[user_id]
            return await self.adaptive_generator.generate_adaptive_code(requirements, profile, app_type)
        else:
            # Generate standard app for new users
            return await self.adaptive_generator.generate_adaptive_code(
                requirements, 
                UserProfile(user_id, {}, {}, [], {}, {}, datetime.now()),
                app_type
            )

    async def learn_from_feedback(self, user_id: str, session_id: str, app_result: Dict[str, Any], 
                                feedback: Dict[str, Any]):
        """Learn from user feedback on generated apps"""
        await self.record_interaction(
            user_id, session_id, 'feedback',
            {
                'app_result': app_result,
                'feedback': feedback,
                'satisfaction_score': feedback.get('satisfaction', 5)
            }
        )

    def get_system_insights(self) -> List[Dict[str, Any]]:
        """Get system-wide learning insights"""
        insights = []
        
        # Analyze all user profiles for patterns
        all_patterns = defaultdict(list)
        
        for profile in self.user_profiles.values():
            for pattern_type, pattern_data in profile.coding_patterns.items():
                all_patterns[pattern_type].append(pattern_data)
        
        # Generate insights
        for pattern_type, pattern_list in all_patterns.items():
            if len(pattern_list) > 5:  # Need enough data
                insight = {
                    'type': 'global_pattern',
                    'pattern': pattern_type,
                    'description': f"Global trend in {pattern_type}",
                    'confidence': min(len(pattern_list) / 20, 1.0),
                    'data': pattern_list
                }
                insights.append(insight)
        
        return insights

async def main():
    """Demo of Intelligent Learning System"""
    print("🧠 Intelligent Learning System")
    print("=" * 40)
    
    # Initialize system
    learning_system = IntelligentLearningSystem()
    
    print("🎓 Simulating user interactions and learning...")
    
    # Simulate user interactions
    user_id = "user_123"
    session_id = f"session_{int(time.time())}"
    
    # Record various interactions
    interactions = [
        {
            'type': 'app_request',
            'data': {
                'app_type': 'website',
                'requirements': 'Create a modern portfolio website with dark theme',
                'preferences': {'theme': 'dark', 'style': 'modern'}
            }
        },
        {
            'type': 'modification',
            'data': {
                'change': 'color scheme',
                'from': 'light',
                'to': 'dark',
                'reason': 'prefer dark themes'
            }
        },
        {
            'type': 'modification',
            'data': {
                'change': 'layout',
                'modification': 'add grid layout for portfolio items'
            }
        },
        {
            'type': 'feedback',
            'data': {
                'satisfaction': 4,
                'likes': ['dark theme', 'modern design'],
                'improvements': ['add more animations']
            }
        }
    ]
    
    # Record interactions
    for i, interaction in enumerate(interactions):
        await learning_system.record_interaction(
            user_id, f"{session_id}_{i}", 
            interaction['type'], 
            interaction['data']
        )
        print(f"   ✓ Recorded {interaction['type']} interaction")
    
    print(f"\n🔍 Analyzing user patterns...")
    
    # Get personalized recommendations
    recommendations = await learning_system.get_personalized_recommendations(user_id)
    
    print(f"\n💡 Personalized Recommendations ({len(recommendations)}):")
    for rec in recommendations[:5]:  # Show top 5
        print(f"   • {rec['suggestion']}")
        print(f"     Relevance: {rec['relevance_score']:.2f} - {rec['reasoning']}")
    
    print(f"\n🎨 Generating personalized app...")
    
    # Generate personalized app
    personalized_app = await learning_system.generate_personalized_app(
        user_id,
        "Create a portfolio website for a web developer",
        "website"
    )
    
    print(f"   ✓ Generated app with personalization")
    print(f"   ✓ Confidence score: {personalized_app['personalization_applied']['confidence_score']:.2f}")
    print(f"   ✓ Adaptations applied: {len(personalized_app['personalization_applied']['adaptations'])}")
    
    # Simulate feedback learning
    await learning_system.learn_from_feedback(
        user_id, session_id,
        personalized_app,
        {'satisfaction': 5, 'comments': 'Perfect! Exactly what I wanted'}
    )
    
    print(f"\n📊 System Insights:")
    insights = learning_system.get_system_insights()
    for insight in insights[:3]:
        print(f"   • {insight['description']} (confidence: {insight['confidence']:.2f})")
    
    print(f"\n✅ Learning system demonstration complete!")
    print(f"🧠 Key capabilities:")
    print(f"   • User behavior pattern analysis")
    print(f"   • Personalized recommendations")
    print(f"   • Adaptive code generation")
    print(f"   • Continuous learning from feedback")
    print(f"   • Global insight generation")

if __name__ == "__main__":
    asyncio.run(main())