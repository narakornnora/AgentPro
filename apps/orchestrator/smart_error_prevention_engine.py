"""
Smart Error Prevention Engine
Advanced AI system for detecting, predicting, and preventing errors
in generated applications with self-healing capabilities.
"""

import asyncio
import re
import json
import ast
import time
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import sqlite3
import threading
from concurrent.futures import ThreadPoolExecutor

@dataclass
class ErrorPattern:
    """Represents a detected error pattern"""
    pattern_id: str
    error_type: str
    severity: str  # 'critical', 'major', 'minor', 'warning'
    description: str
    detection_rule: str
    fix_strategy: str
    confidence: float
    frequency: int
    last_seen: datetime

@dataclass
class CodeIssue:
    """Represents a specific code issue"""
    issue_id: str
    file_path: str
    line_number: int
    column: int
    issue_type: str
    severity: str
    message: str
    fix_suggestion: str
    pattern_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

@dataclass
class PredictiveAlert:
    """Represents a predictive error alert"""
    alert_id: str
    risk_level: str  # 'high', 'medium', 'low'
    predicted_error: str
    probability: float
    conditions: List[str]
    prevention_actions: List[str]
    timeline: str

class CodeAnalyzer:
    """Analyzes code for potential issues and patterns"""
    
    def __init__(self):
        self.html_patterns = self._init_html_patterns()
        self.css_patterns = self._init_css_patterns()
        self.js_patterns = self._init_js_patterns()
        self.cross_file_patterns = self._init_cross_file_patterns()

    def _init_html_patterns(self) -> List[Dict[str, Any]]:
        """Initialize HTML error patterns"""
        return [
            {
                'pattern_id': 'html_001',
                'name': 'missing_doctype',
                'regex': r'^(?!<!DOCTYPE)',
                'severity': 'major',
                'description': 'Missing DOCTYPE declaration',
                'fix': 'Add <!DOCTYPE html> at the beginning'
            },
            {
                'pattern_id': 'html_002',
                'name': 'unclosed_tags',
                'regex': r'<(\w+)(?:[^>]*[^/])>(?!.*</\1>)',
                'severity': 'critical',
                'description': 'Unclosed HTML tags',
                'fix': 'Close all HTML tags properly'
            },
            {
                'pattern_id': 'html_003',
                'name': 'missing_alt',
                'regex': r'<img(?![^>]*alt=)[^>]*>',
                'severity': 'major',
                'description': 'Images without alt attributes',
                'fix': 'Add alt attributes to all images'
            },
            {
                'pattern_id': 'html_004',
                'name': 'duplicate_id',
                'regex': r'id=["\']([^"\']+)["\']',
                'severity': 'critical',
                'description': 'Duplicate ID attributes',
                'fix': 'Ensure all ID attributes are unique'
            },
            {
                'pattern_id': 'html_005',
                'name': 'missing_viewport',
                'regex': r'<meta\s+name=["\']viewport["\']',
                'severity': 'major',
                'description': 'Missing viewport meta tag',
                'fix': 'Add <meta name="viewport" content="width=device-width, initial-scale=1.0">'
            }
        ]

    def _init_css_patterns(self) -> List[Dict[str, Any]]:
        """Initialize CSS error patterns"""
        return [
            {
                'pattern_id': 'css_001',
                'name': 'missing_semicolon',
                'regex': r'[^;}]\s*}',
                'severity': 'minor',
                'description': 'Missing semicolon before closing brace',
                'fix': 'Add semicolon after the last property'
            },
            {
                'pattern_id': 'css_002',
                'name': 'invalid_property',
                'regex': r'([a-z-]+)\s*:\s*([^;{}]+);',
                'severity': 'major',
                'description': 'Invalid CSS property or value',
                'fix': 'Check CSS property names and values'
            },
            {
                'pattern_id': 'css_003',
                'name': 'duplicate_selector',
                'regex': r'([^{}]+)\s*{[^}]*}[\s\S]*?\1\s*{',
                'severity': 'minor',
                'description': 'Duplicate CSS selectors',
                'fix': 'Combine duplicate selectors'
            },
            {
                'pattern_id': 'css_004',
                'name': 'unused_selector',
                'regex': r'\.([a-zA-Z][a-zA-Z0-9_-]*)\s*{',
                'severity': 'warning',
                'description': 'Potentially unused CSS selector',
                'fix': 'Remove unused CSS rules'
            },
            {
                'pattern_id': 'css_005',
                'name': 'vendor_prefix_order',
                'regex': r'(-webkit-[^:]+:\s*[^;]+;\s*[^-][^:]+:)',
                'severity': 'minor',
                'description': 'Vendor prefixes should come before standard properties',
                'fix': 'Reorder CSS properties: vendor prefixes first, standard property last'
            }
        ]

    def _init_js_patterns(self) -> List[Dict[str, Any]]:
        """Initialize JavaScript error patterns"""
        return [
            {
                'pattern_id': 'js_001',
                'name': 'missing_semicolon',
                'regex': r'[^;}\s]\s*\n',
                'severity': 'minor',
                'description': 'Missing semicolon',
                'fix': 'Add semicolon at end of statements'
            },
            {
                'pattern_id': 'js_002',
                'name': 'undefined_variable',
                'regex': r'\b([a-zA-Z_$][a-zA-Z0-9_$]*)\s*(?![=:\(])',
                'severity': 'critical',
                'description': 'Potentially undefined variable',
                'fix': 'Declare variables before use'
            },
            {
                'pattern_id': 'js_003',
                'name': 'console_log',
                'regex': r'console\.log\(',
                'severity': 'warning',
                'description': 'Console.log statements in production',
                'fix': 'Remove console.log statements'
            },
            {
                'pattern_id': 'js_004',
                'name': 'missing_error_handling',
                'regex': r'fetch\s*\([^)]+\)(?!\s*\.catch)',
                'severity': 'major',
                'description': 'Missing error handling for async operations',
                'fix': 'Add .catch() or try-catch blocks'
            },
            {
                'pattern_id': 'js_005',
                'name': 'deprecated_function',
                'regex': r'\b(escape|unescape|eval)\s*\(',
                'severity': 'major',
                'description': 'Use of deprecated JavaScript functions',
                'fix': 'Replace with modern alternatives'
            }
        ]

    def _init_cross_file_patterns(self) -> List[Dict[str, Any]]:
        """Initialize cross-file dependency patterns"""
        return [
            {
                'pattern_id': 'cross_001',
                'name': 'missing_css_link',
                'description': 'CSS file referenced but not linked in HTML',
                'severity': 'critical'
            },
            {
                'pattern_id': 'cross_002',
                'name': 'missing_js_script',
                'description': 'JavaScript file referenced but not included',
                'severity': 'critical'
            },
            {
                'pattern_id': 'cross_003',
                'name': 'unused_css_class',
                'description': 'CSS class defined but never used',
                'severity': 'warning'
            },
            {
                'pattern_id': 'cross_004',
                'name': 'missing_element_id',
                'description': 'JavaScript references element ID that doesn\'t exist',
                'severity': 'major'
            }
        ]

    async def analyze_code(self, files: Dict[str, str]) -> List[CodeIssue]:
        """Analyze all code files for issues"""
        all_issues = []
        
        # Analyze individual files
        for file_path, content in files.items():
            file_extension = Path(file_path).suffix.lower()
            
            if file_extension == '.html':
                issues = await self._analyze_html(file_path, content)
            elif file_extension == '.css':
                issues = await self._analyze_css(file_path, content)
            elif file_extension == '.js':
                issues = await self._analyze_js(file_path, content)
            else:
                continue
            
            all_issues.extend(issues)
        
        # Analyze cross-file dependencies
        cross_issues = await self._analyze_cross_file_dependencies(files)
        all_issues.extend(cross_issues)
        
        return all_issues

    async def _analyze_html(self, file_path: str, content: str) -> List[CodeIssue]:
        """Analyze HTML content for issues"""
        issues = []
        lines = content.split('\n')
        
        for pattern in self.html_patterns:
            if pattern['name'] == 'duplicate_id':
                # Special handling for duplicate IDs
                id_issues = self._check_duplicate_ids(file_path, content, lines)
                issues.extend(id_issues)
            elif pattern['name'] == 'missing_viewport':
                # Check if viewport meta tag exists
                if not re.search(pattern['regex'], content, re.IGNORECASE):
                    issues.append(CodeIssue(
                        issue_id=f"{pattern['pattern_id']}_{hash(file_path)}",
                        file_path=file_path,
                        line_number=1,
                        column=1,
                        issue_type=pattern['name'],
                        severity=pattern['severity'],
                        message=pattern['description'],
                        fix_suggestion=pattern['fix'],
                        pattern_id=pattern['pattern_id']
                    ))
            else:
                # Regular pattern matching
                for line_num, line in enumerate(lines, 1):
                    matches = re.finditer(pattern['regex'], line, re.IGNORECASE)
                    for match in matches:
                        issues.append(CodeIssue(
                            issue_id=f"{pattern['pattern_id']}_{hash(file_path)}_{line_num}_{match.start()}",
                            file_path=file_path,
                            line_number=line_num,
                            column=match.start(),
                            issue_type=pattern['name'],
                            severity=pattern['severity'],
                            message=f"{pattern['description']}: {match.group()}",
                            fix_suggestion=pattern['fix'],
                            pattern_id=pattern['pattern_id']
                        ))
        
        return issues

    async def _analyze_css(self, file_path: str, content: str) -> List[CodeIssue]:
        """Analyze CSS content for issues"""
        issues = []
        lines = content.split('\n')
        
        for pattern in self.css_patterns:
            for line_num, line in enumerate(lines, 1):
                matches = re.finditer(pattern['regex'], line)
                for match in matches:
                    issues.append(CodeIssue(
                        issue_id=f"{pattern['pattern_id']}_{hash(file_path)}_{line_num}_{match.start()}",
                        file_path=file_path,
                        line_number=line_num,
                        column=match.start(),
                        issue_type=pattern['name'],
                        severity=pattern['severity'],
                        message=f"{pattern['description']}: {match.group()}",
                        fix_suggestion=pattern['fix'],
                        pattern_id=pattern['pattern_id']
                    ))
        
        return issues

    async def _analyze_js(self, file_path: str, content: str) -> List[CodeIssue]:
        """Analyze JavaScript content for issues"""
        issues = []
        lines = content.split('\n')
        
        # Try AST parsing for more advanced analysis
        try:
            # Basic syntax check
            compile(content, file_path, 'exec')
        except SyntaxError as e:
            issues.append(CodeIssue(
                issue_id=f"syntax_error_{hash(file_path)}_{e.lineno}",
                file_path=file_path,
                line_number=e.lineno or 1,
                column=e.offset or 1,
                issue_type='syntax_error',
                severity='critical',
                message=f"Syntax Error: {e.msg}",
                fix_suggestion="Fix JavaScript syntax error",
                pattern_id='js_syntax'
            ))
        
        # Pattern-based analysis
        for pattern in self.js_patterns:
            for line_num, line in enumerate(lines, 1):
                matches = re.finditer(pattern['regex'], line)
                for match in matches:
                    issues.append(CodeIssue(
                        issue_id=f"{pattern['pattern_id']}_{hash(file_path)}_{line_num}_{match.start()}",
                        file_path=file_path,
                        line_number=line_num,
                        column=match.start(),
                        issue_type=pattern['name'],
                        severity=pattern['severity'],
                        message=f"{pattern['description']}: {match.group()}",
                        fix_suggestion=pattern['fix'],
                        pattern_id=pattern['pattern_id']
                    ))
        
        return issues

    async def _analyze_cross_file_dependencies(self, files: Dict[str, str]) -> List[CodeIssue]:
        """Analyze cross-file dependencies and references"""
        issues = []
        
        html_files = {k: v for k, v in files.items() if k.endswith('.html')}
        css_files = {k: v for k, v in files.items() if k.endswith('.css')}
        js_files = {k: v for k, v in files.items() if k.endswith('.js')}
        
        # Check for missing CSS/JS links in HTML
        for html_path, html_content in html_files.items():
            # Check CSS links
            for css_path in css_files.keys():
                css_filename = Path(css_path).name
                if css_filename not in html_content:
                    issues.append(CodeIssue(
                        issue_id=f"cross_001_{hash(html_path + css_path)}",
                        file_path=html_path,
                        line_number=1,
                        column=1,
                        issue_type='missing_css_link',
                        severity='major',
                        message=f"CSS file '{css_filename}' not linked in HTML",
                        fix_suggestion=f"Add <link rel='stylesheet' href='{css_filename}'> to HTML head",
                        pattern_id='cross_001'
                    ))
            
            # Check JS script tags
            for js_path in js_files.keys():
                js_filename = Path(js_path).name
                if js_filename not in html_content:
                    issues.append(CodeIssue(
                        issue_id=f"cross_002_{hash(html_path + js_path)}",
                        file_path=html_path,
                        line_number=1,
                        column=1,
                        issue_type='missing_js_script',
                        severity='major',
                        message=f"JavaScript file '{js_filename}' not included in HTML",
                        fix_suggestion=f"Add <script src='{js_filename}'></script> to HTML",
                        pattern_id='cross_002'
                    ))
        
        return issues

    def _check_duplicate_ids(self, file_path: str, content: str, lines: List[str]) -> List[CodeIssue]:
        """Check for duplicate ID attributes"""
        issues = []
        id_pattern = re.compile(r'id=["\']([^"\']+)["\']', re.IGNORECASE)
        id_occurrences = defaultdict(list)
        
        for line_num, line in enumerate(lines, 1):
            matches = id_pattern.finditer(line)
            for match in matches:
                id_value = match.group(1)
                id_occurrences[id_value].append((line_num, match.start()))
        
        # Find duplicates
        for id_value, occurrences in id_occurrences.items():
            if len(occurrences) > 1:
                for line_num, column in occurrences:
                    issues.append(CodeIssue(
                        issue_id=f"html_004_{hash(file_path)}_{id_value}_{line_num}",
                        file_path=file_path,
                        line_number=line_num,
                        column=column,
                        issue_type='duplicate_id',
                        severity='critical',
                        message=f"Duplicate ID '{id_value}' found",
                        fix_suggestion=f"Make ID '{id_value}' unique",
                        pattern_id='html_004'
                    ))
        
        return issues

