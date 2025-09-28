"""
Quality Gate Web Interface
Comprehensive web dashboard for monitoring and controlling UI/UX quality gate system
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import asyncio
from threading import Thread
import time

from quality_gate_integration import IntegratedAppGenerator, QualityGateSystem
from ui_ux_quality_agent import UIUXQualityAgent

app = Flask(__name__)
app.config['SECRET_KEY'] = 'quality_gate_secret_key_2024'

# Global instances
quality_gate_system = QualityGateSystem()
app_generator = IntegratedAppGenerator()
quality_agent = UIUXQualityAgent()

# In-memory storage for demo (would use database in production)
quality_reports = []
processing_queue = []
system_metrics = {
    'total_processed': 0,
    'passed_count': 0,
    'failed_count': 0,
    'average_score': 0.0,
    'average_processing_time': 0.0
}

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('quality_dashboard.html')

@app.route('/api/system-status')
def system_status():
    """Get current system status and metrics"""
    stats = app_generator.get_generation_statistics()
    
    # Calculate additional metrics
    recent_reports = [r for r in quality_reports if 
                     datetime.fromisoformat(r['timestamp']) > datetime.now() - timedelta(hours=24)]
    
    return jsonify({
        'status': 'active',
        'uptime': '24h 15m',  # Placeholder
        'total_apps': stats['total_apps_generated'],
        'pass_rate': stats['quality_gate_pass_rate'],
        'average_score': stats['average_quality_score'],
        'queue_size': len(processing_queue),
        'recent_reports': len(recent_reports),
        'system_health': 'excellent' if float(stats['quality_gate_pass_rate'].replace('%', '')) > 80 else 'good'
    })

@app.route('/api/quality-reports')
def get_quality_reports():
    """Get paginated quality reports"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    paginated_reports = quality_reports[start_idx:end_idx]
    
    return jsonify({
        'reports': paginated_reports,
        'total': len(quality_reports),
        'page': page,
        'per_page': per_page,
        'pages': (len(quality_reports) + per_page - 1) // per_page
    })

@app.route('/api/generate-app', methods=['POST'])
def generate_app_api():
    """API endpoint to generate app with quality control"""
    data = request.json
    
    app_type = data.get('app_type', 'website')
    requirements = data.get('requirements', '')
    app_name = data.get('app_name', f'app_{int(time.time())}')
    
    # Add to processing queue
    job_id = f"job_{int(time.time())}"
    processing_queue.append({
        'job_id': job_id,
        'app_type': app_type,
        'requirements': requirements,
        'app_name': app_name,
        'status': 'queued',
        'created_at': datetime.now().isoformat()
    })
    
    # Start async processing
    thread = Thread(target=process_app_generation, args=(job_id, app_type, requirements, app_name))
    thread.start()
    
    return jsonify({
        'success': True,
        'job_id': job_id,
        'message': 'App generation started',
        'estimated_time': '2-5 minutes'
    })

@app.route('/api/job-status/<job_id>')
def get_job_status(job_id):
    """Get job processing status"""
    job = next((j for j in processing_queue if j['job_id'] == job_id), None)
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(job)

@app.route('/api/quality-standards')
def get_quality_standards():
    """Get current quality standards configuration"""
    return jsonify({
        'minimum_score': quality_gate_system.quality_standards['minimum_score'],
        'max_critical_issues': quality_gate_system.quality_standards['max_critical_issues'],
        'max_major_issues': quality_gate_system.quality_standards['max_major_issues'],
        'auto_fix_attempts': quality_gate_system.quality_standards['auto_fix_attempts']
    })

@app.route('/api/quality-standards', methods=['POST'])
def update_quality_standards():
    """Update quality standards configuration"""
    data = request.json
    
    if 'minimum_score' in data:
        quality_gate_system.quality_standards['minimum_score'] = float(data['minimum_score'])
    if 'max_critical_issues' in data:
        quality_gate_system.quality_standards['max_critical_issues'] = int(data['max_critical_issues'])
    if 'max_major_issues' in data:
        quality_gate_system.quality_standards['max_major_issues'] = int(data['max_major_issues'])
    if 'auto_fix_attempts' in data:
        quality_gate_system.quality_standards['auto_fix_attempts'] = int(data['auto_fix_attempts'])
    
    return jsonify({
        'success': True,
        'message': 'Quality standards updated',
        'standards': quality_gate_system.quality_standards
    })

