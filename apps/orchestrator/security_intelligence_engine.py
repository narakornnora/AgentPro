"""
Security Intelligence Engine
============================
Advanced security system that scans, detects, and auto-fixes security vulnerabilities.
Implements security best practices, monitors threats, and provides intelligent security insights.
"""

import asyncio
import json
import logging
import os
import sqlite3
import hashlib
import re
import base64
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set
import subprocess
import secrets
import uuid
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SecurityVulnerability:
    """Represents a security vulnerability"""
    
    def __init__(self, vuln_id: str, severity: str, category: str, 
                 description: str, file_path: str, line_number: int = 0):
        self.vuln_id = vuln_id
        self.severity = severity  # critical, high, medium, low
        self.category = category
        self.description = description
        self.file_path = file_path
        self.line_number = line_number
        self.detected_at = datetime.now()
        self.fixed = False
        self.fix_suggestion = ""
        self.auto_fixable = False
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            'vuln_id': self.vuln_id,
            'severity': self.severity,
            'category': self.category,
            'description': self.description,
            'file_path': self.file_path,
            'line_number': self.line_number,
            'detected_at': self.detected_at.isoformat(),
            'fixed': self.fixed,
            'fix_suggestion': self.fix_suggestion,
            'auto_fixable': self.auto_fixable
        }

