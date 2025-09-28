"""
Automated Regression Testing System
ทดสอบอัตโนมัติเพื่อให้แน่ใจว่าการแก้ไขใหม่ไม่ทำลายฟีเจอร์เก่า
"""

import asyncio
import json
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import aiohttp
from pathlib import Path
import re
from bs4 import BeautifulSoup
import difflib

class TestStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"

class TestType(Enum):
    FUNCTIONAL = "functional"
    UI = "ui"
    PERFORMANCE = "performance"
    ACCESSIBILITY = "accessibility"
    CONTENT = "content"
    REGRESSION = "regression"

@dataclass
class TestResult:
    test_id: str
    requirement_id: str
    status: TestStatus
    message: str
    execution_time: float
    screenshot_path: Optional[str] = None
    error_details: Optional[str] = None
    artifacts: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

@dataclass
class TestCase:
    id: str
    requirement_id: str
    title: str
    description: str
    type: TestType
    priority: int
    test_steps: List[str]
    expected_result: str
    files_to_check: List[str]
    test_data: Dict[str, Any] = field(default_factory=dict)
    preconditions: List[str] = field(default_factory=list)
    timeout: int = 30  # seconds

class RegressionTester:
    """ระบบทดสอบ regression อัตโนมัติ"""
    
    def __init__(self, base_url: str = "http://localhost:8080", webroot: Path = None):
        self.base_url = base_url
        self.webroot = webroot or Path("/usr/share/nginx/html/app")
        self.test_results: Dict[str, TestResult] = {}
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def run_all_tests(self, test_cases: List[TestCase], project_slug: str) -> Dict[str, TestResult]:
        """รันการทดสอบทั้งหมด"""
        
        results = {}
        project_url = f"{self.base_url}/app/{project_slug}"
        
        print(f"Starting regression tests for project: {project_slug}")
        print(f"Project URL: {project_url}")
        
        # ตรวจสอบว่าโปรเจคมีอยู่จริง
        if not await self._check_project_exists(project_url):
            error_result = TestResult(
                test_id="project_check",
                requirement_id="system",
                status=TestStatus.ERROR,
                message=f"Project not accessible at {project_url}",
                execution_time=0
            )
            return {"project_check": error_result}
        
        # จัดเรียงการทดสอบตาม priority
        sorted_tests = sorted(test_cases, key=lambda t: t.priority, reverse=True)
        
        # รันการทดสอบแต่ละอัน
        for test_case in sorted_tests:
            print(f"Running test: {test_case.title}")
            
            start_time = time.time()
            result = await self._run_single_test(test_case, project_url)
            result.execution_time = time.time() - start_time
            
            results[test_case.id] = result
            self.test_results[test_case.id] = result
            
            print(f"Test {test_case.id}: {result.status.value} - {result.message}")
            
            # หยุดทดสอบถ้าเจอ critical error
            if (result.status == TestStatus.ERROR and 
                test_case.priority >= 3):
                print("Critical test failed, stopping execution")
                break
        
        return results
    
    async def _check_project_exists(self, project_url: str) -> bool:
        """ตรวจสอบว่าโปรเจคเข้าถึงได้"""
        try:
            async with self.session.get(f"{project_url}/index.html") as response:
                return response.status == 200
        except Exception:
            return False
    
    async def _run_single_test(self, test_case: TestCase, project_url: str) -> TestResult:
        """รันการทดสอบเดียว"""
        
        try:
            if test_case.type == TestType.FUNCTIONAL:
                return await self._test_functional(test_case, project_url)
            elif test_case.type == TestType.UI:
                return await self._test_ui(test_case, project_url)
            elif test_case.type == TestType.CONTENT:
                return await self._test_content(test_case, project_url)
            elif test_case.type == TestType.PERFORMANCE:
                return await self._test_performance(test_case, project_url)
            elif test_case.type == TestType.ACCESSIBILITY:
                return await self._test_accessibility(test_case, project_url)
            else:
                return await self._test_regression(test_case, project_url)
                
        except Exception as e:
            return TestResult(
                test_id=test_case.id,
                requirement_id=test_case.requirement_id,
                status=TestStatus.ERROR,
                message=f"Test execution error: {str(e)}",
                error_details=str(e),
                execution_time=0
            )
    
    async def _test_functional(self, test_case: TestCase, project_url: str) -> TestResult:
        """ทดสอบการทำงานของฟีเจอร์"""
        
        try:
            # โหลดหน้าเว็บ
            async with self.session.get(f"{project_url}/index.html") as response:
                if response.status != 200:
                    return TestResult(
                        test_id=test_case.id,
                        requirement_id=test_case.requirement_id,
                        status=TestStatus.FAILED,
                        message=f"Failed to load page: HTTP {response.status}",
                        execution_time=0
                    )
                
                html_content = await response.text()
                soup = BeautifulSoup(html_content, 'html.parser')
            
            # ทดสอบตาม expected_result
            if "ปุ่ม" in test_case.expected_result or "button" in test_case.expected_result:
                return await self._test_button_functionality(test_case, soup, html_content)
            elif "เมนู" in test_case.expected_result or "menu" in test_case.expected_result:
                return await self._test_menu_functionality(test_case, soup, html_content)
            elif "แสดงผล" in test_case.expected_result or "display" in test_case.expected_result:
                return await self._test_display_functionality(test_case, soup, html_content)
            else:
                return await self._test_general_functionality(test_case, soup, html_content)
                
        except Exception as e:
            return TestResult(
                test_id=test_case.id,
                requirement_id=test_case.requirement_id,
                status=TestStatus.ERROR,
                message=f"Functional test error: {str(e)}",
                error_details=str(e),
                execution_time=0
            )
    
    async def _test_button_functionality(self, test_case: TestCase, soup: BeautifulSoup, html: str) -> TestResult:
        """ทดสอบการทำงานของปุ่ม"""
        
        # ค้นหาปุ่มในหน้าเว็บ
        buttons = soup.find_all(['button', 'input'], type=['button', 'submit'])
        clickable_elements = soup.find_all(attrs={'onclick': True})
        
        all_buttons = buttons + clickable_elements
        
        if not all_buttons:
            return TestResult(
                test_id=test_case.id,
                requirement_id=test_case.requirement_id,
                status=TestStatus.FAILED,
                message="No buttons found on the page",
                execution_time=0
            )
        
        # ตรวจสอบ attributes ของปุ่ม
        button_issues = []
        for button in all_buttons:
            # ตรวจสอบว่ามี text หรือ aria-label
            button_text = button.get_text(strip=True)
            aria_label = button.get('aria-label', '')
            
            if not button_text and not aria_label:
                button_issues.append(f"Button without text or aria-label: {button}")
            
            # ตรวจสอบ accessibility
            if not button.get('aria-label') and not button_text:
                button_issues.append(f"Button lacks accessibility attributes: {button}")
        
        status = TestStatus.PASSED if not button_issues else TestStatus.FAILED
        message = "All buttons are properly implemented" if not button_issues else f"Button issues found: {'; '.join(button_issues[:3])}"
        
        return TestResult(
            test_id=test_case.id,
            requirement_id=test_case.requirement_id,
            status=status,
            message=message,
            artifacts={"buttons_found": len(all_buttons), "issues": button_issues},
            execution_time=0
        )
    
    async def _test_ui(self, test_case: TestCase, project_url: str) -> TestResult:
        """ทดสอบ UI elements"""
        
        try:
            async with self.session.get(f"{project_url}/index.html") as response:
                html_content = await response.text()
                soup = BeautifulSoup(html_content, 'html.parser')
            
            # ทดสอบสีสัน
            if "สี" in test_case.expected_result or "color" in test_case.expected_result:
                return await self._test_color_scheme(test_case, soup, html_content)
            
            # ทดสอบ responsive design
            elif "responsive" in test_case.expected_result:
                return await self._test_responsive_design(test_case, soup, html_content)
            
            # ทดสอบ layout
            elif "layout" in test_case.expected_result or "จัดวาง" in test_case.expected_result:
                return await self._test_layout(test_case, soup, html_content)
            
            else:
                return await self._test_general_ui(test_case, soup, html_content)
                
        except Exception as e:
            return TestResult(
                test_id=test_case.id,
                requirement_id=test_case.requirement_id,
                status=TestStatus.ERROR,
                message=f"UI test error: {str(e)}",
                error_details=str(e),
                execution_time=0
            )
    
    async def _test_color_scheme(self, test_case: TestCase, soup: BeautifulSoup, html: str) -> TestResult:
        """ทดสอบ color scheme"""
        
        # ค้นหา CSS styles
        style_tags = soup.find_all('style')
        inline_styles = soup.find_all(attrs={'style': True})
        
        colors_found = []
        
        # Extract colors from style tags
        for style_tag in style_tags:
            css_content = style_tag.get_text()
            color_matches = re.findall(r'color\s*:\s*([^;]+)', css_content, re.IGNORECASE)
            background_matches = re.findall(r'background(?:-color)?\s*:\s*([^;]+)', css_content, re.IGNORECASE)
            colors_found.extend(color_matches + background_matches)
        
        # Extract colors from inline styles
        for element in inline_styles:
            style_content = element.get('style', '')
            color_matches = re.findall(r'color\s*:\s*([^;]+)', style_content, re.IGNORECASE)
            background_matches = re.findall(r'background(?:-color)?\s*:\s*([^;]+)', style_content, re.IGNORECASE)
            colors_found.extend(color_matches + background_matches)
        
        # Clean and analyze colors
        cleaned_colors = [color.strip() for color in colors_found if color.strip()]
        unique_colors = list(set(cleaned_colors))
        
        status = TestStatus.PASSED if len(unique_colors) > 0 else TestStatus.FAILED
        message = f"Found {len(unique_colors)} unique colors in design" if unique_colors else "No colors found in CSS"
        
        return TestResult(
            test_id=test_case.id,
            requirement_id=test_case.requirement_id,
            status=status,
            message=message,
            artifacts={"colors_found": unique_colors[:10]},  # Limit to first 10
            execution_time=0
        )
    
    async def _test_content(self, test_case: TestCase, project_url: str) -> TestResult:
        """ทดสอบเนื้อหา"""
        
        try:
            async with self.session.get(f"{project_url}/index.html") as response:
                html_content = await response.text()
                soup = BeautifulSoup(html_content, 'html.parser')
            
            # ลบ script และ style tags
            for script in soup(["script", "style"]):
                script.decompose()
            
            # ดึงเนื้อหาที่มองเห็นได้
            visible_text = soup.get_text()
            text_length = len(visible_text.strip())
            
            # ตรวจสอบเนื้อหาพื้นฐาน
            has_title = bool(soup.find('title') or soup.find('h1'))
            has_content = text_length > 50  # มีเนื้อหาอย่างน้อย 50 ตัวอักษร
            
            # ตรวจสอบ meta tags
            has_meta_description = bool(soup.find('meta', attrs={'name': 'description'}))
            has_meta_viewport = bool(soup.find('meta', attrs={'name': 'viewport'}))
            
            issues = []
            if not has_title:
                issues.append("Missing title or main heading")
            if not has_content:
                issues.append("Insufficient content (less than 50 characters)")
            if not has_meta_description:
                issues.append("Missing meta description")
            if not has_meta_viewport:
                issues.append("Missing viewport meta tag")
            
            status = TestStatus.PASSED if not issues else TestStatus.FAILED
            message = "Content validation passed" if not issues else f"Content issues: {'; '.join(issues[:3])}"
            
            return TestResult(
                test_id=test_case.id,
                requirement_id=test_case.requirement_id,
                status=status,
                message=message,
                artifacts={
                    "text_length": text_length,
                    "has_title": has_title,
                    "has_meta_tags": has_meta_description and has_meta_viewport,
                    "issues": issues
                },
                execution_time=0
            )
            
        except Exception as e:
            return TestResult(
                test_id=test_case.id,
                requirement_id=test_case.requirement_id,
                status=TestStatus.ERROR,
                message=f"Content test error: {str(e)}",
                error_details=str(e),
                execution_time=0
            )
    
    async def _test_performance(self, test_case: TestCase, project_url: str) -> TestResult:
        """ทดสอบประสิทธิภาพ"""
        
        try:
            # วัดเวลาโหลดหน้าเว็บ
            start_time = time.time()
            
            async with self.session.get(f"{project_url}/index.html") as response:
                content = await response.text()
                load_time = time.time() - start_time
            
            # ตรวจสอบขนาดไฟล์
            content_size = len(content.encode('utf-8'))
            
            # เกณฑ์การประเมิน
            max_load_time = 2.0  # 2 seconds
            max_content_size = 1024 * 1024  # 1MB
            
            issues = []
            if load_time > max_load_time:
                issues.append(f"Slow load time: {load_time:.2f}s (max: {max_load_time}s)")
            if content_size > max_content_size:
                issues.append(f"Large content size: {content_size/1024:.1f}KB (max: {max_content_size/1024:.1f}KB)")
            
            status = TestStatus.PASSED if not issues else TestStatus.FAILED
            message = f"Performance test passed (load: {load_time:.2f}s, size: {content_size/1024:.1f}KB)" if not issues else f"Performance issues: {'; '.join(issues)}"
            
            return TestResult(
                test_id=test_case.id,
                requirement_id=test_case.requirement_id,
                status=status,
                message=message,
                artifacts={
                    "load_time": load_time,
                    "content_size_kb": content_size / 1024,
                    "issues": issues
                },
                execution_time=0
            )
            
        except Exception as e:
            return TestResult(
                test_id=test_case.id,
                requirement_id=test_case.requirement_id,
                status=TestStatus.ERROR,
                message=f"Performance test error: {str(e)}",
                error_details=str(e),
                execution_time=0
            )
    
    async def _test_accessibility(self, test_case: TestCase, project_url: str) -> TestResult:
        """ทดสอบ accessibility"""
        
        try:
            async with self.session.get(f"{project_url}/index.html") as response:
                html_content = await response.text()
                soup = BeautifulSoup(html_content, 'html.parser')
            
            accessibility_issues = []
            
            # ตรวจสอบ alt text สำหรับรูปภาพ
            images = soup.find_all('img')
            for img in images:
                if not img.get('alt'):
                    accessibility_issues.append(f"Image without alt text: {img.get('src', 'unknown')}")
            
            # ตรวจสอบ form labels
            inputs = soup.find_all('input', type=['text', 'email', 'password', 'tel'])
            for input_elem in inputs:
                input_id = input_elem.get('id')
                if input_id:
                    label = soup.find('label', attrs={'for': input_id})
                    if not label:
                        accessibility_issues.append(f"Input without label: {input_id}")
            
            # ตรวจสอบ heading structure
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            if not headings:
                accessibility_issues.append("No heading structure found")
            
            # ตรวจสอบ color contrast (basic check)
            # ในการใช้งานจริงควรใช้เครื่องมือที่เฉพาะเจาะจงกว่า
            
            status = TestStatus.PASSED if not accessibility_issues else TestStatus.FAILED
            message = "Accessibility test passed" if not accessibility_issues else f"Accessibility issues: {'; '.join(accessibility_issues[:3])}"
            
            return TestResult(
                test_id=test_case.id,
                requirement_id=test_case.requirement_id,
                status=status,
                message=message,
                artifacts={
                    "images_count": len(images),
                    "inputs_count": len(inputs),
                    "headings_count": len(headings),
                    "issues": accessibility_issues
                },
                execution_time=0
            )
            
        except Exception as e:
            return TestResult(
                test_id=test_case.id,
                requirement_id=test_case.requirement_id,
                status=TestStatus.ERROR,
                message=f"Accessibility test error: {str(e)}",
                error_details=str(e),
                execution_time=0
            )
    
    async def _test_regression(self, test_case: TestCase, project_url: str) -> TestResult:
        """ทดสอบ regression ทั่วไป"""
        
        try:
            # รวมการทดสอบหลายๆ ด้าน
            functional_result = await self._test_functional(test_case, project_url)
            ui_result = await self._test_ui(test_case, project_url) 
            content_result = await self._test_content(test_case, project_url)
            
            # รวมผลลัพธ์
            all_passed = all(result.status == TestStatus.PASSED for result in [functional_result, ui_result, content_result])
            
            messages = []
            if functional_result.status != TestStatus.PASSED:
                messages.append(f"Functional: {functional_result.message}")
            if ui_result.status != TestStatus.PASSED:
                messages.append(f"UI: {ui_result.message}")
            if content_result.status != TestStatus.PASSED:
                messages.append(f"Content: {content_result.message}")
            
            status = TestStatus.PASSED if all_passed else TestStatus.FAILED
            message = "All regression tests passed" if all_passed else f"Regression failures: {'; '.join(messages[:2])}"
            
            return TestResult(
                test_id=test_case.id,
                requirement_id=test_case.requirement_id,
                status=status,
                message=message,
                artifacts={
                    "functional_status": functional_result.status.value,
                    "ui_status": ui_result.status.value,
                    "content_status": content_result.status.value
                },
                execution_time=0
            )
            
        except Exception as e:
            return TestResult(
                test_id=test_case.id,
                requirement_id=test_case.requirement_id,
                status=TestStatus.ERROR,
                message=f"Regression test error: {str(e)}",
                error_details=str(e),
                execution_time=0
            )
    
    # Helper methods for specific functionality tests
    async def _test_menu_functionality(self, test_case: TestCase, soup: BeautifulSoup, html: str) -> TestResult:
        """ทดสอบเมนู"""
        
        # ค้นหาเมนู
        nav_elements = soup.find_all(['nav', 'ul', 'ol'])
        menu_links = soup.find_all('a')
        
        if not nav_elements and not menu_links:
            return TestResult(
                test_id=test_case.id,
                requirement_id=test_case.requirement_id,
                status=TestStatus.FAILED,
                message="No navigation or menu elements found",
                execution_time=0
            )
        
        return TestResult(
            test_id=test_case.id,
            requirement_id=test_case.requirement_id,
            status=TestStatus.PASSED,
            message=f"Found {len(nav_elements)} nav elements and {len(menu_links)} links",
            artifacts={"nav_elements": len(nav_elements), "links": len(menu_links)},
            execution_time=0
        )
    
    async def _test_display_functionality(self, test_case: TestCase, soup: BeautifulSoup, html: str) -> TestResult:
        """ทดสอบการแสดงผล"""
        
        # ตรวจสอบ basic HTML structure
        has_doctype = "<!doctype" in html.lower()
        has_html_tag = bool(soup.find('html'))
        has_head_tag = bool(soup.find('head'))
        has_body_tag = bool(soup.find('body'))
        
        issues = []
        if not has_doctype:
            issues.append("Missing DOCTYPE declaration")
        if not has_html_tag:
            issues.append("Missing HTML tag")
        if not has_head_tag:
            issues.append("Missing HEAD tag")
        if not has_body_tag:
            issues.append("Missing BODY tag")
        
        status = TestStatus.PASSED if not issues else TestStatus.FAILED
        message = "Page structure is valid" if not issues else f"Structure issues: {'; '.join(issues)}"
        
        return TestResult(
            test_id=test_case.id,
            requirement_id=test_case.requirement_id,
            status=status,
            message=message,
            artifacts={"issues": issues},
            execution_time=0
        )
    
    async def _test_general_functionality(self, test_case: TestCase, soup: BeautifulSoup, html: str) -> TestResult:
        """ทดสอบการทำงานทั่วไป"""
        
        # ตรวจสอบว่ามีเนื้อหาที่เกี่ยวข้องกับ requirement หรือไม่
        page_text = soup.get_text().lower()
        expected_lower = test_case.expected_result.lower()
        
        # ค้นหาคำสำคัญใน expected result
        keywords = re.findall(r'\b\w+\b', expected_lower)
        found_keywords = [kw for kw in keywords if kw in page_text]
        
        relevance_score = len(found_keywords) / len(keywords) if keywords else 0
        
        status = TestStatus.PASSED if relevance_score > 0.3 else TestStatus.FAILED
        message = f"Content relevance: {relevance_score:.2f} ({len(found_keywords)}/{len(keywords)} keywords found)"
        
        return TestResult(
            test_id=test_case.id,
            requirement_id=test_case.requirement_id,
            status=status,
            message=message,
            artifacts={
                "relevance_score": relevance_score,
                "keywords_found": found_keywords,
                "total_keywords": len(keywords)
            },
            execution_time=0
        )
    
    async def _test_responsive_design(self, test_case: TestCase, soup: BeautifulSoup, html: str) -> TestResult:
        """ทดสอบ responsive design"""
        
        # ตรวจสอบ viewport meta tag
        viewport_tag = soup.find('meta', attrs={'name': 'viewport'})
        
        # ตรวจสอบ CSS media queries
        style_tags = soup.find_all('style')
        css_content = ' '.join([tag.get_text() for tag in style_tags])
        
        has_media_queries = bool(re.search(r'@media\s*\([^)]*\)', css_content, re.IGNORECASE))
        
        issues = []
        if not viewport_tag:
            issues.append("Missing viewport meta tag")
        if not has_media_queries:
            issues.append("No CSS media queries found")
        
        status = TestStatus.PASSED if not issues else TestStatus.FAILED
        message = "Responsive design elements found" if not issues else f"Responsive issues: {'; '.join(issues)}"
        
        return TestResult(
            test_id=test_case.id,
            requirement_id=test_case.requirement_id,
            status=status,
            message=message,
            artifacts={"issues": issues},
            execution_time=0
        )
    
    async def _test_layout(self, test_case: TestCase, soup: BeautifulSoup, html: str) -> TestResult:
        """ทดสอบ layout"""
        
        # ตรวจสอบ CSS layout properties
        style_tags = soup.find_all('style')
        css_content = ' '.join([tag.get_text() for tag in style_tags])
        
        layout_properties = ['display:', 'flex', 'grid', 'float:', 'position:']
        found_properties = [prop for prop in layout_properties if prop in css_content.lower()]
        
        # ตรวจสอบ container elements
        containers = soup.find_all(['div', 'main', 'section', 'article', 'header', 'footer'])
        
        has_layout_structure = len(containers) > 0
        has_css_layout = len(found_properties) > 0
        
        status = TestStatus.PASSED if (has_layout_structure or has_css_layout) else TestStatus.FAILED
        message = f"Layout structure found: {len(containers)} containers, {len(found_properties)} CSS properties"
        
        return TestResult(
            test_id=test_case.id,
            requirement_id=test_case.requirement_id,
            status=status,
            message=message,
            artifacts={
                "containers": len(containers),
                "css_properties": found_properties,
                "layout_found": has_layout_structure or has_css_layout
            },
            execution_time=0
        )
    
    async def _test_general_ui(self, test_case: TestCase, soup: BeautifulSoup, html: str) -> TestResult:
        """ทดสอบ UI ทั่วไป"""
        
        # นับ UI elements
        buttons = len(soup.find_all(['button', 'input'], type=['button', 'submit']))
        links = len(soup.find_all('a'))
        images = len(soup.find_all('img'))
        forms = len(soup.find_all('form'))
        
        total_interactive = buttons + links + forms
        
        # ตรวจสอบ CSS
        style_tags = soup.find_all(['style', 'link'], rel='stylesheet')
        has_styling = len(style_tags) > 0
        
        status = TestStatus.PASSED if (total_interactive > 0 or has_styling) else TestStatus.FAILED
        message = f"UI elements: {buttons} buttons, {links} links, {images} images, {forms} forms"
        
        return TestResult(
            test_id=test_case.id,
            requirement_id=test_case.requirement_id,
            status=status,
            message=message,
            artifacts={
                "buttons": buttons,
                "links": links,
                "images": images,
                "forms": forms,
                "has_styling": has_styling
            },
            execution_time=0
        )
    
    def generate_test_report(self, results: Dict[str, TestResult]) -> Dict[str, Any]:
        """สร้างรายงานผลการทดสอบ"""
        
        total_tests = len(results)
        passed_tests = len([r for r in results.values() if r.status == TestStatus.PASSED])
        failed_tests = len([r for r in results.values() if r.status == TestStatus.FAILED])
        error_tests = len([r for r in results.values() if r.status == TestStatus.ERROR])
        
        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Group by requirement
        by_requirement = {}
        for result in results.values():
            req_id = result.requirement_id
            if req_id not in by_requirement:
                by_requirement[req_id] = []
            by_requirement[req_id].append(result)
        
        # Calculate requirement coverage
        requirement_status = {}
        for req_id, req_results in by_requirement.items():
            req_passed = all(r.status == TestStatus.PASSED for r in req_results)
            requirement_status[req_id] = "PASSED" if req_passed else "FAILED"
        
        return {
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "errors": error_tests,
                "pass_rate": round(pass_rate, 2),
                "execution_time": sum(r.execution_time for r in results.values())
            },
            "requirement_coverage": requirement_status,
            "test_details": {test_id: result.message for test_id, result in results.items()},
            "failed_tests": [
                {"test_id": test_id, "message": result.message, "error": result.error_details}
                for test_id, result in results.items()
                if result.status in [TestStatus.FAILED, TestStatus.ERROR]
            ],
            "generated_at": time.time()
        }