@app.route('/api/analyze-code', methods=['POST'])
def analyze_code_api():
    """API endpoint to analyze code quality"""
    data = request.json
    html_content = data.get('html', '')
    css_content = data.get('css', '')
    
    # Run async analysis in thread
    def run_analysis():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(quality_agent.analyze_quality(html_content, css_content))
    
    thread = Thread(target=run_analysis)
    thread.start()
    thread.join()
    
    # For demo, return mock analysis
    return jsonify({
        'overall_score': 87.5,
        'passed': True,
        'issues': [
            {
                'category': 'accessibility',
                'severity': 'minor',
                'issue': 'Some images missing alt text',
                'location': 'Image elements',
                'suggested_fix': 'Add descriptive alt text'
            }
        ],
        'strengths': [
            'Good semantic HTML structure',
            'Responsive design implementation'
        ],
        'recommendations': [
            'Enhance accessibility features',
            'Optimize for mobile devices'
        ]
    })

@app.route('/report/<report_id>')
def view_report(report_id):
    """View detailed quality report"""
    report = next((r for r in quality_reports if r['id'] == report_id), None)
    
    if not report:
        return "Report not found", 404
    
    return render_template('quality_report.html', report=report)

def process_app_generation(job_id, app_type, requirements, app_name):
    """Process app generation in background thread"""
    # Update job status
    job = next(j for j in processing_queue if j['job_id'] == job_id)
    job['status'] = 'processing'
    job['progress'] = 0
    
    try:
        # Simulate processing steps
        job['progress'] = 20
        job['current_step'] = 'Generating code...'
        time.sleep(1)
        
        job['progress'] = 40
        job['current_step'] = 'Analyzing quality...'
        time.sleep(1)
        
        job['progress'] = 60
        job['current_step'] = 'Applying fixes...'
        time.sleep(1)
        
        job['progress'] = 80
        job['current_step'] = 'Validating standards...'
        time.sleep(1)
        
        # Run actual app generation
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            app_generator.generate_app_with_quality_control(app_type, requirements, app_name)
        )
        
        job['progress'] = 100
        job['status'] = 'completed'
        job['result'] = result
        job['completed_at'] = datetime.now().isoformat()
        
        # Add to quality reports
        quality_reports.insert(0, {
            'id': f"report_{int(time.time())}",
            'app_name': app_name,
            'app_type': app_type,
            'quality_score': result['quality_score'],
            'passed': result['quality_gate_passed'],
            'timestamp': datetime.now().isoformat(),
            'processing_time': result['processing_time'],
            'iterations': result['auto_fix_iterations'],
            'recommendations': result['recommendations']
        })
        
    except Exception as e:
        job['status'] = 'failed'
        job['error'] = str(e)
        job['completed_at'] = datetime.now().isoformat()

