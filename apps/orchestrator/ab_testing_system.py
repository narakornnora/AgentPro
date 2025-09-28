"""
A/B Testing System
==================
Intelligent A/B testing framework for automatic UI/UX optimization.
Creates variations, runs experiments, analyzes results, and selects best-performing versions.
"""

import asyncio
import json
import logging
import os
import random
import sqlite3
import hashlib
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import re
import statistics
from collections import defaultdict
import copy

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Variation:
    """Represents a UI/UX variation for A/B testing"""
    
    def __init__(self, variation_id: str, name: str, description: str, 
                 changes: Dict[str, Any], original_files: Dict[str, str]):
        self.variation_id = variation_id
        self.name = name
        self.description = description
        self.changes = changes
        self.original_files = original_files
        self.created_at = datetime.now()
        self.metrics = {}
        self.is_active = True
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            'variation_id': self.variation_id,
            'name': self.name,
            'description': self.description,
            'changes': self.changes,
            'created_at': self.created_at.isoformat(),
            'metrics': self.metrics,
            'is_active': self.is_active
        }

class ExperimentTracker:
    """Tracks experiment metrics and user interactions"""
    
    def __init__(self):
        self.sessions = {}
        self.metrics = defaultdict(list)
        
    def start_session(self, session_id: str, variation_id: str) -> None:
        """Start tracking a user session"""
        self.sessions[session_id] = {
            'variation_id': variation_id,
            'start_time': datetime.now(),
            'interactions': [],
            'metrics': {}
        }
        
    def record_interaction(self, session_id: str, interaction_type: str, 
                          element: str, value: Any = None) -> None:
        """Record user interaction"""
        if session_id in self.sessions:
            self.sessions[session_id]['interactions'].append({
                'type': interaction_type,
                'element': element,
                'value': value,
                'timestamp': datetime.now().isoformat()
            })
    
    def record_metric(self, session_id: str, metric_name: str, value: float) -> None:
        """Record session metric"""
        if session_id in self.sessions:
            self.sessions[session_id]['metrics'][metric_name] = value
            
    def get_variation_metrics(self, variation_id: str) -> Dict[str, float]:
        """Get aggregated metrics for a variation"""
        variation_sessions = [
            session for session in self.sessions.values()
            if session['variation_id'] == variation_id
        ]
        
        if not variation_sessions:
            return {}
            
        metrics = {}
        
        # Calculate average session duration
        durations = []
        for session in variation_sessions:
            if 'end_time' in session:
                duration = (session['end_time'] - session['start_time']).total_seconds()
                durations.append(duration)
        
        if durations:
            metrics['avg_session_duration'] = statistics.mean(durations)
            metrics['session_count'] = len(durations)
            
        # Calculate interaction rates
        total_interactions = sum(len(session['interactions']) for session in variation_sessions)
        metrics['avg_interactions_per_session'] = total_interactions / len(variation_sessions) if variation_sessions else 0
        
        # Calculate conversion rates (placeholder)
        conversions = sum(1 for session in variation_sessions if session['metrics'].get('converted', False))
        metrics['conversion_rate'] = (conversions / len(variation_sessions)) * 100 if variation_sessions else 0
        
        return metrics

