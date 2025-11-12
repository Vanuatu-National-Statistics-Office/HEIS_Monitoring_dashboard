"""
Flask application for Vanuatu Household Income & Expenditure Survey Progress Monitoring
"""
from flask import Flask, render_template, jsonify, request, make_response, send_file
from flask_cors import CORS
from functools import wraps
from config import Config
from data_models import SurveyProgressGenerator, SurveyProgressAnalytics
from visualizations import ProgressCharts
from data_loader import DataLoader, DataExporter
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS if configured
if Config.CORS_ENABLED:
    CORS(app, origins=Config.CORS_ORIGINS)

# Initialize data loader
data_loader = DataLoader()

# Load survey data based on configured source
print("\n" + "="*60)
print("🚀 VANUATU HIES SURVEY DASHBOARD - DATA SOURCE")
print("="*60)
survey_data = data_loader.load_data()
print("="*60 + "\n")


# API Authentication decorator
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not Config.API_KEY_REQUIRED:
            return f(*args, **kwargs)
        
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        if api_key and api_key == Config.API_KEY:
            return f(*args, **kwargs)
        else:
            return jsonify({'error': 'Invalid or missing API key'}), 401
    return decorated_function


# API response wrapper
def api_response(data, message='Success', status_code=200):
    """Standardized API response format"""
    response = {
        'status': 'success' if status_code < 400 else 'error',
        'message': message,
        'data': data,
    }
    
    if Config.API_INCLUDE_METADATA:
        response['metadata'] = {
            'timestamp': datetime.now().isoformat(),
            'version': Config.API_VERSION,
            'total_records': len(data) if isinstance(data, (list, dict)) else 1
        }
    
    return jsonify(response), status_code


@app.route('/')
def index():
    """Main dashboard page with overview"""
    progress = SurveyProgressAnalytics.get_overall_progress(
        survey_data,
        target_surveys=Config.TARGET_SURVEYS
    )
    
    return render_template('index.html', 
                         progress=progress,
                         config=Config)


@app.route('/api')
@app.route('/api/docs')
def api_documentation():
    """API Documentation endpoint"""
    docs = {
        'api_info': {
            'title': Config.API_TITLE,
            'version': Config.API_VERSION,
            'description': Config.API_DESCRIPTION,
            'base_url': request.url_root + 'api/',
            'authentication': 'API Key (optional)' if not Config.API_KEY_REQUIRED else 'API Key (required)',
            'auth_method': 'X-API-Key header or api_key query parameter'
        },
        'endpoints': {
            'progress': {
                'url': '/api/progress',
                'method': 'GET',
                'description': 'Get overall survey progress summary',
                'parameters': {},
                'response_fields': ['total_surveys', 'completed', 'in_progress', 'pending_review', 'completion_rate', 'daily_average']
            },
            'provinces': {
                'url': '/api/provinces',
                'method': 'GET',
                'description': 'Get province-level statistics',
                'parameters': {},
                'response_fields': ['province', 'total', 'completed', 'in_progress', 'completion_rate']
            },
            'teams': {
                'url': '/api/teams',
                'method': 'GET',
                'description': 'Get team performance data',
                'parameters': {},
                'response_fields': ['team', 'supervisor', 'total', 'completed', 'avg_quality']
            },
            'interviewers': {
                'url': '/api/interviewers',
                'method': 'GET',
                'description': 'Get interviewer statistics',
                'parameters': {},
                'response_fields': ['interviewer_id', 'interviewer_name', 'team', 'total', 'completed']
            },
            'daily': {
                'url': '/api/daily',
                'method': 'GET',
                'description': 'Get daily progress tracking',
                'parameters': {},
                'response_fields': ['date', 'surveys_completed', 'cumulative_total']
            },
            'quality': {
                'url': '/api/quality',
                'method': 'GET',
                'description': 'Get data quality metrics',
                'parameters': {},
                'response_fields': ['avg_quality_score', 'error_rate', 'gps_capture_rate', 'avg_duration']
            },
            'logistics': {
                'url': '/api/logistics',
                'method': 'GET',
                'description': 'Get logistics and equipment status',
                'parameters': {},
                'response_fields': ['tablets_active', 'tablets_issues', 'transport_available']
            },
            'ea-stats': {
                'url': '/api/ea-stats',
                'method': 'GET',
                'description': 'Get Enumeration Area statistics',
                'parameters': {},
                'response_fields': ['ea_code', 'province', 'island', 'total_households', 'completed']
            },
            'supervisors': {
                'url': '/api/supervisors',
                'method': 'GET',
                'description': 'Get supervisor review summary',
                'parameters': {},
                'response_fields': ['supervisor', 'team', 'approved', 'rejected', 'pending']
            },
            'survey-solutions-sync': {
                'url': '/api/survey-solutions-sync',
                'method': 'GET',
                'description': 'Get Survey Solutions tablet sync status',
                'parameters': {},
                'response_fields': ['synced', 'pending', 'failed', 'sync_rate']
            },
            'device-sync-performance': {
                'url': '/api/device-sync-performance',
                'method': 'GET',
                'description': 'Get device sync performance metrics',
                'parameters': {},
                'response_fields': ['interviewer', 'device_id', 'sync_success_rate', 'last_sync']
            },
            'filter': {
                'url': '/api/filter',
                'method': 'GET',
                'description': 'Get filtered survey data',
                'parameters': {
                    'province': 'Filter by province name',
                    'island': 'Filter by island name',
                    'team': 'Filter by team name',
                    'interviewer': 'Filter by interviewer ID'
                },
                'response_fields': ['filtered progress data based on query parameters']
            }
        },
        'usage_examples': {
            'curl': 'curl -H "X-API-Key: your-api-key" ' + request.url_root + 'api/progress',
            'python': 'import requests\nheaders = {"X-API-Key": "your-api-key"}\nresponse = requests.get("' + request.url_root + 'api/progress", headers=headers)',
            'javascript': 'fetch("' + request.url_root + 'api/progress", {\n  headers: {"X-API-Key": "your-api-key"}\n}).then(r => r.json())'
        },
        'response_format': {
            'success': {
                'status': 'success',
                'message': 'Success',
                'data': '{ ... endpoint specific data ... }',
                'metadata': {
                    'timestamp': 'ISO 8601 datetime',
                    'version': Config.API_VERSION,
                    'total_records': 'number of records'
                }
            },
            'error': {
                'status': 'error',
                'message': 'Error description',
                'data': None
            }
        }
    }
    
    return jsonify(docs)


