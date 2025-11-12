"""
Data models for Vanuatu Household Income & Expenditure Survey Progress Monitoring
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class SurveyProgressGenerator:
    """Generates sample survey progress data for demonstration"""
    
    # Team and interviewer structure
    TEAMS = {
        'Team A': ['INT-001', 'INT-002', 'INT-003', 'INT-004'],
        'Team B': ['INT-005', 'INT-006', 'INT-007', 'INT-008'],
        'Team C': ['INT-009', 'INT-010', 'INT-011', 'INT-012'],
        'Team D': ['INT-013', 'INT-014', 'INT-015', 'INT-016'],
        'Team E': ['INT-017', 'INT-018', 'INT-019', 'INT-020'],
        'Team F': ['INT-021', 'INT-022', 'INT-023', 'INT-024'],
    }
    
    INTERVIEWER_NAMES = {
        'INT-001': 'John Tari', 'INT-002': 'Mary Kalo', 'INT-003': 'Peter Toka', 'INT-004': 'Sarah Noel',
        'INT-005': 'David Mali', 'INT-006': 'Grace Bani', 'INT-007': 'James Tasso', 'INT-008': 'Lucy Mera',
        'INT-009': 'Robert Kali', 'INT-010': 'Anna Tari', 'INT-011': 'Thomas Nalu', 'INT-012': 'Helen Boe',
        'INT-013': 'Michael Toka', 'INT-014': 'Ruth Kalo', 'INT-015': 'Daniel Mali', 'INT-016': 'Rebecca Noel',
        'INT-017': 'Joseph Tari', 'INT-018': 'Elizabeth Mera', 'INT-019': 'Samuel Kali', 'INT-020': 'Martha Bani',
        'INT-021': 'Benjamin Tasso', 'INT-022': 'Esther Nalu', 'INT-023': 'Joshua Boe', 'INT-024': 'Rachel Toka',
    }
    
    SURVEY_STATUS = ['Completed', 'In Progress', 'Pending Review', 'Validated']
    
    # Supervisor structure
    SUPERVISORS = {
        'Team A': 'SUP-001',
        'Team B': 'SUP-002',
        'Team C': 'SUP-003',
        'Team D': 'SUP-004',
        'Team E': 'SUP-005',
        'Team F': 'SUP-006',
    }
    
    SUPERVISOR_NAMES = {
        'SUP-001': 'Wilson Tari',
        'SUP-002': 'Monica Kalo',
        'SUP-003': 'Francis Noel',
        'SUP-004': 'Christine Mali',
        'SUP-005': 'George Toka',
        'SUP-006': 'Patricia Bani',
    }
    
    VILLAGES = [
        'Melsisi', 'Lakatoro', 'Norsup', 'Port Vila', 'Luganville', 
        'Isangel', 'Sola', 'Saratamata', 'Lenakel', 'Lonorore',
        'Lolowai', 'Baie Barrier', 'Port Olry', 'Hog Harbour', 'Natawa'
    ]
    
    @staticmethod
    def generate_survey_progress_data(num_surveys=1200, start_date='2025-10-01'):
        """Generate comprehensive survey progress tracking data"""
        np.random.seed(42)
        random.seed(42)
        
        data = []
        current_date = datetime.now()
        start = datetime.strptime(start_date, '%Y-%m-%d')
        days_elapsed = (current_date - start).days
        
        # Import config for geographic structure
        from config import Config
        
        survey_id = 1
        household_listing_id = 1000
        
        for province, details in Config.GEOGRAPHIC_STRUCTURE.items():
            islands = details['islands']
            area_councils = details['area_councils']
            
            # Distribute surveys across province
            province_surveys = int(num_surveys * random.uniform(0.12, 0.22))
            
            for _ in range(province_surveys):
                # 🗂️ Basic Identification
                island = random.choice(islands)
                area_council = random.choice(area_councils)
                enumeration_area = f"EA-{random.randint(1, 50):03d}"
                village = random.choice(SurveyProgressGenerator.VILLAGES)
                household_id = f"HH-{household_listing_id:06d}"
                household_listing_id += 1
                
                # Assign to team, interviewer, and supervisor
                team_name = random.choice(list(SurveyProgressGenerator.TEAMS.keys()))
                interviewer_id = random.choice(SurveyProgressGenerator.TEAMS[team_name])
                interviewer_name = SurveyProgressGenerator.INTERVIEWER_NAMES[interviewer_id]
                supervisor_id = SurveyProgressGenerator.SUPERVISORS[team_name]
                supervisor_name = SurveyProgressGenerator.SUPERVISOR_NAMES[supervisor_id]
                
                # Survey date (within elapsed days)
                survey_date = start + timedelta(days=random.randint(0, max(1, days_elapsed)))
                visit_date = survey_date
                
                # 📊 Progress Tracking - EA level (simulated)
                ea_total_households = random.randint(30, 100)
                ea_completed = random.randint(10, ea_total_households)
                ea_refused = random.randint(0, 5)
                ea_not_found = random.randint(0, 3)
                ea_partial = random.randint(0, 2)
                ea_remaining = ea_total_households - (ea_completed + ea_refused + ea_not_found)
                completion_rate_ea = round((ea_completed / ea_total_households * 100), 1)
                
                # 🕐 Timing and Duration
                ea_start_date = start + timedelta(days=random.randint(0, 5))
                expected_end_date = ea_start_date + timedelta(days=random.randint(7, 21))
                actual_end_date = expected_end_date + timedelta(days=random.randint(-3, 5)) if survey_date > expected_end_date else None
                interview_duration = random.randint(30, 120)
                daily_progress_hh = round(random.uniform(3, 8), 1)
                
                # Status (most should be completed if date is in past)
                if survey_date < current_date - timedelta(days=2):
                    status = random.choice(['Completed', 'Validated', 'Validated', 'Completed'])
                elif survey_date < current_date:
                    status = random.choice(['Completed', 'In Progress', 'Pending Review', 'Refused', 'Not Found'])
                else:
                    status = 'In Progress'
                
                # Survey Solutions specific statuses
                ss_interview_status = random.choice([
                    'Completed',
                    'InterviewerAssigned',
                    'RejectedBySupervisor',
                    'ApprovedBySupervisor',
                    'RejectedByHeadquarters',
                    'ApprovedByHeadquarters'
                ]) if status in ['Completed', 'Validated', 'Pending Review'] else 'InterviewerAssigned'
                
                # Survey Solutions: Number of questions answered
                total_questions = 85  # Typical HIES questionnaire size
                questions_answered = random.randint(40, total_questions) if status == 'In Progress' else total_questions
                
                # Survey Solutions: Number of invalid answers (data validation errors)
                invalid_answers = random.randint(0, 3) if status in ['In Progress', 'Pending Review'] else 0
                
                # Survey Solutions: Sync status
                sync_status = random.choice(['Synced', 'Synced', 'Synced', 'Pending', 'Failed']) 
                last_sync_time = survey_date + timedelta(hours=random.randint(1, 24)) if sync_status == 'Synced' else None
                
                # 📋 Data Quality Checks
                incomplete_forms = random.randint(0, 2) if status in ['In Progress', 'Pending Review'] else 0
                rejected_forms = random.randint(0, 1) if status == 'Pending Review' else 0
                supervisor_review = random.choice(['Approved', 'Approved', 'Approved', 'Pending', 'Sent Back']) if status in ['Completed', 'Validated', 'Pending Review'] else 'Pending'
                gps_captured = random.choice([True, True, True, False])  # Mostly yes
                photo_attached = random.choice([True, True, False]) if status in ['Completed', 'Validated'] else False
                
                # Data quality score (0-100)
                quality_score = random.randint(70, 100) if status in ['Completed', 'Validated'] else None
                
                # 🧭 Logistics and Field Issues
                transport = random.choice(['Good', 'Good', 'Good', 'Poor', 'None'])
                network = random.choice(['Good', 'Good', 'Poor', 'Poor', 'None'])
                device_status = random.choice(['OK', 'OK', 'OK', 'OK', 'Faulty', 'Replaced'])
                power_supply = random.choice(['Good', 'Good', 'Poor', 'Poor'])
                field_notes = random.choice([
                    'No issues', 
                    'Remote area, difficult access', 
                    'Poor network coverage',
                    'Household head unavailable, rescheduled',
                    'Language barrier, used local interpreter',
                    'Good cooperation from community',
                    ''
                ])
                
                # Generate income and expenditure data
                household_income = np.random.lognormal(11.5, 0.8) * 1000
                household_expenditure = household_income * random.uniform(0.7, 1.1)
                household_size = random.randint(1, 10)
                
                data.append({
                    # Survey ID
                    'survey_id': f"HIES-{survey_id:05d}",
                    
                    # 🗂️ Basic Identification
                    'province': province,
                    'island': island,
                    'area_council': area_council,
                    'enumeration_area': enumeration_area,
                    'village': village,
                    'household_id': household_id,
                    'team': team_name,
                    'interviewer_id': interviewer_id,
                    'interviewer_name': interviewer_name,
                    'supervisor_id': supervisor_id,
                    'supervisor_name': supervisor_name,
                    'survey_date': survey_date,
                    'visit_date': visit_date,
                    
                    # 📊 Progress Tracking
                    'ea_total_households': ea_total_households,
                    'ea_completed': ea_completed,
                    'ea_refused': ea_refused,
                    'ea_not_found': ea_not_found,
                    'ea_partial': ea_partial,
                    'ea_remaining': ea_remaining,
                    'completion_rate_ea': completion_rate_ea,
                    
                    # 🕐 Timing and Duration
                    'ea_start_date': ea_start_date,
                    'expected_end_date': expected_end_date,
                    'actual_end_date': actual_end_date,
                    'interview_duration_minutes': interview_duration,
                    'daily_progress_hh': daily_progress_hh,
                    
                    # Status
                    'status': status,
                    
                    # Survey Solutions specific fields
                    'ss_interview_status': ss_interview_status,
                    'ss_questions_total': total_questions,
                    'ss_questions_answered': questions_answered,
                    'ss_invalid_answers': invalid_answers,
                    'ss_sync_status': sync_status,
                    'ss_last_sync': last_sync_time,
                    
                    # 📋 Data Quality Checks
                    'incomplete_forms': incomplete_forms,
                    'rejected_forms': rejected_forms,
                    'supervisor_review': supervisor_review,
                    'gps_captured': gps_captured,
                    'photo_attached': photo_attached,
                    'quality_score': quality_score,
                    
                    # 🧭 Logistics and Field Issues
                    'transport_availability': transport,
                    'network_coverage': network,
                    'device_status': device_status,
                    'power_supply': power_supply,
                    'field_notes': field_notes,
                    
                    # Survey data
                    'household_size': household_size,
                    'household_income': round(household_income, 2),
                    'household_expenditure': round(household_expenditure, 2),
                    'urban_rural': random.choice(['Urban', 'Rural', 'Rural', 'Rural'])  # More rural
                })
                
                survey_id += 1
        
        return pd.DataFrame(data)


class SurveyProgressAnalytics:
    """Analytics functions for survey progress monitoring"""
    
    @staticmethod
    def get_overall_progress(df, target_surveys=5000):
        """Get overall survey progress statistics"""
        total_surveys = len(df)
        completed = len(df[df['status'].isin(['Completed', 'Validated'])])
        in_progress = len(df[df['status'] == 'In Progress'])
        pending_review = len(df[df['status'] == 'Pending Review'])
        
        completion_rate = (completed / target_surveys * 100) if target_surveys > 0 else 0
        avg_quality = df[df['quality_score'].notna()]['quality_score'].mean()
        
        # Calculate daily average
        df_sorted = df.sort_values('survey_date')
        if len(df_sorted) > 0:
            date_range = (df_sorted['survey_date'].max() - df_sorted['survey_date'].min()).days
            daily_avg = total_surveys / max(1, date_range)
        else:
            daily_avg = 0
        
        return {
            'total_surveys': total_surveys,
            'target_surveys': target_surveys,
            'completed': completed,
            'in_progress': in_progress,
            'pending_review': pending_review,
            'completion_rate': round(completion_rate, 1),
            'avg_quality_score': round(avg_quality, 1) if pd.notna(avg_quality) else 0,
            'daily_average': round(daily_avg, 1)
        }
    
    @staticmethod
    def get_progress_by_province(df):
        """Get survey progress by province"""
        return df.groupby('province').agg({
            'survey_id': 'count',
            'status': lambda x: (x.isin(['Completed', 'Validated'])).sum(),
            'quality_score': 'mean',
            'interview_duration_minutes': 'mean'
        }).rename(columns={
            'survey_id': 'total_surveys',
            'status': 'completed_surveys',
            'interview_duration_minutes': 'avg_duration_minutes'
        }).round(2)
    
    @staticmethod
    def get_progress_by_island(df):
        """Get survey progress by island"""
        return df.groupby(['province', 'island']).agg({
            'survey_id': 'count',
            'status': lambda x: (x.isin(['Completed', 'Validated'])).sum(),
        }).rename(columns={
            'survey_id': 'total_surveys',
            'status': 'completed_surveys'
        }).round(2)
    
    @staticmethod
    def get_progress_by_team(df):
        """Get survey progress by team"""
        return df.groupby('team').agg({
            'survey_id': 'count',
            'status': lambda x: (x.isin(['Completed', 'Validated'])).sum(),
            'quality_score': 'mean',
            'interview_duration_minutes': 'mean'
        }).rename(columns={
            'survey_id': 'total_surveys',
            'status': 'completed_surveys',
            'interview_duration_minutes': 'avg_duration_minutes'
        }).round(2).sort_values('total_surveys', ascending=False)
    
    @staticmethod
    def get_progress_by_interviewer(df):
        """Get survey progress by interviewer"""
        return df.groupby(['interviewer_id', 'interviewer_name', 'team']).agg({
            'survey_id': 'count',
            'status': lambda x: (x.isin(['Completed', 'Validated'])).sum(),
            'quality_score': 'mean',
            'interview_duration_minutes': 'mean'
        }).rename(columns={
            'survey_id': 'total_surveys',
            'status': 'completed_surveys',
            'interview_duration_minutes': 'avg_duration_minutes'
        }).round(2).sort_values('total_surveys', ascending=False)
    
    @staticmethod
    def get_daily_progress(df):
        """Get daily survey completion data"""
        df_copy = df.copy()
        df_copy['date'] = pd.to_datetime(df_copy['survey_date']).dt.date
        daily = df_copy.groupby('date').agg({
            'survey_id': 'count',
            'status': lambda x: (x.isin(['Completed', 'Validated'])).sum(),
        }).rename(columns={
            'survey_id': 'total',
            'status': 'completed'
        })
        return daily
    
    @staticmethod
    def get_status_distribution(df):
        """Get distribution of survey statuses"""
        return df['status'].value_counts().to_dict()
    
    @staticmethod
    def get_top_performers(df, top_n=10):
        """Get top performing interviewers"""
        interviewer_stats = df.groupby(['interviewer_id', 'interviewer_name']).agg({
            'survey_id': 'count',
            'status': lambda x: (x.isin(['Completed', 'Validated'])).sum(),
            'quality_score': 'mean'
        }).rename(columns={
            'survey_id': 'total_surveys',
            'status': 'completed_surveys'
        })
        interviewer_stats['completion_rate'] = (
            interviewer_stats['completed_surveys'] / interviewer_stats['total_surveys'] * 100
        ).round(1)
        return interviewer_stats.sort_values('total_surveys', ascending=False).head(top_n)
    
    @staticmethod
    def get_enumeration_area_progress(df):
        """Get progress by enumeration area"""
        return df.groupby(['province', 'enumeration_area']).agg({
            'survey_id': 'count',
            'status': lambda x: (x.isin(['Completed', 'Validated'])).sum(),
        }).rename(columns={
            'survey_id': 'total_surveys',
            'status': 'completed_surveys'
        }).round(2)
    
    @staticmethod
    def get_data_quality_metrics(df):
        """Get comprehensive data quality metrics"""
        quality_metrics = {
            'total_incomplete_forms': df['incomplete_forms'].sum(),
            'total_rejected_forms': df['rejected_forms'].sum(),
            'forms_pending_review': len(df[df['supervisor_review'] == 'Pending']),
            'forms_approved': len(df[df['supervisor_review'] == 'Approved']),
            'forms_sent_back': len(df[df['supervisor_review'] == 'Sent Back']),
            'gps_capture_rate': round((df['gps_captured'].sum() / len(df) * 100), 1),
            'photo_attach_rate': round((df['photo_attached'].sum() / len(df) * 100), 1),
            'avg_quality_score': round(df['quality_score'].mean(), 1) if df['quality_score'].notna().any() else 0,
            'error_rate': round(((df['incomplete_forms'].sum() + df['rejected_forms'].sum()) / len(df) * 100), 2)
        }
        return quality_metrics
    
    @staticmethod
    def get_logistics_status(df):
        """Get logistics and field conditions status"""
        logistics = {
            'transport_good': len(df[df['transport_availability'] == 'Good']),
            'transport_poor': len(df[df['transport_availability'] == 'Poor']),
            'transport_none': len(df[df['transport_availability'] == 'None']),
            'network_good': len(df[df['network_coverage'] == 'Good']),
            'network_poor': len(df[df['network_coverage'] == 'Poor']),
            'network_none': len(df[df['network_coverage'] == 'None']),
            'devices_ok': len(df[df['device_status'] == 'OK']),
            'devices_faulty': len(df[df['device_status'] == 'Faulty']),
            'devices_replaced': len(df[df['device_status'] == 'Replaced']),
            'power_good': len(df[df['power_supply'] == 'Good']),
            'power_poor': len(df[df['power_supply'] == 'Poor']),
        }
        return logistics
    
    @staticmethod
    def get_ea_completion_stats(df):
        """Get enumeration area completion statistics"""
        ea_stats = df.groupby('enumeration_area').agg({
            'ea_total_households': 'first',
            'ea_completed': 'first',
            'ea_refused': 'first',
            'ea_not_found': 'first',
            'ea_remaining': 'first',
            'completion_rate_ea': 'first',
            'province': 'first',
            'area_council': 'first'
        }).reset_index()
        
        return ea_stats
    
    @staticmethod
    def get_supervisor_review_summary(df):
        """Get supervisor review summary by team/supervisor"""
        return df.groupby(['team', 'supervisor_name']).agg({
            'survey_id': 'count',
            'supervisor_review': lambda x: (x == 'Approved').sum(),
            'rejected_forms': 'sum',
            'quality_score': 'mean'
        }).rename(columns={
            'survey_id': 'total_reviews',
            'supervisor_review': 'approved',
            'rejected_forms': 'total_rejected'
        }).round(2)
    
    @staticmethod
    def get_interviewer_performance_detailed(df):
        """Get detailed interviewer performance metrics"""
        return df.groupby(['interviewer_id', 'interviewer_name', 'team']).agg({
            'survey_id': 'count',
            'status': lambda x: (x.isin(['Completed', 'Validated'])).sum(),
            'interview_duration_minutes': 'mean',
            'daily_progress_hh': 'mean',
            'quality_score': 'mean',
            'incomplete_forms': 'sum',
            'rejected_forms': 'sum',
            'gps_captured': lambda x: (x == True).sum() / len(x) * 100 if len(x) > 0 else 0
        }).rename(columns={
            'survey_id': 'total_surveys',
            'status': 'completed_surveys',
            'interview_duration_minutes': 'avg_duration',
            'daily_progress_hh': 'avg_daily_progress',
            'quality_score': 'avg_quality',
            'gps_captured': 'gps_capture_rate'
        }).round(2).sort_values('total_surveys', ascending=False)
    
    @staticmethod
    def get_province_ea_completion_rate(df):
        """Get percentage of EAs completed by province"""
        # Group by province and EA, check if EA has all households completed
        ea_by_province = df.groupby(['province', 'enumeration_area']).agg({
            'ea_remaining': 'first',
            'completion_rate_ea': 'first'
        }).reset_index()
        
        # Count EAs that are 100% complete
        province_ea_complete = ea_by_province[ea_by_province['completion_rate_ea'] == 100.0].groupby('province').size()
        province_ea_total = ea_by_province.groupby('province').size()
        
        result = pd.DataFrame({
            'total_eas': province_ea_total,
            'completed_eas': province_ea_complete
        }).fillna(0)
        result['ea_completion_percentage'] = round((result['completed_eas'] / result['total_eas'] * 100), 1)
        
        return result.sort_values('ea_completion_percentage', ascending=False)
    
    @staticmethod
    def get_survey_solutions_sync_status(df):
        """Get Survey Solutions sync status summary"""
        sync_summary = {
            'synced': len(df[df['ss_sync_status'] == 'Synced']),
            'pending': len(df[df['ss_sync_status'] == 'Pending']),
            'failed': len(df[df['ss_sync_status'] == 'Failed']),
            'sync_rate': round((len(df[df['ss_sync_status'] == 'Synced']) / len(df) * 100), 1) if len(df) > 0 else 0,
            'avg_questions_answered': round(df['ss_questions_answered'].mean(), 1),
            'avg_invalid_answers': round(df['ss_invalid_answers'].mean(), 2),
            'total_invalid_answers': df['ss_invalid_answers'].sum()
        }
        return sync_summary
    
    @staticmethod
    def get_survey_solutions_interview_status(df):
        """Get Survey Solutions interview status distribution"""
        status_counts = df['ss_interview_status'].value_counts().to_dict()
        return status_counts
    
    @staticmethod
    def get_device_sync_performance(df):
        """Get sync performance by device/interviewer"""
        return df.groupby(['interviewer_id', 'interviewer_name']).agg({
            'ss_sync_status': lambda x: (x == 'Synced').sum() / len(x) * 100 if len(x) > 0 else 0,
            'ss_invalid_answers': 'sum',
            'ss_questions_answered': 'mean',
            'survey_id': 'count'
        }).rename(columns={
            'ss_sync_status': 'sync_success_rate',
            'ss_invalid_answers': 'total_validation_errors',
            'ss_questions_answered': 'avg_questions_completed',
            'survey_id': 'total_interviews'
        }).round(2).sort_values('sync_success_rate', ascending=False)