class VulnerabilityScanner:
    """Scans code for security vulnerabilities"""
    
    def __init__(self):
        self.vulnerability_patterns = self._load_vulnerability_patterns()
        self.security_headers = self._load_security_headers()
        
    def _load_vulnerability_patterns(self) -> Dict[str, Dict]:
        """Load vulnerability detection patterns"""
        return {
            'xss': {
                'patterns': [
                    r'innerHTML\s*=\s*["\']?[^"\']*\+',
                    r'document\.write\s*\(',
                    r'eval\s*\(',
                    r'setTimeout\s*\(\s*["\'][^"\']*\+',
                    r'setInterval\s*\(\s*["\'][^"\']*\+'
                ],
                'severity': 'high',
                'description': 'Potential Cross-Site Scripting (XSS) vulnerability',
                'fix': 'Use textContent instead of innerHTML, validate and sanitize user input'
            },
            'sql_injection': {
                'patterns': [
                    r'SELECT\s+.*\+.*FROM',
                    r'INSERT\s+.*\+.*VALUES',
                    r'UPDATE\s+.*SET.*\+',
                    r'DELETE\s+.*WHERE.*\+'
                ],
                'severity': 'critical',
                'description': 'Potential SQL Injection vulnerability',
                'fix': 'Use parameterized queries or prepared statements'
            },
            'insecure_random': {
                'patterns': [
                    r'Math\.random\(\)',
                    r'new Date\(\)\.getTime\(\)',
                    r'Math\.floor\(Math\.random\(\)'
                ],
                'severity': 'medium',
                'description': 'Insecure random number generation',
                'fix': 'Use crypto.getRandomValues() for cryptographic purposes'
            },
            'hardcoded_secrets': {
                'patterns': [
                    r'password\s*=\s*["\'][^"\']{6,}["\']',
                    r'api_key\s*=\s*["\'][^"\']{10,}["\']',
                    r'secret\s*=\s*["\'][^"\']{10,}["\']',
                    r'token\s*=\s*["\'][^"\']{20,}["\']'
                ],
                'severity': 'critical',
                'description': 'Hardcoded secrets or credentials',
                'fix': 'Move secrets to environment variables or secure configuration'
            },
            'unsafe_url': {
                'patterns': [
                    r'http://[^"\'\s]+',
                    r'window\.location\s*=\s*[^"\']*\+',
                    r'location\.href\s*=\s*[^"\']*\+'
                ],
                'severity': 'medium',
                'description': 'Insecure URL or potential open redirect',
                'fix': 'Use HTTPS and validate URLs before redirecting'
            },
            'missing_csrf': {
                'patterns': [
                    r'<form[^>]*method\s*=\s*["\']post["\'][^>]*>(?!.*csrf)',
                    r'fetch\([^)]*method:\s*["\']POST["\'](?!.*csrf)'
                ],
                'severity': 'high',
                'description': 'Missing CSRF protection',
                'fix': 'Add CSRF tokens to forms and AJAX requests'
            },
            'insecure_storage': {
                'patterns': [
                    r'localStorage\.setItem\([^)]*password',
                    r'sessionStorage\.setItem\([^)]*token',
                    r'document\.cookie\s*=.*secure.*httponly'
                ],
                'severity': 'high',
                'description': 'Insecure client-side storage',
                'fix': 'Use secure, HttpOnly cookies for sensitive data'
            }
        }
    
    def _load_security_headers(self) -> Dict[str, str]:
        """Load security headers requirements"""
        return {
            'Content-Security-Policy': "default-src 'self'",
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Referrer-Policy': 'strict-origin-when-cross-origin'
        }
    
    async def scan_application(self, app_path: str) -> List[SecurityVulnerability]:
        """Scan application for security vulnerabilities"""
        vulnerabilities = []
        
        try:
            app_dir = Path(app_path)
            
            # Scan different file types
            for file_pattern in ['*.html', '*.js', '*.css', '*.py', '*.php']:
                for file_path in app_dir.rglob(file_pattern):
                    if file_path.is_file():
                        file_vulns = await self._scan_file(file_path)
                        vulnerabilities.extend(file_vulns)
            
            # Check for missing security configurations
            config_vulns = await self._check_security_configuration(app_dir)
            vulnerabilities.extend(config_vulns)
            
            logger.info(f"🔍 Security scan completed - found {len(vulnerabilities)} vulnerabilities")
            
        except Exception as e:
            logger.error(f"Security scan failed: {e}")
            
        return vulnerabilities
    
    async def _scan_file(self, file_path: Path) -> List[SecurityVulnerability]:
        """Scan individual file for vulnerabilities"""
        vulnerabilities = []
        
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            lines = content.splitlines()
            
            for vuln_type, vuln_info in self.vulnerability_patterns.items():
                for pattern in vuln_info['patterns']:
                    matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                    
                    for match in matches:
                        # Find line number
                        line_num = content[:match.start()].count('\n') + 1
                        
                        vuln_id = f"{vuln_type}_{hashlib.md5(str(match.group()).encode()).hexdigest()[:8]}"
                        
                        vulnerability = SecurityVulnerability(
                            vuln_id,
                            vuln_info['severity'],
                            vuln_type,
                            vuln_info['description'],
                            str(file_path),
                            line_num
                        )
                        vulnerability.fix_suggestion = vuln_info['fix']
                        vulnerability.auto_fixable = vuln_type in ['insecure_random', 'unsafe_url']
                        
                        vulnerabilities.append(vulnerability)
            
        except Exception as e:
            logger.error(f"File scan failed for {file_path}: {e}")
            
        return vulnerabilities
    
    async def _check_security_configuration(self, app_dir: Path) -> List[SecurityVulnerability]:
        """Check for missing security configurations"""
        vulnerabilities = []
        
        try:
            # Check for security headers in HTML files
            html_files = list(app_dir.glob('*.html'))
            
            for html_file in html_files:
                content = html_file.read_text(encoding='utf-8', errors='ignore')
                
                # Check for missing meta security tags
                if '<meta http-equiv="Content-Security-Policy"' not in content:
                    vulnerability = SecurityVulnerability(
                        f"missing_csp_{html_file.name}",
                        'medium',
                        'missing_security_header',
                        'Missing Content Security Policy',
                        str(html_file)
                    )
                    vulnerability.fix_suggestion = 'Add CSP meta tag to prevent XSS attacks'
                    vulnerability.auto_fixable = True
                    vulnerabilities.append(vulnerability)
                
                if '<meta http-equiv="X-Content-Type-Options"' not in content:
                    vulnerability = SecurityVulnerability(
                        f"missing_nosniff_{html_file.name}",
                        'low',
                        'missing_security_header',
                        'Missing X-Content-Type-Options header',
                        str(html_file)
                    )
                    vulnerability.fix_suggestion = 'Add X-Content-Type-Options: nosniff'
                    vulnerability.auto_fixable = True
                    vulnerabilities.append(vulnerability)
            
        except Exception as e:
            logger.error(f"Security configuration check failed: {e}")
            
        return vulnerabilities