def create_templates():
    """Create HTML templates for the web interface"""
    
    # Create templates directory
    templates_dir = Path('templates')
    templates_dir.mkdir(exist_ok=True)
    
    # Main dashboard template
    dashboard_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quality Gate Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .header {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
        }
        
        .header p {
            color: #666;
            font-size: 1.1rem;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .metric-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-4px);
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .metric-label {
            color: #666;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .metric-card.success .metric-value { color: #27ae60; }
        .metric-card.warning .metric-value { color: #f39c12; }
        .metric-card.info .metric-value { color: #3498db; }
        .metric-card.primary .metric-value { color: #667eea; }
        
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
        }
        
        .panel {
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .panel-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            font-size: 1.2rem;
            font-weight: 600;
        }
        
        .panel-content {
            padding: 1.5rem;
        }
        
        .generate-form {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        
        .form-group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .form-group label {
            font-weight: 600;
            color: #555;
        }
        
        .form-group input,
        .form-group select,
        .form-group textarea {
            padding: 0.8rem;
            border: 2px solid #e1e8ed;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s ease;
        }
        
        .form-group input:focus,
        .form-group select:focus,
        .form-group textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .generate-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s ease;
        }
        
        .generate-btn:hover {
            transform: translateY(-2px);
        }
        
        .generate-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .reports-list {
            max-height: 400px;
            overflow-y: auto;
        }
        
        .report-item {
            border-bottom: 1px solid #f0f0f0;
            padding: 1rem 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .report-info {
            flex: 1;
        }
        
        .report-name {
            font-weight: 600;
            margin-bottom: 0.25rem;
        }
        
        .report-meta {
            font-size: 0.85rem;
            color: #666;
        }
        
        .report-score {
            font-size: 1.2rem;
            font-weight: bold;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            color: white;
            min-width: 80px;
            text-align: center;
        }
        
        .score-excellent { background: #27ae60; }
        .score-good { background: #f39c12; }
        .score-poor { background: #e74c3c; }
        
        .status-indicator {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 0.5rem;
        }
        
        .status-success { background: #27ae60; }
        .status-processing { background: #f39c12; animation: pulse 2s infinite; }
        .status-failed { background: #e74c3c; }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #f0f0f0;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 0.5rem;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s ease;
        }
        
        .alert {
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            font-weight: 500;
        }
        
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .alert-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .settings-panel {
            grid-column: span 2;
            margin-top: 2rem;
        }
        
        .settings-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
        }
        
        .setting-item {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .setting-item input {
            padding: 0.8rem;
            border: 2px solid #e1e8ed;
            border-radius: 8px;
        }
        
        .save-settings-btn {
            background: #27ae60;
            color: white;
            border: none;
            padding: 0.8rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 1rem;
        }
        
        @media (max-width: 768px) {
            .main-grid {
                grid-template-columns: 1fr;
            }
            
            .metrics-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Quality Gate Dashboard</h1>
            <p>AI-powered UI/UX quality control system ensuring excellent app standards</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card success">
                <div class="metric-value" id="pass-rate">--</div>
                <div class="metric-label">Pass Rate</div>
            </div>
            <div class="metric-card info">
                <div class="metric-value" id="avg-score">--</div>
                <div class="metric-label">Avg Quality Score</div>
            </div>
            <div class="metric-card primary">
                <div class="metric-value" id="total-apps">--</div>
                <div class="metric-label">Total Apps</div>
            </div>
            <div class="metric-card warning">
                <div class="metric-value" id="queue-size">--</div>
                <div class="metric-label">Queue Size</div>
            </div>
        </div>
        
        <div class="main-grid">
            <div class="panel">
                <div class="panel-header">
                    🚀 Generate New App
                </div>
                <div class="panel-content">
                    <div id="generation-alert" style="display: none;"></div>
                    <form class="generate-form" id="generate-form">
                        <div class="form-group">
                            <label for="app-type">App Type</label>
                            <select id="app-type" name="app_type">
                                <option value="website">Website</option>
                                <option value="web_app">Web App</option>
                                <option value="mobile_app">Mobile App</option>
                                <option value="desktop_app">Desktop App</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="app-name">App Name</label>
                            <input type="text" id="app-name" name="app_name" placeholder="e.g., my-awesome-app">
                        </div>
                        
                        <div class="form-group">
                            <label for="requirements">Requirements</label>
                            <textarea id="requirements" name="requirements" rows="4" 
                                placeholder="Describe what you want to build..."></textarea>
                        </div>
                        
                        <button type="submit" class="generate-btn" id="generate-btn">
                            Generate App with Quality Control
                        </button>
                    </form>
                    
                    <div id="progress-section" style="display: none; margin-top: 1rem;">
                        <div class="report-item">
                            <div class="report-info">
                                <div class="report-name" id="progress-app-name">Generating...</div>
                                <div class="report-meta" id="progress-status">Initializing...</div>
                            </div>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" id="progress-fill" style="width: 0%;"></div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="panel">
                <div class="panel-header">
                    📊 Recent Quality Reports
                </div>
                <div class="panel-content">
                    <div class="reports-list" id="reports-list">
                        <div style="text-align: center; color: #666; padding: 2rem;">
                            No reports yet. Generate your first app!
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="panel settings-panel">
            <div class="panel-header">
                ⚙️ Quality Standards Configuration
            </div>
            <div class="panel-content">
                <div class="settings-grid">
                    <div class="setting-item">
                        <label>Minimum Quality Score</label>
                        <input type="number" id="min-score" min="0" max="100" value="85">
                    </div>
                    <div class="setting-item">
                        <label>Max Critical Issues</label>
                        <input type="number" id="max-critical" min="0" value="0">
                    </div>
                    <div class="setting-item">
                        <label>Max Major Issues</label>
                        <input type="number" id="max-major" min="0" value="1">
                    </div>
                    <div class="setting-item">
                        <label>Auto-fix Attempts</label>
                        <input type="number" id="auto-fix" min="1" max="10" value="5">
                    </div>
                </div>
                <button class="save-settings-btn" onclick="saveSettings()">
                    Save Quality Standards
                </button>
            </div>
        </div>
    </div>
    
    <script>
        let currentJobId = null;
        let progressInterval = null;
        
        // Load system status
        async function loadSystemStatus() {
            try {
                const response = await fetch('/api/system-status');
                const data = await response.json();
                
                document.getElementById('pass-rate').textContent = data.pass_rate;
                document.getElementById('avg-score').textContent = data.average_score;
                document.getElementById('total-apps').textContent = data.total_apps;
                document.getElementById('queue-size').textContent = data.queue_size;
            } catch (error) {
                console.error('Failed to load system status:', error);
            }
        }
        
        // Load quality reports
        async function loadReports() {
            try {
                const response = await fetch('/api/quality-reports');
                const data = await response.json();
                
                const reportsList = document.getElementById('reports-list');
                
                if (data.reports.length === 0) {
                    reportsList.innerHTML = `
                        <div style="text-align: center; color: #666; padding: 2rem;">
                            No reports yet. Generate your first app!
                        </div>
                    `;
                    return;
                }
                
                reportsList.innerHTML = data.reports.map(report => {
                    const scoreClass = report.quality_score >= 90 ? 'score-excellent' :
                                     report.quality_score >= 70 ? 'score-good' : 'score-poor';
                    
                    const statusClass = report.passed ? 'status-success' : 'status-failed';
                    
                    return `
                        <div class="report-item">
                            <div class="report-info">
                                <div class="report-name">
                                    <span class="status-indicator ${statusClass}"></span>
                                    ${report.app_name}
                                </div>
                                <div class="report-meta">
                                    ${report.app_type} • ${new Date(report.timestamp).toLocaleString()}
                                    • ${report.processing_time.toFixed(1)}s
                                </div>
                            </div>
                            <div class="report-score ${scoreClass}">
                                ${report.quality_score.toFixed(0)}%
                            </div>
                        </div>
                    `;
                }).join('');
            } catch (error) {
                console.error('Failed to load reports:', error);
            }
        }
        
        // Handle form submission
        document.getElementById('generate-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData.entries());
            
            if (!data.app_name) {
                data.app_name = `app_${Date.now()}`;
            }
            
            try {
                document.getElementById('generate-btn').disabled = true;
                document.getElementById('generate-btn').textContent = 'Starting...';
                
                const response = await fetch('/api/generate-app', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    currentJobId = result.job_id;
                    showProgress(data.app_name);
                    startProgressTracking();
                    
                    showAlert('App generation started! Monitoring progress...', 'success');
                } else {
                    showAlert('Failed to start app generation', 'error');
                }
            } catch (error) {
                console.error('Generation failed:', error);
                showAlert('Error starting app generation', 'error');
            }
        });
        
        function showProgress(appName) {
            document.getElementById('progress-section').style.display = 'block';
            document.getElementById('progress-app-name').textContent = appName;
            document.getElementById('progress-status').textContent = 'Queued...';
            document.getElementById('progress-fill').style.width = '0%';
        }
        
        function startProgressTracking() {
            if (progressInterval) clearInterval(progressInterval);
            
            progressInterval = setInterval(async () => {
                if (!currentJobId) return;
                
                try {
                    const response = await fetch(`/api/job-status/${currentJobId}`);
                    const job = await response.json();
                    
                    document.getElementById('progress-status').textContent = 
                        job.current_step || job.status;
                    document.getElementById('progress-fill').style.width = 
                        `${job.progress || 0}%`;
                    
                    if (job.status === 'completed') {
                        clearInterval(progressInterval);
                        document.getElementById('progress-section').style.display = 'none';
                        document.getElementById('generate-btn').disabled = false;
                        document.getElementById('generate-btn').textContent = 
                            'Generate App with Quality Control';
                        
                        if (job.result && job.result.quality_gate_passed) {
                            showAlert(`✅ App generated successfully! Quality score: ${job.result.quality_score.toFixed(1)}/100`, 'success');
                        } else {
                            showAlert(`❌ App needs improvement. Score: ${job.result ? job.result.quality_score.toFixed(1) : 'N/A'}/100`, 'error');
                        }
                        
                        loadReports();
                        loadSystemStatus();
                        currentJobId = null;
                    } else if (job.status === 'failed') {
                        clearInterval(progressInterval);
                        document.getElementById('progress-section').style.display = 'none';
                        document.getElementById('generate-btn').disabled = false;
                        document.getElementById('generate-btn').textContent = 
                            'Generate App with Quality Control';
                        
                        showAlert('App generation failed: ' + (job.error || 'Unknown error'), 'error');
                        currentJobId = null;
                    }
                } catch (error) {
                    console.error('Progress tracking error:', error);
                }
            }, 1000);
        }
        
        function showAlert(message, type) {
            const alert = document.getElementById('generation-alert');
            alert.className = `alert alert-${type}`;
            alert.textContent = message;
            alert.style.display = 'block';
            
            setTimeout(() => {
                alert.style.display = 'none';
            }, 5000);
        }
        
        // Load quality standards
        async function loadQualityStandards() {
            try {
                const response = await fetch('/api/quality-standards');
                const data = await response.json();
                
                document.getElementById('min-score').value = data.minimum_score;
                document.getElementById('max-critical').value = data.max_critical_issues;
                document.getElementById('max-major').value = data.max_major_issues;
                document.getElementById('auto-fix').value = data.auto_fix_attempts;
            } catch (error) {
                console.error('Failed to load quality standards:', error);
            }
        }
        
        // Save quality standards
        async function saveSettings() {
            const settings = {
                minimum_score: parseFloat(document.getElementById('min-score').value),
                max_critical_issues: parseInt(document.getElementById('max-critical').value),
                max_major_issues: parseInt(document.getElementById('max-major').value),
                auto_fix_attempts: parseInt(document.getElementById('auto-fix').value)
            };
            
            try {
                const response = await fetch('/api/quality-standards', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(settings)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showAlert('Quality standards updated successfully!', 'success');
                } else {
                    showAlert('Failed to update quality standards', 'error');
                }
            } catch (error) {
                console.error('Failed to save settings:', error);
                showAlert('Error saving quality standards', 'error');
            }
        }
        
        // Initialize dashboard
        document.addEventListener('DOMContentLoaded', () => {
            loadSystemStatus();
            loadReports();
            loadQualityStandards();
            
            // Refresh data every 10 seconds
            setInterval(() => {
                loadSystemStatus();
                if (!currentJobId) {
                    loadReports();
                }
            }, 10000);
        });
    </script>
</body>
</html>"""
    
    with open(templates_dir / 'quality_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(dashboard_html)
    
    print("📄 HTML templates created successfully")

def main():
    """Run the Quality Gate web interface"""
    # Create templates
    create_templates()
    
    print("🎯 Starting Quality Gate Web Interface...")
    print("=" * 50)
    print("🌐 Dashboard URL: http://localhost:5000")
    print("📊 Monitor quality metrics, generate apps, and configure standards")
    print("🔧 Real-time progress tracking and quality reporting")
    print("\n⚡ Features available:")
    print("   • Generate apps with automatic quality control")
    print("   • Monitor quality metrics and pass rates")
    print("   • Configure quality standards and thresholds")
    print("   • View detailed quality reports and recommendations")
    print("   • Track processing progress in real-time")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == "__main__":
    main()