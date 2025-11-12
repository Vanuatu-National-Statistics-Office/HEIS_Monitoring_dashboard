import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-vanuatu-survey'
    PORT = int(os.environ.get('PORT', 5000))
    DEBUG = os.environ.get('FLASK_ENV') == 'development'
    
    # Survey configuration
    SURVEY_NAME = "Vanuatu Household Income & Expenditure Survey"
    SURVEY_SHORT_NAME = "HIES Survey Progress Monitor"
    CURRENCY = "VUV"  # Vanuatu Vatu
    
    # Survey Solutions Designer Configuration
    SURVEY_PLATFORM = "Survey Solutions Designer"
    SURVEY_PLATFORM_VERSION = "24.09"
    CAPI_MODE = True  # Computer-Assisted Personal Interviewing
    CAWI_MODE = False  # Computer-Assisted Web Interviewing
    OFFLINE_SYNC = True  # Tablets sync when online
    
    # Survey Solutions Server
    SURVEY_SOLUTIONS_SERVER = "https://vnsocapi.gov.vu/"
    SURVEY_SOLUTIONS_API_USER = os.environ.get('SS_API_USER', 'api_user')
    SURVEY_SOLUTIONS_API_PASSWORD = os.environ.get('SS_API_PASSWORD', '')
    
    # API Configuration
    API_TITLE = "Vanuatu HIES Survey Progress API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "REST API for Vanuatu Household Income & Expenditure Survey monitoring"
    
    # CORS Configuration
    CORS_ENABLED = True
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')  # In production, specify allowed origins
    
    # API Rate Limiting (requests per minute)
    API_RATE_LIMIT = int(os.environ.get('API_RATE_LIMIT', 100))
    
    # API Authentication
    API_KEY_REQUIRED = os.environ.get('API_KEY_REQUIRED', 'False').lower() == 'true'
    API_KEY = os.environ.get('API_KEY', 'your-secret-api-key-here')
    
    # API Response Format
    API_DEFAULT_FORMAT = 'json'  # json, csv
    API_INCLUDE_METADATA = True
    
    # Target surveys
    TARGET_SURVEYS = 5000  # Total target number of surveys
    SURVEY_START_DATE = "2025-10-01"
    SURVEY_END_DATE = "2025-12-31"
    
    # Geographic hierarchy: Province > Island > Area Council > Enumeration Area
    GEOGRAPHIC_STRUCTURE = {
        'Malampa': {
            'islands': ['Malekula', 'Ambrym', 'Paama'],
            'area_councils': ['North Malekula', 'South Malekula', 'North Ambrym', 'South Ambrym', 'Paama'],
        },
        'Penama': {
            'islands': ['Pentecost', 'Ambae', 'Maewo'],
            'area_councils': ['North Pentecost', 'South Pentecost', 'Ambae', 'Maewo'],
        },
        'Sanma': {
            'islands': ['Espiritu Santo', 'Malo'],
            'area_councils': ['Luganville', 'South Santo', 'North Santo', 'East Santo', 'Malo'],
        },
        'Shefa': {
            'islands': ['Efate', 'Epi', 'Shepherd Islands'],
            'area_councils': ['Port Vila', 'Efate Rural', 'Epi', 'Shepherd Islands'],
        },
        'Tafea': {
            'islands': ['Tanna', 'Aniwa', 'Futuna', 'Erromango', 'Aneityum'],
            'area_councils': ['Tanna', 'Aniwa', 'Futuna', 'Erromango', 'Aneityum'],
        },
        'Torba': {
            'islands': ['Torres Islands', 'Banks Islands'],
            'area_councils': ['Torres', 'Banks East', 'Banks West'],
        }
    }
    
    PROVINCES = list(GEOGRAPHIC_STRUCTURE.keys())