class SecurityFixer:
    """Automatically fixes security vulnerabilities"""
    
    def __init__(self):
        self.fix_strategies = self._load_fix_strategies()
        
    def _load_fix_strategies(self) -> Dict[str, callable]:
        """Load automatic fix strategies"""
        return {
            'insecure_random': self._fix_insecure_random,
            'unsafe_url': self._fix_unsafe_url,
            'missing_security_header': self._fix_missing_headers,
            'hardcoded_secrets': self._fix_hardcoded_secrets
        }
    
    async def auto_fix_vulnerability(self, vulnerability: SecurityVulnerability) -> bool:
        """Automatically fix a vulnerability"""
        if not vulnerability.auto_fixable:
            return False
            
        try:
            if vulnerability.category in self.fix_strategies:
                success = await self.fix_strategies[vulnerability.category](vulnerability)
                if success:
                    vulnerability.fixed = True
                    logger.info(f"✅ Auto-fixed vulnerability: {vulnerability.vuln_id}")
                return success
                
        except Exception as e:
            logger.error(f"Auto-fix failed for {vulnerability.vuln_id}: {e}")
            
        return False
    
    async def _fix_insecure_random(self, vulnerability: SecurityVulnerability) -> bool:
        """Fix insecure random number generation"""
        try:
            file_path = Path(vulnerability.file_path)
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            # Replace Math.random() with crypto.getRandomValues()
            fixes = [
                (r'Math\.random\(\)', 'crypto.getRandomValues(new Uint32Array(1))[0] / 2**32'),
                (r'Math\.floor\(Math\.random\(\)\s*\*\s*(\d+)\)', r'crypto.getRandomValues(new Uint32Array(1))[0] % \1')
            ]
            
            modified = False
            for pattern, replacement in fixes:
                if re.search(pattern, content):
                    content = re.sub(pattern, replacement, content)
                    modified = True
            
            if modified:
                # Add crypto import if it's a JS file
                if file_path.suffix == '.js' and 'crypto' not in content:
                    content = '// Security fix: Use crypto for random generation\n' + content
                
                file_path.write_text(content, encoding='utf-8')
                return True
                
        except Exception as e:
            logger.error(f"Failed to fix insecure random: {e}")
            
        return False
    
    async def _fix_unsafe_url(self, vulnerability: SecurityVulnerability) -> bool:
        """Fix unsafe URL usage"""
        try:
            file_path = Path(vulnerability.file_path)
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            # Replace http:// with https://
            content = re.sub(r'http://', 'https://', content)
            
            file_path.write_text(content, encoding='utf-8')
            return True
            
        except Exception as e:
            logger.error(f"Failed to fix unsafe URL: {e}")
            
        return False
    
    async def _fix_missing_headers(self, vulnerability: SecurityVulnerability) -> bool:
        """Fix missing security headers"""
        try:
            file_path = Path(vulnerability.file_path)
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            # Add security meta tags to HTML
            if '<head>' in content:
                security_tags = """
    <!-- Security Headers -->
    <meta http-equiv="Content-Security-Policy" content="default-src 'self'">
    <meta http-equiv="X-Content-Type-Options" content="nosniff">
    <meta http-equiv="X-Frame-Options" content="DENY">
    <meta http-equiv="X-XSS-Protection" content="1; mode=block">"""
                
                content = content.replace('<head>', f'<head>{security_tags}')
                file_path.write_text(content, encoding='utf-8')
                return True
                
        except Exception as e:
            logger.error(f"Failed to fix missing headers: {e}")
            
        return False
    
    async def _fix_hardcoded_secrets(self, vulnerability: SecurityVulnerability) -> bool:
        """Fix hardcoded secrets (replace with placeholder)"""
        try:
            file_path = Path(vulnerability.file_path)
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            # Replace hardcoded secrets with environment variable placeholders
            patterns = [
                (r'password\s*=\s*["\'][^"\']+["\']', 'password = process.env.PASSWORD || ""'),
                (r'api_key\s*=\s*["\'][^"\']+["\']', 'api_key = process.env.API_KEY || ""'),
                (r'secret\s*=\s*["\'][^"\']+["\']', 'secret = process.env.SECRET || ""'),
                (r'token\s*=\s*["\'][^"\']+["\']', 'token = process.env.TOKEN || ""')
            ]
            
            for pattern, replacement in patterns:
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            
            file_path.write_text(content, encoding='utf-8')
            return True
            
        except Exception as e:
            logger.error(f"Failed to fix hardcoded secrets: {e}")
            
        return False

