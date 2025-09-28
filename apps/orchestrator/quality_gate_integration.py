"""
Quality Gate Integration System
Integrates UI/UX Quality Agent with app generation pipeline
Ensures all generated apps meet high quality standards before preview
"""

import asyncio
import json
import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

from ui_ux_quality_agent import UIUXQualityAgent, QualityReport

@dataclass
class AppGenerationResult:
    """Result from app generation process"""
    app_type: str
    app_name: str
    files: Dict[str, str]  # filename -> content
    metadata: Dict[str, Any]
    success: bool
    error_message: Optional[str] = None

@dataclass
class QualityGateResult:
    """Result from quality gate validation"""
    passed: bool
    quality_report: QualityReport
    fixed_files: Dict[str, str]
    iterations: int
    processing_time: float

class QualityGateSystem:
    """Main quality gate system that validates all generated apps"""
    
    def __init__(self):
        self.quality_agent = UIUXQualityAgent()
        self.quality_standards = {
            'minimum_score': 85.0,  # Higher standard for production apps
            'max_critical_issues': 0,
            'max_major_issues': 1,
            'auto_fix_attempts': 5
        }
        self.processing_history = []

    async def validate_app(self, app_result: AppGenerationResult) -> QualityGateResult:
        """Validate generated app through quality gate"""
        start_time = datetime.now()
        print(f"\n🚪 Quality Gate: Validating {app_result.app_name} ({app_result.app_type})")
        
        if not app_result.success:
            print(f"❌ App generation failed: {app_result.error_message}")
            return QualityGateResult(
                passed=False,
                quality_report=None,
                fixed_files={},
                iterations=0,
                processing_time=0
            )
        
        # Extract HTML and CSS content
        html_content = self._extract_html_content(app_result.files)
        css_content = self._extract_css_content(app_result.files)
        
        if not html_content:
            print("❌ No HTML content found to validate")
            return QualityGateResult(
                passed=False,
                quality_report=None,
                fixed_files={},
                iterations=0,
                processing_time=0
            )
        
        # Run quality analysis with auto-fix
        print("🔍 Running comprehensive quality analysis...")
        final_report, fixed_code = await self.quality_agent.auto_fix_and_retry(
            html_content, 
            css_content, 
            max_iterations=self.quality_standards['auto_fix_attempts']
        )
        
        # Check if meets our higher standards
        passed = self._meets_production_standards(final_report)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Log result
        result = QualityGateResult(
            passed=passed,
            quality_report=final_report,
            fixed_files=fixed_code,
            iterations=fixed_code.get('iterations', 0),
            processing_time=processing_time
        )
        
        self.processing_history.append({
            'app_name': app_result.app_name,
            'app_type': app_result.app_type,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        
        # Print result summary
        status = "✅ PASSED" if passed else "❌ REJECTED"
        print(f"\n🏁 Quality Gate Result: {status}")
        print(f"   Score: {final_report.overall_score:.1f}/100")
        print(f"   Issues: {len(final_report.issues)} total")
        print(f"   Processing Time: {processing_time:.2f}s")
        
        if not passed:
            print(f"   Reasons for rejection:")
            critical_issues = [i for i in final_report.issues if i.severity == 'critical']
            major_issues = [i for i in final_report.issues if i.severity == 'major']
            
            if critical_issues:
                print(f"   • {len(critical_issues)} critical issues")
            if major_issues:
                print(f"   • {len(major_issues)} major issues")
            if final_report.overall_score < self.quality_standards['minimum_score']:
                print(f"   • Score below minimum ({self.quality_standards['minimum_score']})")
        
        return result

    def _extract_html_content(self, files: Dict[str, str]) -> str:
        """Extract HTML content from app files"""
        # Look for main HTML files
        html_files = [f for f in files.keys() if f.endswith('.html')]
        
        # Prioritize index.html or main.html
        priority_files = ['index.html', 'main.html', 'app.html']
        for priority in priority_files:
            if priority in files:
                return files[priority]
        
        # Return first HTML file found
        if html_files:
            return files[html_files[0]]
        
        return ""

    def _extract_css_content(self, files: Dict[str, str]) -> str:
        """Extract CSS content from app files"""
        css_content = ""
        
        # Combine all CSS files
        css_files = [f for f in files.keys() if f.endswith('.css')]
        for css_file in css_files:
            css_content += files[css_file] + "\n\n"
        
        # Extract inline CSS from HTML
        html_files = [f for f in files.keys() if f.endswith('.html')]
        for html_file in html_files:
            html_content = files[html_file]
            # Simple regex to extract style tags (could be improved)
            import re
            style_matches = re.findall(r'<style[^>]*>(.*?)</style>', html_content, re.DOTALL)
            for style in style_matches:
                css_content += style + "\n\n"
        
        return css_content

    def _meets_production_standards(self, report: QualityReport) -> bool:
        """Check if report meets production quality standards"""
        critical_count = sum(1 for issue in report.issues if issue.severity == 'critical')
        major_count = sum(1 for issue in report.issues if issue.severity == 'major')
        
        return (
            report.overall_score >= self.quality_standards['minimum_score'] and
            critical_count <= self.quality_standards['max_critical_issues'] and
            major_count <= self.quality_standards['max_major_issues']
        )

    async def process_with_quality_gate(self, app_result: AppGenerationResult, save_artifacts: bool = True) -> Tuple[bool, Dict[str, Any]]:
        """Process app through complete quality gate pipeline"""
        # Validate through quality gate
        gate_result = await self.validate_app(app_result)
        
        if save_artifacts:
            await self._save_processing_artifacts(app_result, gate_result)
        
        # Prepare response
        response = {
            'passed_quality_gate': gate_result.passed,
            'quality_score': gate_result.quality_report.overall_score if gate_result.quality_report else 0,
            'processing_time': gate_result.processing_time,
            'iterations': gate_result.iterations,
            'files': gate_result.fixed_files if gate_result.passed else app_result.files,
            'quality_report': gate_result.quality_report,
            'recommendations': gate_result.quality_report.recommendations if gate_result.quality_report else []
        }
        
        return gate_result.passed, response

    async def _save_processing_artifacts(self, app_result: AppGenerationResult, gate_result: QualityGateResult):
        """Save processing artifacts for debugging and review"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        artifact_dir = Path(f"quality_artifacts/{app_result.app_name}_{timestamp}")
        artifact_dir.mkdir(parents=True, exist_ok=True)
        
        # Save original files
        original_dir = artifact_dir / "original"
        original_dir.mkdir(exist_ok=True)
        for filename, content in app_result.files.items():
            (original_dir / filename).write_text(content, encoding='utf-8')
        
        # Save quality report
        if gate_result.quality_report:
            report_html = self.quality_agent.generate_quality_report_html(gate_result.quality_report)
            (artifact_dir / "quality_report.html").write_text(report_html, encoding='utf-8')
        
        # Save fixed files if available
        if gate_result.fixed_files:
            fixed_dir = artifact_dir / "fixed"
            fixed_dir.mkdir(exist_ok=True)
            
            if 'html' in gate_result.fixed_files:
                (fixed_dir / "index.html").write_text(gate_result.fixed_files['html'], encoding='utf-8')
            if 'css' in gate_result.fixed_files:
                (fixed_dir / "styles.css").write_text(gate_result.fixed_files['css'], encoding='utf-8')
            if 'js' in gate_result.fixed_files:
                (fixed_dir / "script.js").write_text(gate_result.fixed_files['js'], encoding='utf-8')
        
        # Save processing metadata
        metadata = {
            'app_name': app_result.app_name,
            'app_type': app_result.app_type,
            'passed_quality_gate': gate_result.passed,
            'quality_score': gate_result.quality_report.overall_score if gate_result.quality_report else 0,
            'processing_time': gate_result.processing_time,
            'iterations': gate_result.iterations,
            'timestamp': datetime.now().isoformat(),
            'applied_fixes': gate_result.fixed_files.get('applied_fixes', [])
        }
        
        (artifact_dir / "metadata.json").write_text(
            json.dumps(metadata, indent=2),
            encoding='utf-8'
        )

class IntegratedAppGenerator:
    """App generator with integrated quality gate"""
    
    def __init__(self):
        self.quality_gate = QualityGateSystem()
        self.generation_stats = {
            'total_apps': 0,
            'passed_quality_gate': 0,
            'failed_quality_gate': 0,
            'average_score': 0.0
        }

    async def generate_app_with_quality_control(self, app_type: str, requirements: str, app_name: str = None) -> Dict[str, Any]:
        """Generate app with automatic quality control"""
        if not app_name:
            app_name = f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"🚀 Generating {app_type} app: {app_name}")
        print(f"📋 Requirements: {requirements}")
        
        # Generate app (simplified for demo)
        app_result = await self._generate_app_code(app_type, requirements, app_name)
        
        # Process through quality gate
        passed, response = await self.quality_gate.process_with_quality_gate(app_result)
        
        # Update stats
        self.generation_stats['total_apps'] += 1
        if passed:
            self.generation_stats['passed_quality_gate'] += 1
        else:
            self.generation_stats['failed_quality_gate'] += 1
        
        if response['quality_score'] > 0:
            total_scores = (self.generation_stats['average_score'] * (self.generation_stats['total_apps'] - 1) + response['quality_score'])
            self.generation_stats['average_score'] = total_scores / self.generation_stats['total_apps']
        
        # Prepare final response
        final_response = {
            'success': passed,
            'app_name': app_name,
            'app_type': app_type,
            'files': response['files'],
            'quality_gate_passed': passed,
            'quality_score': response['quality_score'],
            'processing_time': response['processing_time'],
            'auto_fix_iterations': response['iterations'],
            'recommendations': response['recommendations'],
            'preview_ready': passed,
            'message': self._generate_result_message(passed, response)
        }
        
        return final_response

    async def _generate_app_code(self, app_type: str, requirements: str, app_name: str) -> AppGenerationResult:
        """Generate app code based on type and requirements"""
        
        # Simulate app generation with different quality levels
        templates = {
            'website': self._generate_website_template,
            'web_app': self._generate_webapp_template,
            'mobile_app': self._generate_mobile_template
        }
        
        generator = templates.get(app_type.lower(), self._generate_website_template)
        files = generator(requirements, app_name)
        
        return AppGenerationResult(
            app_type=app_type,
            app_name=app_name,
            files=files,
            metadata={'requirements': requirements, 'generated_at': datetime.now().isoformat()},
            success=True
        )

    def _generate_website_template(self, requirements: str, app_name: str) -> Dict[str, str]:
        """Generate a basic website template"""
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{app_name.replace('_', ' ').title()}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <nav>
            <h1>{app_name.replace('_', ' ').title()}</h1>
            <ul>
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        <section id="home">
            <h2>Welcome to {app_name.replace('_', ' ').title()}</h2>
            <p>This app was generated based on: {requirements}</p>
            <img src="hero-image.jpg" alt="Hero image for {app_name}">
        </section>
        
        <section id="about">
            <h2>About Us</h2>
            <p>Learn more about our application and mission.</p>
        </section>
        
        <section id="contact">
            <h2>Contact Us</h2>
            <form>
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required>
                
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required>
                
                <label for="message">Message:</label>
                <textarea id="message" name="message" required></textarea>
                
                <button type="submit">Send Message</button>
            </form>
        </section>
    </main>
    
    <footer>
        <p>&copy; 2024 {app_name.replace('_', ' ').title()}. All rights reserved.</p>
    </footer>
    
    <script src="script.js"></script>
</body>
</html>"""
        
        css_content = """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #fff;
}

header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem 0;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}

nav h1 {
    font-size: 1.8rem;
    font-weight: 600;
}

nav ul {
    display: flex;
    list-style: none;
    gap: 2rem;
}

nav a {
    color: white;
    text-decoration: none;
    font-weight: 500;
    transition: opacity 0.3s ease;
}

nav a:hover {
    opacity: 0.8;
}

main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

section {
    margin-bottom: 3rem;
}

h2 {
    font-size: 2rem;
    margin-bottom: 1rem;
    color: #2c3e50;
}

p {
    font-size: 1.1rem;
    line-height: 1.7;
    margin-bottom: 1rem;
}

img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    margin: 1rem 0;
}

form {
    background: #f8f9fa;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: #555;
}

input, textarea {
    width: 100%;
    padding: 0.8rem;
    margin-bottom: 1rem;
    border: 2px solid #e1e8ed;
    border-radius: 6px;
    font-size: 1rem;
    transition: border-color 0.3s ease;
}

input:focus, textarea:focus {
    outline: none;
    border-color: #667eea;
}

button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 0.8rem 2rem;
    border: none;
    border-radius: 6px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
}

footer {
    background: #2c3e50;
    color: white;
    text-align: center;
    padding: 2rem 0;
    margin-top: 3rem;
}

@media (max-width: 768px) {
    nav {
        flex-direction: column;
        gap: 1rem;
    }
    
    nav ul {
        gap: 1rem;
    }
    
    main {
        padding: 1rem;
    }
    
    h2 {
        font-size: 1.5rem;
    }
}"""
        
        js_content = """// Enhanced interactivity for the app
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('nav a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Form submission handling
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Show loading state
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Sending...';
            submitBtn.disabled = true;
            
            // Simulate form submission
            setTimeout(() => {
                alert('Thank you for your message! We will get back to you soon.');
                form.reset();
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }, 1500);
        });
    }
    
    // Add fade-in animation for sections
    const sections = document.querySelectorAll('section');
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    sections.forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(section);
    });
});"""
        
        return {
            'index.html': html_content,
            'styles.css': css_content,
            'script.js': js_content
        }

    def _generate_webapp_template(self, requirements: str, app_name: str) -> Dict[str, str]:
        """Generate a web app template with more interactive features"""
        # Similar to website but with more dynamic features
        return self._generate_website_template(requirements, app_name)

    def _generate_mobile_template(self, requirements: str, app_name: str) -> Dict[str, str]:
        """Generate a mobile-optimized template"""
        # Similar to website but with mobile-first approach
        return self._generate_website_template(requirements, app_name)

    def _generate_result_message(self, passed: bool, response: Dict[str, Any]) -> str:
        """Generate human-friendly result message"""
        if passed:
            return f"✅ App generated successfully! Quality score: {response['quality_score']:.1f}/100. Ready for preview."
        else:
            reasons = []
            if response['quality_score'] < 85:
                reasons.append(f"quality score too low ({response['quality_score']:.1f}/100)")
            
            critical_issues = len([r for r in response.get('recommendations', []) if 'critical' in r.lower()])
            if critical_issues > 0:
                reasons.append(f"{critical_issues} critical issues")
            
            reason_text = " and ".join(reasons) if reasons else "quality standards not met"
            return f"❌ App needs improvement: {reason_text}. Auto-fixes applied in {response['auto_fix_iterations']} iterations."

    def get_generation_statistics(self) -> Dict[str, Any]:
        """Get generation statistics"""
        pass_rate = (self.generation_stats['passed_quality_gate'] / max(1, self.generation_stats['total_apps'])) * 100
        
        return {
            'total_apps_generated': self.generation_stats['total_apps'],
            'quality_gate_pass_rate': f"{pass_rate:.1f}%",
            'average_quality_score': f"{self.generation_stats['average_score']:.1f}/100",
            'apps_passed': self.generation_stats['passed_quality_gate'],
            'apps_failed': self.generation_stats['failed_quality_gate']
        }

async def main():
    """Demo of integrated app generation with quality control"""
    print("🎯 Integrated App Generator with Quality Control")
    print("=" * 55)
    
    generator = IntegratedAppGenerator()
    
    # Test different app types
    test_cases = [
        {
            'app_type': 'website',
            'requirements': 'Create a modern business website for a coffee shop with online menu',
            'app_name': 'coffee_shop_website'
        },
        {
            'app_type': 'web_app',
            'requirements': 'Build a task management app with user authentication',
            'app_name': 'task_manager_app'
        }
    ]
    
    print("🧪 Testing app generation with quality control...\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📱 Test Case {i}: {test_case['app_type'].title()}")
        print(f"   Requirements: {test_case['requirements']}")
        
        result = await generator.generate_app_with_quality_control(
            test_case['app_type'],
            test_case['requirements'],
            test_case['app_name']
        )
        
        print(f"   Result: {result['message']}")
        print(f"   Quality Score: {result['quality_score']:.1f}/100")
        print(f"   Auto-fix Iterations: {result['auto_fix_iterations']}")
        print(f"   Preview Ready: {'Yes' if result['preview_ready'] else 'No'}")
        
        if result['recommendations']:
            print(f"   Top Recommendations:")
            for rec in result['recommendations'][:2]:
                print(f"     • {rec}")
        
        print()
    
    # Show overall statistics
    stats = generator.get_generation_statistics()
    print("📊 Generation Statistics:")
    for key, value in stats.items():
        print(f"   {key.replace('_', ' ').title()}: {value}")
    
    print("\n✅ Quality Gate Integration System demonstration complete!")
    print("\n🔄 Complete Workflow:")
    print("   1. User requests app → 2. Generate code → 3. Quality analysis")
    print("   4. Auto-fix issues → 5. Validate standards → 6. Preview (if passed)")
    print("   7. Return to step 4 if failed → 8. Save artifacts for review")

if __name__ == "__main__":
    asyncio.run(main())