@app.route('/dashboard')
def dashboard():
    """Full dashboard with all visualizations"""
    # Get analytics
    progress = SurveyProgressAnalytics.get_overall_progress(
        survey_data,
        target_surveys=Config.TARGET_SURVEYS
    )
    province_stats = SurveyProgressAnalytics.get_progress_by_province(survey_data)
    island_stats = SurveyProgressAnalytics.get_progress_by_island(survey_data)
    team_stats = SurveyProgressAnalytics.get_progress_by_team(survey_data)
    interviewer_stats = SurveyProgressAnalytics.get_progress_by_interviewer(survey_data)
    daily_progress = SurveyProgressAnalytics.get_daily_progress(survey_data)
    status_distribution = SurveyProgressAnalytics.get_status_distribution(survey_data)
    top_performers = SurveyProgressAnalytics.get_top_performers(survey_data, top_n=15)
    
    # Generate charts
    progress_gauge = ProgressCharts.create_progress_gauge(
        progress['completed'],
        Config.TARGET_SURVEYS
    )
    daily_chart = ProgressCharts.create_daily_progress_chart(daily_progress)
    status_chart = ProgressCharts.create_status_distribution_chart(status_distribution)
    province_chart = ProgressCharts.create_province_progress_chart(province_stats)
    team_chart = ProgressCharts.create_team_performance_chart(team_stats)
    interviewer_chart = ProgressCharts.create_interviewer_leaderboard_chart(top_performers)
    island_heatmap = ProgressCharts.create_island_heatmap(island_stats)
    quality_chart = ProgressCharts.create_quality_trend_chart(survey_data)
    time_chart = ProgressCharts.create_time_efficiency_chart(team_stats)
    
    return render_template('dashboard.html',
                         progress=progress,
                         config=Config,
                         progress_gauge=progress_gauge,
                         daily_chart=daily_chart,
                         status_chart=status_chart,
                         province_chart=province_chart,
                         team_chart=team_chart,
                         interviewer_chart=interviewer_chart,
                         island_heatmap=island_heatmap,
                         quality_chart=quality_chart,
                         time_chart=time_chart)


@app.route('/api/progress')
@require_api_key
def api_progress():
    """API endpoint for overall progress"""
    progress = SurveyProgressAnalytics.get_overall_progress(
        survey_data,
        target_surveys=Config.TARGET_SURVEYS
    )
    return api_response(progress, 'Survey progress retrieved successfully')


@app.route('/api/provinces')
@require_api_key
def api_provinces():
    """API endpoint for province statistics"""
    province_stats = SurveyProgressAnalytics.get_progress_by_province(survey_data)
    return api_response(province_stats.to_dict(), 'Province statistics retrieved successfully')


