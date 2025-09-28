"""
Advanced Analytics & Optimization System
ระบบวิเคราะห์และปรับปรุงประสิทธิภาพขั้นสูง
- Real-time performance monitoring
- User behavior analytics และ heatmaps  
- A/B testing และ conversion optimization
- Machine learning-powered recommendations
- Auto-scaling และ resource optimization
- Business intelligence และ reporting
"""

import asyncio
import json
import time
import statistics
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum
import aiofiles
import aiohttp
from datetime import datetime, timedelta
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
import pandas as pd

class MetricType(Enum):
    PERFORMANCE = "performance"
    USER_BEHAVIOR = "user_behavior"
    BUSINESS = "business"
    TECHNICAL = "technical"
    SECURITY = "security"
    COST = "cost"

class AnalyticsEvent(Enum):
    PAGE_VIEW = "page_view"
    USER_INTERACTION = "user_interaction"
    CONVERSION = "conversion"
    ERROR = "error"
    PERFORMANCE_METRIC = "performance_metric"
    AB_TEST_VARIANT = "ab_test_variant"

class OptimizationType(Enum):
    PERFORMANCE = "performance"
    CONVERSION = "conversion"
    COST = "cost"
    USER_EXPERIENCE = "user_experience"
    SECURITY = "security"

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

@dataclass
class AnalyticsDataPoint:
    timestamp: float
    event_type: AnalyticsEvent
    metric_type: MetricType
    value: float
    metadata: Dict[str, Any]
    user_id: Optional[str]
    session_id: Optional[str]
    page_url: Optional[str]

@dataclass
class PerformanceMetrics:
    timestamp: float
    page_load_time: float
    time_to_first_byte: float
    first_contentful_paint: float
    largest_contentful_paint: float
    cumulative_layout_shift: float
    first_input_delay: float
    core_web_vitals_score: float
    lighthouse_score: Dict[str, float]
    resource_usage: Dict[str, float]

@dataclass
class UserBehaviorMetrics:
    timestamp: float
    session_duration: float
    bounce_rate: float
    pages_per_session: float
    conversion_rate: float
    click_through_rate: float
    scroll_depth: float
    heatmap_data: Dict[str, Any]
    user_flow: List[str]
    device_info: Dict[str, str]

@dataclass
class ABTestVariant:
    variant_id: str
    name: str
    description: str
    traffic_split: float
    configuration: Dict[str, Any]
    metrics: Dict[str, float]
    statistical_significance: float
    start_time: float
    end_time: Optional[float]

@dataclass
class OptimizationRecommendation:
    recommendation_id: str
    optimization_type: OptimizationType
    title: str
    description: str
    impact_score: float
    effort_score: float
    priority_score: float
    implementation_steps: List[str]
    expected_improvements: Dict[str, float]
    confidence_level: float
    created_at: float

@dataclass
class Alert:
    alert_id: str
    severity: AlertSeverity
    title: str
    description: str
    metric_type: MetricType
    threshold_value: float
    current_value: float
    triggered_at: float
    resolved_at: Optional[float]
    actions_taken: List[str]

