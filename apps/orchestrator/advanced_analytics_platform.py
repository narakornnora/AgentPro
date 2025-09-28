"""
Advanced Analytics Platform
===========================
Comprehensive analytics system for tracking user behavior, app performance, 
error patterns, and generating intelligent insights for continuous improvement.
"""

import asyncio
import json
import logging
import sqlite3
import statistics
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set
from collections import defaultdict, Counter
import math
import random
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class UserSession:
    """Represents a user session with tracking data"""
    
    def __init__(self, session_id: str, user_id: str, app_id: str):
        self.session_id = session_id
        self.user_id = user_id
        self.app_id = app_id
        self.start_time = datetime.now()
        self.end_time = None
        self.events = []
        self.page_views = []
        self.interactions = []
        self.errors = []
        self.performance_metrics = {}
        
    def add_event(self, event_type: str, data: Dict[str, Any]):
        """Add an event to the session"""
        event = {
            'event_id': str(uuid.uuid4()),
            'type': event_type,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        self.events.append(event)
        
        # Categorize events
        if event_type == 'page_view':
            self.page_views.append(event)
        elif event_type in ['click', 'scroll', 'form_submit', 'input_change']:
            self.interactions.append(event)
        elif event_type == 'error':
            self.errors.append(event)
    
    def end_session(self):
        """End the session"""
        self.end_time = datetime.now()
        
    def get_duration(self) -> float:
        """Get session duration in seconds"""
        end = self.end_time or datetime.now()
        return (end - self.start_time).total_seconds()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary"""
        return {
            'session_id': self.session_id,
            'user_id': self.user_id,
            'app_id': self.app_id,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration': self.get_duration(),
            'events': self.events,
            'page_views': len(self.page_views),
            'interactions': len(self.interactions),
            'errors': len(self.errors),
            'performance_metrics': self.performance_metrics
        }

class EventTracker:
    """Tracks and processes user events"""
    
    def __init__(self):
        self.active_sessions = {}
        self.event_patterns = self._load_event_patterns()
        
    def _load_event_patterns(self) -> Dict[str, Dict]:
        """Load event analysis patterns"""
        return {
            'engagement_indicators': [
                'scroll_depth_75', 'form_interaction', 'multi_page_visit',
                'long_session', 'repeat_visitor', 'social_share'
            ],
            'conversion_events': [
                'form_submit', 'button_click_cta', 'download', 'signup',
                'purchase', 'contact_form', 'newsletter_signup'
            ],
            'exit_indicators': [
                'high_bounce_rate', 'short_session', 'error_encountered',
                'load_timeout', 'navigation_confusion'
            ]
        }
    
    def start_session(self, user_id: str, app_id: str) -> str:
        """Start tracking a new user session"""
        session_id = str(uuid.uuid4())
        session = UserSession(session_id, user_id, app_id)
        self.active_sessions[session_id] = session
        
        # Track session start event
        session.add_event('session_start', {
            'timestamp': datetime.now().isoformat(),
            'user_agent': 'unknown',
            'referrer': 'direct'
        })
        
        return session_id
    
    def track_event(self, session_id: str, event_type: str, data: Dict[str, Any]):
        """Track a user event"""
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            session.add_event(event_type, data)
            
            # Update performance metrics
            if event_type == 'page_load':
                load_time = data.get('load_time', 0)
                session.performance_metrics['avg_load_time'] = statistics.mean([
                    session.performance_metrics.get('avg_load_time', load_time), load_time
                ])
    
    def end_session(self, session_id: str):
        """End a user session"""
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            session.end_session()
            session.add_event('session_end', {
                'duration': session.get_duration(),
                'total_events': len(session.events)
            })
            
            # Move to completed sessions for analysis
            return self.active_sessions.pop(session_id)
        return None

class BehaviorAnalyzer:
    """Analyzes user behavior patterns"""
    
    def __init__(self):
        self.behavior_models = {}
        
    def analyze_user_journey(self, sessions: List[UserSession]) -> Dict[str, Any]:
        """Analyze user journey patterns"""
        analysis = {
            'total_sessions': len(sessions),
            'avg_session_duration': 0,
            'page_flow_analysis': {},
            'drop_off_points': [],
            'engagement_score': 0,
            'user_segments': {}
        }
        
        if not sessions:
            return analysis
            
        try:
            # Session duration analysis
            durations = [session.get_duration() for session in sessions]
            analysis['avg_session_duration'] = statistics.mean(durations)
            analysis['median_session_duration'] = statistics.median(durations)
            
            # Page flow analysis
            page_flows = defaultdict(int)
            for session in sessions:
                page_sequence = [event['data'].get('page', 'unknown') 
                               for event in session.page_views]
                
                for i in range(len(page_sequence) - 1):
                    flow = f"{page_sequence[i]} -> {page_sequence[i+1]}"
                    page_flows[flow] += 1
            
            analysis['page_flow_analysis'] = dict(page_flows)
            
            # Engagement scoring
            engagement_scores = []
            for session in sessions:
                score = self._calculate_engagement_score(session)
                engagement_scores.append(score)
            
            analysis['engagement_score'] = statistics.mean(engagement_scores) if engagement_scores else 0
            
            # User segmentation
            analysis['user_segments'] = self._segment_users(sessions)
            
        except Exception as e:
            logger.error(f"User journey analysis failed: {e}")
            
        return analysis
    
    def _calculate_engagement_score(self, session: UserSession) -> float:
        """Calculate engagement score for a session"""
        score = 0
        
        # Duration factor (up to 30 points)
        duration_minutes = session.get_duration() / 60
        score += min(30, duration_minutes * 2)
        
        # Interaction factor (up to 25 points)
        score += min(25, len(session.interactions) * 2)
        
        # Page views factor (up to 20 points)
        score += min(20, len(session.page_views) * 3)
        
        # Error penalty (subtract 5 per error)
        score -= len(session.errors) * 5
        
        # Conversion events bonus (10 points each)
        conversion_events = [e for e in session.events 
                           if e['type'] in ['form_submit', 'signup', 'purchase']]
        score += len(conversion_events) * 10
        
        return max(0, min(100, score))
    
    def _segment_users(self, sessions: List[UserSession]) -> Dict[str, int]:
        """Segment users based on behavior"""
        segments = {
            'highly_engaged': 0,
            'moderately_engaged': 0,
            'low_engagement': 0,
            'bounce_users': 0,
            'power_users': 0
        }
        
        user_data = defaultdict(list)
        for session in sessions:
            user_data[session.user_id].append(session)
        
        for user_id, user_sessions in user_data.items():
            avg_duration = statistics.mean([s.get_duration() for s in user_sessions])
            total_interactions = sum(len(s.interactions) for s in user_sessions)
            session_count = len(user_sessions)
            
            # Segmentation logic
            if session_count >= 5 and avg_duration > 300:  # 5+ sessions, 5+ min avg
                segments['power_users'] += 1
            elif avg_duration > 120 and total_interactions > 10:  # 2+ min, 10+ interactions
                segments['highly_engaged'] += 1
            elif avg_duration > 60 and total_interactions > 3:  # 1+ min, 3+ interactions
                segments['moderately_engaged'] += 1
            elif avg_duration < 30:  # Less than 30 seconds
                segments['bounce_users'] += 1
            else:
                segments['low_engagement'] += 1
        
        return segments

class PerformanceAnalyzer:
    """Analyzes application performance metrics"""
    
    def __init__(self):
        self.performance_thresholds = {
            'page_load_time': 3.0,  # seconds
            'first_contentful_paint': 1.5,
            'largest_contentful_paint': 2.5,
            'cumulative_layout_shift': 0.1,
            'first_input_delay': 0.1
        }
    
    def analyze_performance_data(self, sessions: List[UserSession]) -> Dict[str, Any]:
        """Analyze performance metrics across sessions"""
        analysis = {
            'performance_summary': {},
            'bottlenecks': [],
            'trends': {},
            'recommendations': []
        }
        
        try:
            # Collect performance metrics
            load_times = []
            error_rates = []
            
            for session in sessions:
                # Extract load times from events
                for event in session.events:
                    if event['type'] == 'page_load':
                        load_time = event['data'].get('load_time', 0)
                        if load_time > 0:
                            load_times.append(load_time)
                
                # Calculate error rate
                if session.events:
                    error_rate = len(session.errors) / len(session.events) * 100
                    error_rates.append(error_rate)
            
            # Performance summary
            if load_times:
                analysis['performance_summary'] = {
                    'avg_load_time': statistics.mean(load_times),
                    'median_load_time': statistics.median(load_times),
                    'p95_load_time': self._percentile(load_times, 95),
                    'slow_pages_percent': len([t for t in load_times if t > 3.0]) / len(load_times) * 100
                }
            
            if error_rates:
                analysis['performance_summary']['avg_error_rate'] = statistics.mean(error_rates)
            
            # Identify bottlenecks
            analysis['bottlenecks'] = self._identify_bottlenecks(sessions)
            
            # Generate recommendations
            analysis['recommendations'] = self._generate_performance_recommendations(analysis)
            
        except Exception as e:
            logger.error(f"Performance analysis failed: {e}")
            
        return analysis
    
    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile of data"""
        if not data:
            return 0
        sorted_data = sorted(data)
        index = (percentile / 100) * (len(sorted_data) - 1)
        if index.is_integer():
            return sorted_data[int(index)]
        else:
            lower = sorted_data[int(index)]
            upper = sorted_data[int(index) + 1]
            return lower + (upper - lower) * (index - int(index))
    
    def _identify_bottlenecks(self, sessions: List[UserSession]) -> List[Dict[str, Any]]:
        """Identify performance bottlenecks"""
        bottlenecks = []
        
        # Analyze page-specific performance
        page_performance = defaultdict(list)
        
        for session in sessions:
            for event in session.events:
                if event['type'] == 'page_load':
                    page = event['data'].get('page', 'unknown')
                    load_time = event['data'].get('load_time', 0)
                    page_performance[page].append(load_time)
        
        # Find slow pages
        for page, load_times in page_performance.items():
            if load_times:
                avg_load_time = statistics.mean(load_times)
                if avg_load_time > self.performance_thresholds['page_load_time']:
                    bottlenecks.append({
                        'type': 'slow_page',
                        'page': page,
                        'avg_load_time': avg_load_time,
                        'severity': 'high' if avg_load_time > 5 else 'medium'
                    })
        
        return bottlenecks
    
    def _generate_performance_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []
        
        summary = analysis.get('performance_summary', {})
        
        if summary.get('avg_load_time', 0) > 3:
            recommendations.append("🚀 Optimize page load times - consider image compression and lazy loading")
        
        if summary.get('slow_pages_percent', 0) > 20:
            recommendations.append("📄 Multiple pages are loading slowly - review code splitting strategy")
        
        if summary.get('avg_error_rate', 0) > 5:
            recommendations.append("🐛 High error rate detected - implement better error handling")
        
        if analysis.get('bottlenecks'):
            recommendations.append(f"⚡ {len(analysis['bottlenecks'])} performance bottlenecks identified")
        
        return recommendations

class ErrorAnalyzer:
    """Analyzes error patterns and trends"""
    
    def __init__(self):
        self.error_categories = {
            'javascript_error': ['TypeError', 'ReferenceError', 'SyntaxError'],
            'network_error': ['Failed to fetch', 'NetworkError', 'CORS'],
            'ui_error': ['Element not found', 'Invalid selector', 'DOM'],
            'validation_error': ['Invalid input', 'Required field', 'Format']
        }
    
    def analyze_errors(self, sessions: List[UserSession]) -> Dict[str, Any]:
        """Analyze error patterns"""
        analysis = {
            'error_summary': {},
            'error_trends': {},
            'critical_errors': [],
            'error_impact': {},
            'recommendations': []
        }
        
        try:
            # Collect all errors
            all_errors = []
            for session in sessions:
                all_errors.extend(session.errors)
            
            if not all_errors:
                return analysis
            
            # Error summary
            error_counts = Counter(error['data'].get('message', 'Unknown') for error in all_errors)
            analysis['error_summary'] = {
                'total_errors': len(all_errors),
                'unique_errors': len(error_counts),
                'most_common_errors': error_counts.most_common(5)
            }
            
            # Categorize errors
            categorized_errors = self._categorize_errors(all_errors)
            analysis['error_trends'] = categorized_errors
            
            # Identify critical errors
            analysis['critical_errors'] = self._identify_critical_errors(sessions, all_errors)
            
            # Analyze error impact on user sessions
            analysis['error_impact'] = self._analyze_error_impact(sessions)
            
            # Generate recommendations
            analysis['recommendations'] = self._generate_error_recommendations(analysis)
            
        except Exception as e:
            logger.error(f"Error analysis failed: {e}")
            
        return analysis
    
    def _categorize_errors(self, errors: List[Dict[str, Any]]) -> Dict[str, int]:
        """Categorize errors by type"""
        categories = defaultdict(int)
        
        for error in errors:
            message = error['data'].get('message', '').lower()
            categorized = False
            
            for category, keywords in self.error_categories.items():
                if any(keyword.lower() in message for keyword in keywords):
                    categories[category] += 1
                    categorized = True
                    break
            
            if not categorized:
                categories['unknown'] += 1
        
        return dict(categories)
    
    def _identify_critical_errors(self, sessions: List[UserSession], 
                                 errors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify critical errors that impact user experience"""
        critical_errors = []
        
        # Errors that cause session termination
        for session in sessions:
            if session.errors and len(session.events) <= 3:  # Session ended soon after error
                for error in session.errors:
                    critical_errors.append({
                        'type': 'session_terminating',
                        'message': error['data'].get('message', 'Unknown'),
                        'session_id': session.session_id,
                        'severity': 'critical'
                    })
        
        # Frequently occurring errors
        error_counts = Counter(error['data'].get('message', 'Unknown') for error in errors)
        for error_msg, count in error_counts.items():
            if count > len(sessions) * 0.1:  # Affects > 10% of sessions
                critical_errors.append({
                    'type': 'high_frequency',
                    'message': error_msg,
                    'frequency': count,
                    'severity': 'high'
                })
        
        return critical_errors
    
    def _analyze_error_impact(self, sessions: List[UserSession]) -> Dict[str, Any]:
        """Analyze how errors impact user behavior"""
        impact = {
            'sessions_with_errors': 0,
            'avg_duration_with_errors': 0,
            'avg_duration_without_errors': 0,
            'bounce_rate_with_errors': 0
        }
        
        sessions_with_errors = [s for s in sessions if s.errors]
        sessions_without_errors = [s for s in sessions if not s.errors]
        
        impact['sessions_with_errors'] = len(sessions_with_errors)
        
        if sessions_with_errors:
            impact['avg_duration_with_errors'] = statistics.mean([
                s.get_duration() for s in sessions_with_errors
            ])
            
            # Calculate bounce rate (sessions < 30 seconds)
            bounce_sessions = [s for s in sessions_with_errors if s.get_duration() < 30]
            impact['bounce_rate_with_errors'] = len(bounce_sessions) / len(sessions_with_errors) * 100
        
        if sessions_without_errors:
            impact['avg_duration_without_errors'] = statistics.mean([
                s.get_duration() for s in sessions_without_errors
            ])
        
        return impact
    
    def _generate_error_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate error handling recommendations"""
        recommendations = []
        
        summary = analysis.get('error_summary', {})
        
        if summary.get('total_errors', 0) > 0:
            recommendations.append(f"🐛 Address {summary['total_errors']} errors detected")
        
        if analysis.get('critical_errors'):
            recommendations.append(f"🚨 {len(analysis['critical_errors'])} critical errors need immediate attention")
        
        error_trends = analysis.get('error_trends', {})
        if error_trends.get('javascript_error', 0) > 0:
            recommendations.append("⚡ JavaScript errors detected - review code quality")
        
        if error_trends.get('network_error', 0) > 0:
            recommendations.append("🌐 Network errors found - improve error handling for API calls")
        
        return recommendations

class InsightGenerator:
    """Generates intelligent insights from analytics data"""
    
    def __init__(self):
        self.insight_templates = self._load_insight_templates()
        
    def _load_insight_templates(self) -> Dict[str, str]:
        """Load insight generation templates"""
        return {
            'high_bounce_rate': "High bounce rate detected on {page} - consider improving content or user experience",
            'conversion_opportunity': "Users spending {avg_time} minutes show {conversion_rate}% higher conversion rates",
            'performance_impact': "Pages loading in under {threshold}s have {engagement_boost}% better engagement",
            'user_flow_issue': "Drop-off rate of {rate}% between {page1} and {page2} indicates navigation issues",
            'error_correlation': "Sessions with {error_type} errors have {impact}% lower engagement"
        }
    
    def generate_insights(self, behavior_analysis: Dict[str, Any], 
                         performance_analysis: Dict[str, Any],
                         error_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate actionable insights"""
        insights = []
        
        try:
            # User behavior insights
            insights.extend(self._generate_behavior_insights(behavior_analysis))
            
            # Performance insights
            insights.extend(self._generate_performance_insights(performance_analysis))
            
            # Error insights
            insights.extend(self._generate_error_insights(error_analysis))
            
            # Cross-analysis insights
            insights.extend(self._generate_correlation_insights(
                behavior_analysis, performance_analysis, error_analysis
            ))
            
        except Exception as e:
            logger.error(f"Insight generation failed: {e}")
            
        return insights
    
    def _generate_behavior_insights(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate behavior-based insights"""
        insights = []
        
        segments = analysis.get('user_segments', {})
        
        if segments.get('bounce_users', 0) > segments.get('highly_engaged', 0):
            insights.append({
                'type': 'user_behavior',
                'priority': 'high',
                'title': 'High Bounce Rate Concern',
                'description': f"Bounce users ({segments['bounce_users']}) exceed engaged users ({segments.get('highly_engaged', 0)})",
                'recommendation': "Improve landing page content and reduce initial load time",
                'impact': 'user_retention'
            })
        
        if analysis.get('engagement_score', 0) < 50:
            insights.append({
                'type': 'user_behavior',
                'priority': 'medium',
                'title': 'Low User Engagement',
                'description': f"Average engagement score is {analysis['engagement_score']:.1f}/100",
                'recommendation': "Add more interactive elements and improve content quality",
                'impact': 'user_engagement'
            })
        
        return insights
    
    def _generate_performance_insights(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate performance-based insights"""
        insights = []
        
        summary = analysis.get('performance_summary', {})
        
        if summary.get('avg_load_time', 0) > 3:
            insights.append({
                'type': 'performance',
                'priority': 'high',
                'title': 'Slow Page Load Times',
                'description': f"Average load time is {summary['avg_load_time']:.2f}s",
                'recommendation': "Optimize images, enable compression, and implement caching",
                'impact': 'user_experience'
            })
        
        if summary.get('slow_pages_percent', 0) > 25:
            insights.append({
                'type': 'performance',
                'priority': 'medium',
                'title': 'Multiple Slow Pages',
                'description': f"{summary['slow_pages_percent']:.1f}% of pages load slowly",
                'recommendation': "Implement code splitting and lazy loading",
                'impact': 'overall_performance'
            })
        
        return insights
    
    def _generate_error_insights(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate error-based insights"""
        insights = []
        
        summary = analysis.get('error_summary', {})
        
        if summary.get('total_errors', 0) > 0:
            insights.append({
                'type': 'error_handling',
                'priority': 'high' if summary['total_errors'] > 10 else 'medium',
                'title': 'Error Rate Concern',
                'description': f"{summary['total_errors']} errors across {summary.get('unique_errors', 0)} types",
                'recommendation': "Implement comprehensive error tracking and handling",
                'impact': 'stability'
            })
        
        if analysis.get('critical_errors'):
            insights.append({
                'type': 'error_handling',
                'priority': 'critical',
                'title': 'Critical Errors Detected',
                'description': f"{len(analysis['critical_errors'])} critical errors affecting user sessions",
                'recommendation': "Immediate investigation and fixes required",
                'impact': 'user_retention'
            })
        
        return insights
    
    def _generate_correlation_insights(self, behavior_analysis: Dict[str, Any],
                                     performance_analysis: Dict[str, Any],
                                     error_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate insights from cross-analysis correlations"""
        insights = []
        
        # Performance-Behavior correlation
        avg_load_time = performance_analysis.get('performance_summary', {}).get('avg_load_time', 0)
        engagement_score = behavior_analysis.get('engagement_score', 0)
        
        if avg_load_time > 3 and engagement_score < 60:
            insights.append({
                'type': 'correlation',
                'priority': 'high',
                'title': 'Performance-Engagement Correlation',
                'description': f"Slow load times ({avg_load_time:.1f}s) correlate with low engagement ({engagement_score:.1f})",
                'recommendation': "Prioritize performance optimization to improve user engagement",
                'impact': 'conversion_rate'
            })
        
        # Error-Behavior correlation
        error_impact = error_analysis.get('error_impact', {})
        if (error_impact.get('avg_duration_with_errors', 0) < 
            error_impact.get('avg_duration_without_errors', 0) * 0.5):
            insights.append({
                'type': 'correlation',
                'priority': 'high',
                'title': 'Errors Significantly Impact Session Duration',
                'description': "Sessions with errors are 50% shorter than error-free sessions",
                'recommendation': "Implement proactive error prevention and graceful error handling",
                'impact': 'user_retention'
            })
        
        return insights

class AdvancedAnalyticsPlatform:
    """Main Advanced Analytics Platform orchestrator"""
    
    def __init__(self):
        self.event_tracker = EventTracker()
        self.behavior_analyzer = BehaviorAnalyzer()
        self.performance_analyzer = PerformanceAnalyzer()
        self.error_analyzer = ErrorAnalyzer()
        self.insight_generator = InsightGenerator()
        self.db_path = "analytics_platform.db"
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Initialize analytics database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    app_id TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    duration REAL,
                    events_count INTEGER,
                    page_views INTEGER,
                    interactions INTEGER,
                    errors INTEGER,
                    engagement_score REAL
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    event_id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    data TEXT NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES user_sessions (session_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analytics_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    app_id TEXT NOT NULL,
                    report_type TEXT NOT NULL,
                    generated_at TEXT NOT NULL,
                    data TEXT NOT NULL,
                    insights TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS insights (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    app_id TEXT NOT NULL,
                    insight_type TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    recommendation TEXT NOT NULL,
                    impact TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    status TEXT DEFAULT 'active'
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info("📊 Analytics Platform database initialized")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
    
    async def generate_comprehensive_report(self, app_id: str) -> Dict[str, Any]:
        """Generate comprehensive analytics report"""
        logger.info(f"📊 Generating comprehensive analytics report for {app_id}")
        
        report = {
            'app_id': app_id,
            'generated_at': datetime.now().isoformat(),
            'behavior_analysis': {},
            'performance_analysis': {},
            'error_analysis': {},
            'insights': [],
            'summary': {},
            'recommendations': []
        }
        
        try:
            # Get recent sessions for analysis
            sessions = await self._get_recent_sessions(app_id)
            
            if not sessions:
                # Generate demo data for testing
                sessions = self._generate_demo_sessions(app_id)
            
            # Run analyses
            report['behavior_analysis'] = self.behavior_analyzer.analyze_user_journey(sessions)
            report['performance_analysis'] = self.performance_analyzer.analyze_performance_data(sessions)
            report['error_analysis'] = self.error_analyzer.analyze_errors(sessions)
            
            # Generate insights
            report['insights'] = self.insight_generator.generate_insights(
                report['behavior_analysis'],
                report['performance_analysis'], 
                report['error_analysis']
            )
            
            # Create summary
            report['summary'] = self._create_report_summary(report)
            
            # Consolidate recommendations
            report['recommendations'] = self._consolidate_recommendations(report)
            
            # Save report to database
            await self._save_report(report)
            
            logger.info(f"✅ Analytics report generated with {len(report['insights'])} insights")
            
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            report['error'] = str(e)
            
        return report
    
    async def _get_recent_sessions(self, app_id: str) -> List[UserSession]:
        """Get recent user sessions from database"""
        sessions = []
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get sessions from last 7 days
            week_ago = (datetime.now() - timedelta(days=7)).isoformat()
            
            cursor.execute("""
                SELECT session_id, user_id, app_id, start_time, end_time, 
                       events_count, page_views, interactions, errors
                FROM user_sessions 
                WHERE app_id = ? AND start_time > ?
                ORDER BY start_time DESC
            """, (app_id, week_ago))
            
            for row in cursor.fetchall():
                session = UserSession(row[0], row[1], row[2])
                session.start_time = datetime.fromisoformat(row[3])
                if row[4]:
                    session.end_time = datetime.fromisoformat(row[4])
                
                # Load events for this session
                cursor.execute("""
                    SELECT event_type, timestamp, data 
                    FROM events 
                    WHERE session_id = ?
                    ORDER BY timestamp
                """, (row[0],))
                
                for event_row in cursor.fetchall():
                    event = {
                        'type': event_row[0],
                        'timestamp': event_row[1],
                        'data': json.loads(event_row[2])
                    }
                    session.events.append(event)
                    
                    # Categorize events
                    if event['type'] == 'page_view':
                        session.page_views.append(event)
                    elif event['type'] in ['click', 'scroll', 'form_submit']:
                        session.interactions.append(event)
                    elif event['type'] == 'error':
                        session.errors.append(event)
                
                sessions.append(session)
            
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to load sessions: {e}")
            
        return sessions
    
    def _generate_demo_sessions(self, app_id: str) -> List[UserSession]:
        """Generate demo sessions for testing"""
        sessions = []
        
        pages = ['home', 'about', 'contact', 'products', 'blog']
        
        for i in range(20):  # Generate 20 demo sessions
            user_id = f"demo_user_{i % 10}"  # 10 different users
            session = UserSession(f"demo_session_{i}", user_id, app_id)
            
            # Add realistic events
            session.add_event('session_start', {'referrer': 'google.com'})
            
            # Page views
            visited_pages = random.sample(pages, random.randint(1, 4))
            for page in visited_pages:
                session.add_event('page_view', {
                    'page': page,
                    'load_time': random.uniform(0.5, 5.0)
                })
            
            # Interactions
            for _ in range(random.randint(0, 8)):
                session.add_event('click', {
                    'element': random.choice(['button', 'link', 'menu']),
                    'page': random.choice(visited_pages)
                })
            
            # Occasional errors
            if random.random() < 0.2:  # 20% chance of error
                session.add_event('error', {
                    'message': random.choice([
                        'TypeError: Cannot read property',
                        'NetworkError: Failed to fetch',
                        'ReferenceError: undefined variable'
                    ])
                })
            
            # End session
            session.end_time = session.start_time + timedelta(seconds=random.randint(30, 600))
            session.add_event('session_end', {'duration': session.get_duration()})
            
            sessions.append(session)
        
        return sessions
    
    def _create_report_summary(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """Create executive summary of the report"""
        summary = {
            'total_sessions': 0,
            'avg_engagement': 0,
            'performance_score': 0,
            'error_rate': 0,
            'key_metrics': {},
            'top_insights': []
        }
        
        try:
            behavior = report.get('behavior_analysis', {})
            performance = report.get('performance_analysis', {})
            error_analysis = report.get('error_analysis', {})
            
            summary['total_sessions'] = behavior.get('total_sessions', 0)
            summary['avg_engagement'] = behavior.get('engagement_score', 0)
            
            # Calculate performance score
            perf_summary = performance.get('performance_summary', {})
            load_time = perf_summary.get('avg_load_time', 0)
            performance_score = max(0, 100 - (load_time - 1) * 20)  # Score based on load time
            summary['performance_score'] = performance_score
            
            # Error rate
            error_summary = error_analysis.get('error_summary', {})
            if summary['total_sessions'] > 0:
                summary['error_rate'] = error_summary.get('total_errors', 0) / summary['total_sessions'] * 100
            
            # Key metrics
            summary['key_metrics'] = {
                'avg_session_duration': behavior.get('avg_session_duration', 0),
                'bounce_rate': behavior.get('user_segments', {}).get('bounce_users', 0) / max(1, summary['total_sessions']) * 100,
                'avg_load_time': load_time,
                'total_errors': error_summary.get('total_errors', 0)
            }
            
            # Top insights
            insights = report.get('insights', [])
            high_priority = [i for i in insights if i.get('priority') in ['critical', 'high']]
            summary['top_insights'] = high_priority[:5]  # Top 5 high-priority insights
            
        except Exception as e:
            logger.error(f"Summary creation failed: {e}")
            
        return summary
    
    def _consolidate_recommendations(self, report: Dict[str, Any]) -> List[str]:
        """Consolidate recommendations from all analyses"""
        recommendations = []
        
        # From behavior analysis
        behavior = report.get('behavior_analysis', {})
        if behavior.get('engagement_score', 0) < 60:
            recommendations.append("📈 Improve user engagement through interactive content and better UX")
        
        # From performance analysis
        performance = report.get('performance_analysis', {})
        perf_recs = performance.get('recommendations', [])
        recommendations.extend(perf_recs)
        
        # From error analysis
        error_analysis = report.get('error_analysis', {})
        error_recs = error_analysis.get('recommendations', [])
        recommendations.extend(error_recs)
        
        # From insights
        insights = report.get('insights', [])
        critical_insights = [i for i in insights if i.get('priority') == 'critical']
        for insight in critical_insights:
            recommendations.append(f"🚨 {insight['recommendation']}")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec not in seen:
                seen.add(rec)
                unique_recommendations.append(rec)
        
        return unique_recommendations[:10]  # Top 10 recommendations
    
    async def _save_report(self, report: Dict[str, Any]):
        """Save analytics report to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO analytics_reports (app_id, report_type, generated_at, data, insights)
                VALUES (?, ?, ?, ?, ?)
            """, (
                report['app_id'],
                'comprehensive',
                report['generated_at'],
                json.dumps(report),
                json.dumps(report['insights'])
            ))
            
            # Save insights
            for insight in report['insights']:
                cursor.execute("""
                    INSERT INTO insights 
                    (app_id, insight_type, priority, title, description, recommendation, impact, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    report['app_id'],
                    insight.get('type', 'general'),
                    insight.get('priority', 'medium'),
                    insight.get('title', ''),
                    insight.get('description', ''),
                    insight.get('recommendation', ''),
                    insight.get('impact', ''),
                    datetime.now().isoformat()
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to save report: {e}")
    
    async def get_analytics_dashboard(self) -> Dict[str, Any]:
        """Get analytics dashboard data"""
        dashboard = {
            'overview': {},
            'recent_reports': [],
            'trending_insights': [],
            'performance_metrics': {}
        }
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Overall statistics
            cursor.execute("SELECT COUNT(*) FROM user_sessions")
            total_sessions = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT app_id) FROM user_sessions")
            tracked_apps = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM insights WHERE status = 'active'")
            active_insights = cursor.fetchone()[0]
            
            dashboard['overview'] = {
                'total_sessions': total_sessions,
                'tracked_apps': tracked_apps,
                'active_insights': active_insights
            }
            
            # Recent reports
            cursor.execute("""
                SELECT app_id, report_type, generated_at 
                FROM analytics_reports 
                ORDER BY generated_at DESC 
                LIMIT 10
            """)
            
            for row in cursor.fetchall():
                dashboard['recent_reports'].append({
                    'app_id': row[0],
                    'report_type': row[1],
                    'generated_at': row[2]
                })
            
            conn.close()
            
        except Exception as e:
            logger.error(f"Dashboard generation failed: {e}")
            
        return dashboard

# Main execution
async def main():
    """Main function to demonstrate Advanced Analytics Platform"""
    platform = AdvancedAnalyticsPlatform()
    
    print("📊 Advanced Analytics Platform Demo")
    print("=" * 50)
    
    # Generate demo report
    app_id = "demo_app_001"
    print(f"📈 Generating analytics report for: {app_id}")
    
    report = await platform.generate_comprehensive_report(app_id)
    
    print(f"\n📊 Analytics Report Summary:")
    summary = report['summary']
    print(f"   Total Sessions: {summary['total_sessions']}")
    print(f"   Avg Engagement: {summary['avg_engagement']:.1f}/100")
    print(f"   Performance Score: {summary['performance_score']:.1f}/100")
    print(f"   Error Rate: {summary['error_rate']:.1f}%")
    
    print(f"\n💡 Key Insights ({len(report['insights'])}):")
    for i, insight in enumerate(report['insights'][:3], 1):
        print(f"   {i}. [{insight['priority'].upper()}] {insight['title']}")
    
    print(f"\n🔧 Top Recommendations:")
    for i, rec in enumerate(report['recommendations'][:3], 1):
        print(f"   {i}. {rec}")
    
    # Get dashboard
    dashboard = await platform.get_analytics_dashboard()
    print(f"\n📈 Platform Overview:")
    print(f"   Tracked Apps: {dashboard['overview']['tracked_apps']}")
    print(f"   Total Sessions: {dashboard['overview']['total_sessions']}")
    print(f"   Active Insights: {dashboard['overview']['active_insights']}")
    
    print("\n✨ Advanced Analytics Platform initialized successfully!")

if __name__ == "__main__":
    asyncio.run(main())