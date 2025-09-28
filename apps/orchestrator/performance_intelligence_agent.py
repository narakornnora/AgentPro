"""
Performance Intelligence Agent
================================
AI-powered system to monitor, analyze, and optimize application performance automatically.
Provides real-time performance insights, predictive analysis, and auto-optimization capabilities.
"""

import asyncio
import json
import logging
import os
import sqlite3
import subprocess
import time
import psutil
import aiohttp
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from urllib.parse import urljoin
import threading
import statistics
from collections import defaultdict, deque

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PerformanceMetrics:
    """Collects and manages performance metrics"""
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.thresholds = {
            'load_time': 3.0,  # seconds
            'memory_usage': 512,  # MB
            'cpu_usage': 80,  # percentage
            'file_size': 5,  # MB
            'response_time': 1.0,  # seconds
            'error_rate': 5,  # percentage
        }
        
    def add_metric(self, metric_type: str, value: float, timestamp: Optional[datetime] = None):
        """Add a performance metric"""
        if timestamp is None:
            timestamp = datetime.now()
            
        self.metrics[metric_type].append({
            'value': value,
            'timestamp': timestamp
        })
        
        # Keep only last 1000 metrics per type
        if len(self.metrics[metric_type]) > 1000:
            self.metrics[metric_type] = self.metrics[metric_type][-1000:]
    
    def get_average(self, metric_type: str, duration_minutes: int = 60) -> float:
        """Get average metric value for specified duration"""
        cutoff_time = datetime.now() - timedelta(minutes=duration_minutes)
        values = [
            m['value'] for m in self.metrics[metric_type]
            if m['timestamp'] > cutoff_time
        ]
        return statistics.mean(values) if values else 0.0
    
    def get_trend(self, metric_type: str) -> str:
        """Analyze trend for a metric (improving, degrading, stable)"""
        if len(self.metrics[metric_type]) < 10:
            return "insufficient_data"
            
        recent_values = [m['value'] for m in self.metrics[metric_type][-10:]]
        older_values = [m['value'] for m in self.metrics[metric_type][-20:-10]]
        
        if not older_values:
            return "insufficient_data"
            
        recent_avg = statistics.mean(recent_values)
        older_avg = statistics.mean(older_values)
        
        if recent_avg < older_avg * 0.95:
            return "improving"
        elif recent_avg > older_avg * 1.05:
            return "degrading"
        else:
            return "stable"

class ResourceMonitor:
    """Monitors system and application resources"""
    
    def __init__(self):
        self.monitoring = False
        self.monitor_thread = None
        self.metrics = PerformanceMetrics()
        
    def start_monitoring(self):
        """Start continuous resource monitoring"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            logger.info("🔍 Resource monitoring started")
    
    def stop_monitoring(self):
        """Stop resource monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("⏹️ Resource monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                # System metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                self.metrics.add_metric('cpu_usage', cpu_percent)
                self.metrics.add_metric('memory_usage', memory.used / 1024 / 1024)  # MB
                self.metrics.add_metric('disk_usage', disk.used / 1024 / 1024 / 1024)  # GB
                
                # Network monitoring
                net_io = psutil.net_io_counters()
                self.metrics.add_metric('network_sent', net_io.bytes_sent)
                self.metrics.add_metric('network_recv', net_io.bytes_recv)
                
                time.sleep(10)  # Monitor every 10 seconds
                
            except Exception as e:
                logger.error(f"Error in resource monitoring: {e}")
                time.sleep(30)  # Wait longer on error

class WebPageAnalyzer:
    """Analyzes web page performance"""
    
    async def analyze_page(self, url: str) -> Dict[str, Any]:
        """Comprehensive page performance analysis"""
        results = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'metrics': {},
            'recommendations': [],
            'issues': []
        }
        
        try:
            start_time = time.time()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    load_time = time.time() - start_time
                    content = await response.text()
                    
                    results['metrics']['load_time'] = load_time
                    results['metrics']['status_code'] = response.status
                    results['metrics']['content_size'] = len(content)
                    results['metrics']['headers'] = dict(response.headers)
                    
                    # Analyze content
                    content_analysis = self._analyze_content(content)
                    results['metrics'].update(content_analysis)
                    
                    # Generate recommendations
                    results['recommendations'] = self._generate_recommendations(results['metrics'])
                    
        except Exception as e:
            results['issues'].append(f"Failed to analyze page: {str(e)}")
            logger.error(f"Page analysis failed for {url}: {e}")
            
        return results
    
    def _analyze_content(self, html_content: str) -> Dict[str, Any]:
        """Analyze HTML content for performance issues"""
        analysis = {
            'html_size': len(html_content),
            'script_count': html_content.count('<script'),
            'style_count': html_content.count('<style'),
            'img_count': html_content.count('<img'),
            'link_count': html_content.count('<link'),
            'inline_styles': html_content.count('style='),
        }
        
        # Check for performance issues
        if analysis['script_count'] > 10:
            analysis['too_many_scripts'] = True
        if analysis['img_count'] > 20:
            analysis['too_many_images'] = True
        if analysis['html_size'] > 100000:  # 100KB
            analysis['large_html'] = True
            
        return analysis
    
    def _generate_recommendations(self, metrics: Dict[str, Any]) -> List[str]:
        """Generate performance optimization recommendations"""
        recommendations = []
        
        if metrics.get('load_time', 0) > 3:
            recommendations.append("Optimize loading time - consider image compression and lazy loading")
        
        if metrics.get('script_count', 0) > 10:
            recommendations.append("Too many scripts - consider bundling and minification")
        
        if metrics.get('img_count', 0) > 20:
            recommendations.append("Many images detected - implement lazy loading")
        
        if metrics.get('html_size', 0) > 100000:
            recommendations.append("Large HTML size - consider code splitting")
        
        if metrics.get('inline_styles', 0) > 5:
            recommendations.append("Multiple inline styles - extract to external CSS")
        
        return recommendations