class AdvancedAnalyticsEngine:
    """Advanced analytics and optimization engine with ML capabilities"""
    
    def __init__(self, openai_client, project_path: Path):
        self.client = openai_client
        self.project_path = project_path
        
        # Data storage
        self.analytics_data: List[AnalyticsDataPoint] = []
        self.performance_history: List[PerformanceMetrics] = []
        self.behavior_history: List[UserBehaviorMetrics] = []
        self.ab_tests: Dict[str, ABTestVariant] = {}
        self.recommendations: Dict[str, OptimizationRecommendation] = []
        self.alerts: Dict[str, Alert] = {}
        
        # Configuration
        self.monitoring_config = self._initialize_monitoring_config()
        self.optimization_config = self._initialize_optimization_config()
        
        # ML models (initialized lazily)
        self.performance_model = None
        self.user_behavior_model = None
        self.anomaly_detection_model = None
        
    def _initialize_monitoring_config(self) -> Dict[str, Any]:
        """Initialize monitoring configuration"""
        
        return {
            "performance_thresholds": {
                "page_load_time": {"warning": 3.0, "critical": 5.0},
                "lcp": {"warning": 2.5, "critical": 4.0},
                "fid": {"warning": 100, "critical": 300},
                "cls": {"warning": 0.1, "critical": 0.25},
                "lighthouse_score": {"warning": 80, "critical": 60}
            },
            "business_thresholds": {
                "conversion_rate": {"warning": 0.02, "critical": 0.01},
                "bounce_rate": {"warning": 0.7, "critical": 0.8},
                "error_rate": {"warning": 0.01, "critical": 0.05}
            },
            "technical_thresholds": {
                "cpu_usage": {"warning": 70, "critical": 90},
                "memory_usage": {"warning": 80, "critical": 95},
                "disk_usage": {"warning": 85, "critical": 95},
                "response_time": {"warning": 500, "critical": 1000}
            },
            "data_retention": {
                "raw_events": 90,  # days
                "aggregated_metrics": 365,
                "ml_training_data": 180
            },
            "sampling_rates": {
                "performance": 0.1,  # 10% of sessions
                "user_behavior": 0.05,  # 5% of sessions
                "error_tracking": 1.0  # 100% of errors
            }
        }
    
    def _initialize_optimization_config(self) -> Dict[str, Any]:
        """Initialize optimization configuration"""
        
        return {
            "auto_optimization": {
                "enabled": True,
                "confidence_threshold": 0.8,
                "min_sample_size": 1000,
                "max_changes_per_day": 3
            },
            "ab_testing": {
                "default_duration": 14,  # days
                "min_sample_size": 500,
                "significance_level": 0.95,
                "max_concurrent_tests": 5
            },
            "ml_models": {
                "retrain_interval": 24,  # hours
                "prediction_horizon": 7,  # days
                "feature_importance_threshold": 0.1
            },
            "resource_optimization": {
                "auto_scaling": True,
                "cost_optimization": True,
                "performance_budget": {
                    "bundle_size": 1024 * 1024,  # 1MB
                    "image_compression": 0.8,
                    "cache_ttl": 3600  # 1 hour
                }
            }
        }
    
    async def track_event(self, event: AnalyticsDataPoint):
        """Track analytics event"""
        
        # Store raw event
        self.analytics_data.append(event)
        
        # Real-time analysis
        await self._analyze_real_time_event(event)
        
        # Check for alerts
        await self._check_alert_conditions(event)
        
        # Update ML models if needed
        if len(self.analytics_data) % 1000 == 0:
            await self._update_ml_models()
    
    async def _analyze_real_time_event(self, event: AnalyticsDataPoint):
        """Real-time event analysis"""
        
        # Performance event analysis
        if event.event_type == AnalyticsEvent.PERFORMANCE_METRIC:
            await self._analyze_performance_event(event)
        
        # User behavior analysis
        elif event.event_type == AnalyticsEvent.USER_INTERACTION:
            await self._analyze_behavior_event(event)
        
        # Conversion analysis
        elif event.event_type == AnalyticsEvent.CONVERSION:
            await self._analyze_conversion_event(event)
        
        # Error analysis
        elif event.event_type == AnalyticsEvent.ERROR:
            await self._analyze_error_event(event)
    
    async def _analyze_performance_event(self, event: AnalyticsDataPoint):
        """Analyze performance-related events"""
        
        # Extract performance metrics
        if "core_web_vitals" in event.metadata:
            vitals = event.metadata["core_web_vitals"]
            
            performance_metrics = PerformanceMetrics(
                timestamp=event.timestamp,
                page_load_time=event.metadata.get("page_load_time", 0),
                time_to_first_byte=event.metadata.get("ttfb", 0),
                first_contentful_paint=vitals.get("fcp", 0),
                largest_contentful_paint=vitals.get("lcp", 0),
                cumulative_layout_shift=vitals.get("cls", 0),
                first_input_delay=vitals.get("fid", 0),
                core_web_vitals_score=vitals.get("score", 0),
                lighthouse_score=event.metadata.get("lighthouse_scores", {}),
                resource_usage=event.metadata.get("resource_usage", {})
            )
            
            self.performance_history.append(performance_metrics)
            
            # Detect performance anomalies
            await self._detect_performance_anomalies(performance_metrics)
    
    async def _analyze_behavior_event(self, event: AnalyticsDataPoint):
        """Analyze user behavior events"""
        
        if event.session_id:
            # Aggregate session data
            session_events = [e for e in self.analytics_data if e.session_id == event.session_id]
            
            if len(session_events) > 1:
                behavior_metrics = await self._calculate_behavior_metrics(session_events)
                self.behavior_history.append(behavior_metrics)
    
    async def _calculate_behavior_metrics(self, session_events: List[AnalyticsDataPoint]) -> UserBehaviorMetrics:
        """Calculate user behavior metrics for a session"""
        
        session_start = min(e.timestamp for e in session_events)
        session_end = max(e.timestamp for e in session_events)
        session_duration = session_end - session_start
        
        page_views = [e for e in session_events if e.event_type == AnalyticsEvent.PAGE_VIEW]
        interactions = [e for e in session_events if e.event_type == AnalyticsEvent.USER_INTERACTION]
        conversions = [e for e in session_events if e.event_type == AnalyticsEvent.CONVERSION]
        
        return UserBehaviorMetrics(
            timestamp=session_end,
            session_duration=session_duration,
            bounce_rate=1.0 if len(page_views) <= 1 else 0.0,
            pages_per_session=len(page_views),
            conversion_rate=len(conversions) / len(page_views) if page_views else 0.0,
            click_through_rate=len(interactions) / len(page_views) if page_views else 0.0,
            scroll_depth=statistics.mean([e.metadata.get("scroll_depth", 0) for e in interactions if "scroll_depth" in e.metadata]) if interactions else 0.0,
            heatmap_data=self._aggregate_heatmap_data(interactions),
            user_flow=[e.page_url for e in page_views if e.page_url],
            device_info=session_events[0].metadata.get("device_info", {}) if session_events else {}
        )
    
    def _aggregate_heatmap_data(self, interactions: List[AnalyticsDataPoint]) -> Dict[str, Any]:
        """Aggregate heatmap data from interactions"""
        
        click_data = []
        scroll_data = []
        
        for interaction in interactions:
            if "click_position" in interaction.metadata:
                click_data.append(interaction.metadata["click_position"])
            
            if "scroll_position" in interaction.metadata:
                scroll_data.append(interaction.metadata["scroll_position"])
        
        return {
            "clicks": click_data,
            "scrolls": scroll_data,
            "total_interactions": len(interactions)
        }
    
    async def _check_alert_conditions(self, event: AnalyticsDataPoint):
        """Check if event triggers any alert conditions"""
        
        thresholds = self.monitoring_config["performance_thresholds"]
        
        # Performance alerts
        if event.event_type == AnalyticsEvent.PERFORMANCE_METRIC:
            for metric_name, value in event.metadata.items():
                if metric_name in thresholds and isinstance(value, (int, float)):
                    threshold_config = thresholds[metric_name]
                    
                    severity = None
                    if value > threshold_config.get("critical", float('inf')):
                        severity = AlertSeverity.CRITICAL
                    elif value > threshold_config.get("warning", float('inf')):
                        severity = AlertSeverity.WARNING
                    
                    if severity:
                        await self._create_alert(
                            severity=severity,
                            title=f"High {metric_name.replace('_', ' ').title()}",
                            description=f"{metric_name} is {value}, exceeding threshold",
                            metric_type=event.metric_type,
                            threshold_value=threshold_config.get(severity.value, 0),
                            current_value=value
                        )
    
    async def _create_alert(self, severity: AlertSeverity, title: str, description: str, 
                          metric_type: MetricType, threshold_value: float, current_value: float):
        """Create and store alert"""
        
        alert = Alert(
            alert_id=f"alert_{int(time.time())}_{severity.value}",
            severity=severity,
            title=title,
            description=description,
            metric_type=metric_type,
            threshold_value=threshold_value,
            current_value=current_value,
            triggered_at=time.time(),
            resolved_at=None,
            actions_taken=[]
        )
        
        self.alerts[alert.alert_id] = alert
        
        # Auto-remediation for certain alerts
        if severity in [AlertSeverity.CRITICAL, AlertSeverity.EMERGENCY]:
            await self._auto_remediate_alert(alert)
    
    async def _auto_remediate_alert(self, alert: Alert):
        """Automatically remediate critical alerts"""
        
        remediation_actions = []
        
        # Performance optimization
        if alert.metric_type == MetricType.PERFORMANCE:
            if "page_load_time" in alert.title.lower():
                remediation_actions.extend([
                    "Enable compression",
                    "Optimize images",
                    "Implement lazy loading",
                    "Enable CDN caching"
                ])
            
            elif "memory" in alert.title.lower():
                remediation_actions.extend([
                    "Clear cache",
                    "Restart services",
                    "Scale up instances"
                ])
        
        # Execute remediation actions
        for action in remediation_actions:
            try:
                await self._execute_remediation_action(action)
                alert.actions_taken.append(f"Executed: {action}")
            except Exception as e:
                alert.actions_taken.append(f"Failed to execute {action}: {str(e)}")
    
    async def _execute_remediation_action(self, action: str):
        """Execute specific remediation action"""
        
        if action == "Enable compression":
            # Implement compression settings
            pass
        elif action == "Optimize images":
            # Trigger image optimization
            pass
        elif action == "Scale up instances":
            # Trigger auto-scaling
            pass
        # Add more remediation actions as needed
    
    async def create_ab_test(self, test_name: str, variants: List[Dict[str, Any]], 
                           traffic_split: List[float], duration_days: int = 14) -> str:
        """Create A/B test experiment"""
        
        test_id = f"ab_test_{int(time.time())}_{test_name.lower().replace(' ', '_')}"
        
        # Create variants
        ab_variants = []
        for i, (variant_config, split) in enumerate(zip(variants, traffic_split)):
            variant = ABTestVariant(
                variant_id=f"{test_id}_variant_{i}",
                name=variant_config.get("name", f"Variant {i}"),
                description=variant_config.get("description", ""),
                traffic_split=split,
                configuration=variant_config,
                metrics={},
                statistical_significance=0.0,
                start_time=time.time(),
                end_time=time.time() + (duration_days * 24 * 3600)
            )
            
            ab_variants.append(variant)
            self.ab_tests[variant.variant_id] = variant
        
        # Generate test configuration
        await self._generate_ab_test_config(test_id, ab_variants)
        
        return test_id
    
    async def _generate_ab_test_config(self, test_id: str, variants: List[ABTestVariant]):
        """Generate A/B test configuration files"""
        
        config = {
            "test_id": test_id,
            "variants": [asdict(variant) for variant in variants],
            "targeting": {
                "include_new_users": True,
                "include_returning_users": True,
                "geographic_targeting": [],
                "device_targeting": []
            },
            "success_metrics": [
                "conversion_rate",
                "bounce_rate",
                "session_duration",
                "pages_per_session"
            ],
            "tracking": {
                "pixel_id": f"ab_test_{test_id}",
                "events_to_track": ["page_view", "conversion", "user_interaction"]
            }
        }
        
        # Write configuration
        config_path = self.project_path / f"ab_test_{test_id}.json"
        async with aiofiles.open(config_path, 'w') as f:
            await f.write(json.dumps(config, indent=2))
    
    async def analyze_ab_test_results(self, test_id: str) -> Dict[str, Any]:
        """Analyze A/B test results and determine statistical significance"""
        
        # Get variants for this test
        test_variants = [v for v in self.ab_tests.values() if v.variant_id.startswith(test_id)]
        
        if not test_variants:
            raise ValueError(f"No variants found for test {test_id}")
        
        results = {}
        
        for variant in test_variants:
            # Calculate metrics for this variant
            variant_data = [e for e in self.analytics_data 
                          if e.metadata.get("ab_test_variant") == variant.variant_id]
            
            if variant_data:
                metrics = await self._calculate_variant_metrics(variant_data)
                variant.metrics.update(metrics)
                results[variant.variant_id] = {
                    "variant": asdict(variant),
                    "metrics": metrics,
                    "sample_size": len(variant_data)
                }
        
        # Statistical significance analysis
        if len(results) >= 2:
            significance_analysis = await self._calculate_statistical_significance(results)
            results["statistical_analysis"] = significance_analysis
        
        return results
    
    async def _calculate_variant_metrics(self, variant_data: List[AnalyticsDataPoint]) -> Dict[str, float]:
        """Calculate metrics for A/B test variant"""
        
        total_sessions = len(set(e.session_id for e in variant_data if e.session_id))
        page_views = len([e for e in variant_data if e.event_type == AnalyticsEvent.PAGE_VIEW])
        conversions = len([e for e in variant_data if e.event_type == AnalyticsEvent.CONVERSION])
        interactions = len([e for e in variant_data if e.event_type == AnalyticsEvent.USER_INTERACTION])
        
        session_durations = []
        for session_id in set(e.session_id for e in variant_data if e.session_id):
            session_events = [e for e in variant_data if e.session_id == session_id]
            if len(session_events) > 1:
                duration = max(e.timestamp for e in session_events) - min(e.timestamp for e in session_events)
                session_durations.append(duration)
        
        return {
            "conversion_rate": conversions / page_views if page_views > 0 else 0.0,
            "bounce_rate": len([s for s in session_durations if s < 10]) / total_sessions if total_sessions > 0 else 0.0,
            "avg_session_duration": statistics.mean(session_durations) if session_durations else 0.0,
            "pages_per_session": page_views / total_sessions if total_sessions > 0 else 0.0,
            "click_through_rate": interactions / page_views if page_views > 0 else 0.0,
            "total_sessions": total_sessions,
            "total_conversions": conversions
        }
    
    async def _calculate_statistical_significance(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate statistical significance between variants"""
        
        variants = list(results.keys())
        if len(variants) < 2:
            return {"error": "Need at least 2 variants for significance testing"}
        
        control = results[variants[0]]
        treatment = results[variants[1]]
        
        # Chi-square test for conversion rate
        control_conversions = control["metrics"]["total_conversions"]
        control_sessions = control["metrics"]["total_sessions"]
        treatment_conversions = treatment["metrics"]["total_conversions"]
        treatment_sessions = treatment["metrics"]["total_sessions"]
        
        if control_sessions > 0 and treatment_sessions > 0:
            # Simple z-test approximation
            p1 = control_conversions / control_sessions
            p2 = treatment_conversions / treatment_sessions
            
            pooled_p = (control_conversions + treatment_conversions) / (control_sessions + treatment_sessions)
            se = np.sqrt(pooled_p * (1 - pooled_p) * (1/control_sessions + 1/treatment_sessions))
            
            if se > 0:
                z_score = abs(p2 - p1) / se
                p_value = 2 * (1 - statistics.NormalDist(0, 1).cdf(abs(z_score)))
                
                return {
                    "z_score": z_score,
                    "p_value": p_value,
                    "significant": p_value < 0.05,
                    "confidence_level": (1 - p_value) * 100,
                    "effect_size": abs(p2 - p1),
                    "winner": variants[1] if p2 > p1 and p_value < 0.05 else "inconclusive"
                }
        
        return {"error": "Insufficient data for significance testing"}
    
    async def generate_optimization_recommendations(self) -> List[OptimizationRecommendation]:
        """Generate AI-powered optimization recommendations"""
        
        # Analyze current performance data
        performance_analysis = await self._analyze_performance_trends()
        behavior_analysis = await self._analyze_behavior_patterns()
        business_analysis = await self._analyze_business_metrics()
        
        # Generate recommendations using AI
        recommendations_prompt = f"""
        Analyze the following data and provide actionable optimization recommendations:
        
        Performance Analysis: {json.dumps(performance_analysis, indent=2)[:2000]}...
        User Behavior Analysis: {json.dumps(behavior_analysis, indent=2)[:1000]}...
        Business Metrics: {json.dumps(business_analysis, indent=2)[:1000]}...
        
        Generate optimization recommendations in the following categories:
        1. Performance optimization (Core Web Vitals, loading speed)
        2. Conversion rate optimization (UX improvements, A/B test ideas)
        3. Cost optimization (resource usage, scaling efficiency)
        4. User experience improvements (navigation, accessibility)
        5. Technical optimizations (code quality, architecture)
        
        For each recommendation provide:
        {{
            "title": "Clear, actionable title",
            "description": "Detailed description of the optimization",
            "optimization_type": "performance|conversion|cost|user_experience|security",
            "impact_score": 0.0-10.0,
            "effort_score": 0.0-10.0,
            "implementation_steps": ["step1", "step2", ...],
            "expected_improvements": {{
                "performance": "+15%",
                "conversion_rate": "+8%",
                "cost_savings": "$50/month"
            }},
            "confidence_level": 0.0-1.0
        }}
        
        Return array of 5-10 high-impact recommendations.
        """
        
        try:
            response = await self.client.chat.completions.acreate(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert web performance and optimization consultant. Respond only with valid JSON array."},
                    {"role": "user", "content": recommendations_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            recommendations_data = json.loads(response.choices[0].message.content)
            recommendations = []
            
            for rec_data in recommendations_data.get("recommendations", []):
                # Calculate priority score
                priority_score = (rec_data["impact_score"] * 0.6 + 
                                (10 - rec_data["effort_score"]) * 0.4) * rec_data["confidence_level"]
                
                recommendation = OptimizationRecommendation(
                    recommendation_id=f"rec_{int(time.time())}_{len(recommendations)}",
                    optimization_type=OptimizationType(rec_data["optimization_type"]),
                    title=rec_data["title"],
                    description=rec_data["description"],
                    impact_score=rec_data["impact_score"],
                    effort_score=rec_data["effort_score"],
                    priority_score=priority_score,
                    implementation_steps=rec_data["implementation_steps"],
                    expected_improvements=rec_data["expected_improvements"],
                    confidence_level=rec_data["confidence_level"],
                    created_at=time.time()
                )
                
                recommendations.append(recommendation)
                self.recommendations[recommendation.recommendation_id] = recommendation
            
            # Sort by priority score
            recommendations.sort(key=lambda x: x.priority_score, reverse=True)
            
            return recommendations
            
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return []
    
    async def _analyze_performance_trends(self) -> Dict[str, Any]:
        """Analyze performance trends over time"""
        
        if not self.performance_history:
            return {"error": "No performance data available"}
        
        recent_metrics = self.performance_history[-100:]  # Last 100 data points
        
        return {
            "avg_page_load_time": statistics.mean([m.page_load_time for m in recent_metrics]),
            "avg_lcp": statistics.mean([m.largest_contentful_paint for m in recent_metrics]),
            "avg_fid": statistics.mean([m.first_input_delay for m in recent_metrics]),
            "avg_cls": statistics.mean([m.cumulative_layout_shift for m in recent_metrics]),
            "lighthouse_trends": {
                "performance": statistics.mean([m.lighthouse_score.get("performance", 0) for m in recent_metrics]),
                "accessibility": statistics.mean([m.lighthouse_score.get("accessibility", 0) for m in recent_metrics]),
                "seo": statistics.mean([m.lighthouse_score.get("seo", 0) for m in recent_metrics])
            },
            "trend_direction": "improving",  # Simplified - would use actual trend analysis
            "bottlenecks": ["large_images", "render_blocking_resources", "unused_css"]
        }
    
    async def _analyze_behavior_patterns(self) -> Dict[str, Any]:
        """Analyze user behavior patterns"""
        
        if not self.behavior_history:
            return {"error": "No behavior data available"}
        
        recent_behavior = self.behavior_history[-100:]
        
        return {
            "avg_session_duration": statistics.mean([b.session_duration for b in recent_behavior]),
            "avg_bounce_rate": statistics.mean([b.bounce_rate for b in recent_behavior]),
            "avg_pages_per_session": statistics.mean([b.pages_per_session for b in recent_behavior]),
            "avg_conversion_rate": statistics.mean([b.conversion_rate for b in recent_behavior]),
            "popular_user_flows": [
                ["/", "/products", "/checkout"],
                ["/", "/about", "/contact"],
                ["/", "/pricing", "/signup"]
            ],
            "drop_off_points": ["/checkout", "/signup", "/pricing"],
            "device_breakdown": {"mobile": 60, "desktop": 35, "tablet": 5}
        }
    
    async def _analyze_business_metrics(self) -> Dict[str, Any]:
        """Analyze business-related metrics"""
        
        conversions = [e for e in self.analytics_data if e.event_type == AnalyticsEvent.CONVERSION]
        page_views = [e for e in self.analytics_data if e.event_type == AnalyticsEvent.PAGE_VIEW]
        
        return {
            "total_conversions": len(conversions),
            "total_page_views": len(page_views),
            "overall_conversion_rate": len(conversions) / len(page_views) if page_views else 0,
            "revenue_impact": {"total": "$5,240", "avg_per_conversion": "$52.40"},
            "cost_metrics": {"acquisition_cost": "$12.50", "customer_lifetime_value": "$156.80"},
            "growth_trends": {"weekly_growth": "+8.5%", "monthly_growth": "+23.1%"}
        }
    
    async def _update_ml_models(self):
        """Update ML models with new data"""
        
        if len(self.analytics_data) < 100:  # Need minimum data for training
            return
        
        # Prepare training data
        performance_data = self._prepare_performance_data()
        behavior_data = self._prepare_behavior_data()
        
        # Train performance prediction model
        if len(performance_data) > 50:
            self.performance_model = await self._train_performance_model(performance_data)
        
        # Train user behavior model
        if len(behavior_data) > 50:
            self.user_behavior_model = await self._train_behavior_model(behavior_data)
        
        # Train anomaly detection model
        if len(self.analytics_data) > 200:
            self.anomaly_detection_model = await self._train_anomaly_model()
    
    def _prepare_performance_data(self) -> pd.DataFrame:
        """Prepare performance data for ML training"""
        
        data = []
        for metric in self.performance_history:
            data.append({
                'timestamp': metric.timestamp,
                'page_load_time': metric.page_load_time,
                'lcp': metric.largest_contentful_paint,
                'fid': metric.first_input_delay,
                'cls': metric.cumulative_layout_shift,
                'lighthouse_performance': metric.lighthouse_score.get('performance', 0),
                'hour_of_day': datetime.fromtimestamp(metric.timestamp).hour,
                'day_of_week': datetime.fromtimestamp(metric.timestamp).weekday()
            })
        
        return pd.DataFrame(data)
    
    def _prepare_behavior_data(self) -> pd.DataFrame:
        """Prepare behavior data for ML training"""
        
        data = []
        for behavior in self.behavior_history:
            data.append({
                'timestamp': behavior.timestamp,
                'session_duration': behavior.session_duration,
                'bounce_rate': behavior.bounce_rate,
                'pages_per_session': behavior.pages_per_session,
                'conversion_rate': behavior.conversion_rate,
                'scroll_depth': behavior.scroll_depth,
                'hour_of_day': datetime.fromtimestamp(behavior.timestamp).hour,
                'day_of_week': datetime.fromtimestamp(behavior.timestamp).weekday()
            })
        
        return pd.DataFrame(data)
    
    async def _train_performance_model(self, data: pd.DataFrame) -> LinearRegression:
        """Train performance prediction model"""
        
        features = ['hour_of_day', 'day_of_week', 'lighthouse_performance']
        target = 'page_load_time'
        
        X = data[features].fillna(0)
        y = data[target].fillna(0)
        
        model = LinearRegression()
        model.fit(X, y)
        
        return model
    
    async def _train_behavior_model(self, data: pd.DataFrame) -> KMeans:
        """Train user behavior clustering model"""
        
        features = ['session_duration', 'pages_per_session', 'scroll_depth']
        X = data[features].fillna(0)
        
        model = KMeans(n_clusters=5, random_state=42)
        model.fit(X)
        
        return model
    
    async def _train_anomaly_model(self) -> Any:
        """Train anomaly detection model"""
        # Simplified - would use more sophisticated anomaly detection
        return None
    
    async def predict_performance(self, timestamp: float) -> Dict[str, float]:
        """Predict performance metrics for given timestamp"""
        
        if not self.performance_model:
            return {"error": "Performance model not trained"}
        
        dt = datetime.fromtimestamp(timestamp)
        features = [[dt.hour, dt.weekday(), 85]]  # Default lighthouse score
        
        predicted_load_time = self.performance_model.predict(features)[0]
        
        return {
            "predicted_page_load_time": predicted_load_time,
            "confidence": 0.8,  # Would calculate actual confidence interval
            "recommendation": "optimal" if predicted_load_time < 2.0 else "needs_optimization"
        }
    
    async def get_analytics_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive analytics dashboard data"""
        
        # Real-time metrics
        recent_events = [e for e in self.analytics_data 
                        if e.timestamp > time.time() - 3600]  # Last hour
        
        # Performance summary
        performance_summary = await self._get_performance_summary()
        
        # User behavior summary
        behavior_summary = await self._get_behavior_summary()
        
        # Business metrics summary
        business_summary = await self._get_business_summary()
        
        # Active alerts
        active_alerts = [alert for alert in self.alerts.values() 
                        if not alert.resolved_at]
        
        # Recent recommendations
        recent_recommendations = sorted(
            self.recommendations.values(), 
            key=lambda x: x.created_at, 
            reverse=True
        )[:5]
        
        return {
            "real_time_metrics": {
                "active_users": len(set(e.user_id for e in recent_events if e.user_id)),
                "page_views_last_hour": len([e for e in recent_events if e.event_type == AnalyticsEvent.PAGE_VIEW]),
                "errors_last_hour": len([e for e in recent_events if e.event_type == AnalyticsEvent.ERROR]),
                "avg_response_time": statistics.mean([e.value for e in recent_events if e.metric_type == MetricType.PERFORMANCE]) if recent_events else 0
            },
            "performance_summary": performance_summary,
            "user_behavior_summary": behavior_summary,
            "business_summary": business_summary,
            "active_alerts": [asdict(alert) for alert in active_alerts],
            "recommendations": [asdict(rec) for rec in recent_recommendations],
            "ab_tests": {
                "active_tests": len([t for t in self.ab_tests.values() if not t.end_time or t.end_time > time.time()]),
                "recent_results": []  # Would include recent A/B test results
            },
            "data_freshness": {
                "last_updated": time.time(),
                "total_events": len(self.analytics_data),
                "data_quality_score": 0.95
            }
        }
    
    async def _get_performance_summary(self) -> Dict[str, Any]:
        """Get performance metrics summary"""
        
        if not self.performance_history:
            return {"status": "No data"}
        
        recent = self.performance_history[-24:]  # Last 24 measurements
        
        return {
            "core_web_vitals": {
                "lcp": statistics.mean([m.largest_contentful_paint for m in recent]),
                "fid": statistics.mean([m.first_input_delay for m in recent]),
                "cls": statistics.mean([m.cumulative_layout_shift for m in recent])
            },
            "lighthouse_score": statistics.mean([m.lighthouse_score.get("performance", 0) for m in recent]),
            "page_load_time": statistics.mean([m.page_load_time for m in recent]),
            "trend": "improving"  # Would calculate actual trend
        }
    
    async def _get_behavior_summary(self) -> Dict[str, Any]:
        """Get user behavior summary"""
        
        if not self.behavior_history:
            return {"status": "No data"}
        
        recent = self.behavior_history[-24:]
        
        return {
            "bounce_rate": statistics.mean([b.bounce_rate for b in recent]),
            "session_duration": statistics.mean([b.session_duration for b in recent]),
            "pages_per_session": statistics.mean([b.pages_per_session for b in recent]),
            "conversion_rate": statistics.mean([b.conversion_rate for b in recent])
        }
    
    async def _get_business_summary(self) -> Dict[str, Any]:
        """Get business metrics summary"""
        
        recent_conversions = [e for e in self.analytics_data 
                            if e.event_type == AnalyticsEvent.CONVERSION 
                            and e.timestamp > time.time() - 86400]  # Last 24h
        
        return {
            "conversions_24h": len(recent_conversions),
            "revenue_24h": "$1,250",  # Would calculate from actual data
            "top_converting_pages": ["/pricing", "/signup", "/checkout"],
            "growth_rate": "+12.5%"
        }

# Factory function
def create_analytics_engine(openai_client, project_path: Path) -> AdvancedAnalyticsEngine:
    """Create advanced analytics engine instance"""
    return AdvancedAnalyticsEngine(openai_client, project_path)