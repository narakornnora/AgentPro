"""
UI/UX Quality Control Agent
AI-powered system to monitor, analyze, and ensure high-quality UI/UX standards
before preview with automated correction loop.
"""

import asyncio
import json
import re
import time
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import base64
from bs4 import BeautifulSoup
import cssutils
import logging

# Suppress CSS warnings
cssutils.log.setLevel(logging.ERROR)

@dataclass
class QualityIssue:
    """Represents a UI/UX quality issue"""
    category: str  # 'visual', 'ux', 'accessibility', 'responsive', 'performance'
    severity: str  # 'critical', 'major', 'minor', 'suggestion'
    issue: str
    location: str
    suggested_fix: str
    code_snippet: Optional[str] = None

@dataclass
class QualityReport:
    """Complete quality assessment report"""
    overall_score: float
    passed: bool
    issues: List[QualityIssue]
    strengths: List[str]
    recommendations: List[str]
    timestamp: str

class VisualQualityAnalyzer:
    """Analyzes visual design quality including colors, typography, spacing, layout"""
    
    def __init__(self):
        self.color_standards = {
            'contrast_ratio_aa': 4.5,
            'contrast_ratio_aaa': 7.0,
            'max_colors': 8,
            'primary_colors': 3
        }
        
        self.typography_standards = {
            'min_font_size': 14,
            'max_font_families': 3,
            'line_height_ratio': 1.4,
            'heading_hierarchy': True
        }
        
        self.spacing_standards = {
            'consistent_spacing': True,
            'margin_padding_ratio': 2.0,
            'grid_alignment': True
        }

    async def analyze_visual_quality(self, html_content: str, css_content: str) -> List[QualityIssue]:
        """Analyze visual design quality"""
        issues = []
        
        # Parse HTML and CSS
        soup = BeautifulSoup(html_content, 'html.parser')
        
        try:
            css_sheet = cssutils.parseString(css_content)
        except:
            css_sheet = None
        
        # Color Analysis
        issues.extend(await self._analyze_colors(soup, css_sheet))
        
        # Typography Analysis
        issues.extend(await self._analyze_typography(soup, css_sheet))
        
        # Spacing and Layout Analysis
        issues.extend(await self._analyze_spacing_layout(soup, css_sheet))
        
        # Visual Hierarchy Analysis
        issues.extend(await self._analyze_visual_hierarchy(soup, css_sheet))
        
        return issues

    async def _analyze_colors(self, soup, css_sheet) -> List[QualityIssue]:
        """Analyze color usage and contrast"""
        issues = []
        colors_used = set()
        
        if css_sheet:
            for rule in css_sheet:
                if rule.type == rule.STYLE_RULE:
                    for prop in rule.style:
                        if 'color' in prop.name or 'background' in prop.name:
                            colors_used.add(prop.value)
        
        # Check color count
        if len(colors_used) > self.color_standards['max_colors']:
            issues.append(QualityIssue(
                category='visual',
                severity='major',
                issue=f'Too many colors used ({len(colors_used)}). Recommended maximum: {self.color_standards["max_colors"]}',
                location='Global CSS',
                suggested_fix='Reduce color palette to maintain visual consistency'
            ))
        
        # Check for sufficient contrast (simulated analysis)
        text_elements = soup.find_all(['p', 'span', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if len(text_elements) > 10:  # If many text elements without explicit contrast consideration
            issues.append(QualityIssue(
                category='accessibility',
                severity='major',
                issue='Potential contrast issues detected. Ensure text-background contrast meets WCAG AA standards (4.5:1)',
                location='Text elements',
                suggested_fix='Add explicit color declarations with proper contrast ratios'
            ))
        
        return issues

    async def _analyze_typography(self, soup, css_sheet) -> List[QualityIssue]:
        """Analyze typography quality"""
        issues = []
        font_families = set()
        font_sizes = []
        
        if css_sheet:
            for rule in css_sheet:
                if rule.type == rule.STYLE_RULE:
                    for prop in rule.style:
                        if prop.name == 'font-family':
                            font_families.add(prop.value)
                        elif prop.name == 'font-size':
                            try:
                                size = float(re.findall(r'\d+', prop.value)[0])
                                font_sizes.append(size)
                            except:
                                pass
        
        # Check font family count
        if len(font_families) > self.typography_standards['max_font_families']:
            issues.append(QualityIssue(
                category='visual',
                severity='major',
                issue=f'Too many font families ({len(font_families)}). Recommended maximum: {self.typography_standards["max_font_families"]}',
                location='Typography CSS',
                suggested_fix='Limit to 2-3 font families for consistency'
            ))
        
        # Check minimum font sizes
        if font_sizes and min(font_sizes) < self.typography_standards['min_font_size']:
            issues.append(QualityIssue(
                category='accessibility',
                severity='major',
                issue=f'Font sizes too small (minimum: {min(font_sizes)}px). Recommended minimum: {self.typography_standards["min_font_size"]}px',
                location='Font size declarations',
                suggested_fix='Increase font sizes for better readability'
            ))
        
        # Check heading hierarchy
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        heading_levels = [int(h.name[1]) for h in headings]
        if heading_levels and (min(heading_levels) != 1 or not self._is_sequential(heading_levels)):
            issues.append(QualityIssue(
                category='ux',
                severity='minor',
                issue='Heading hierarchy not properly structured',
                location='HTML headings',
                suggested_fix='Use sequential heading levels (h1, h2, h3...) for proper structure'
            ))
        
        return issues

    async def _analyze_spacing_layout(self, soup, css_sheet) -> List[QualityIssue]:
        """Analyze spacing and layout quality"""
        issues = []
        margins = []
        paddings = []
        
        if css_sheet:
            for rule in css_sheet:
                if rule.type == rule.STYLE_RULE:
                    for prop in rule.style:
                        if 'margin' in prop.name:
                            try:
                                value = float(re.findall(r'\d+', prop.value)[0])
                                margins.append(value)
                            except:
                                pass
                        elif 'padding' in prop.name:
                            try:
                                value = float(re.findall(r'\d+', prop.value)[0])
                                paddings.append(value)
                            except:
                                pass
        
        # Check for consistent spacing
        if margins and len(set(margins)) > 5:
            issues.append(QualityIssue(
                category='visual',
                severity='minor',
                issue='Inconsistent margin values detected',
                location='Margin CSS',
                suggested_fix='Use consistent spacing system (e.g., 8px, 16px, 24px, 32px)'
            ))
        
        if paddings and len(set(paddings)) > 5:
            issues.append(QualityIssue(
                category='visual',
                severity='minor',
                issue='Inconsistent padding values detected',
                location='Padding CSS',
                suggested_fix='Use consistent spacing system for padding'
            ))
        
        return issues

    async def _analyze_visual_hierarchy(self, soup, css_sheet) -> List[QualityIssue]:
        """Analyze visual hierarchy and information architecture"""
        issues = []
        
        # Check for proper use of headings
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if len(headings) == 0:
            issues.append(QualityIssue(
                category='ux',
                severity='major',
                issue='No headings found. Content lacks proper structure',
                location='HTML structure',
                suggested_fix='Add appropriate headings to structure content'
            ))
        
        # Check for navigation elements
        nav_elements = soup.find_all(['nav', 'menu']) + soup.find_all(class_=re.compile(r'nav|menu'))
        if len(nav_elements) == 0 and len(soup.find_all('a')) > 3:
            issues.append(QualityIssue(
                category='ux',
                severity='major',
                issue='Multiple links without proper navigation structure',
                location='Navigation',
                suggested_fix='Organize links in proper navigation components'
            ))
        
        return issues

    def _is_sequential(self, numbers: List[int]) -> bool:
        """Check if heading levels are properly sequential"""
        unique_sorted = sorted(set(numbers))
        for i in range(1, len(unique_sorted)):
            if unique_sorted[i] - unique_sorted[i-1] > 1:
                return False
        return True

class UXValidator:
    """Validates user experience patterns and interactions"""
    
    def __init__(self):
        self.ux_standards = {
            'max_navigation_depth': 3,
            'min_touch_target_size': 44,
            'max_form_fields': 7,
            'required_feedback': True
        }

    async def validate_ux_patterns(self, html_content: str, css_content: str) -> List[QualityIssue]:
        """Validate UX patterns and usability"""
        issues = []
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Navigation UX
        issues.extend(await self._validate_navigation(soup))
        
        # Form UX
        issues.extend(await self._validate_forms(soup))
        
        # Interaction UX
        issues.extend(await self._validate_interactions(soup))
        
        # Content UX
        issues.extend(await self._validate_content(soup))
        
        return issues

    async def _validate_navigation(self, soup) -> List[QualityIssue]:
        """Validate navigation usability"""
        issues = []
        
        # Check for navigation menu
        nav_elements = soup.find_all(['nav', 'menu'])
        links = soup.find_all('a')
        
        if len(links) > 5 and len(nav_elements) == 0:
            issues.append(QualityIssue(
                category='ux',
                severity='major',
                issue='Multiple links without organized navigation',
                location='Navigation structure',
                suggested_fix='Group related links in navigation menus'
            ))
        
        # Check for breadcrumbs on complex sites
        if len(links) > 10 and not soup.find(class_=re.compile(r'breadcrumb')):
            issues.append(QualityIssue(
                category='ux',
                severity='minor',
                issue='Complex site without breadcrumb navigation',
                location='Navigation aids',
                suggested_fix='Add breadcrumb navigation for better orientation'
            ))
        
        return issues

    async def _validate_forms(self, soup) -> List[QualityIssue]:
        """Validate form usability"""
        issues = []
        forms = soup.find_all('form')
        
        for i, form in enumerate(forms):
            inputs = form.find_all(['input', 'select', 'textarea'])
            
            # Check form length
            if len(inputs) > self.ux_standards['max_form_fields']:
                issues.append(QualityIssue(
                    category='ux',
                    severity='major',
                    issue=f'Form {i+1} has too many fields ({len(inputs)}). Recommended maximum: {self.ux_standards["max_form_fields"]}',
                    location=f'Form {i+1}',
                    suggested_fix='Break long forms into multiple steps or sections'
                ))
            
            # Check for labels
            labels = form.find_all('label')
            if len(labels) < len(inputs):
                issues.append(QualityIssue(
                    category='accessibility',
                    severity='major',
                    issue=f'Form {i+1} has inputs without proper labels',
                    location=f'Form {i+1}',
                    suggested_fix='Add descriptive labels for all form inputs'
                ))
            
            # Check for submit button
            submit_buttons = form.find_all(['input', 'button'], type='submit') + form.find_all('button')
            if len(submit_buttons) == 0:
                issues.append(QualityIssue(
                    category='ux',
                    severity='critical',
                    issue=f'Form {i+1} has no submit mechanism',
                    location=f'Form {i+1}',
                    suggested_fix='Add a clear submit button'
                ))
        
        return issues

    async def _validate_interactions(self, soup) -> List[QualityIssue]:
        """Validate interaction patterns"""
        issues = []
        
        # Check for interactive elements
        buttons = soup.find_all('button')
        clickable_elements = soup.find_all(class_=re.compile(r'button|btn|click'))
        
        # Check button text clarity
        for i, button in enumerate(buttons):
            if not button.get_text(strip=True) and not button.get('aria-label'):
                issues.append(QualityIssue(
                    category='accessibility',
                    severity='major',
                    issue=f'Button {i+1} has no descriptive text or label',
                    location=f'Button element {i+1}',
                    suggested_fix='Add descriptive text or aria-label to buttons'
                ))
        
        # Check for loading states indication
        if len(buttons) > 0 and not soup.find(class_=re.compile(r'loading|spinner')):
            issues.append(QualityIssue(
                category='ux',
                severity='minor',
                issue='No loading state indicators found',
                location='Interactive elements',
                suggested_fix='Add loading indicators for better user feedback'
            ))
        
        return issues

    async def _validate_content(self, soup) -> List[QualityIssue]:
        """Validate content presentation"""
        issues = []
        
        # Check for alt text on images
        images = soup.find_all('img')
        images_without_alt = [img for img in images if not img.get('alt')]
        
        if images_without_alt:
            issues.append(QualityIssue(
                category='accessibility',
                severity='major',
                issue=f'{len(images_without_alt)} images without alt text',
                location='Image elements',
                suggested_fix='Add descriptive alt text to all images'
            ))
        
        # Check for empty elements
        empty_elements = soup.find_all(lambda tag: tag.name in ['div', 'span', 'p'] and not tag.get_text(strip=True) and not tag.find_all())
        if empty_elements:
            issues.append(QualityIssue(
                category='visual',
                severity='minor',
                issue=f'{len(empty_elements)} empty content elements found',
                location='Content structure',
                suggested_fix='Remove empty elements or add meaningful content'
            ))
        
        return issues

class ResponsiveAnalyzer:
    """Analyzes responsive design quality"""
    
    def __init__(self):
        self.breakpoints = {
            'mobile': 768,
            'tablet': 1024,
            'desktop': 1200
        }

    async def analyze_responsive_design(self, html_content: str, css_content: str) -> List[QualityIssue]:
        """Analyze responsive design implementation"""
        issues = []
        
        # Check for viewport meta tag
        soup = BeautifulSoup(html_content, 'html.parser')
        viewport_meta = soup.find('meta', attrs={'name': 'viewport'})
        
        if not viewport_meta:
            issues.append(QualityIssue(
                category='responsive',
                severity='critical',
                issue='Missing viewport meta tag',
                location='HTML head',
                suggested_fix='Add <meta name="viewport" content="width=device-width, initial-scale=1.0">'
            ))
        
        # Check for media queries
        media_queries = re.findall(r'@media[^{]*{[^}]*}', css_content, re.DOTALL)
        if not media_queries:
            issues.append(QualityIssue(
                category='responsive',
                severity='major',
                issue='No responsive media queries found',
                location='CSS',
                suggested_fix='Add media queries for different screen sizes'
            ))
        
        # Check for flexible units
        fixed_widths = re.findall(r'width:\s*\d+px', css_content)
        if len(fixed_widths) > 5:
            issues.append(QualityIssue(
                category='responsive',
                severity='minor',
                issue='Excessive use of fixed pixel widths',
                location='CSS width properties',
                suggested_fix='Use relative units (%, em, rem, vw) for better responsiveness'
            ))
        
        return issues

class PerformanceAnalyzer:
    """Analyzes performance-related UI issues"""
    
    async def analyze_performance(self, html_content: str, css_content: str) -> List[QualityIssue]:
        """Analyze performance implications of UI code"""
        issues = []
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Check for large images without optimization
        images = soup.find_all('img')
        for i, img in enumerate(images):
            src = img.get('src', '')
            if src and not any(format in src.lower() for format in ['webp', 'avif']):
                issues.append(QualityIssue(
                    category='performance',
                    severity='minor',
                    issue=f'Image {i+1} not using optimized format',
                    location=f'Image: {src}',
                    suggested_fix='Use WebP or AVIF format for better compression'
                ))
        
        # Check for excessive CSS complexity
        css_rules_count = len(re.findall(r'{[^}]*}', css_content))
        if css_rules_count > 100:
            issues.append(QualityIssue(
                category='performance',
                severity='minor',
                issue=f'CSS complexity is high ({css_rules_count} rules)',
                location='CSS structure',
                suggested_fix='Consider CSS optimization and minification'
            ))
        
        # Check for inline styles
        inline_styles = soup.find_all(style=True)
        if len(inline_styles) > 5:
            issues.append(QualityIssue(
                category='performance',
                severity='minor',
                issue=f'{len(inline_styles)} elements with inline styles',
                location='HTML style attributes',
                suggested_fix='Move inline styles to CSS files for better caching'
            ))
        
        return issues

class AutoFixGenerator:
    """Generates automatic fixes for common UI/UX issues"""
    
    async def generate_fixes(self, issues: List[QualityIssue], html_content: str, css_content: str) -> Dict[str, str]:
        """Generate automatic fixes for detected issues"""
        fixes = {
            'html': html_content,
            'css': css_content,
            'js': '',
            'applied_fixes': []
        }
        
        soup = BeautifulSoup(html_content, 'html.parser')
        modified = False
        
        for issue in issues:
            if issue.severity in ['critical', 'major']:
                if 'viewport meta tag' in issue.issue.lower():
                    # Add viewport meta tag
                    if not soup.find('meta', attrs={'name': 'viewport'}):
                        if soup.head:
                            viewport_tag = soup.new_tag('meta', attrs={
                                'name': 'viewport',
                                'content': 'width=device-width, initial-scale=1.0'
                            })
                            soup.head.insert(0, viewport_tag)
                            modified = True
                            fixes['applied_fixes'].append('Added viewport meta tag')
                
                elif 'images without alt text' in issue.issue.lower():
                    # Add alt text to images
                    images = soup.find_all('img')
                    for i, img in enumerate(images):
                        if not img.get('alt'):
                            img['alt'] = f'Image {i+1}'
                            modified = True
                    if modified:
                        fixes['applied_fixes'].append('Added alt text to images')
                
                elif 'no headings found' in issue.issue.lower():
                    # Add main heading if missing
                    if not soup.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                        body = soup.find('body')
                        if body and body.get_text(strip=True):
                            h1_tag = soup.new_tag('h1')
                            h1_tag.string = 'Main Content'
                            body.insert(0, h1_tag)
                            modified = True
                            fixes['applied_fixes'].append('Added main heading')
        
        if modified:
            fixes['html'] = str(soup)
        
        # CSS fixes
        css_fixes = await self._generate_css_fixes(issues, css_content)
        if css_fixes:
            fixes['css'] = css_fixes
            fixes['applied_fixes'].extend(['Applied CSS improvements'])
        
        return fixes

    async def _generate_css_fixes(self, issues: List[QualityIssue], css_content: str) -> str:
        """Generate CSS fixes for common issues"""
        fixed_css = css_content
        
        # Add responsive base if missing media queries
        if any('media queries' in issue.issue.lower() for issue in issues):
            responsive_base = """
/* Responsive base styles */
@media (max-width: 768px) {
    .container { padding: 1rem; }
    h1 { font-size: 1.8rem; }
    h2 { font-size: 1.5rem; }
}

@media (min-width: 769px) and (max-width: 1024px) {
    .container { padding: 2rem; }
}

@media (min-width: 1025px) {
    .container { max-width: 1200px; margin: 0 auto; }
}
"""
            fixed_css += responsive_base
        
        # Add accessibility improvements
        if any('contrast' in issue.issue.lower() for issue in issues):
            accessibility_css = """
/* Accessibility improvements */
:focus {
    outline: 2px solid #0066cc;
    outline-offset: 2px;
}

button, input, select, textarea {
    font-size: inherit;
    line-height: 1.4;
}
"""
            fixed_css += accessibility_css
        
        return fixed_css

class UIUXQualityAgent:
    """Main UI/UX Quality Control Agent"""
    
    def __init__(self):
        self.visual_analyzer = VisualQualityAnalyzer()
        self.ux_validator = UXValidator()
        self.responsive_analyzer = ResponsiveAnalyzer()
        self.performance_analyzer = PerformanceAnalyzer()
        self.auto_fix_generator = AutoFixGenerator()
        
        self.quality_standards = {
            'minimum_score': 80.0,
            'max_critical_issues': 0,
            'max_major_issues': 2,
            'max_total_issues': 8
        }
        
        self.report_history = []

    async def analyze_quality(self, html_content: str, css_content: str = '', js_content: str = '') -> QualityReport:
        """Perform comprehensive UI/UX quality analysis"""
        print("🔍 Starting UI/UX Quality Analysis...")
        
        all_issues = []
        
        # Visual Quality Analysis
        print("   Analyzing visual design...")
        visual_issues = await self.visual_analyzer.analyze_visual_quality(html_content, css_content)
        all_issues.extend(visual_issues)
        
        # UX Pattern Validation
        print("   Validating UX patterns...")
        ux_issues = await self.ux_validator.validate_ux_patterns(html_content, css_content)
        all_issues.extend(ux_issues)
        
        # Responsive Design Analysis
        print("   Checking responsive design...")
        responsive_issues = await self.responsive_analyzer.analyze_responsive_design(html_content, css_content)
        all_issues.extend(responsive_issues)
        
        # Performance Analysis
        print("   Analyzing performance impact...")
        performance_issues = await self.performance_analyzer.analyze_performance(html_content, css_content)
        all_issues.extend(performance_issues)
        
        # Calculate quality score
        score = self._calculate_quality_score(all_issues)
        
        # Determine if quality passes standards
        passed = self._meets_quality_standards(all_issues, score)
        
        # Generate strengths and recommendations
        strengths = self._identify_strengths(html_content, css_content, all_issues)
        recommendations = self._generate_recommendations(all_issues)
        
        report = QualityReport(
            overall_score=score,
            passed=passed,
            issues=all_issues,
            strengths=strengths,
            recommendations=recommendations,
            timestamp=datetime.now().isoformat()
        )
        
        self.report_history.append(report)
        return report

    def _calculate_quality_score(self, issues: List[QualityIssue]) -> float:
        """Calculate overall quality score (0-100)"""
        base_score = 100.0
        
        for issue in issues:
            if issue.severity == 'critical':
                base_score -= 15.0
            elif issue.severity == 'major':
                base_score -= 8.0
            elif issue.severity == 'minor':
                base_score -= 3.0
            else:  # suggestion
                base_score -= 1.0
        
        return max(0.0, min(100.0, base_score))

    def _meets_quality_standards(self, issues: List[QualityIssue], score: float) -> bool:
        """Check if quality meets minimum standards"""
        critical_count = sum(1 for issue in issues if issue.severity == 'critical')
        major_count = sum(1 for issue in issues if issue.severity == 'major')
        total_count = len(issues)
        
        return (
            score >= self.quality_standards['minimum_score'] and
            critical_count <= self.quality_standards['max_critical_issues'] and
            major_count <= self.quality_standards['max_major_issues'] and
            total_count <= self.quality_standards['max_total_issues']
        )

    def _identify_strengths(self, html_content: str, css_content: str, issues: List[QualityIssue]) -> List[str]:
        """Identify positive aspects of the UI/UX"""
        strengths = []
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Check for semantic HTML
        semantic_tags = soup.find_all(['header', 'nav', 'main', 'section', 'article', 'aside', 'footer'])
        if semantic_tags:
            strengths.append("Good use of semantic HTML elements")
        
        # Check for proper heading structure
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if headings and not any('heading hierarchy' in issue.issue.lower() for issue in issues):
            strengths.append("Well-structured heading hierarchy")
        
        # Check for responsive design
        if '@media' in css_content:
            strengths.append("Responsive design implementation")
        
        # Check for accessibility features
        if soup.find_all(attrs={'aria-label': True}) or soup.find_all(attrs={'role': True}):
            strengths.append("Accessibility attributes present")
        
        # Check for consistent styling
        if 'inconsistent' not in ' '.join([issue.issue.lower() for issue in issues]):
            strengths.append("Consistent design patterns")
        
        return strengths

    def _generate_recommendations(self, issues: List[QualityIssue]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        issue_categories = {}
        for issue in issues:
            if issue.category not in issue_categories:
                issue_categories[issue.category] = []
            issue_categories[issue.category].append(issue)
        
        if 'visual' in issue_categories:
            recommendations.append("Improve visual consistency with unified color palette and typography system")
        
        if 'accessibility' in issue_categories:
            recommendations.append("Enhance accessibility with proper labels, alt text, and WCAG compliance")
        
        if 'ux' in issue_categories:
            recommendations.append("Optimize user experience with better navigation and interaction patterns")
        
        if 'responsive' in issue_categories:
            recommendations.append("Implement comprehensive responsive design for all device sizes")
        
        if 'performance' in issue_categories:
            recommendations.append("Optimize performance with image compression and CSS optimization")
        
        return recommendations

    async def auto_fix_and_retry(self, html_content: str, css_content: str = '', js_content: str = '', max_iterations: int = 3) -> Tuple[QualityReport, Dict[str, str]]:
        """Automatically fix issues and retry analysis until quality standards are met"""
        print("🔄 Starting auto-fix and quality validation loop...")
        
        current_html = html_content
        current_css = css_content
        current_js = js_content
        iteration = 0
        all_applied_fixes = []
        
        while iteration < max_iterations:
            iteration += 1
            print(f"\n📊 Quality Analysis - Iteration {iteration}")
            
            # Analyze current quality
            report = await self.analyze_quality(current_html, current_css, current_js)
            
            print(f"   Quality Score: {report.overall_score:.1f}/100")
            print(f"   Issues Found: {len(report.issues)} ({len([i for i in report.issues if i.severity == 'critical'])} critical, {len([i for i in report.issues if i.severity == 'major'])} major)")
            
            if report.passed:
                print("✅ Quality standards met!")
                break
            
            print("❌ Quality standards not met. Applying automatic fixes...")
            
            # Generate and apply fixes
            fixes = await self.auto_fix_generator.generate_fixes(report.issues, current_html, current_css)
            
            if fixes['applied_fixes']:
                current_html = fixes['html']
                current_css = fixes['css']
                current_js = fixes.get('js', current_js)
                all_applied_fixes.extend(fixes['applied_fixes'])
                
                print(f"   Applied fixes: {', '.join(fixes['applied_fixes'])}")
            else:
                print("   No automatic fixes available for remaining issues")
                break
        
        final_code = {
            'html': current_html,
            'css': current_css,
            'js': current_js,
            'applied_fixes': all_applied_fixes,
            'iterations': iteration
        }
        
        return report, final_code

    def generate_quality_report_html(self, report: QualityReport) -> str:
        """Generate HTML report for quality analysis"""
        status_color = "#4CAF50" if report.passed else "#F44336"
        status_text = "PASSED" if report.passed else "NEEDS IMPROVEMENT"
        
        issues_by_category = {}
        for issue in report.issues:
            if issue.category not in issues_by_category:
                issues_by_category[issue.category] = []
            issues_by_category[issue.category].append(issue)
        
        issues_html = ""
        for category, issues in issues_by_category.items():
            issues_html += f"""
            <div class="category-section">
                <h3>{category.title()} Issues ({len(issues)})</h3>
                <div class="issues-list">
            """
            
            for issue in issues:
                severity_color = {
                    'critical': '#F44336',
                    'major': '#FF9800',
                    'minor': '#FFC107',
                    'suggestion': '#2196F3'
                }.get(issue.severity, '#666')
                
                issues_html += f"""
                <div class="issue-item">
                    <div class="issue-header">
                        <span class="severity {issue.severity}" style="background-color: {severity_color}">{issue.severity.upper()}</span>
                        <span class="location">{issue.location}</span>
                    </div>
                    <div class="issue-description">{issue.issue}</div>
                    <div class="suggested-fix">💡 {issue.suggested_fix}</div>
                </div>
                """
            
            issues_html += "</div></div>"
        
        strengths_html = "".join([f"<li>{strength}</li>" for strength in report.strengths])
        recommendations_html = "".join([f"<li>{rec}</li>" for rec in report.recommendations])
        
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>UI/UX Quality Report</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    background-color: #f5f5f5;
                }}
                
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 2rem;
                }}
                
                .report-header {{
                    background: white;
                    padding: 2rem;
                    border-radius: 12px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    margin-bottom: 2rem;
                    text-align: center;
                }}
                
                .score-display {{
                    font-size: 3rem;
                    font-weight: bold;
                    color: {status_color};
                    margin: 1rem 0;
                }}
                
                .status-badge {{
                    display: inline-block;
                    padding: 0.5rem 1rem;
                    background-color: {status_color};
                    color: white;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 1.1rem;
                }}
                
                .section {{
                    background: white;
                    padding: 2rem;
                    border-radius: 12px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    margin-bottom: 2rem;
                }}
                
                .section h2 {{
                    color: #2c3e50;
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 0.5rem;
                    margin-bottom: 1.5rem;
                }}
                
                .category-section {{
                    margin-bottom: 2rem;
                }}
                
                .category-section h3 {{
                    color: #34495e;
                    margin-bottom: 1rem;
                }}
                
                .issue-item {{
                    border-left: 4px solid #e0e0e0;
                    padding: 1rem;
                    margin-bottom: 1rem;
                    background-color: #fafafa;
                    border-radius: 0 8px 8px 0;
                }}
                
                .issue-header {{
                    display: flex;
                    align-items: center;
                    gap: 1rem;
                    margin-bottom: 0.5rem;
                }}
                
                .severity {{
                    padding: 0.2rem 0.6rem;
                    border-radius: 4px;
                    color: white;
                    font-size: 0.8rem;
                    font-weight: bold;
                }}
                
                .location {{
                    color: #666;
                    font-size: 0.9rem;
                }}
                
                .issue-description {{
                    margin-bottom: 0.5rem;
                    color: #2c3e50;
                }}
                
                .suggested-fix {{
                    color: #27ae60;
                    font-size: 0.9rem;
                    font-style: italic;
                }}
                
                .strengths-list, .recommendations-list {{
                    list-style: none;
                }}
                
                .strengths-list li, .recommendations-list li {{
                    padding: 0.5rem 0;
                    border-bottom: 1px solid #eee;
                }}
                
                .strengths-list li:before {{
                    content: "✅ ";
                    margin-right: 0.5rem;
                }}
                
                .recommendations-list li:before {{
                    content: "💡 ";
                    margin-right: 0.5rem;
                }}
                
                .timestamp {{
                    color: #666;
                    font-size: 0.9rem;
                    text-align: center;
                    margin-top: 2rem;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="report-header">
                    <h1>UI/UX Quality Analysis Report</h1>
                    <div class="score-display">{report.overall_score:.1f}/100</div>
                    <div class="status-badge">{status_text}</div>
                </div>
                
                {f'''
                <div class="section">
                    <h2>Issues Found ({len(report.issues)})</h2>
                    {issues_html}
                </div>
                ''' if report.issues else ''}
                
                {f'''
                <div class="section">
                    <h2>Strengths Identified</h2>
                    <ul class="strengths-list">
                        {strengths_html}
                    </ul>
                </div>
                ''' if report.strengths else ''}
                
                {f'''
                <div class="section">
                    <h2>Recommendations</h2>
                    <ul class="recommendations-list">
                        {recommendations_html}
                    </ul>
                </div>
                ''' if report.recommendations else ''}
                
                <div class="timestamp">
                    Generated on {report.timestamp}
                </div>
            </div>
        </body>
        </html>
        """

async def main():
    """Demo of UI/UX Quality Control Agent"""
    print("🎨 UI/UX Quality Control Agent")
    print("=" * 50)
    
    # Initialize the agent
    agent = UIUXQualityAgent()
    
    # Sample HTML and CSS for testing
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sample App</title>
    </head>
    <body>
        <div>
            <img src="logo.png">
            <form>
                <input type="text">
                <input type="email">
                <input type="password">
                <input type="text">
                <input type="text">
                <input type="text">
                <input type="text">
                <input type="text">
                <select></select>
            </form>
            <button></button>
            <div></div>
            <div></div>
            <div></div>
        </div>
    </body>
    </html>
    """
    
    sample_css = """
    body {
        font-family: Arial, Helvetica, "Times New Roman", serif, cursive;
        color: #333;
        background: white;
    }
    
    .container {
        width: 800px;
        margin: 10px;
        padding: 5px;
    }
    
    h1 {
        font-size: 8px;
        color: #444;
        margin: 3px;
        padding: 7px;
    }
    
    .button {
        background: red;
        color: yellow;
        padding: 2px;
        margin: 1px;
    }
    """
    
    print("🔍 Analyzing sample code with intentional issues...")
    
    # Perform quality analysis with auto-fix
    final_report, fixed_code = await agent.auto_fix_and_retry(sample_html, sample_css)
    
    print(f"\n📊 Final Quality Report:")
    print(f"   Overall Score: {final_report.overall_score:.1f}/100")
    print(f"   Status: {'PASSED' if final_report.passed else 'NEEDS IMPROVEMENT'}")
    print(f"   Issues: {len(final_report.issues)} total")
    print(f"   Fixes Applied: {len(fixed_code['applied_fixes'])} ({fixed_code['iterations']} iterations)")
    
    if fixed_code['applied_fixes']:
        print(f"\n🔧 Applied Fixes:")
        for fix in fixed_code['applied_fixes']:
            print(f"   • {fix}")
    
    # Generate and save quality report
    report_html = agent.generate_quality_report_html(final_report)
    
    # Save report
    os.makedirs('quality_reports', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f'quality_reports/ui_ux_report_{timestamp}.html'
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_html)
    
    print(f"\n📄 Quality report saved: {report_path}")
    
    # Save fixed code
    if fixed_code['applied_fixes']:
        with open(f'quality_reports/fixed_html_{timestamp}.html', 'w', encoding='utf-8') as f:
            f.write(fixed_code['html'])
        
        with open(f'quality_reports/fixed_css_{timestamp}.css', 'w', encoding='utf-8') as f:
            f.write(fixed_code['css'])
        
        print(f"🔧 Fixed code saved: fixed_html_{timestamp}.html, fixed_css_{timestamp}.css")
    
    print(f"\n✅ UI/UX Quality Control Agent demonstration complete!")
    
    # Show integration example
    print(f"\n🔄 Integration with app generation:")
    print("   1. Generate app code → 2. Quality analysis → 3. Auto-fix → 4. Validate → 5. Preview")
    print("   Quality gate ensures all previews meet high UI/UX standards")

if __name__ == "__main__":
    asyncio.run(main())