class PerformanceOptimizer:
    """Automatically optimizes application performance"""
    
    def __init__(self):
        self.optimization_history = []
        
    async def optimize_application(self, app_path: str) -> Dict[str, Any]:
        """Perform comprehensive application optimization"""
        logger.info(f"🚀 Starting optimization for {app_path}")
        
        results = {
            'app_path': app_path,
            'timestamp': datetime.now().isoformat(),
            'optimizations': [],
            'before_metrics': {},
            'after_metrics': {},
            'improvement': {}
        }
        
        try:
            # Measure before optimization
            results['before_metrics'] = await self._measure_app_performance(app_path)
            
            # Apply optimizations
            optimizations = await self._apply_optimizations(app_path)
            results['optimizations'] = optimizations
            
            # Measure after optimization
            results['after_metrics'] = await self._measure_app_performance(app_path)
            
            # Calculate improvements
            results['improvement'] = self._calculate_improvement(
                results['before_metrics'], 
                results['after_metrics']
            )
            
            self.optimization_history.append(results)
            logger.info(f"✅ Optimization complete - {len(optimizations)} optimizations applied")
            
        except Exception as e:
            results['error'] = str(e)
            logger.error(f"Optimization failed: {e}")
            
        return results
    
    async def _measure_app_performance(self, app_path: str) -> Dict[str, float]:
        """Measure application performance metrics"""
        metrics = {}
        
        try:
            # File size analysis
            total_size = 0
            file_count = 0
            
            for root, dirs, files in os.walk(app_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.exists(file_path):
                        total_size += os.path.getsize(file_path)
                        file_count += 1
            
            metrics['total_size_mb'] = total_size / 1024 / 1024
            metrics['file_count'] = file_count
            
            # Code complexity analysis
            html_files = list(Path(app_path).glob('*.html'))
            css_files = list(Path(app_path).glob('*.css'))
            js_files = list(Path(app_path).glob('*.js'))
            
            metrics['html_files'] = len(html_files)
            metrics['css_files'] = len(css_files)
            metrics['js_files'] = len(js_files)
            
            # Analyze content complexity
            if html_files:
                html_content = html_files[0].read_text(encoding='utf-8', errors='ignore')
                metrics['html_lines'] = len(html_content.splitlines())
                metrics['html_chars'] = len(html_content)
            
        except Exception as e:
            logger.error(f"Performance measurement failed: {e}")
            
        return metrics
    
    async def _apply_optimizations(self, app_path: str) -> List[str]:
        """Apply various performance optimizations"""
        optimizations = []
        
        try:
            # HTML optimizations
            html_opts = await self._optimize_html_files(app_path)
            optimizations.extend(html_opts)
            
            # CSS optimizations
            css_opts = await self._optimize_css_files(app_path)
            optimizations.extend(css_opts)
            
            # JS optimizations
            js_opts = await self._optimize_js_files(app_path)
            optimizations.extend(js_opts)
            
            # Image optimizations
            img_opts = await self._optimize_images(app_path)
            optimizations.extend(img_opts)
            
        except Exception as e:
            logger.error(f"Optimization application failed: {e}")
            
        return optimizations
    
    async def _optimize_html_files(self, app_path: str) -> List[str]:
        """Optimize HTML files"""
        optimizations = []
        
        try:
            html_files = list(Path(app_path).glob('*.html'))
            
            for html_file in html_files:
                content = html_file.read_text(encoding='utf-8', errors='ignore')
                original_size = len(content)
                
                # Remove extra whitespace
                lines = content.splitlines()
                optimized_lines = []
                
                for line in lines:
                    stripped = line.strip()
                    if stripped:
                        optimized_lines.append(stripped)
                
                optimized_content = '\n'.join(optimized_lines)
                
                # Add performance enhancements
                if '<head>' in optimized_content and 'viewport' not in optimized_content:
                    optimized_content = optimized_content.replace(
                        '<head>',
                        '<head>\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">'
                    )
                    optimizations.append(f"Added viewport meta tag to {html_file.name}")
                
                # Add lazy loading to images
                if '<img' in optimized_content and 'loading="lazy"' not in optimized_content:
                    optimized_content = optimized_content.replace('<img ', '<img loading="lazy" ')
                    optimizations.append(f"Added lazy loading to images in {html_file.name}")
                
                # Save optimized content
                if len(optimized_content) < original_size:
                    html_file.write_text(optimized_content, encoding='utf-8')
                    reduction = ((original_size - len(optimized_content)) / original_size) * 100
                    optimizations.append(f"Compressed {html_file.name} by {reduction:.1f}%")
                    
        except Exception as e:
            logger.error(f"HTML optimization failed: {e}")
            
        return optimizations
    
    async def _optimize_css_files(self, app_path: str) -> List[str]:
        """Optimize CSS files"""
        optimizations = []
        
        try:
            css_files = list(Path(app_path).glob('*.css'))
            
            for css_file in css_files:
                content = css_file.read_text(encoding='utf-8', errors='ignore')
                original_size = len(content)
                
                # Basic CSS minification
                # Remove comments
                lines = []
                in_comment = False
                
                for line in content.splitlines():
                    if '/*' in line and '*/' in line:
                        # Single line comment
                        before_comment = line[:line.index('/*')]
                        after_comment = line[line.index('*/') + 2:]
                        line = before_comment + after_comment
                    elif '/*' in line:
                        in_comment = True
                        line = line[:line.index('/*')]
                    elif '*/' in line:
                        in_comment = False
                        line = line[line.index('*/') + 2:]
                        
                    if not in_comment and line.strip():
                        lines.append(line.strip())
                
                optimized_content = '\n'.join(lines)
                
                # Save if smaller
                if len(optimized_content) < original_size:
                    css_file.write_text(optimized_content, encoding='utf-8')
                    reduction = ((original_size - len(optimized_content)) / original_size) * 100
                    optimizations.append(f"Optimized {css_file.name} by {reduction:.1f}%")
                    
        except Exception as e:
            logger.error(f"CSS optimization failed: {e}")
            
        return optimizations
    
    async def _optimize_js_files(self, app_path: str) -> List[str]:
        """Optimize JavaScript files"""
        optimizations = []
        
        try:
            js_files = list(Path(app_path).glob('*.js'))
            
            for js_file in js_files:
                content = js_file.read_text(encoding='utf-8', errors='ignore')
                original_size = len(content)
                
                # Basic JS optimization
                lines = []
                for line in content.splitlines():
                    stripped = line.strip()
                    # Remove empty lines and comments
                    if stripped and not stripped.startswith('//') and not stripped.startswith('/*'):
                        lines.append(stripped)
                
                optimized_content = '\n'.join(lines)
                
                # Save if smaller
                if len(optimized_content) < original_size:
                    js_file.write_text(optimized_content, encoding='utf-8')
                    reduction = ((original_size - len(optimized_content)) / original_size) * 100
                    optimizations.append(f"Optimized {js_file.name} by {reduction:.1f}%")
                    
        except Exception as e:
            logger.error(f"JavaScript optimization failed: {e}")
            
        return optimizations
    
    async def _optimize_images(self, app_path: str) -> List[str]:
        """Optimize images (placeholder for future implementation)"""
        optimizations = []
        
        try:
            # Count image files
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']
            image_files = []
            
            for ext in image_extensions:
                image_files.extend(list(Path(app_path).glob(f'*{ext}')))
                image_files.extend(list(Path(app_path).glob(f'**/*{ext}')))
            
            if image_files:
                optimizations.append(f"Found {len(image_files)} images - consider compression")
                
        except Exception as e:
            logger.error(f"Image optimization analysis failed: {e}")
            
        return optimizations
    
    def _calculate_improvement(self, before: Dict, after: Dict) -> Dict[str, float]:
        """Calculate performance improvements"""
        improvements = {}
        
        for key in before:
            if key in after and before[key] > 0:
                improvement = ((before[key] - after[key]) / before[key]) * 100
                improvements[f"{key}_improvement_percent"] = improvement
                
        return improvements

class PerformanceIntelligenceAgent:
    """Main Performance Intelligence Agent orchestrator"""
    
    def __init__(self):
        self.resource_monitor = ResourceMonitor()
        self.page_analyzer = WebPageAnalyzer()
        self.optimizer = PerformanceOptimizer()
        self.db_path = "performance_intelligence.db"
        self.running = False
        
        # Initialize database
        self._init_database()
        
    def _init_database(self):
        """Initialize performance database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS performance_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    app_path TEXT,
                    report_type TEXT NOT NULL,
                    metrics TEXT NOT NULL,
                    recommendations TEXT,
                    status TEXT DEFAULT 'active'
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS optimization_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    app_path TEXT NOT NULL,
                    optimizations TEXT NOT NULL,
                    before_metrics TEXT,
                    after_metrics TEXT,
                    improvement TEXT
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info("📊 Performance database initialized")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
    
    async def start_agent(self):
        """Start the Performance Intelligence Agent"""
        if not self.running:
            self.running = True
            self.resource_monitor.start_monitoring()
            logger.info("🚀 Performance Intelligence Agent started")
            
            # Start background analysis tasks
            asyncio.create_task(self._continuous_analysis())
    
    async def stop_agent(self):
        """Stop the Performance Intelligence Agent"""
        self.running = False
        self.resource_monitor.stop_monitoring()
        logger.info("⏹️ Performance Intelligence Agent stopped")
    
    async def _continuous_analysis(self):
        """Continuous performance analysis loop"""
        while self.running:
            try:
                # Analyze workspace applications
                workspace_path = Path("C:/agent/workspace/generated-app")
                if workspace_path.exists():
                    await self._analyze_workspace_performance(str(workspace_path))
                
                await asyncio.sleep(300)  # Analyze every 5 minutes
                
            except Exception as e:
                logger.error(f"Continuous analysis error: {e}")
                await asyncio.sleep(60)
    
    async def _analyze_workspace_performance(self, workspace_path: str):
        """Analyze performance of workspace applications"""
        try:
            app_dirs = [d for d in Path(workspace_path).iterdir() if d.is_dir()]
            
            for app_dir in app_dirs[-3:]:  # Analyze last 3 apps
                logger.info(f"🔍 Analyzing performance for {app_dir.name}")
                
                # Generate performance report
                report = await self._generate_performance_report(str(app_dir))
                
                # Auto-optimize if needed
                if report.get('needs_optimization', False):
                    optimization_result = await self.optimizer.optimize_application(str(app_dir))
                    await self._save_optimization_result(optimization_result)
                
        except Exception as e:
            logger.error(f"Workspace analysis failed: {e}")
    
    async def _generate_performance_report(self, app_path: str) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        report = {
            'app_path': app_path,
            'timestamp': datetime.now().isoformat(),
            'metrics': {},
            'issues': [],
            'recommendations': [],
            'needs_optimization': False
        }
        
        try:
            # File system analysis
            metrics = await self.optimizer._measure_app_performance(app_path)
            report['metrics'] = metrics
            
            # Check for performance issues
            if metrics.get('total_size_mb', 0) > 10:  # 10MB
                report['issues'].append("Application size is large")
                report['needs_optimization'] = True
                report['recommendations'].append("Consider code splitting and asset optimization")
            
            if metrics.get('file_count', 0) > 50:
                report['issues'].append("Many files in application")
                report['recommendations'].append("Consider file bundling")
            
            # Save report to database
            await self._save_performance_report(report)
            
        except Exception as e:
            logger.error(f"Performance report generation failed: {e}")
            report['error'] = str(e)
            
        return report
    
    async def _save_performance_report(self, report: Dict[str, Any]):
        """Save performance report to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO performance_reports 
                (timestamp, app_path, report_type, metrics, recommendations)
                VALUES (?, ?, ?, ?, ?)
            """, (
                report['timestamp'],
                report['app_path'],
                'auto_analysis',
                json.dumps(report['metrics']),
                json.dumps(report['recommendations'])
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to save performance report: {e}")
    
    async def _save_optimization_result(self, result: Dict[str, Any]):
        """Save optimization result to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO optimization_history 
                (timestamp, app_path, optimizations, before_metrics, after_metrics, improvement)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                result['timestamp'],
                result['app_path'],
                json.dumps(result['optimizations']),
                json.dumps(result['before_metrics']),
                json.dumps(result['after_metrics']),
                json.dumps(result['improvement'])
            ))
            
            conn.commit()
            conn.close()
            logger.info("💾 Optimization result saved to database")
            
        except Exception as e:
            logger.error(f"Failed to save optimization result: {e}")
    
    async def get_performance_dashboard(self) -> Dict[str, Any]:
        """Get performance dashboard data"""
        dashboard = {
            'system_metrics': {},
            'recent_reports': [],
            'optimization_history': [],
            'recommendations': []
        }
        
        try:
            # System metrics
            dashboard['system_metrics'] = {
                'cpu_avg': self.resource_monitor.metrics.get_average('cpu_usage'),
                'memory_avg': self.resource_monitor.metrics.get_average('memory_usage'),
                'cpu_trend': self.resource_monitor.metrics.get_trend('cpu_usage'),
                'memory_trend': self.resource_monitor.metrics.get_trend('memory_usage')
            }
            
            # Recent reports
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT timestamp, app_path, metrics, recommendations 
                FROM performance_reports 
                ORDER BY timestamp DESC 
                LIMIT 10
            """)
            
            for row in cursor.fetchall():
                dashboard['recent_reports'].append({
                    'timestamp': row[0],
                    'app_path': row[1],
                    'metrics': json.loads(row[2]) if row[2] else {},
                    'recommendations': json.loads(row[3]) if row[3] else []
                })
            
            conn.close()
            
        except Exception as e:
            logger.error(f"Dashboard generation failed: {e}")
            
        return dashboard

# Main execution
async def main():
    """Main function to run Performance Intelligence Agent"""
    agent = PerformanceIntelligenceAgent()
    
    print("🚀 Starting Performance Intelligence Agent...")
    print("==================================================")
    print("🔍 Monitoring system resources and application performance")
    print("📊 Generating intelligent insights and optimizations")
    print("⚡ Auto-optimizing applications for better performance")
    print("🎯 Real-time performance analysis and recommendations")
    print()
    
    await agent.start_agent()
    
    try:
        # Keep running
        while True:
            dashboard = await agent.get_performance_dashboard()
            
            print(f"\n📊 Performance Dashboard - {datetime.now().strftime('%H:%M:%S')}")
            print("=" * 50)
            print(f"💻 CPU Average: {dashboard['system_metrics'].get('cpu_avg', 0):.1f}% "
                  f"({dashboard['system_metrics'].get('cpu_trend', 'unknown')})")
            print(f"🧠 Memory Average: {dashboard['system_metrics'].get('memory_avg', 0):.1f}MB "
                  f"({dashboard['system_metrics'].get('memory_trend', 'unknown')})")
            print(f"📈 Recent Reports: {len(dashboard['recent_reports'])}")
            
            await asyncio.sleep(30)  # Update every 30 seconds
            
    except KeyboardInterrupt:
        print("\n⏹️ Shutting down Performance Intelligence Agent...")
        await agent.stop_agent()

if __name__ == "__main__":
    asyncio.run(main())