@app.route('/api/teams')
@require_api_key
def api_teams():
    """API endpoint for team statistics"""
    team_stats = SurveyProgressAnalytics.get_progress_by_team(survey_data)
    return api_response(team_stats.to_dict(), 'Team statistics retrieved successfully')


@app.route('/api/interviewers')
@require_api_key
def api_interviewers():
    """API endpoint for interviewer statistics"""
    interviewer_stats = SurveyProgressAnalytics.get_progress_by_interviewer(survey_data)
    return jsonify(interviewer_stats.to_dict())


@app.route('/api/daily')
def api_daily():
    """API endpoint for daily progress"""
    daily_progress = SurveyProgressAnalytics.get_daily_progress(survey_data)
    return jsonify(daily_progress.to_dict())


@app.route('/api/filter')
def api_filter():
    """API endpoint for filtered data"""
    province = request.args.get('province')
    island = request.args.get('island')
    team = request.args.get('team')
    interviewer = request.args.get('interviewer')
    
    filtered_data = survey_data.copy()
    
    if province:
        filtered_data = filtered_data[filtered_data['province'] == province]
    
    if island:
        filtered_data = filtered_data[filtered_data['island'] == island]
    
    if team:
        filtered_data = filtered_data[filtered_data['team'] == team]
    
    if interviewer:
        filtered_data = filtered_data[filtered_data['interviewer_id'] == interviewer]
    
    progress = SurveyProgressAnalytics.get_overall_progress(
        filtered_data,
        target_surveys=Config.TARGET_SURVEYS
    )
    return jsonify(progress)


@app.route('/api/quality')
def api_quality():
    """API endpoint for data quality metrics"""
    quality_metrics = SurveyProgressAnalytics.get_data_quality_metrics(survey_data)
    return jsonify(quality_metrics)


@app.route('/api/logistics')
def api_logistics():
    """API endpoint for logistics status"""
    logistics = SurveyProgressAnalytics.get_logistics_status(survey_data)
    return jsonify(logistics)


@app.route('/api/ea-stats')
def api_ea_stats():
    """API endpoint for enumeration area statistics"""
    ea_stats = SurveyProgressAnalytics.get_ea_completion_stats(survey_data)
    return jsonify(ea_stats.to_dict(orient='records'))


@app.route('/api/supervisors')
def api_supervisors():
    """API endpoint for supervisor review summary"""
    supervisor_data = SurveyProgressAnalytics.get_supervisor_review_summary(survey_data)
    return jsonify(supervisor_data.to_dict())


@app.route('/api/interviewer-detailed')
def api_interviewer_detailed():
    """API endpoint for detailed interviewer performance"""
    interviewer_data = SurveyProgressAnalytics.get_interviewer_performance_detailed(survey_data)
    return jsonify(interviewer_data.to_dict())


@app.route('/api/province-ea-completion')
def api_province_ea_completion():
    """API endpoint for EA completion rate by province"""
    province_ea_data = SurveyProgressAnalytics.get_province_ea_completion_rate(survey_data)
    return jsonify(province_ea_data.to_dict())


@app.route('/api/survey-solutions-sync')
def api_survey_solutions_sync():
    """API endpoint for Survey Solutions sync status"""
    sync_summary = SurveyProgressAnalytics.get_survey_solutions_sync_status(survey_data)
    return jsonify(sync_summary)


@app.route('/api/survey-solutions-interview-status')
def api_survey_solutions_interview_status():
    """API endpoint for Survey Solutions interview status"""
    status_counts = SurveyProgressAnalytics.get_survey_solutions_interview_status(survey_data)
    return jsonify(status_counts)


@app.route('/api/device-sync-performance')
def api_device_sync_performance():
    """API endpoint for device sync performance"""
    device_sync = SurveyProgressAnalytics.get_device_sync_performance(survey_data)
    return jsonify(device_sync.to_dict())


@app.route('/survey-solutions')
def survey_solutions_dashboard():
    """Survey Solutions specific monitoring dashboard"""
    # Get analytics
    progress = SurveyProgressAnalytics.get_overall_progress(
        survey_data,
        target_surveys=Config.TARGET_SURVEYS
    )
    sync_summary = SurveyProgressAnalytics.get_survey_solutions_sync_status(survey_data)
    interview_status = SurveyProgressAnalytics.get_survey_solutions_interview_status(survey_data)
    device_sync_data = SurveyProgressAnalytics.get_device_sync_performance(survey_data)
    
    # Generate charts
    sync_chart = ProgressCharts.create_survey_solutions_sync_chart(sync_summary)
    interview_status_chart = ProgressCharts.create_ss_interview_status_chart(interview_status)
    device_sync_chart = ProgressCharts.create_device_sync_performance_chart(device_sync_data)
    validation_errors_chart = ProgressCharts.create_validation_errors_chart(device_sync_data)
    
    return render_template('survey_solutions.html',
                         progress=progress,
                         sync_summary=sync_summary,
                         interview_status=interview_status,
                         config=Config,
                         sync_chart=sync_chart,
                         interview_status_chart=interview_status_chart,
                         device_sync_chart=device_sync_chart,
                         validation_errors_chart=validation_errors_chart)