class VariationGenerator:
    """Generates UI/UX variations automatically"""
    
    def __init__(self):
        self.color_palettes = [
            {'primary': '#3498db', 'secondary': '#2c3e50', 'accent': '#e74c3c'},
            {'primary': '#27ae60', 'secondary': '#34495e', 'accent': '#f39c12'},
            {'primary': '#9b59b6', 'secondary': '#2c3e50', 'accent': '#1abc9c'},
            {'primary': '#e67e22', 'secondary': '#34495e', 'accent': '#3498db'},
            {'primary': '#e74c3c', 'secondary': '#2c3e50', 'accent': '#27ae60'}
        ]
        
        self.font_combinations = [
            {'heading': 'Arial, sans-serif', 'body': 'Georgia, serif'},
            {'heading': 'Impact, sans-serif', 'body': 'Helvetica, sans-serif'},
            {'heading': 'Times New Roman, serif', 'body': 'Verdana, sans-serif'},
            {'heading': 'Trebuchet MS, sans-serif', 'body': 'Tahoma, sans-serif'},
            {'heading': 'Palatino, serif', 'body': 'Lucida Sans, sans-serif'}
        ]
        
        self.layout_variations = [
            {'header_position': 'top', 'sidebar': 'left', 'content_width': '80%'},
            {'header_position': 'top', 'sidebar': 'right', 'content_width': '85%'},
            {'header_position': 'sticky', 'sidebar': 'none', 'content_width': '100%'},
            {'header_position': 'top', 'sidebar': 'bottom', 'content_width': '90%'}
        ]
    
    async def generate_variations(self, app_path: str, num_variations: int = 3) -> List[Variation]:
        """Generate multiple UI/UX variations"""
        variations = []
        
        try:
            # Read original files
            original_files = await self._read_app_files(app_path)
            
            for i in range(num_variations):
                variation = await self._create_variation(app_path, original_files, i + 1)
                variations.append(variation)
                
            logger.info(f"✨ Generated {len(variations)} variations")
            
        except Exception as e:
            logger.error(f"Variation generation failed: {e}")
            
        return variations
    
    async def _read_app_files(self, app_path: str) -> Dict[str, str]:
        """Read application files"""
        files = {}
        
        try:
            app_dir = Path(app_path)
            
            # Read HTML files
            for html_file in app_dir.glob('*.html'):
                files[html_file.name] = html_file.read_text(encoding='utf-8', errors='ignore')
                
            # Read CSS files
            for css_file in app_dir.glob('*.css'):
                files[css_file.name] = css_file.read_text(encoding='utf-8', errors='ignore')
                
            # Read JS files
            for js_file in app_dir.glob('*.js'):
                files[js_file.name] = js_file.read_text(encoding='utf-8', errors='ignore')
                
        except Exception as e:
            logger.error(f"Failed to read app files: {e}")
            
        return files
    
    async def _create_variation(self, app_path: str, original_files: Dict[str, str], 
                               variation_num: int) -> Variation:
        """Create a single variation"""
        variation_id = f"var_{uuid.uuid4().hex[:8]}"
        
        # Select variation type
        variation_types = ['color_scheme', 'typography', 'layout', 'button_style', 'spacing']
        selected_type = random.choice(variation_types)
        
        changes = {}
        name = f"Variation {variation_num}"
        description = f"Testing {selected_type} changes"
        
        if selected_type == 'color_scheme':
            palette = random.choice(self.color_palettes)
            changes = await self._apply_color_changes(original_files, palette)
            name = f"Color Scheme {variation_num}"
            description = f"Testing color palette: {palette['primary']}"
            
        elif selected_type == 'typography':
            fonts = random.choice(self.font_combinations)
            changes = await self._apply_typography_changes(original_files, fonts)
            name = f"Typography {variation_num}"
            description = f"Testing fonts: {fonts['heading']} / {fonts['body']}"
            
        elif selected_type == 'layout':
            layout = random.choice(self.layout_variations)
            changes = await self._apply_layout_changes(original_files, layout)
            name = f"Layout {variation_num}"
            description = f"Testing layout: {layout}"
            
        elif selected_type == 'button_style':
            changes = await self._apply_button_changes(original_files, variation_num)
            name = f"Button Style {variation_num}"
            description = "Testing button styling variations"
            
        elif selected_type == 'spacing':
            changes = await self._apply_spacing_changes(original_files, variation_num)
            name = f"Spacing {variation_num}"
            description = "Testing spacing and padding variations"
        
        return Variation(variation_id, name, description, changes, original_files)
    
    async def _apply_color_changes(self, files: Dict[str, str], palette: Dict[str, str]) -> Dict[str, str]:
        """Apply color scheme changes"""
        modified_files = {}
        
        try:
            for filename, content in files.items():
                if filename.endswith('.css'):
                    modified_content = content
                    
                    # Replace common colors
                    color_replacements = {
                        '#3498db': palette['primary'],
                        '#007bff': palette['primary'],
                        'blue': palette['primary'],
                        '#28a745': palette['secondary'],
                        'green': palette['secondary'],
                        '#dc3545': palette['accent'],
                        'red': palette['accent']
                    }
                    
                    for old_color, new_color in color_replacements.items():
                        modified_content = modified_content.replace(old_color, new_color)
                    
                    modified_files[filename] = modified_content
                else:
                    modified_files[filename] = content
                    
        except Exception as e:
            logger.error(f"Color changes failed: {e}")
            
        return modified_files
    
    async def _apply_typography_changes(self, files: Dict[str, str], fonts: Dict[str, str]) -> Dict[str, str]:
        """Apply typography changes"""
        modified_files = {}
        
        try:
            for filename, content in files.items():
                if filename.endswith('.css'):
                    modified_content = content
                    
                    # Add typography rules
                    typography_css = f"""
/* A/B Test Typography Variation */
h1, h2, h3, h4, h5, h6 {{
    font-family: {fonts['heading']} !important;
}}
body, p, div, span {{
    font-family: {fonts['body']} !important;
}}
"""
                    modified_content += typography_css
                    modified_files[filename] = modified_content
                else:
                    modified_files[filename] = content
                    
        except Exception as e:
            logger.error(f"Typography changes failed: {e}")
            
        return modified_files
    
    async def _apply_layout_changes(self, files: Dict[str, str], layout: Dict[str, str]) -> Dict[str, str]:
        """Apply layout changes"""
        modified_files = {}
        
        try:
            for filename, content in files.items():
                if filename.endswith('.css'):
                    modified_content = content
                    
                    # Add layout rules
                    layout_css = f"""
/* A/B Test Layout Variation */
.main-content {{
    width: {layout['content_width']} !important;
    margin: 0 auto;
}}
header {{
    position: {'fixed' if layout['header_position'] == 'sticky' else 'relative'} !important;
}}
"""
                    modified_content += layout_css
                    modified_files[filename] = modified_content
                else:
                    modified_files[filename] = content
                    
        except Exception as e:
            logger.error(f"Layout changes failed: {e}")
            
        return modified_files
    
    async def _apply_button_changes(self, files: Dict[str, str], variation_num: int) -> Dict[str, str]:
        """Apply button style changes"""
        modified_files = {}
        
        try:
            button_styles = [
                "border-radius: 25px; padding: 12px 24px; font-weight: bold;",
                "border-radius: 4px; padding: 10px 20px; text-transform: uppercase;", 
                "border-radius: 0; padding: 15px 30px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);",
                "border-radius: 50px; padding: 8px 16px; border: 2px solid;"
            ]
            
            selected_style = button_styles[variation_num % len(button_styles)]
            
            for filename, content in files.items():
                if filename.endswith('.css'):
                    modified_content = content
                    
                    button_css = f"""
/* A/B Test Button Variation */
button, .btn, input[type="submit"] {{
    {selected_style}
}}
"""
                    modified_content += button_css
                    modified_files[filename] = modified_content
                else:
                    modified_files[filename] = content
                    
        except Exception as e:
            logger.error(f"Button changes failed: {e}")
            
        return modified_files
    
    async def _apply_spacing_changes(self, files: Dict[str, str], variation_num: int) -> Dict[str, str]:
        """Apply spacing changes"""
        modified_files = {}
        
        try:
            spacing_multipliers = [1.2, 1.5, 0.8, 2.0]
            multiplier = spacing_multipliers[variation_num % len(spacing_multipliers)]
            
            for filename, content in files.items():
                if filename.endswith('.css'):
                    modified_content = content
                    
                    spacing_css = f"""
/* A/B Test Spacing Variation */
.container, .content {{
    padding: {16 * multiplier}px !important;
    margin: {8 * multiplier}px !important;
}}
h1, h2, h3 {{
    margin-bottom: {12 * multiplier}px !important;
}}
p {{
    margin-bottom: {10 * multiplier}px !important;
}}
"""
                    modified_content += spacing_css
                    modified_files[filename] = modified_content
                else:
                    modified_files[filename] = content
                    
        except Exception as e:
            logger.error(f"Spacing changes failed: {e}")
            
        return modified_files

