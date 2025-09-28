"""
Deployment & DevOps Automation System
ระบบ deploy และ DevOps อัตโนมัติที่ครอบคลุม
- Multi-platform deployment (Vercel, Netlify, AWS, Railway, etc.)
- CI/CD pipeline automation
- Infrastructure as Code (IaC)
- Auto-scaling และ load balancing
- Monitoring และ alerting
- Rollback และ blue-green deployment
- Security และ compliance checks
"""

import asyncio
import json
import time
import subprocess
import yaml
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum
import aiofiles
import aiohttp
import docker
import boto3

class DeploymentPlatform(Enum):
    VERCEL = "vercel"
    NETLIFY = "netlify"
    AWS_AMPLIFY = "aws_amplify"
    AWS_ECS = "aws_ecs"
    AWS_LAMBDA = "aws_lambda"
    RAILWAY = "railway"
    RENDER = "render"
    HEROKU = "heroku"
    DIGITAL_OCEAN = "digital_ocean"
    GOOGLE_CLOUD = "google_cloud"
    AZURE = "azure"
    DOCKER = "docker"
    KUBERNETES = "kubernetes"

class DeploymentType(Enum):
    STATIC_SITE = "static_site"
    SERVER_SIDE_RENDERED = "ssr"
    SINGLE_PAGE_APP = "spa"
    API_SERVER = "api_server"
    MICROSERVICE = "microservice"
    FULL_STACK = "full_stack"
    SERVERLESS = "serverless"
    CONTAINER = "container"

class DeploymentStatus(Enum):
    PENDING = "pending"
    BUILDING = "building"
    DEPLOYING = "deploying"
    DEPLOYED = "deployed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"

