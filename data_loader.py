"""
Data loader for Vanuatu HIES Survey Dashboard
Supports multiple data sources: CSV upload, Survey Solutions API, Database, Mock data
"""
import pandas as pd
import requests
from datetime import datetime
import os
from config import Config
from data_models import SurveyProgressGenerator

class DataLoader:
    """Handles loading survey data from various sources"""
    
    def __init__(self):
        self.data_source = os.environ.get('DATA_SOURCE', 'mock')  # mock, csv, api, database
        self.csv_file_path = os.environ.get('CSV_FILE_PATH', 'data/survey_data.csv')
        
    def load_data(self):
        """Load data based on configured source"""
        if self.data_source == 'csv':
            return self.load_from_csv()
        elif self.data_source == 'api':
            return self.load_from_survey_solutions_api()
        elif self.data_source == 'database':
            return self.load_from_database()
        else:
            return self.load_mock_data()
    
    def load_mock_data(self):
        """Generate sample/mock data for testing"""
        print("📊 Loading MOCK data for testing...")
        return SurveyProgressGenerator.generate_survey_progress_data(
            num_surveys=1200,
            start_date=Config.SURVEY_START_DATE
        )
    
    def load_from_csv(self):
        """Load data from CSV file"""
        try:
            print(f"📁 Loading data from CSV: {self.csv_file_path}")
            
            if not os.path.exists(self.csv_file_path):
                print(f"❌ CSV file not found: {self.csv_file_path}")
                print("⚠️  Falling back to mock data...")
                return self.load_mock_data()
            
            df = pd.read_csv(self.csv_file_path)
            
            # Validate required columns
            required_columns = [
                'survey_id', 'province', 'island', 'team', 'interviewer_id',
                'status', 'interview_date'
            ]
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                print(f"❌ Missing required columns: {missing_columns}")
                print("⚠️  Falling back to mock data...")
                return self.load_mock_data()
            
            # Convert date column
            df['interview_date'] = pd.to_datetime(df['interview_date'])
            
            print(f"✅ Successfully loaded {len(df)} records from CSV")
            return df
            
        except Exception as e:
            print(f"❌ Error loading CSV: {str(e)}")
            print("⚠️  Falling back to mock data...")
            return self.load_mock_data()
    
    def load_from_survey_solutions_api(self):
        """Load data directly from Survey Solutions API"""
        try:
            print("🌐 Connecting to Survey Solutions API...")
            
            # Survey Solutions API endpoints
            base_url = Config.SURVEY_SOLUTIONS_SERVER.rstrip('/')
            api_user = Config.SURVEY_SOLUTIONS_API_USER
            api_password = Config.SURVEY_SOLUTIONS_API_PASSWORD
            
            # Check if credentials are configured
            if not api_password or api_password == '':
                print("❌ Survey Solutions API credentials not configured")
                print("⚠️  Please set SS_API_PASSWORD in .env file")
                print("⚠️  Falling back to mock data...")
                return self.load_mock_data()
            
            # Example API endpoint - adjust based on your Survey Solutions setup
            # This is a placeholder - actual endpoint depends on your questionnaire ID
            interviews_endpoint = f"{base_url}/api/v1/interviews"
            
            # Make API request with authentication
            auth = (api_user, api_password)
            response = requests.get(interviews_endpoint, auth=auth, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                df = self._parse_survey_solutions_response(data)
                print(f"✅ Successfully loaded {len(df)} records from Survey Solutions API")
                return df
            else:
                print(f"❌ API request failed with status {response.status_code}")
                print("⚠️  Falling back to mock data...")
                return self.load_mock_data()
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error connecting to Survey Solutions API: {str(e)}")
            print("⚠️  Falling back to mock data...")
            return self.load_mock_data()
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            print("⚠️  Falling back to mock data...")
            return self.load_mock_data()
    
    def load_from_database(self):
        """Load data from PostgreSQL/MySQL database"""
        try:
            print("🗄️  Loading data from database...")
            
            # Database connection string from environment
            db_url = os.environ.get('DATABASE_URL')
            
            if not db_url:
                print("❌ DATABASE_URL not configured")
                print("⚠️  Falling back to mock data...")
                return self.load_mock_data()
            
            # Use SQLAlchemy to connect
            from sqlalchemy import create_engine
            engine = create_engine(db_url)
            
            # Query survey data
            query = """
                SELECT 
                    survey_id, province, island, area_council, ea_code, team,
                    interviewer_id, interviewer_name, supervisor_id, supervisor_name,
                    status, interview_date, household_id, household_head_name,
                    quality_score, data_errors, gps_latitude, gps_longitude,
                    interview_duration_minutes, device_id, 
                    ss_interview_status, ss_sync_status
                FROM survey_responses
                WHERE interview_date >= :start_date
            """
            
            df = pd.read_sql(query, engine, params={'start_date': Config.SURVEY_START_DATE})
            
            print(f"✅ Successfully loaded {len(df)} records from database")
            return df
            
        except ImportError:
            print("❌ SQLAlchemy not installed. Run: pip install sqlalchemy psycopg2-binary")
            print("⚠️  Falling back to mock data...")
            return self.load_mock_data()
        except Exception as e:
            print(f"❌ Database error: {str(e)}")
            print("⚠️  Falling back to mock data...")
            return self.load_mock_data()
    
    def _parse_survey_solutions_response(self, api_response):
        """Parse Survey Solutions API response into DataFrame"""
        # This is a placeholder - adjust based on actual API response structure
        records = []
        
        for interview in api_response.get('interviews', []):
            record = {
                'survey_id': interview.get('interviewId'),
                'province': interview.get('province'),
                'island': interview.get('island'),
                'team': interview.get('teamName'),
                'interviewer_id': interview.get('interviewerId'),
                'interviewer_name': interview.get('interviewerName'),
                'status': self._map_ss_status(interview.get('status')),
                'interview_date': interview.get('updateDate'),
                'ss_interview_status': interview.get('status'),
                'ss_sync_status': 'Synced' if interview.get('receivedByInterviewerAtUtc') else 'Pending'
            }
            records.append(record)
        
        return pd.DataFrame(records)
    
    def _map_ss_status(self, ss_status):
        """Map Survey Solutions status to dashboard status"""
        status_mapping = {
            'Completed': 'Completed',
            'InterviewerAssigned': 'In Progress',
            'SupervisorAssigned': 'Pending Review',
            'ApprovedBySupervisor': 'Validated',
            'ApprovedByHeadquarters': 'Validated',
            'RejectedBySupervisor': 'In Progress',
            'RejectedByHeadquarters': 'Pending Review'
        }
        return status_mapping.get(ss_status, 'In Progress')
    
    def save_uploaded_csv(self, file):
        """Save uploaded CSV file"""
        try:
            # Create data directory if it doesn't exist
            os.makedirs('data', exist_ok=True)
            
            # Save file with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"survey_data_{timestamp}.csv"
            filepath = os.path.join('data', filename)
            
            file.save(filepath)
            
            print(f"✅ CSV file saved: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Error saving CSV: {str(e)}")
            return None
    
    def refresh_data(self):
        """Refresh data from source"""
        print("🔄 Refreshing data...")
        return self.load_data()


class DataExporter:
    """Export survey data to various formats"""
    
    @staticmethod
    def export_to_csv(dataframe, filename='export'):
        """Export DataFrame to CSV"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = f"exports/{filename}_{timestamp}.csv"
        
        os.makedirs('exports', exist_ok=True)
        dataframe.to_csv(filepath, index=False)
        
        return filepath
    
    @staticmethod
    def export_to_excel(dataframe, filename='export'):
        """Export DataFrame to Excel"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = f"exports/{filename}_{timestamp}.xlsx"
        
        os.makedirs('exports', exist_ok=True)
        dataframe.to_excel(filepath, index=False)
        
        return filepath