@app.route('/embed')
def embed():
    """Embeddable dashboard for Joomla integration"""
    progress = SurveyProgressAnalytics.get_overall_progress(
        survey_data,
        target_surveys=Config.TARGET_SURVEYS
    )
    return render_template('embed.html', 
                         progress=progress,
                         config=Config)


@app.route('/analytics')
def analytics():
    """Advanced analytics dashboard with new metrics"""
    # Get all analytics
    progress = SurveyProgressAnalytics.get_overall_progress(
        survey_data,
        target_surveys=Config.TARGET_SURVEYS
    )
    quality_metrics = SurveyProgressAnalytics.get_data_quality_metrics(survey_data)
    logistics = SurveyProgressAnalytics.get_logistics_status(survey_data)
    ea_stats = SurveyProgressAnalytics.get_ea_completion_stats(survey_data)
    supervisor_data = SurveyProgressAnalytics.get_supervisor_review_summary(survey_data)
    interviewer_detailed = SurveyProgressAnalytics.get_interviewer_performance_detailed(survey_data)
    province_ea_data = SurveyProgressAnalytics.get_province_ea_completion_rate(survey_data)
    
    # Generate enhanced charts
    quality_chart = ProgressCharts.create_data_quality_chart(quality_metrics)
    logistics_chart = ProgressCharts.create_logistics_status_chart(logistics)
    supervisor_chart = ProgressCharts.create_supervisor_review_chart(supervisor_data)
    ea_completion_chart = ProgressCharts.create_ea_completion_map(province_ea_data)
    error_rate_chart = ProgressCharts.create_data_error_rate_chart(interviewer_detailed)
    household_status_chart = ProgressCharts.create_household_status_chart(ea_stats)
    daily_progress_chart = ProgressCharts.create_interviewer_daily_progress_chart(interviewer_detailed)
    
    return render_template('analytics.html',
                         progress=progress,
                         quality_metrics=quality_metrics,
                         logistics=logistics,
                         ea_stats=ea_stats,
                         config=Config,
                         quality_chart=quality_chart,
                         logistics_chart=logistics_chart,
                         supervisor_chart=supervisor_chart,
                         ea_completion_chart=ea_completion_chart,
                         error_rate_chart=error_rate_chart,
                         household_status_chart=household_status_chart,
                         daily_progress_chart=daily_progress_chart)


@app.route('/api/upload-csv', methods=['POST'])
def upload_csv():
    """Upload CSV data file"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Only CSV files are allowed'}), 400
    
    try:
        # Save the uploaded file
        filepath = data_loader.save_uploaded_csv(file)
        
        if filepath:
            # Update data source to CSV
            data_loader.data_source = 'csv'
            data_loader.csv_file_path = filepath
            
            # Reload data
            global survey_data
            survey_data = data_loader.load_data()
            
            return jsonify({
                'status': 'success',
                'message': f'CSV file uploaded successfully. {len(survey_data)} records loaded.',
                'records': len(survey_data),
                'filepath': filepath
            }), 200
        else:
            return jsonify({'error': 'Failed to save file'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/refresh-data', methods=['POST'])
def refresh_data():
    """Refresh data from configured source"""
    try:
        global survey_data
        survey_data = data_loader.refresh_data()
        
        return jsonify({
            'status': 'success',
            'message': 'Data refreshed successfully',
            'records': len(survey_data),
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download-template')
def download_template():
    """Download CSV template for data upload"""
    template_path = 'data/survey_data_template.csv'
    
    if os.path.exists(template_path):
        return send_file(template_path, as_attachment=True, download_name='survey_data_template.csv')
    else:
        return jsonify({'error': 'Template file not found'}), 404


@app.route('/api/export-data')
def export_data():
    """Export current survey data to CSV"""
    try:
        filepath = DataExporter.export_to_csv(survey_data, 'survey_export')
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/data-management')
def data_management():
    """Data management page"""
    data_info = {
        'source': data_loader.data_source,
        'records': len(survey_data),
        'last_updated': datetime.now().isoformat()
    }
    
    return render_template('data_management.html', 
                         data_info=data_info,
                         config=Config)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config['PORT'], debug=app.config['DEBUG'])