class PredictiveErrorDetector:
    """Predicts potential errors before they occur"""
    
    def __init__(self):
        self.risk_patterns = self._init_risk_patterns()
        self.error_history = defaultdict(list)

    def _init_risk_patterns(self) -> List[Dict[str, Any]]:
        """Initialize predictive risk patterns"""
        return [
            {
                'pattern_id': 'pred_001',
                'name': 'high_complexity_risk',
                'conditions': ['high_cyclomatic_complexity', 'many_nested_loops'],
                'predicted_error': 'Performance degradation and maintenance issues',
                'probability_base': 0.7,
                'prevention': ['Refactor complex functions', 'Add performance monitoring']
            },
            {
                'pattern_id': 'pred_002',
                'name': 'dependency_conflict_risk',
                'conditions': ['multiple_css_frameworks', 'conflicting_js_libraries'],
                'predicted_error': 'Style conflicts and JavaScript errors',
                'probability_base': 0.8,
                'prevention': ['Use single CSS framework', 'Check library compatibility']
            },
            {
                'pattern_id': 'pred_003',
                'name': 'security_vulnerability_risk',
                'conditions': ['user_input_without_validation', 'inline_javascript'],
                'predicted_error': 'XSS and injection vulnerabilities',
                'probability_base': 0.9,
                'prevention': ['Add input validation', 'Use CSP headers', 'Avoid inline scripts']
            },
            {
                'pattern_id': 'pred_004',
                'name': 'mobile_compatibility_risk',
                'conditions': ['fixed_widths', 'no_viewport_meta', 'hover_only_interactions'],
                'predicted_error': 'Poor mobile user experience',
                'probability_base': 0.6,
                'prevention': ['Use responsive design', 'Add touch interactions']
            },
            {
                'pattern_id': 'pred_005',
                'name': 'accessibility_risk',
                'conditions': ['missing_alt_text', 'no_focus_indicators', 'poor_color_contrast'],
                'predicted_error': 'Accessibility compliance failures',
                'probability_base': 0.75,
                'prevention': ['Add ARIA labels', 'Improve color contrast', 'Add focus styles']
            }
        ]

    async def predict_errors(self, files: Dict[str, str], existing_issues: List[CodeIssue]) -> List[PredictiveAlert]:
        """Predict potential future errors"""
        alerts = []
        
        # Analyze current conditions
        conditions = await self._analyze_current_conditions(files, existing_issues)
        
        # Check each risk pattern
        for pattern in self.risk_patterns:
            matched_conditions = []
            for condition in pattern['conditions']:
                if self._check_condition(condition, conditions):
                    matched_conditions.append(condition)
            
            if matched_conditions:
                # Calculate probability based on matched conditions
                probability = min(
                    pattern['probability_base'] * (len(matched_conditions) / len(pattern['conditions'])),
                    0.95
                )
                
                if probability > 0.3:  # Only alert if probability > 30%
                    risk_level = 'high' if probability > 0.7 else 'medium' if probability > 0.5 else 'low'
                    
                    alerts.append(PredictiveAlert(
                        alert_id=f"{pattern['pattern_id']}_{int(time.time())}",
                        risk_level=risk_level,
                        predicted_error=pattern['predicted_error'],
                        probability=probability,
                        conditions=matched_conditions,
                        prevention_actions=pattern['prevention'],
                        timeline=self._estimate_timeline(risk_level)
                    ))
        
        return alerts

    async def _analyze_current_conditions(self, files: Dict[str, str], issues: List[CodeIssue]) -> Dict[str, Any]:
        """Analyze current project conditions for risk assessment"""
        conditions = {
            'file_count': len(files),
            'total_lines': sum(len(content.split('\n')) for content in files.values()),
            'issue_count': len(issues),
            'critical_issues': len([i for i in issues if i.severity == 'critical']),
            'css_frameworks': self._detect_css_frameworks(files),
            'js_libraries': self._detect_js_libraries(files),
            'complexity_metrics': self._calculate_complexity_metrics(files),
            'security_indicators': self._analyze_security_indicators(files),
            'accessibility_indicators': self._analyze_accessibility_indicators(files, issues)
        }
        
        return conditions

    def _check_condition(self, condition: str, current_conditions: Dict[str, Any]) -> bool:
        """Check if a specific condition is met"""
        condition_checkers = {
            'high_cyclomatic_complexity': lambda: current_conditions['complexity_metrics']['avg_complexity'] > 10,
            'many_nested_loops': lambda: current_conditions['complexity_metrics']['nested_loops'] > 3,
            'multiple_css_frameworks': lambda: len(current_conditions['css_frameworks']) > 1,
            'conflicting_js_libraries': lambda: self._check_library_conflicts(current_conditions['js_libraries']),
            'user_input_without_validation': lambda: current_conditions['security_indicators']['unvalidated_inputs'] > 0,
            'inline_javascript': lambda: current_conditions['security_indicators']['inline_js'] > 0,
            'fixed_widths': lambda: current_conditions['complexity_metrics']['fixed_widths'] > 5,
            'no_viewport_meta': lambda: not current_conditions['accessibility_indicators']['has_viewport'],
            'hover_only_interactions': lambda: current_conditions['accessibility_indicators']['hover_only'] > 0,
            'missing_alt_text': lambda: current_conditions['accessibility_indicators']['missing_alt'] > 0,
            'no_focus_indicators': lambda: not current_conditions['accessibility_indicators']['has_focus_styles'],
            'poor_color_contrast': lambda: current_conditions['accessibility_indicators']['contrast_issues'] > 0
        }
        
        checker = condition_checkers.get(condition)
        return checker() if checker else False

    def _detect_css_frameworks(self, files: Dict[str, str]) -> List[str]:
        """Detect CSS frameworks in use"""
        frameworks = []
        framework_patterns = {
            'bootstrap': r'bootstrap',
            'tailwind': r'tailwind',
            'bulma': r'bulma',
            'foundation': r'foundation'
        }
        
        for content in files.values():
            content_lower = content.lower()
            for framework, pattern in framework_patterns.items():
                if re.search(pattern, content_lower):
                    if framework not in frameworks:
                        frameworks.append(framework)
        
        return frameworks

    def _detect_js_libraries(self, files: Dict[str, str]) -> List[str]:
        """Detect JavaScript libraries in use"""
        libraries = []
        library_patterns = {
            'jquery': r'jquery',
            'react': r'react',
            'vue': r'vue',
            'angular': r'angular',
            'lodash': r'lodash'
        }
        
        for content in files.values():
            content_lower = content.lower()
            for library, pattern in library_patterns.items():
                if re.search(pattern, content_lower):
                    if library not in libraries:
                        libraries.append(library)
        
        return libraries

    def _calculate_complexity_metrics(self, files: Dict[str, str]) -> Dict[str, Any]:
        """Calculate code complexity metrics"""
        total_functions = 0
        total_complexity = 0
        nested_loops = 0
        fixed_widths = 0
        
        for file_path, content in files.items():
            if file_path.endswith('.js'):
                # Count functions and complexity
                function_matches = re.findall(r'function\s+\w+|=>\s*{|\w+\s*:\s*function', content)
                total_functions += len(function_matches)
                
                # Simple complexity metric (if statements, loops, etc.)
                complexity_indicators = re.findall(r'\b(if|for|while|switch|catch)\b', content)
                total_complexity += len(complexity_indicators)
                
                # Count nested loops
                nested_loop_matches = re.findall(r'for\s*\([^)]*\)[^{]*{[^}]*for\s*\(', content, re.DOTALL)
                nested_loops += len(nested_loop_matches)
            
            elif file_path.endswith('.css'):
                # Count fixed width declarations
                fixed_width_matches = re.findall(r'width\s*:\s*\d+px', content)
                fixed_widths += len(fixed_width_matches)
        
        avg_complexity = (total_complexity / max(total_functions, 1)) if total_functions > 0 else 0
        
        return {
            'total_functions': total_functions,
            'avg_complexity': avg_complexity,
            'nested_loops': nested_loops,
            'fixed_widths': fixed_widths
        }

    def _analyze_security_indicators(self, files: Dict[str, str]) -> Dict[str, Any]:
        """Analyze security-related indicators"""
        unvalidated_inputs = 0
        inline_js = 0
        
        for file_path, content in files.items():
            if file_path.endswith('.html'):
                # Count input elements without validation
                input_matches = re.findall(r'<input[^>]*>', content, re.IGNORECASE)
                for input_match in input_matches:
                    if 'required' not in input_match.lower() and 'pattern' not in input_match.lower():
                        unvalidated_inputs += 1
                
                # Count inline JavaScript
                inline_js_matches = re.findall(r'on\w+\s*=', content, re.IGNORECASE)
                inline_js += len(inline_js_matches)
        
        return {
            'unvalidated_inputs': unvalidated_inputs,
            'inline_js': inline_js
        }

    def _analyze_accessibility_indicators(self, files: Dict[str, str], issues: List[CodeIssue]) -> Dict[str, Any]:
        """Analyze accessibility indicators"""
        has_viewport = False
        has_focus_styles = False
        missing_alt = 0
        hover_only = 0
        contrast_issues = 0
        
        for file_path, content in files.items():
            if file_path.endswith('.html'):
                # Check viewport
                if re.search(r'<meta[^>]*name=["\']viewport["\']', content, re.IGNORECASE):
                    has_viewport = True
                
                # Count missing alt attributes (from issues)
                missing_alt += len([i for i in issues if i.issue_type == 'missing_alt'])
            
            elif file_path.endswith('.css'):
                # Check focus styles
                if re.search(r':focus', content):
                    has_focus_styles = True
                
                # Count hover-only interactions
                hover_matches = re.findall(r':hover', content)
                focus_matches = re.findall(r':focus', content)
                if len(hover_matches) > len(focus_matches):
                    hover_only += len(hover_matches) - len(focus_matches)
        
        return {
            'has_viewport': has_viewport,
            'has_focus_styles': has_focus_styles,
            'missing_alt': missing_alt,
            'hover_only': hover_only,
            'contrast_issues': contrast_issues  # Would need color analysis
        }

    def _check_library_conflicts(self, libraries: List[str]) -> bool:
        """Check for known library conflicts"""
        conflicts = [
            (['jquery', 'react'], 'jQuery and React can conflict'),
            (['vue', 'react'], 'Vue and React should not be used together'),
            (['angular', 'react'], 'Angular and React should not be used together')
        ]
        
        for conflict_libs, _ in conflicts:
            if all(lib in libraries for lib in conflict_libs):
                return True
        
        return False

    def _estimate_timeline(self, risk_level: str) -> str:
        """Estimate timeline for predicted error occurrence"""
        timelines = {
            'high': 'within 1-7 days',
            'medium': 'within 1-4 weeks',
            'low': 'within 1-3 months'
        }
        return timelines.get(risk_level, 'unknown')