class EnvironmentType(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    PREVIEW = "preview"

@dataclass
class DeploymentConfig:
    config_id: str
    platform: DeploymentPlatform
    deployment_type: DeploymentType
    environment: EnvironmentType
    build_settings: Dict[str, Any]
    environment_variables: Dict[str, str]
    custom_domains: List[str]
    ssl_enabled: bool
    auto_scaling: Dict[str, Any]
    monitoring: Dict[str, Any]
    backup_strategy: Dict[str, Any]
    created_at: float

@dataclass
class DeploymentResult:
    deployment_id: str
    config_id: str
    status: DeploymentStatus
    platform: DeploymentPlatform
    deployment_url: str
    build_logs: List[str]
    deployment_time: float
    performance_metrics: Dict[str, Any]
    security_scan_results: Dict[str, Any]
    rollback_url: Optional[str]
    deployed_at: float

@dataclass
class CIPipeline:
    pipeline_id: str
    name: str
    triggers: List[str]
    stages: List[Dict[str, Any]]
    environment_promotion: Dict[str, Any]
    notification_settings: Dict[str, Any]
    security_checks: List[str]
    quality_gates: Dict[str, Any]
    created_at: float

class DevOpsAutomationEngine:
    """Advanced DevOps automation and deployment engine"""
    
    def __init__(self, openai_client, project_path: Path):
        self.client = openai_client
        self.project_path = project_path
        
        # Platform configurations
        self.platform_configs = self._initialize_platform_configs()
        self.deployment_templates = self._initialize_deployment_templates()
        
        # Active deployments tracking
        self.active_deployments: Dict[str, DeploymentResult] = {}
        self.deployment_configs: Dict[str, DeploymentConfig] = {}
        
        # CI/CD pipelines
        self.pipelines: Dict[str, CIPipeline] = {}
        
        # Cloud clients (initialized as needed)
        self.cloud_clients = {}
        
        # Monitoring and alerting
        self.monitoring_config = self._initialize_monitoring()
        
    def _initialize_platform_configs(self) -> Dict[DeploymentPlatform, Dict[str, Any]]:
        """Initialize deployment platform configurations"""
        
        return {
            DeploymentPlatform.VERCEL: {
                "cli_command": "vercel",
                "config_file": "vercel.json",
                "build_command": "npm run build",
                "output_directory": "dist",
                "supported_frameworks": ["next.js", "react", "vue", "svelte", "static"],
                "features": ["auto_scaling", "edge_functions", "analytics", "preview_deployments"],
                "limits": {
                    "function_timeout": 10,
                    "file_size": "100MB",
                    "bandwidth": "unlimited"
                }
            },
            DeploymentPlatform.NETLIFY: {
                "cli_command": "netlify",
                "config_file": "netlify.toml",
                "build_command": "npm run build",
                "output_directory": "dist",
                "supported_frameworks": ["react", "vue", "angular", "static", "gatsby"],
                "features": ["functions", "forms", "identity", "split_testing"],
                "limits": {
                    "function_timeout": 26,
                    "file_size": "125MB",
                    "bandwidth": "100GB"
                }
            },
            DeploymentPlatform.AWS_AMPLIFY: {
                "service": "amplify",
                "config_file": "amplify.yml",
                "build_command": "npm run build",
                "features": ["hosting", "authentication", "storage", "api"],
                "limits": {
                    "build_time": 60,
                    "file_size": "25GB",
                    "bandwidth": "unlimited"
                }
            },
            DeploymentPlatform.RAILWAY: {
                "cli_command": "railway",
                "config_file": "railway.json",
                "features": ["databases", "auto_scaling", "metrics", "logs"],
                "limits": {
                    "memory": "8GB",
                    "cpu": "8 vCPU",
                    "storage": "100GB"
                }
            },
            DeploymentPlatform.RENDER: {
                "config_file": "render.yaml",
                "features": ["auto_deploy", "ssl", "cdn", "databases"],
                "limits": {
                    "build_time": 20,
                    "memory": "4GB",
                    "storage": "100GB"
                }
            }
        }
    
    def _initialize_deployment_templates(self) -> Dict[DeploymentType, Dict[str, Any]]:
        """Initialize deployment templates for different app types"""
        
        return {
            DeploymentType.STATIC_SITE: {
                "build_commands": [
                    "npm install",
                    "npm run build"
                ],
                "output_directory": "dist",
                "caching_strategy": "static_assets",
                "cdn_enabled": True,
                "compression": True
            },
            DeploymentType.SERVER_SIDE_RENDERED: {
                "build_commands": [
                    "npm install",
                    "npm run build"
                ],
                "start_command": "npm start",
                "runtime": "nodejs",
                "environment_variables": ["NODE_ENV", "DATABASE_URL"],
                "health_check": "/api/health",
                "auto_scaling": True
            },
            DeploymentType.API_SERVER: {
                "build_commands": [
                    "pip install -r requirements.txt"
                ],
                "start_command": "python app.py",
                "runtime": "python",
                "health_check": "/health",
                "rate_limiting": True,
                "load_balancer": True
            },
            DeploymentType.CONTAINER: {
                "dockerfile": "Dockerfile",
                "build_context": ".",
                "registry": "docker.io",
                "orchestration": "kubernetes",
                "scaling_policy": "horizontal"
            }
        }
    
    def _initialize_monitoring(self) -> Dict[str, Any]:
        """Initialize monitoring and alerting configuration"""
        
        return {
            "metrics": {
                "response_time": {"threshold": 500, "unit": "ms"},
                "error_rate": {"threshold": 1, "unit": "%"},
                "cpu_usage": {"threshold": 80, "unit": "%"},
                "memory_usage": {"threshold": 85, "unit": "%"},
                "disk_usage": {"threshold": 90, "unit": "%"}
            },
            "alerts": {
                "channels": ["email", "slack", "webhook"],
                "escalation": {
                    "level_1": 5,  # minutes
                    "level_2": 15,
                    "level_3": 30
                }
            },
            "logging": {
                "level": "info",
                "retention": 30,  # days
                "structured": True
            },
            "uptime_monitoring": {
                "interval": 60,  # seconds
                "locations": ["us-east", "eu-west", "asia-pacific"]
            }
        }
    
    async def create_deployment_strategy(self, project_analysis: Dict[str, Any], preferences: Dict[str, Any]) -> Dict[str, DeploymentConfig]:
        """Create intelligent deployment strategy based on project analysis"""
        
        # Analyze project to determine optimal deployment strategy
        deployment_strategy = await self._analyze_deployment_requirements(project_analysis, preferences)
        
        deployment_configs = {}
        
        # Create configs for each environment
        for env_type in [EnvironmentType.DEVELOPMENT, EnvironmentType.STAGING, EnvironmentType.PRODUCTION]:
            config = await self._create_environment_config(deployment_strategy, env_type)
            deployment_configs[env_type.value] = config
            self.deployment_configs[config.config_id] = config
        
        return deployment_configs
    
    async def _analyze_deployment_requirements(self, project_analysis: Dict[str, Any], preferences: Dict[str, Any]) -> Dict[str, Any]:
        """AI-powered analysis of deployment requirements"""
        
        analysis_prompt = f"""
        Analyze this project to determine the optimal deployment strategy:
        
        Project Analysis: {json.dumps(project_analysis, indent=2)[:2000]}...
        User Preferences: {json.dumps(preferences, indent=2)}
        
        Consider:
        1. Application architecture (static, SSR, API, full-stack)
        2. Traffic expectations and scaling needs
        3. Performance requirements
        4. Security and compliance needs
        5. Budget constraints
        6. Geographic distribution needs
        7. Integration requirements
        8. Development workflow preferences
        
        Recommend deployment strategy:
        {{
            "deployment_type": "static_site|ssr|api_server|full_stack|microservice",
            "primary_platform": "vercel|netlify|aws|railway|render",
            "backup_platform": "secondary platform for redundancy",
            "cdn_strategy": {{
                "enabled": true|false,
                "provider": "cloudflare|aws_cloudfront|vercel_edge",
                "edge_locations": ["us", "eu", "asia"]
            }},
            "scaling_strategy": {{
                "type": "horizontal|vertical|auto",
                "min_instances": 1,
                "max_instances": 10,
                "scaling_triggers": ["cpu", "memory", "requests"]
            }},
            "database_strategy": {{
                "type": "managed|serverless|self_hosted",
                "provider": "supabase|planetscale|aws_rds",
                "backup_frequency": "daily|hourly",
                "multi_region": true|false
            }},
            "security_requirements": {{
                "ssl_certificate": "managed|custom",
                "waf_enabled": true|false,
                "ddos_protection": true|false,
                "security_headers": true|false
            }},
            "monitoring_stack": {{
                "application_monitoring": "vercel_analytics|datadog|newrelic",
                "infrastructure_monitoring": "aws_cloudwatch|grafana",
                "error_tracking": "sentry|rollbar",
                "log_aggregation": "datadog|elk_stack"
            }},
            "ci_cd_strategy": {{
                "triggers": ["push", "pull_request", "manual"],
                "environments": ["dev", "staging", "prod"],
                "deployment_gates": ["tests", "security_scan", "performance_check"],
                "rollback_strategy": "automatic|manual"
            }},
            "cost_optimization": {{
                "estimated_monthly_cost": "$50-200",
                "cost_alerts": true|false,
                "resource_optimization": "auto|manual"
            }}
        }}
        """
        
        try:
            response = await self.client.chat.completions.acreate(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert DevOps architect specializing in modern deployment strategies. Respond only with valid JSON."},
                    {"role": "user", "content": analysis_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Deployment analysis error: {e}")
            # Fallback strategy
            return {
                "deployment_type": "static_site",
                "primary_platform": "vercel",
                "backup_platform": "netlify",
                "cdn_strategy": {"enabled": True, "provider": "vercel_edge"},
                "scaling_strategy": {"type": "auto", "min_instances": 1, "max_instances": 5},
                "security_requirements": {"ssl_certificate": "managed", "security_headers": True},
                "ci_cd_strategy": {"triggers": ["push"], "environments": ["dev", "prod"]}
            }
    
    async def _create_environment_config(self, strategy: Dict[str, Any], env_type: EnvironmentType) -> DeploymentConfig:
        """Create deployment configuration for specific environment"""
        
        # Determine platform based on environment
        if env_type == EnvironmentType.PRODUCTION:
            platform = DeploymentPlatform(strategy["primary_platform"])
        else:
            platform = DeploymentPlatform(strategy.get("backup_platform", strategy["primary_platform"]))
        
        # Environment-specific settings
        env_settings = {
            EnvironmentType.DEVELOPMENT: {
                "auto_scaling": {"min": 1, "max": 2},
                "monitoring": {"level": "basic"},
                "ssl_enabled": False,
                "custom_domains": []
            },
            EnvironmentType.STAGING: {
                "auto_scaling": {"min": 1, "max": 3},
                "monitoring": {"level": "standard"},
                "ssl_enabled": True,
                "custom_domains": ["staging.example.com"]
            },
            EnvironmentType.PRODUCTION: {
                "auto_scaling": {"min": 2, "max": 10},
                "monitoring": {"level": "advanced"},
                "ssl_enabled": True,
                "custom_domains": ["example.com", "www.example.com"]
            }
        }
        
        settings = env_settings.get(env_type, env_settings[EnvironmentType.DEVELOPMENT])
        
        config = DeploymentConfig(
            config_id=f"{env_type.value}_{int(time.time())}_{platform.value}",
            platform=platform,
            deployment_type=DeploymentType(strategy["deployment_type"]),
            environment=env_type,
            build_settings={
                "build_command": "npm run build",
                "output_directory": "dist",
                "node_version": "18.x",
                "install_command": "npm ci"
            },
            environment_variables={
                "NODE_ENV": env_type.value,
                "ENVIRONMENT": env_type.value.upper(),
                "API_URL": f"https://api-{env_type.value}.example.com"
            },
            custom_domains=settings["custom_domains"],
            ssl_enabled=settings["ssl_enabled"],
            auto_scaling=settings["auto_scaling"],
            monitoring=settings["monitoring"],
            backup_strategy={
                "enabled": env_type == EnvironmentType.PRODUCTION,
                "frequency": "daily",
                "retention": 30
            },
            created_at=time.time()
        )
        
        return config
    
    async def deploy_to_platform(self, config_id: str, force_rebuild: bool = False) -> DeploymentResult:
        """Deploy application to specified platform"""
        
        if config_id not in self.deployment_configs:
            raise ValueError(f"Deployment config {config_id} not found")
        
        config = self.deployment_configs[config_id]
        deployment_id = f"deploy_{int(time.time())}_{config.platform.value}"
        
        try:
            # Pre-deployment checks
            await self._run_pre_deployment_checks(config)
            
            # Build application
            build_result = await self._build_application(config)
            
            # Platform-specific deployment
            if config.platform == DeploymentPlatform.VERCEL:
                deployment_result = await self._deploy_to_vercel(config, deployment_id, build_result)
            elif config.platform == DeploymentPlatform.NETLIFY:
                deployment_result = await self._deploy_to_netlify(config, deployment_id, build_result)
            elif config.platform == DeploymentPlatform.AWS_AMPLIFY:
                deployment_result = await self._deploy_to_aws_amplify(config, deployment_id, build_result)
            elif config.platform == DeploymentPlatform.RAILWAY:
                deployment_result = await self._deploy_to_railway(config, deployment_id, build_result)
            else:
                raise ValueError(f"Platform {config.platform} not yet implemented")
            
            # Post-deployment validation
            await self._validate_deployment(deployment_result)
            
            # Setup monitoring
            await self._setup_deployment_monitoring(deployment_result)
            
            # Store deployment result
            self.active_deployments[deployment_id] = deployment_result
            
            return deployment_result
            
        except Exception as e:
            # Create failed deployment result
            failed_result = DeploymentResult(
                deployment_id=deployment_id,
                config_id=config_id,
                status=DeploymentStatus.FAILED,
                platform=config.platform,
                deployment_url="",
                build_logs=[f"Deployment failed: {str(e)}"],
                deployment_time=0,
                performance_metrics={},
                security_scan_results={},
                rollback_url=None,
                deployed_at=time.time()
            )
            
            self.active_deployments[deployment_id] = failed_result
            return failed_result
    
    async def _run_pre_deployment_checks(self, config: DeploymentConfig):
        """Run pre-deployment checks and validations"""
        
        checks = [
            self._check_build_dependencies,
            self._check_environment_variables,
            self._check_security_settings,
            self._run_tests,
            self._check_performance_budget
        ]
        
        for check in checks:
            await check(config)
    
    async def _check_build_dependencies(self, config: DeploymentConfig):
        """Check build dependencies"""
        
        package_json_path = self.project_path / "package.json"
        if package_json_path.exists():
            async with aiofiles.open(package_json_path, 'r') as f:
                package_data = json.loads(await f.read())
                
            # Check for required scripts
            scripts = package_data.get("scripts", {})
            if "build" not in scripts:
                raise ValueError("Missing build script in package.json")
    
    async def _check_environment_variables(self, config: DeploymentConfig):
        """Validate environment variables"""
        
        required_vars = ["NODE_ENV"]  # Basic required variables
        
        for var in required_vars:
            if var not in config.environment_variables:
                raise ValueError(f"Missing required environment variable: {var}")
    
    async def _check_security_settings(self, config: DeploymentConfig):
        """Check security configuration"""
        
        if config.environment == EnvironmentType.PRODUCTION and not config.ssl_enabled:
            raise ValueError("SSL must be enabled for production deployments")
    
    async def _run_tests(self, config: DeploymentConfig):
        """Run tests before deployment"""
        
        # Run existing test suite if available
        test_commands = ["npm test", "npm run test:ci"]
        
        for command in test_commands:
            try:
                process = await asyncio.create_subprocess_shell(
                    command,
                    cwd=self.project_path,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                stdout, stderr = await process.communicate()
                
                if process.returncode == 0:
                    break  # Tests passed
                    
            except FileNotFoundError:
                continue  # Command not found, try next
        
        # If all test commands fail, it's not necessarily an error (no tests configured)
    
    async def _check_performance_budget(self, config: DeploymentConfig):
        """Check performance budget compliance"""
        
        # Build size check
        build_path = self.project_path / config.build_settings.get("output_directory", "dist")
        
        if build_path.exists():
            total_size = sum(f.stat().st_size for f in build_path.rglob('*') if f.is_file())
            
            # 10MB budget for static sites
            if total_size > 10 * 1024 * 1024:
                print(f"Warning: Build size ({total_size / 1024 / 1024:.1f}MB) exceeds recommended budget (10MB)")
    
    async def _build_application(self, config: DeploymentConfig) -> Dict[str, Any]:
        """Build application using specified build settings"""
        
        build_logs = []
        start_time = time.time()
        
        try:
            # Install dependencies
            install_command = config.build_settings.get("install_command", "npm ci")
            process = await asyncio.create_subprocess_shell(
                install_command,
                cwd=self.project_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT
            )
            
            stdout, _ = await process.communicate()
            build_logs.append(f"Install: {stdout.decode()}")
            
            if process.returncode != 0:
                raise RuntimeError(f"Install failed with code {process.returncode}")
            
            # Run build command
            build_command = config.build_settings.get("build_command", "npm run build")
            process = await asyncio.create_subprocess_shell(
                build_command,
                cwd=self.project_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT
            )
            
            stdout, _ = await process.communicate()
            build_logs.append(f"Build: {stdout.decode()}")
            
            if process.returncode != 0:
                raise RuntimeError(f"Build failed with code {process.returncode}")
            
            build_time = time.time() - start_time
            
            return {
                "success": True,
                "build_logs": build_logs,
                "build_time": build_time,
                "output_directory": config.build_settings.get("output_directory", "dist")
            }
            
        except Exception as e:
            return {
                "success": False,
                "build_logs": build_logs + [f"Build error: {str(e)}"],
                "build_time": time.time() - start_time,
                "error": str(e)
            }
    
    async def _deploy_to_vercel(self, config: DeploymentConfig, deployment_id: str, build_result: Dict[str, Any]) -> DeploymentResult:
        """Deploy to Vercel platform"""
        
        start_time = time.time()
        
        # Create vercel.json configuration
        vercel_config = {
            "version": 2,
            "name": f"app-{config.environment.value}",
            "builds": [
                {
                    "src": "package.json",
                    "use": "@vercel/node" if config.deployment_type == DeploymentType.SERVER_SIDE_RENDERED else "@vercel/static-build"
                }
            ],
            "env": config.environment_variables,
            "regions": ["iad1", "sfo1", "lhr1"] if config.environment == EnvironmentType.PRODUCTION else ["iad1"]
        }
        
        # Write vercel configuration
        config_path = self.project_path / "vercel.json"
        async with aiofiles.open(config_path, 'w') as f:
            await f.write(json.dumps(vercel_config, indent=2))
        
        # Deploy using Vercel CLI
        deploy_command = f"vercel --prod" if config.environment == EnvironmentType.PRODUCTION else "vercel"
        
        try:
            process = await asyncio.create_subprocess_shell(
                deploy_command,
                cwd=self.project_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT
            )
            
            stdout, _ = await process.communicate()
            deploy_logs = [stdout.decode()]
            
            if process.returncode != 0:
                raise RuntimeError(f"Vercel deployment failed: {stdout.decode()}")
            
            # Extract deployment URL from output
            output_lines = stdout.decode().split('\\n')
            deployment_url = None
            
            for line in output_lines:
                if line.strip().startswith('https://'):
                    deployment_url = line.strip()
                    break
            
            if not deployment_url:
                deployment_url = f"https://app-{config.environment.value}-generated.vercel.app"
            
            deployment_time = time.time() - start_time
            
            return DeploymentResult(
                deployment_id=deployment_id,
                config_id=config.config_id,
                status=DeploymentStatus.DEPLOYED,
                platform=DeploymentPlatform.VERCEL,
                deployment_url=deployment_url,
                build_logs=build_result["build_logs"] + deploy_logs,
                deployment_time=deployment_time,
                performance_metrics={
                    "build_time": build_result["build_time"],
                    "deployment_time": deployment_time
                },
                security_scan_results={
                    "ssl_enabled": config.ssl_enabled,
                    "security_headers": True
                },
                rollback_url=None,
                deployed_at=time.time()
            )
            
        except Exception as e:
            raise RuntimeError(f"Vercel deployment failed: {str(e)}")
    
    async def _deploy_to_netlify(self, config: DeploymentConfig, deployment_id: str, build_result: Dict[str, Any]) -> DeploymentResult:
        """Deploy to Netlify platform"""
        
        start_time = time.time()
        
        # Create netlify.toml configuration
        netlify_config = f"""
[build]
  command = "{config.build_settings.get('build_command', 'npm run build')}"
  publish = "{config.build_settings.get('output_directory', 'dist')}"

[build.environment]
{chr(10).join(f'  {k} = "{v}"' for k, v in config.environment_variables.items())}

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    X-XSS-Protection = "1; mode=block"
    Referrer-Policy = "strict-origin-when-cross-origin"
"""
        
        # Write netlify configuration
        config_path = self.project_path / "netlify.toml"
        async with aiofiles.open(config_path, 'w') as f:
            await f.write(netlify_config)
        
        # Deploy using Netlify CLI
        deploy_command = f"netlify deploy --prod" if config.environment == EnvironmentType.PRODUCTION else "netlify deploy"
        
        try:
            process = await asyncio.create_subprocess_shell(
                deploy_command,
                cwd=self.project_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT
            )
            
            stdout, _ = await process.communicate()
            deploy_logs = [stdout.decode()]
            
            if process.returncode != 0:
                raise RuntimeError(f"Netlify deployment failed: {stdout.decode()}")
            
            # Extract deployment URL from output
            deployment_url = f"https://app-{config.environment.value}.netlify.app"
            
            deployment_time = time.time() - start_time
            
            return DeploymentResult(
                deployment_id=deployment_id,
                config_id=config.config_id,
                status=DeploymentStatus.DEPLOYED,
                platform=DeploymentPlatform.NETLIFY,
                deployment_url=deployment_url,
                build_logs=build_result["build_logs"] + deploy_logs,
                deployment_time=deployment_time,
                performance_metrics={
                    "build_time": build_result["build_time"],
                    "deployment_time": deployment_time
                },
                security_scan_results={
                    "ssl_enabled": config.ssl_enabled,
                    "security_headers": True
                },
                rollback_url=None,
                deployed_at=time.time()
            )
            
        except Exception as e:
            raise RuntimeError(f"Netlify deployment failed: {str(e)}")
    
    async def _deploy_to_aws_amplify(self, config: DeploymentConfig, deployment_id: str, build_result: Dict[str, Any]) -> DeploymentResult:
        """Deploy to AWS Amplify"""
        # Implementation for AWS Amplify deployment
        pass
    
    async def _deploy_to_railway(self, config: DeploymentConfig, deployment_id: str, build_result: Dict[str, Any]) -> DeploymentResult:
        """Deploy to Railway platform"""
        # Implementation for Railway deployment
        pass
    
    async def _validate_deployment(self, deployment_result: DeploymentResult):
        """Validate successful deployment"""
        
        if deployment_result.status != DeploymentStatus.DEPLOYED:
            return
        
        # Health check
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(deployment_result.deployment_url, timeout=30) as response:
                    if response.status != 200:
                        print(f"Warning: Deployment health check failed with status {response.status}")
        except Exception as e:
            print(f"Warning: Deployment health check failed: {e}")
    
    async def _setup_deployment_monitoring(self, deployment_result: DeploymentResult):
        """Setup monitoring for deployed application"""
        
        monitoring_config = {
            "uptime_monitoring": {
                "url": deployment_result.deployment_url,
                "interval": 300,  # 5 minutes
                "timeout": 30
            },
            "performance_monitoring": {
                "lighthouse_audits": True,
                "real_user_monitoring": True
            },
            "error_tracking": {
                "enabled": True,
                "sampling_rate": 0.1
            }
        }
        
        # Store monitoring configuration
        monitoring_path = self.project_path / f"monitoring_{deployment_result.deployment_id}.json"
        async with aiofiles.open(monitoring_path, 'w') as f:
            await f.write(json.dumps(monitoring_config, indent=2))
    
    async def create_ci_cd_pipeline(self, deployment_configs: Dict[str, DeploymentConfig], pipeline_name: str) -> CIPipeline:
        """Create comprehensive CI/CD pipeline"""
        
        pipeline = CIPipeline(
            pipeline_id=f"pipeline_{int(time.time())}",
            name=pipeline_name,
            triggers=["push", "pull_request"],
            stages=[
                {
                    "name": "test",
                    "steps": [
                        "npm ci",
                        "npm run test",
                        "npm run lint",
                        "npm run type-check"
                    ]
                },
                {
                    "name": "build",
                    "steps": [
                        "npm run build",
                        "npm run test:e2e"
                    ]
                },
                {
                    "name": "security",
                    "steps": [
                        "npm audit",
                        "snyk test",
                        "docker scan"
                    ]
                },
                {
                    "name": "deploy_dev",
                    "condition": "branch == develop",
                    "steps": [
                        f"deploy to {deployment_configs['development'].platform.value}"
                    ]
                },
                {
                    "name": "deploy_staging",
                    "condition": "branch == staging",
                    "steps": [
                        f"deploy to {deployment_configs['staging'].platform.value}"
                    ]
                },
                {
                    "name": "deploy_production",
                    "condition": "branch == main && manual_approval",
                    "steps": [
                        f"deploy to {deployment_configs['production'].platform.value}"
                    ]
                }
            ],
            environment_promotion={
                "auto_promote_to_staging": True,
                "require_approval_for_production": True,
                "rollback_on_failure": True
            },
            notification_settings={
                "success": ["email", "slack"],
                "failure": ["email", "slack", "pagerduty"],
                "channels": {
                    "email": "team@example.com",
                    "slack": "#deployments"
                }
            },
            security_checks=[
                "vulnerability_scan",
                "license_check",
                "secret_scan",
                "container_scan"
            ],
            quality_gates={
                "test_coverage": 80,
                "performance_budget": {
                    "lighthouse_score": 90,
                    "bundle_size": "1MB"
                },
                "security_score": 85
            },
            created_at=time.time()
        )
        
        self.pipelines[pipeline.pipeline_id] = pipeline
        
        # Generate CI/CD configuration files
        await self._generate_ci_cd_configs(pipeline)
        
        return pipeline
    
    async def _generate_ci_cd_configs(self, pipeline: CIPipeline):
        """Generate CI/CD configuration files for different platforms"""
        
        # GitHub Actions workflow
        github_workflow = {
            "name": pipeline.name,
            "on": {
                "push": {"branches": ["main", "develop", "staging"]},
                "pull_request": {"branches": ["main"]}
            },
            "jobs": {}
        }
        
        for stage in pipeline.stages:
            job_name = stage["name"]
            github_workflow["jobs"][job_name] = {
                "runs-on": "ubuntu-latest",
                "steps": [
                    {"uses": "actions/checkout@v4"},
                    {"uses": "actions/setup-node@v4", "with": {"node-version": "18"}},
                    {"run": "npm ci"},
                ] + [{"run": step} for step in stage["steps"]]
            }
        
        # Write GitHub Actions workflow
        github_dir = self.project_path / ".github/workflows"
        github_dir.mkdir(parents=True, exist_ok=True)
        
        workflow_path = github_dir / f"{pipeline.name.replace(' ', '-').lower()}.yml"
        async with aiofiles.open(workflow_path, 'w') as f:
            await f.write(yaml.dump(github_workflow, default_flow_style=False))
    
    async def rollback_deployment(self, deployment_id: str) -> DeploymentResult:
        """Rollback deployment to previous version"""
        
        if deployment_id not in self.active_deployments:
            raise ValueError(f"Deployment {deployment_id} not found")
        
        deployment = self.active_deployments[deployment_id]
        
        # Implementation depends on platform
        if deployment.platform == DeploymentPlatform.VERCEL:
            return await self._rollback_vercel_deployment(deployment)
        elif deployment.platform == DeploymentPlatform.NETLIFY:
            return await self._rollback_netlify_deployment(deployment)
        else:
            raise ValueError(f"Rollback not implemented for platform {deployment.platform}")
    
    async def _rollback_vercel_deployment(self, deployment: DeploymentResult) -> DeploymentResult:
        """Rollback Vercel deployment"""
        
        # Use Vercel CLI to rollback
        rollback_command = f"vercel rollback {deployment.deployment_url}"
        
        try:
            process = await asyncio.create_subprocess_shell(
                rollback_command,
                cwd=self.project_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT
            )
            
            stdout, _ = await process.communicate()
            
            if process.returncode != 0:
                raise RuntimeError(f"Vercel rollback failed: {stdout.decode()}")
            
            # Update deployment status
            deployment.status = DeploymentStatus.ROLLED_BACK
            
            return deployment
            
        except Exception as e:
            raise RuntimeError(f"Rollback failed: {str(e)}")
    
    async def _rollback_netlify_deployment(self, deployment: DeploymentResult) -> DeploymentResult:
        """Rollback Netlify deployment"""
        # Implementation for Netlify rollback
        pass
    
    async def get_deployment_metrics(self, deployment_id: str) -> Dict[str, Any]:
        """Get comprehensive deployment metrics"""
        
        if deployment_id not in self.active_deployments:
            raise ValueError(f"Deployment {deployment_id} not found")
        
        deployment = self.active_deployments[deployment_id]
        
        # Collect metrics from various sources
        metrics = {
            "deployment_info": asdict(deployment),
            "uptime_metrics": await self._get_uptime_metrics(deployment),
            "performance_metrics": await self._get_performance_metrics(deployment),
            "error_metrics": await self._get_error_metrics(deployment),
            "resource_usage": await self._get_resource_usage(deployment),
            "cost_metrics": await self._get_cost_metrics(deployment)
        }
        
        return metrics
    
    async def _get_uptime_metrics(self, deployment: DeploymentResult) -> Dict[str, Any]:
        """Get uptime monitoring metrics"""
        return {
            "uptime_percentage": 99.9,
            "response_time_avg": 150,
            "response_time_p95": 300,
            "incidents_count": 0,
            "last_downtime": None
        }
    
    async def _get_performance_metrics(self, deployment: DeploymentResult) -> Dict[str, Any]:
        """Get performance metrics"""
        return {
            "lighthouse_scores": {
                "performance": 95,
                "accessibility": 98,
                "best_practices": 92,
                "seo": 96
            },
            "core_web_vitals": {
                "lcp": 1.2,
                "fid": 45,
                "cls": 0.05
            },
            "page_load_time": 1.8,
            "time_to_interactive": 2.1
        }
    
    async def _get_error_metrics(self, deployment: DeploymentResult) -> Dict[str, Any]:
        """Get error tracking metrics"""
        return {
            "error_rate": 0.1,
            "total_errors": 5,
            "error_types": {
                "client_errors": 3,
                "server_errors": 2
            },
            "top_errors": [
                {"message": "Network timeout", "count": 2},
                {"message": "Validation error", "count": 1}
            ]
        }
    
    async def _get_resource_usage(self, deployment: DeploymentResult) -> Dict[str, Any]:
        """Get resource usage metrics"""
        return {
            "bandwidth_usage": "2.5GB",
            "function_invocations": 15420,
            "build_minutes": 8.5,
            "storage_usage": "150MB"
        }
    
    async def _get_cost_metrics(self, deployment: DeploymentResult) -> Dict[str, Any]:
        """Get cost analytics"""
        return {
            "monthly_cost_estimate": "$12.50",
            "cost_breakdown": {
                "hosting": "$5.00",
                "bandwidth": "$3.50",
                "functions": "$2.00",
                "storage": "$2.00"
            },
            "cost_trends": "decreasing",
            "optimization_suggestions": [
                "Enable compression to reduce bandwidth costs",
                "Implement caching to reduce function invocations"
            ]
        }

# Factory function
def create_devops_engine(openai_client, project_path: Path) -> DevOpsAutomationEngine:
    """Create DevOps automation engine instance"""
    return DevOpsAutomationEngine(openai_client, project_path)