class ThreatMonitor:
    """Monitors for security threats and suspicious activities"""
    
    def __init__(self):
        self.threat_patterns = self._load_threat_patterns()
        self.monitoring_active = False
        
    def _load_threat_patterns(self) -> Dict[str, List[str]]:
        """Load threat detection patterns"""
        return {
            'suspicious_files': [
                r'\.php$',  # PHP files in non-PHP projects
                r'\.exe$',  # Executable files
                r'\.bat$',  # Batch files
                r'\.sh$',   # Shell scripts (suspicious in web projects)
            ],
            'malicious_content': [
                r'<script[^>]*>.*eval\(',
                r'document\.cookie',
                r'window\.location\s*=.*javascript:',
                r'iframe.*src\s*=.*javascript:'
            ],
            'backdoor_patterns': [
                r'eval\s*\(\s*base64_decode',
                r'system\s*\([^)]*\$_',
                r'exec\s*\([^)]*\$_',
                r'shell_exec\s*\('
            ]
        }
    
    async def scan_for_threats(self, app_path: str) -> List[Dict[str, Any]]:
        """Scan for security threats"""
        threats = []
        
        try:
            app_dir = Path(app_path)
            
            # Scan files for threats
            for file_path in app_dir.rglob('*'):
                if file_path.is_file():
                    file_threats = await self._scan_file_for_threats(file_path)
                    threats.extend(file_threats)
            
            logger.info(f"🛡️ Threat scan completed - found {len(threats)} potential threats")
            
        except Exception as e:
            logger.error(f"Threat scanning failed: {e}")
            
        return threats
    
    async def _scan_file_for_threats(self, file_path: Path) -> List[Dict[str, Any]]:
        """Scan individual file for threats"""
        threats = []
        
        try:
            # Check file extension
            for pattern in self.threat_patterns['suspicious_files']:
                if re.search(pattern, str(file_path)):
                    threats.append({
                        'type': 'suspicious_file',
                        'severity': 'medium',
                        'description': f'Suspicious file type: {file_path.suffix}',
                        'file_path': str(file_path),
                        'recommendation': 'Review file necessity and contents'
                    })
            
            # Check file contents
            if file_path.suffix in ['.html', '.js', '.php', '.py']:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                
                # Scan for malicious patterns
                for threat_type, patterns in self.threat_patterns.items():
                    if threat_type == 'suspicious_files':
                        continue
                        
                    for pattern in patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            threats.append({
                                'type': threat_type,
                                'severity': 'high' if threat_type == 'backdoor_patterns' else 'medium',
                                'description': f'Detected {threat_type} pattern',
                                'file_path': str(file_path),
                                'pattern': pattern,
                                'recommendation': 'Manual review required - potential security threat'
                            })
                            
        except Exception as e:
            logger.error(f"Threat scan failed for {file_path}: {e}")
            
        return threats