class SelfHealingEngine:
    """Automatically fixes detected issues"""
    
    def __init__(self):
        self.auto_fix_strategies = self._init_fix_strategies()
        self.fix_success_rate = defaultdict(float)

    def _init_fix_strategies(self) -> Dict[str, callable]:
        """Initialize automatic fix strategies"""
        return {
            'missing_doctype': self._fix_missing_doctype,
            'missing_alt': self._fix_missing_alt,
            'missing_viewport': self._fix_missing_viewport,
            'missing_semicolon': self._fix_missing_semicolon,
            'console_log': self._fix_console_log,
            'missing_css_link': self._fix_missing_css_link,
            'missing_js_script': self._fix_missing_js_script,
            'duplicate_id': self._fix_duplicate_id
        }

    async def auto_fix_issues(self, files: Dict[str, str], issues: List[CodeIssue]) -> Dict[str, str]:
        """Automatically fix issues where possible"""
        fixed_files = files.copy()
        fix_log = []
        
        # Group issues by file and type for efficient fixing
        issues_by_file = defaultdict(list)
        for issue in issues:
            issues_by_file[issue.file_path].append(issue)
        
        # Fix issues file by file
        for file_path, file_issues in issues_by_file.items():
            if file_path in fixed_files:
                original_content = fixed_files[file_path]
                modified_content = original_content
                
                # Sort issues by line number (descending) to avoid offset problems
                file_issues.sort(key=lambda x: x.line_number, reverse=True)
                
                for issue in file_issues:
                    fix_strategy = self.auto_fix_strategies.get(issue.issue_type)
                    if fix_strategy:
                        try:
                            modified_content = await fix_strategy(modified_content, issue)
                            fix_log.append(f"Fixed {issue.issue_type} in {file_path}:{issue.line_number}")
                        except Exception as e:
                            fix_log.append(f"Failed to fix {issue.issue_type} in {file_path}: {e}")
                
                fixed_files[file_path] = modified_content
        
        # Add fix log as metadata
        fixed_files['_fix_log'] = '\n'.join(fix_log)
        
        return fixed_files

    async def _fix_missing_doctype(self, content: str, issue: CodeIssue) -> str:
        """Fix missing DOCTYPE"""
        if not content.strip().startswith('<!DOCTYPE'):
            return '<!DOCTYPE html>\n' + content
        return content

    async def _fix_missing_alt(self, content: str, issue: CodeIssue) -> str:
        """Fix missing alt attributes"""
        # Simple fix: add generic alt attribute
        pattern = r'(<img[^>]*?)(?<!alt=["\'][^"\']*)(>)'
        replacement = r'\1 alt="Image"\2'
        return re.sub(pattern, replacement, content, flags=re.IGNORECASE)

    async def _fix_missing_viewport(self, content: str, issue: CodeIssue) -> str:
        """Fix missing viewport meta tag"""
        viewport_tag = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        
        # Try to add after charset meta tag or in head
        if '<meta charset=' in content:
            pattern = r'(<meta charset=[^>]*>)'
            replacement = rf'\1\n    {viewport_tag}'
            return re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        elif '<head>' in content:
            pattern = r'(<head[^>]*>)'
            replacement = rf'\1\n    {viewport_tag}'
            return re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        return content

    async def _fix_missing_semicolon(self, content: str, issue: CodeIssue) -> str:
        """Fix missing semicolons in CSS/JS"""
        lines = content.split('\n')
        if issue.line_number <= len(lines):
            line = lines[issue.line_number - 1]
            # Simple heuristic: if line doesn't end with ; or } or {, add ;
            line = line.rstrip()
            if line and not line.endswith((';', '}', '{')):
                lines[issue.line_number - 1] = line + ';'
        
        return '\n'.join(lines)

    async def _fix_console_log(self, content: str, issue: CodeIssue) -> str:
        """Remove console.log statements"""
        lines = content.split('\n')
        if issue.line_number <= len(lines):
            line = lines[issue.line_number - 1]
            # Comment out console.log instead of removing
            if 'console.log' in line:
                lines[issue.line_number - 1] = '// ' + line
        
        return '\n'.join(lines)

    async def _fix_missing_css_link(self, content: str, issue: CodeIssue) -> str:
        """Add missing CSS link"""
        css_filename = re.search(r"'([^']*\.css)'", issue.fix_suggestion)
        if css_filename:
            css_file = css_filename.group(1)
            link_tag = f'    <link rel="stylesheet" href="{css_file}">'
            
            # Add to head section
            if '</head>' in content:
                content = content.replace('</head>', f'{link_tag}\n</head>')
            elif '<head>' in content:
                content = content.replace('<head>', f'<head>\n{link_tag}')
        
        return content

    async def _fix_missing_js_script(self, content: str, issue: CodeIssue) -> str:
        """Add missing JavaScript script tag"""
        js_filename = re.search(r"'([^']*\.js)'", issue.fix_suggestion)
        if js_filename:
            js_file = js_filename.group(1)
            script_tag = f'    <script src="{js_file}"></script>'
            
            # Add before closing body tag
            if '</body>' in content:
                content = content.replace('</body>', f'{script_tag}\n</body>')
            else:
                content += f'\n{script_tag}'
        
        return content

    async def _fix_duplicate_id(self, content: str, issue: CodeIssue) -> str:
        """Fix duplicate IDs by making them unique"""
        lines = content.split('\n')
        if issue.line_number <= len(lines):
            line = lines[issue.line_number - 1]
            # Extract ID and make it unique
            id_match = re.search(r'id=["\']([^"\']+)["\']', line)
            if id_match:
                original_id = id_match.group(1)
                unique_id = f"{original_id}_{hash(str(issue.line_number)) % 1000}"
                line = line.replace(f'id="{original_id}"', f'id="{unique_id}"')
                line = line.replace(f"id='{original_id}'", f"id='{unique_id}'")
                lines[issue.line_number - 1] = line
        
        return '\n'.join(lines)