class ExperimentManager:
    """Manages A/B test experiments"""
    
    def __init__(self):
        self.active_experiments = {}
        self.variation_generator = VariationGenerator()
        self.tracker = ExperimentTracker()
        
    async def create_experiment(self, app_path: str, experiment_name: str, 
                               num_variations: int = 3) -> str:
        """Create a new A/B test experiment"""
        experiment_id = f"exp_{uuid.uuid4().hex[:8]}"
        
        try:
            # Generate variations
            variations = await self.variation_generator.generate_variations(app_path, num_variations)
            
            # Create control variation (original)
            original_files = await self.variation_generator._read_app_files(app_path)
            control_variation = Variation(
                "control",
                "Control (Original)",
                "Original version without changes",
                original_files,
                original_files
            )
            variations.insert(0, control_variation)
            
            self.active_experiments[experiment_id] = {
                'id': experiment_id,
                'name': experiment_name,
                'app_path': app_path,
                'variations': {v.variation_id: v for v in variations},
                'created_at': datetime.now(),
                'status': 'active',
                'traffic_split': self._calculate_traffic_split(len(variations))
            }
            
            logger.info(f"🧪 Created experiment '{experiment_name}' with {len(variations)} variations")
            return experiment_id
            
        except Exception as e:
            logger.error(f"Experiment creation failed: {e}")
            return ""
    
    def _calculate_traffic_split(self, num_variations: int) -> Dict[str, float]:
        """Calculate traffic split for variations"""
        split_percentage = 100 / num_variations
        return {f"variation_{i}": split_percentage for i in range(num_variations)}
    
    async def assign_user_to_variation(self, experiment_id: str, user_id: str) -> Optional[str]:
        """Assign user to a variation using consistent hashing"""
        if experiment_id not in self.active_experiments:
            return None
            
        experiment = self.active_experiments[experiment_id]
        variations = list(experiment['variations'].keys())
        
        # Use consistent hashing
        hash_input = f"{experiment_id}_{user_id}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
        variation_index = hash_value % len(variations)
        
        selected_variation = variations[variation_index]
        
        # Start tracking session
        self.tracker.start_session(user_id, selected_variation)
        
        return selected_variation
    
    async def deploy_variation(self, experiment_id: str, variation_id: str, 
                              target_path: str) -> bool:
        """Deploy a specific variation to target path"""
        try:
            if experiment_id not in self.active_experiments:
                return False
                
            experiment = self.active_experiments[experiment_id]
            
            if variation_id not in experiment['variations']:
                return False
                
            variation = experiment['variations'][variation_id]
            
            # Deploy variation files
            target_dir = Path(target_path)
            target_dir.mkdir(parents=True, exist_ok=True)
            
            for filename, content in variation.changes.items():
                file_path = target_dir / filename
                file_path.write_text(content, encoding='utf-8')
            
            logger.info(f"🚀 Deployed variation '{variation.name}' to {target_path}")
            return True
            
        except Exception as e:
            logger.error(f"Variation deployment failed: {e}")
            return False
    
    async def analyze_experiment_results(self, experiment_id: str) -> Dict[str, Any]:
        """Analyze experiment results and determine winner"""
        if experiment_id not in self.active_experiments:
            return {}
            
        experiment = self.active_experiments[experiment_id]
        results = {
            'experiment_id': experiment_id,
            'experiment_name': experiment['name'],
            'analysis_timestamp': datetime.now().isoformat(),
            'variation_results': {},
            'winner': None,
            'confidence': 0,
            'recommendations': []
        }
        
        try:
            # Analyze each variation
            for variation_id, variation in experiment['variations'].items():
                metrics = self.tracker.get_variation_metrics(variation_id)
                
                results['variation_results'][variation_id] = {
                    'name': variation.name,
                    'description': variation.description,
                    'metrics': metrics,
                    'score': self._calculate_variation_score(metrics)
                }
            
            # Determine winner
            winner_info = self._determine_winner(results['variation_results'])
            results['winner'] = winner_info['variation_id']
            results['confidence'] = winner_info['confidence']
            
            # Generate recommendations
            results['recommendations'] = self._generate_recommendations(results)
            
        except Exception as e:
            logger.error(f"Experiment analysis failed: {e}")
            results['error'] = str(e)
            
        return results
    
    def _calculate_variation_score(self, metrics: Dict[str, float]) -> float:
        """Calculate overall score for a variation"""
        score = 0
        
        # Weight different metrics
        if 'conversion_rate' in metrics:
            score += metrics['conversion_rate'] * 0.4
            
        if 'avg_session_duration' in metrics:
            score += min(metrics['avg_session_duration'] / 60, 10) * 0.3  # Cap at 10 minutes
            
        if 'avg_interactions_per_session' in metrics:
            score += min(metrics['avg_interactions_per_session'], 20) * 0.3  # Cap at 20 interactions
            
        return score
    
    def _determine_winner(self, variation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Determine the winning variation"""
        best_variation = None
        best_score = -1
        
        for variation_id, result in variation_results.items():
            score = result.get('score', 0)
            if score > best_score:
                best_score = score
                best_variation = variation_id
        
        # Calculate confidence (simplified)
        scores = [result.get('score', 0) for result in variation_results.values()]
        if len(scores) > 1 and max(scores) > 0:
            second_best = sorted(scores)[-2] if len(scores) > 1 else 0
            confidence = ((best_score - second_best) / best_score) * 100 if best_score > 0 else 0
        else:
            confidence = 0
            
        return {
            'variation_id': best_variation,
            'confidence': min(confidence, 95)  # Cap at 95%
        }
    
    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        winner_id = results['winner']
        if winner_id and winner_id in results['variation_results']:
            winner = results['variation_results'][winner_id]
            recommendations.append(f"Deploy '{winner['name']}' as the winning variation")
            
            # Specific recommendations based on metrics
            metrics = winner.get('metrics', {})
            
            if metrics.get('conversion_rate', 0) > 10:
                recommendations.append("High conversion rate - consider scaling this design pattern")
                
            if metrics.get('avg_session_duration', 0) > 120:  # 2 minutes
                recommendations.append("Strong user engagement - analyze what keeps users interested")
                
        if results['confidence'] < 70:
            recommendations.append("Run experiment longer to increase statistical confidence")
            
        return recommendations

class ABTestingSystem:
    """Main A/B Testing System orchestrator"""
    
    def __init__(self):
        self.experiment_manager = ExperimentManager()
        self.db_path = "ab_testing.db"
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Initialize A/B testing database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS experiments (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    app_path TEXT NOT NULL,
                    variations TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    status TEXT DEFAULT 'active',
                    results TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_assignments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    experiment_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    variation_id TEXT NOT NULL,
                    assigned_at TEXT NOT NULL,
                    UNIQUE(experiment_id, user_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS experiment_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    experiment_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    variation_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    event_data TEXT,
                    timestamp TEXT NOT NULL
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info("🧪 A/B Testing database initialized")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
    
    async def start_ab_test(self, app_path: str, experiment_name: str) -> str:
        """Start a new A/B test"""
        experiment_id = await self.experiment_manager.create_experiment(app_path, experiment_name)
        
        if experiment_id:
            # Save to database
            await self._save_experiment(experiment_id)
            logger.info(f"🚀 A/B test '{experiment_name}' started with ID: {experiment_id}")
        
        return experiment_id
    
    async def _save_experiment(self, experiment_id: str):
        """Save experiment to database"""
        try:
            experiment = self.experiment_manager.active_experiments[experiment_id]
            
            # Convert variations to serializable format
            variations_data = {}
            for var_id, variation in experiment['variations'].items():
                variations_data[var_id] = variation.to_dict()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO experiments 
                (id, name, app_path, variations, created_at, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                experiment_id,
                experiment['name'],
                experiment['app_path'],
                json.dumps(variations_data),
                experiment['created_at'].isoformat(),
                experiment['status']
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to save experiment: {e}")
    
    async def get_experiment_dashboard(self) -> Dict[str, Any]:
        """Get A/B testing dashboard data"""
        dashboard = {
            'active_experiments': [],
            'recent_results': [],
            'overall_stats': {},
            'recommendations': []
        }
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get active experiments
            cursor.execute("""
                SELECT id, name, app_path, created_at, status
                FROM experiments 
                WHERE status = 'active'
                ORDER BY created_at DESC
            """)
            
            for row in cursor.fetchall():
                dashboard['active_experiments'].append({
                    'id': row[0],
                    'name': row[1],
                    'app_path': row[2],
                    'created_at': row[3],
                    'status': row[4]
                })
            
            # Overall statistics
            cursor.execute("SELECT COUNT(*) FROM experiments")
            total_experiments = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM experiments WHERE status = 'active'")
            active_experiments = cursor.fetchone()[0]
            
            dashboard['overall_stats'] = {
                'total_experiments': total_experiments,
                'active_experiments': active_experiments,
                'completed_experiments': total_experiments - active_experiments
            }
            
            conn.close()
            
        except Exception as e:
            logger.error(f"Dashboard generation failed: {e}")
            
        return dashboard

# Main execution
async def main():
    """Main function to demonstrate A/B Testing System"""
    system = ABTestingSystem()
    
    print("🧪 A/B Testing System Demo")
    print("=" * 40)
    
    # Demo with workspace app
    workspace_path = Path("C:/agent/workspace/generated-app")
    if workspace_path.exists():
        app_dirs = [d for d in workspace_path.iterdir() if d.is_dir()]
        
        if app_dirs:
            latest_app = max(app_dirs, key=lambda x: x.stat().st_mtime)
            print(f"📱 Testing app: {latest_app.name}")
            
            # Start A/B test
            experiment_id = await system.start_ab_test(str(latest_app), f"UI Test - {latest_app.name}")
            
            if experiment_id:
                print(f"✅ Experiment started: {experiment_id}")
                
                # Simulate user assignments
                for i in range(5):
                    user_id = f"user_{i+1}"
                    variation = await system.experiment_manager.assign_user_to_variation(experiment_id, user_id)
                    print(f"👤 User {user_id} assigned to: {variation}")
                
                # Get dashboard
                dashboard = await system.get_experiment_dashboard()
                print(f"\n📊 Dashboard Summary:")
                print(f"   Active Experiments: {dashboard['overall_stats']['active_experiments']}")
                print(f"   Total Experiments: {dashboard['overall_stats']['total_experiments']}")
                
    print("\n✨ A/B Testing System initialized successfully!")

if __name__ == "__main__":
    asyncio.run(main())