class SecurityReporter:
    """Generates security reports and recommendations"""
    
    def __init__(self):
        pass
    
    async def generate_security_report(self, app_path: str, vulnerabilities: List[SecurityVulnerability], 
                                      threats: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive security report"""
        report = {
            'app_path': app_path,
            'scan_timestamp': datetime.now().isoformat(),
            'summary': {},
            'vulnerabilities': [],
            'threats': threats,
            'recommendations': [],
            'security_score': 0,
            'compliance': {}
        }
        
        try:
            # Vulnerability summary
            vuln_by_severity = defaultdict(int)
            vuln_by_category = defaultdict(int)
            fixed_count = 0
            
            for vuln in vulnerabilities:
                vuln_by_severity[vuln.severity] += 1
                vuln_by_category[vuln.category] += 1
                if vuln.fixed:
                    fixed_count += 1
                report['vulnerabilities'].append(vuln.to_dict())
            
            report['summary'] = {
                'total_vulnerabilities': len(vulnerabilities),
                'by_severity': dict(vuln_by_severity),
                'by_category': dict(vuln_by_category),
                'fixed_vulnerabilities': fixed_count,
                'total_threats': len(threats)
            }
            
            # Calculate security score (0-100)
            score = 100
            score -= len(vulnerabilities) * 2  # -2 per vulnerability
            score -= sum(vuln_by_severity[s] * w for s, w in [('critical', 10), ('high', 5), ('medium', 2), ('low', 1)])
            score -= len(threats) * 3  # -3 per threat
            score += fixed_count * 2  # +2 per fixed vulnerability
            
            report['security_score'] = max(0, min(100, score))
            
            # Generate recommendations
            report['recommendations'] = self._generate_recommendations(vulnerabilities, threats, report['security_score'])
            
            # Check compliance
            report['compliance'] = await self._check_compliance(app_path, vulnerabilities)
            
        except Exception as e:
            logger.error(f"Security report generation failed: {e}")
            report['error'] = str(e)
            
        return report
    
    def _generate_recommendations(self, vulnerabilities: List[SecurityVulnerability], 
                                 threats: List[Dict[str, Any]], security_score: int) -> List[str]:
        """Generate security recommendations"""
        recommendations = []
        
        # Critical vulnerabilities
        critical_vulns = [v for v in vulnerabilities if v.severity == 'critical']
        if critical_vulns:
            recommendations.append(f"🚨 URGENT: Fix {len(critical_vulns)} critical vulnerabilities immediately")
        
        # High severity vulnerabilities
        high_vulns = [v for v in vulnerabilities if v.severity == 'high']
        if high_vulns:
            recommendations.append(f"⚠️ HIGH PRIORITY: Address {len(high_vulns)} high-severity vulnerabilities")
        
        # Security score based recommendations
        if security_score < 50:
            recommendations.append("❌ Security score is critically low - immediate action required")
        elif security_score < 70:
            recommendations.append("⚠️ Security needs improvement - review and fix vulnerabilities")
        elif security_score >= 90:
            recommendations.append("✅ Excellent security posture - maintain current practices")
        
        # Threat-based recommendations
        if threats:
            recommendations.append(f"🔍 Review {len(threats)} potential threats identified")
        
        # Auto-fix recommendations
        auto_fixable = [v for v in vulnerabilities if v.auto_fixable and not v.fixed]
        if auto_fixable:
            recommendations.append(f"🔧 {len(auto_fixable)} vulnerabilities can be auto-fixed")
        
        # General security practices
        recommendations.extend([
            "🔐 Implement regular security scans in CI/CD pipeline",
            "📚 Train development team on secure coding practices",
            "🛡️ Enable security headers in production deployment",
            "🔄 Keep dependencies updated and scan for known vulnerabilities"
        ])
        
        return recommendations
    
    async def _check_compliance(self, app_path: str, vulnerabilities: List[SecurityVulnerability]) -> Dict[str, Any]:
        """Check security compliance standards"""
        compliance = {
            'owasp_top_10': {'score': 0, 'issues': []},
            'security_headers': {'score': 0, 'missing': []},
            'data_protection': {'score': 0, 'issues': []}
        }
        
        try:
            # OWASP Top 10 compliance
            owasp_categories = ['xss', 'sql_injection', 'insecure_storage', 'missing_csrf']
            owasp_violations = [v for v in vulnerabilities if v.category in owasp_categories]
            
            compliance['owasp_top_10']['score'] = max(0, 100 - len(owasp_violations) * 10)
            compliance['owasp_top_10']['issues'] = [v.category for v in owasp_violations]
            
            # Security headers compliance
            header_violations = [v for v in vulnerabilities if 'missing_security_header' in v.category]
            compliance['security_headers']['score'] = max(0, 100 - len(header_violations) * 15)
            compliance['security_headers']['missing'] = [v.description for v in header_violations]
            
        except Exception as e:
            logger.error(f"Compliance check failed: {e}")
            
        return compliance

class SecurityIntelligenceEngine:
    """Main Security Intelligence Engine orchestrator"""
    
    def __init__(self):
        self.scanner = VulnerabilityScanner()
        self.fixer = SecurityFixer()
        self.threat_monitor = ThreatMonitor()
        self.reporter = SecurityReporter()
        self.db_path = "security_intelligence.db"
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Initialize security database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS security_scans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    app_path TEXT NOT NULL,
                    scan_timestamp TEXT NOT NULL,
                    vulnerabilities_found INTEGER,
                    vulnerabilities_fixed INTEGER,
                    security_score INTEGER,
                    report_data TEXT NOT NULL
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vulnerabilities (
                    id TEXT PRIMARY KEY,
                    app_path TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    line_number INTEGER,
                    detected_at TEXT NOT NULL,
                    fixed BOOLEAN DEFAULT FALSE,
                    fix_suggestion TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS security_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    description TEXT NOT NULL,
                    app_path TEXT,
                    timestamp TEXT NOT NULL,
                    data TEXT
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info("🛡️ Security Intelligence database initialized")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
    
    async def run_security_analysis(self, app_path: str, auto_fix: bool = True) -> Dict[str, Any]:
        """Run comprehensive security analysis"""
        logger.info(f"🔍 Starting security analysis for {app_path}")
        
        analysis_result = {
            'app_path': app_path,
            'timestamp': datetime.now().isoformat(),
            'vulnerabilities': [],
            'threats': [],
            'report': {},
            'auto_fixes_applied': 0
        }
        
        try:
            # Scan for vulnerabilities
            vulnerabilities = await self.scanner.scan_application(app_path)
            analysis_result['vulnerabilities'] = vulnerabilities
            
            # Scan for threats
            threats = await self.threat_monitor.scan_for_threats(app_path)
            analysis_result['threats'] = threats
            
            # Auto-fix vulnerabilities if enabled
            if auto_fix:
                for vuln in vulnerabilities:
                    if await self.fixer.auto_fix_vulnerability(vuln):
                        analysis_result['auto_fixes_applied'] += 1
            
            # Generate security report
            report = await self.reporter.generate_security_report(app_path, vulnerabilities, threats)
            analysis_result['report'] = report
            
            # Save results to database
            await self._save_analysis_results(analysis_result)
            
            logger.info(f"✅ Security analysis complete - Score: {report['security_score']}/100")
            
        except Exception as e:
            logger.error(f"Security analysis failed: {e}")
            analysis_result['error'] = str(e)
            
        return analysis_result
    
    async def _save_analysis_results(self, analysis_result: Dict[str, Any]):
        """Save analysis results to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            report = analysis_result['report']
            
            # Save scan summary
            cursor.execute("""
                INSERT INTO security_scans 
                (app_path, scan_timestamp, vulnerabilities_found, vulnerabilities_fixed, security_score, report_data)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                analysis_result['app_path'],
                analysis_result['timestamp'],
                len(analysis_result['vulnerabilities']),
                analysis_result['auto_fixes_applied'],
                report.get('security_score', 0),
                json.dumps(report)
            ))
            
            # Save individual vulnerabilities
            for vuln in analysis_result['vulnerabilities']:
                cursor.execute("""
                    INSERT OR REPLACE INTO vulnerabilities 
                    (id, app_path, severity, category, description, file_path, line_number, detected_at, fixed, fix_suggestion)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    vuln.vuln_id,
                    analysis_result['app_path'],
                    vuln.severity,
                    vuln.category,
                    vuln.description,
                    vuln.file_path,
                    vuln.line_number,
                    vuln.detected_at.isoformat(),
                    vuln.fixed,
                    vuln.fix_suggestion
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to save analysis results: {e}")
    
    async def get_security_dashboard(self) -> Dict[str, Any]:
        """Get security dashboard data"""
        dashboard = {
            'overall_security_score': 0,
            'recent_scans': [],
            'vulnerability_trends': {},
            'threat_summary': {},
            'compliance_status': {},
            'recommendations': []
        }
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get recent scans
            cursor.execute("""
                SELECT app_path, scan_timestamp, vulnerabilities_found, vulnerabilities_fixed, security_score
                FROM security_scans 
                ORDER BY scan_timestamp DESC 
                LIMIT 10
            """)
            
            recent_scores = []
            for row in cursor.fetchall():
                scan_data = {
                    'app_path': row[0],
                    'timestamp': row[1],
                    'vulnerabilities_found': row[2],
                    'vulnerabilities_fixed': row[3],
                    'security_score': row[4]
                }
                dashboard['recent_scans'].append(scan_data)
                recent_scores.append(row[4])
            
            # Calculate overall security score
            if recent_scores:
                dashboard['overall_security_score'] = sum(recent_scores) / len(recent_scores)
            
            # Get vulnerability statistics
            cursor.execute("""
                SELECT severity, COUNT(*) 
                FROM vulnerabilities 
                WHERE NOT fixed 
                GROUP BY severity
            """)
            
            dashboard['vulnerability_trends'] = dict(cursor.fetchall())
            
            conn.close()
            
        except Exception as e:
            logger.error(f"Dashboard generation failed: {e}")
            
        return dashboard

# Main execution
async def main():
    """Main function to demonstrate Security Intelligence Engine"""
    engine = SecurityIntelligenceEngine()
    
    print("🛡️ Security Intelligence Engine Demo")
    print("=" * 50)
    
    # Demo with workspace app
    workspace_path = Path("C:/agent/workspace/generated-app")
    if workspace_path.exists():
        app_dirs = [d for d in workspace_path.iterdir() if d.is_dir()]
        
        if app_dirs:
            latest_app = max(app_dirs, key=lambda x: x.stat().st_mtime)
            print(f"🔍 Analyzing security for: {latest_app.name}")
            
            # Run security analysis
            results = await engine.run_security_analysis(str(latest_app), auto_fix=True)
            
            print(f"\n📊 Security Analysis Results:")
            print(f"   Vulnerabilities Found: {len(results['vulnerabilities'])}")
            print(f"   Auto-fixes Applied: {results['auto_fixes_applied']}")
            print(f"   Security Score: {results['report']['security_score']}/100")
            print(f"   Threats Detected: {len(results['threats'])}")
            
            # Show recommendations
            if results['report']['recommendations']:
                print(f"\n💡 Top Recommendations:")
                for i, rec in enumerate(results['report']['recommendations'][:3], 1):
                    print(f"   {i}. {rec}")
    
    print("\n✨ Security Intelligence Engine initialized successfully!")

if __name__ == "__main__":
    asyncio.run(main())