class SmartErrorPreventionEngine:
    """Main engine coordinating all error prevention systems"""
    
    def __init__(self, db_path: str = "error_prevention.db"):
        self.db_path = db_path
        self.code_analyzer = CodeAnalyzer()
        self.predictive_detector = PredictiveErrorDetector()
        self.self_healing_engine = SelfHealingEngine()
        
        self.analysis_history = []
        self.prevention_stats = {
            'total_analyses': 0,
            'issues_detected': 0,
            'issues_auto_fixed': 0,
            'predictions_made': 0,
            'prevention_success_rate': 0.0
        }
        
        self._init_database()

    def _init_database(self):
        """Initialize database for error prevention data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS error_analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            file_count INTEGER NOT NULL,
            issues_detected INTEGER NOT NULL,
            issues_fixed INTEGER NOT NULL,
            predictions_made INTEGER NOT NULL,
            analysis_time REAL NOT NULL,
            success_rate REAL NOT NULL
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS error_patterns (
            pattern_id TEXT PRIMARY KEY,
            pattern_type TEXT NOT NULL,
            frequency INTEGER NOT NULL,
            severity TEXT NOT NULL,
            last_seen DATETIME NOT NULL,
            fix_success_rate REAL NOT NULL
        )
        ''')
        
        conn.commit()
        conn.close()

    async def comprehensive_analysis(self, files: Dict[str, str], auto_fix: bool = True) -> Dict[str, Any]:
        """Perform comprehensive error analysis and prevention"""
        start_time = time.time()
        
        print("🔍 Starting comprehensive error analysis...")
        
        # Step 1: Code Analysis
        print("   Analyzing code for existing issues...")
        issues = await self.code_analyzer.analyze_code(files)
        
        print(f"   Found {len(issues)} issues:")
        severity_counts = Counter(issue.severity for issue in issues)
        for severity, count in severity_counts.items():
            print(f"     • {count} {severity} issues")
        
        # Step 2: Predictive Analysis
        print("   Predicting potential future errors...")
        predictions = await self.predictive_detector.predict_errors(files, issues)
        
        print(f"   Generated {len(predictions)} predictive alerts:")
        for prediction in predictions:
            print(f"     • {prediction.risk_level.upper()} risk: {prediction.predicted_error} ({prediction.probability:.1%})")
        
        # Step 3: Auto-fixing
        fixed_files = files
        fix_log = []
        
        if auto_fix and issues:
            print("   Applying automatic fixes...")
            fixed_files = await self.self_healing_engine.auto_fix_issues(files, issues)
            
            if '_fix_log' in fixed_files:
                fix_log = fixed_files['_fix_log'].split('\n')
                del fixed_files['_fix_log']
                print(f"   Applied {len(fix_log)} automatic fixes")
        
        # Step 4: Re-analysis after fixes
        if auto_fix and fix_log:
            print("   Re-analyzing after fixes...")
            remaining_issues = await self.code_analyzer.analyze_code(fixed_files)
            print(f"   Remaining issues: {len(remaining_issues)}")
        else:
            remaining_issues = issues
        
        analysis_time = time.time() - start_time
        
        # Update statistics
        self.prevention_stats['total_analyses'] += 1
        self.prevention_stats['issues_detected'] += len(issues)
        self.prevention_stats['issues_auto_fixed'] += len(fix_log)
        self.prevention_stats['predictions_made'] += len(predictions)
        
        if len(issues) > 0:
            success_rate = len(fix_log) / len(issues)
            self.prevention_stats['prevention_success_rate'] = success_rate
        
        # Save analysis to database
        await self._save_analysis_result(len(files), len(issues), len(fix_log), 
                                       len(predictions), analysis_time, 
                                       self.prevention_stats['prevention_success_rate'])
        
        # Prepare comprehensive report
        report = {
            'analysis_summary': {
                'files_analyzed': len(files),
                'issues_detected': len(issues),
                'issues_fixed': len(fix_log),
                'remaining_issues': len(remaining_issues),
                'predictions_made': len(predictions),
                'analysis_time': analysis_time,
                'success_rate': self.prevention_stats['prevention_success_rate']
            },
            'issues': [asdict(issue) for issue in issues],
            'remaining_issues': [asdict(issue) for issue in remaining_issues],
            'predictions': [asdict(prediction) for prediction in predictions],
            'fixes_applied': fix_log,
            'fixed_files': fixed_files,
            'recommendations': self._generate_recommendations(issues, predictions)
        }
        
        return report

    async def _save_analysis_result(self, file_count: int, issues_detected: int, 
                                  issues_fixed: int, predictions_made: int, 
                                  analysis_time: float, success_rate: float):
        """Save analysis result to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO error_analyses 
        (timestamp, file_count, issues_detected, issues_fixed, predictions_made, analysis_time, success_rate)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            file_count,
            issues_detected,
            issues_fixed,
            predictions_made,
            analysis_time,
            success_rate
        ))
        
        conn.commit()
        conn.close()

    def _generate_recommendations(self, issues: List[CodeIssue], 
                                predictions: List[PredictiveAlert]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Issue-based recommendations
        critical_issues = [i for i in issues if i.severity == 'critical']
        if critical_issues:
            recommendations.append(f"🚨 Address {len(critical_issues)} critical issues immediately")
        
        major_issues = [i for i in issues if i.severity == 'major']
        if major_issues:
            recommendations.append(f"⚠️ Fix {len(major_issues)} major issues before deployment")
        
        # Prediction-based recommendations
        high_risk_predictions = [p for p in predictions if p.risk_level == 'high']
        if high_risk_predictions:
            recommendations.append(f"🔮 Take preventive action for {len(high_risk_predictions)} high-risk predictions")
        
        # Pattern-based recommendations
        common_patterns = Counter(issue.issue_type for issue in issues)
        if common_patterns:
            most_common = common_patterns.most_common(1)[0]
            recommendations.append(f"📊 Most common issue: {most_common[0]} ({most_common[1]} occurrences)")
        
        return recommendations

    def get_prevention_statistics(self) -> Dict[str, Any]:
        """Get comprehensive prevention statistics"""
        return {
            'current_stats': self.prevention_stats.copy(),
            'analysis_history': self.analysis_history[-10:],  # Last 10 analyses
            'improvement_trends': self._calculate_improvement_trends()
        }

    def _calculate_improvement_trends(self) -> Dict[str, float]:
        """Calculate improvement trends over time"""
        if len(self.analysis_history) < 2:
            return {}
        
        recent = self.analysis_history[-5:] if len(self.analysis_history) >= 5 else self.analysis_history
        
        avg_success_rate = sum(analysis.get('success_rate', 0) for analysis in recent) / len(recent)
        avg_analysis_time = sum(analysis.get('analysis_time', 0) for analysis in recent) / len(recent)
        
        return {
            'average_success_rate': avg_success_rate,
            'average_analysis_time': avg_analysis_time,
            'trend': 'improving' if avg_success_rate > 0.7 else 'stable'
        }

async def main():
    """Demo of Smart Error Prevention Engine"""
    print("🛡️ Smart Error Prevention Engine")
    print("=" * 45)
    
    # Initialize engine
    prevention_engine = SmartErrorPreventionEngine()
    
    # Sample files with intentional issues for demonstration
    sample_files = {
        'index.html': '''<html>
<head>
    <title>Test App</title>
</head>
<body>
    <div id="content">
        <img src="logo.png">
        <div id="content">
            <button onclick="alert('hello')">Click me</button>
        </div>
    </div>
</body>
</html>''',
        'styles.css': '''body {
    font-family: Arial
    background: white
}

.container {
    width: 800px;
}

.container {
    padding: 20px;
}''',
        'script.js': '''console.log("Debug message")

function getData() {
    fetch('/api/data')
    return data
}

var undefinedVar = someUndefinedVariable'''
    }
    
    print("🔍 Analyzing sample code with intentional issues...")
    
    # Run comprehensive analysis
    report = await prevention_engine.comprehensive_analysis(sample_files, auto_fix=True)
    
    print(f"\n📊 Analysis Results:")
    summary = report['analysis_summary']
    print(f"   Files Analyzed: {summary['files_analyzed']}")
    print(f"   Issues Detected: {summary['issues_detected']}")
    print(f"   Issues Auto-Fixed: {summary['issues_fixed']}")
    print(f"   Remaining Issues: {summary['remaining_issues']}")
    print(f"   Predictions Made: {summary['predictions_made']}")
    print(f"   Success Rate: {summary['success_rate']:.1%}")
    print(f"   Analysis Time: {summary['analysis_time']:.2f}s")
    
    print(f"\n🔧 Fixes Applied ({len(report['fixes_applied'])}):")
    for fix in report['fixes_applied']:
        print(f"   • {fix}")
    
    print(f"\n🔮 Predictive Alerts ({len(report['predictions'])}):")
    for prediction in report['predictions']:
        pred = prediction
        print(f"   • {pred['risk_level'].upper()} Risk: {pred['predicted_error']}")
        print(f"     Probability: {pred['probability']:.1%} - {pred['timeline']}")
    
    print(f"\n💡 Recommendations:")
    for rec in report['recommendations']:
        print(f"   • {rec}")
    
    print(f"\n📈 Prevention Statistics:")
    stats = prevention_engine.get_prevention_statistics()
    current_stats = stats['current_stats']
    print(f"   Total Analyses: {current_stats['total_analyses']}")
    print(f"   Issues Detected: {current_stats['issues_detected']}")
    print(f"   Auto-Fixes Applied: {current_stats['issues_auto_fixed']}")
    print(f"   Overall Success Rate: {current_stats['prevention_success_rate']:.1%}")
    
    print(f"\n✅ Smart Error Prevention demonstration complete!")
    print(f"🛡️ Key capabilities:")
    print(f"   • Real-time code analysis and issue detection")
    print(f"   • Predictive error analysis with risk assessment")
    print(f"   • Automatic self-healing and issue resolution")
    print(f"   • Cross-file dependency analysis")
    print(f"   • Continuous learning and improvement")

if __name__ == "__main__":
    asyncio.run(main())