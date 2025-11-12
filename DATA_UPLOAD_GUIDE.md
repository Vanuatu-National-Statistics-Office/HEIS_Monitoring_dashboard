# Data Upload & Management Guide

This guide explains how to upload and manage survey data for the Vanuatu HIES Survey Dashboard.

## 📚 Table of Contents

1. [Data Source Options](#data-source-options)
2. [CSV File Upload](#csv-file-upload)
3. [Survey Solutions API](#survey-solutions-api)
4. [Database Connection](#database-connection)
5. [Mock Data](#mock-data)
6. [Troubleshooting](#troubleshooting)

---

## Data Source Options

The dashboard supports **4 data source modes**:

| Mode | Description | Use Case |
|------|-------------|----------|
| **Mock** | Generated test data | Development & testing |
| **CSV** | Upload CSV files | Manual data entry or offline surveys |
| **API** | Survey Solutions API | Real-time data from CAPI system |
| **Database** | PostgreSQL/MySQL | Production deployment |

### Automatic Fallback

The system automatically falls back to mock data if the configured source fails, ensuring the dashboard always works.

---

## CSV File Upload

### Method 1: Web Interface

1. Navigate to **Data Management** page: http://127.0.0.1:5000/data-management
2. Click **"Download CSV Template"** to get the correct format
3. Fill in your survey data in the template
4. Click **"Upload CSV"** and select your file
5. Data will be validated and loaded automatically

### Method 2: Direct File Placement

1. Download the template: http://127.0.0.1:5000/api/download-template
2. Save your data as `data/survey_data.csv`
3. Update `.env`:
   ```bash
   DATA_SOURCE=csv
   CSV_FILE_PATH=data/survey_data.csv
   ```
4. Restart the Flask server

### CSV File Requirements

**Required Columns:**
- `survey_id` - Unique survey identifier
- `province` - Province name
- `island` - Island name  
- `area_council` - Area council name
- `ea_code` - Enumeration area code
- `team` - Team identifier
- `interviewer_id` - Interviewer ID
- `interviewer_name` - Interviewer name
- `supervisor_id` - Supervisor ID
- `supervisor_name` - Supervisor name
- `status` - Interview status (completed/in_progress/pending/rejected)
- `interview_date` - Date in YYYY-MM-DD format
- `household_id` - Household identifier
- `household_head_name` - Head of household name
- `household_size` - Number of household members
- `quality_score` - Quality score (0-100)
- `data_errors` - Number of data errors
- `gps_latitude` - GPS latitude
- `gps_longitude` - GPS longitude
- `gps_accuracy` - GPS accuracy in meters
- `interview_duration_minutes` - Interview duration
- `device_id` - Device/tablet ID
- `tablet_model` - Tablet model
- `battery_level` - Battery percentage
- `data_collection_method` - CAPI or CAWI
- `ss_interview_status` - Survey Solutions status
- `ss_questions_total` - Total questions
- `ss_questions_answered` - Answered questions
- `ss_invalid_answers` - Invalid answers count
- `ss_sync_status` - Sync status (synced/pending/failed)
- `ss_last_sync` - Last sync timestamp

**Example Row:**
```csv
1,Shefa,Efate,Port Vila,EA001,Team A,INT001,John Doe,SUP001,Jane Smith,completed,2024-01-15,HH001,Chief Tom,5,95,0,-17.7334,168.3273,5.2,45,TAB001,Samsung Galaxy,85,CAPI,Completed,150,148,2,synced,2024-01-15 18:30:00
```

---

## Survey Solutions API

### Configuration

1. Open your `.env` file
2. Add/update these settings:
   ```bash
   DATA_SOURCE=api
   SS_API_USER=your_username
   SS_API_PASSWORD=your_password
   ```
3. Restart the Flask server

### API Endpoint

The dashboard connects to: **https://vnsocapi.gov.vu/**

### Authentication

Survey Solutions uses HTTP Basic Authentication:
- Username: Your Survey Solutions API user
- Password: Your API password

### Data Flow

```
Survey Solutions Server
         ↓
    HTTPS API
         ↓
   Data Loader
         ↓
    Dashboard
```

### API Endpoints Used

- `/api/v1/interviews` - Get interview list
- `/api/v1/interviews/{id}` - Get interview details
- `/api/v1/interviews/{id}/statistics` - Get statistics

### Manual Refresh

Use the Data Management page or API:
```bash
POST http://127.0.0.1:5000/api/refresh-data
```

---

## Database Connection

### Supported Databases

- PostgreSQL (recommended)
- MySQL
- SQLite (for testing)

### PostgreSQL Setup

1. Install PostgreSQL
2. Create database:
   ```sql
   CREATE DATABASE vanuatu_survey;
   ```
3. Configure `.env`:
   ```bash
   DATA_SOURCE=database
   DATABASE_URL=postgresql://username:password@localhost/vanuatu_survey
   ```
4. Install Python driver:
   ```bash
   pip install psycopg2-binary
   ```

### MySQL Setup

1. Install MySQL
2. Create database:
   ```sql
   CREATE DATABASE vanuatu_survey;
   ```
3. Configure `.env`:
   ```bash
   DATA_SOURCE=database
   DATABASE_URL=mysql+pymysql://username:password@localhost/vanuatu_survey
   ```
4. Install Python driver:
   ```bash
   pip install pymysql
   ```

### Table Schema

The database should have a table with the same columns as the CSV template. SQL schema:

```sql
CREATE TABLE survey_data (
    survey_id VARCHAR(50) PRIMARY KEY,
    province VARCHAR(100),
    island VARCHAR(100),
    area_council VARCHAR(100),
    ea_code VARCHAR(50),
    team VARCHAR(50),
    interviewer_id VARCHAR(50),
    interviewer_name VARCHAR(200),
    supervisor_id VARCHAR(50),
    supervisor_name VARCHAR(200),
    status VARCHAR(50),
    interview_date DATE,
    household_id VARCHAR(50),
    household_head_name VARCHAR(200),
    household_size INTEGER,
    quality_score INTEGER,
    data_errors INTEGER,
    gps_latitude DECIMAL(10, 6),
    gps_longitude DECIMAL(10, 6),
    gps_accuracy DECIMAL(10, 2),
    interview_duration_minutes INTEGER,
    device_id VARCHAR(50),
    tablet_model VARCHAR(100),
    battery_level INTEGER,
    data_collection_method VARCHAR(20),
    ss_interview_status VARCHAR(50),
    ss_questions_total INTEGER,
    ss_questions_answered INTEGER,
    ss_invalid_answers INTEGER,
    ss_sync_status VARCHAR(20),
    ss_last_sync TIMESTAMP
);
```

---

## Mock Data

### When to Use

- Development and testing
- Demonstrations
- When real data is not yet available

### Activation

```bash
DATA_SOURCE=mock
```

### Characteristics

- Generates 1000 random records
- Includes all 6 provinces
- Realistic interviewer names
- Valid date ranges
- Proper status distributions
- GPS coordinates within Vanuatu

---

## Troubleshooting

### CSV Upload Issues

**Problem:** "Invalid CSV format"
- **Solution:** Ensure all 31 columns are present in the correct order
- Use the template from `/api/download-template`

**Problem:** "No file selected"
- **Solution:** Make sure to select a file before clicking Upload

**Problem:** "Invalid file type"
- **Solution:** Only .csv files are accepted

### API Connection Issues

**Problem:** "Authentication failed"
- **Solution:** Check `SS_API_USER` and `SS_API_PASSWORD` in `.env`

**Problem:** "Cannot connect to server"
- **Solution:** Verify the server URL: https://vnsocapi.gov.vu/
- Check your internet connection
- Ensure the Survey Solutions server is running

**Problem:** "Data not refreshing"
- **Solution:** Click the refresh button in Data Management
- Or restart the Flask server

### Database Issues

**Problem:** "Cannot connect to database"
- **Solution:** Check `DATABASE_URL` format
- Ensure database server is running
- Verify username and password

**Problem:** "Table does not exist"
- **Solution:** Create the table using the SQL schema above

### General Issues

**Problem:** Dashboard shows no data
- **Solution:** Check the console output when starting Flask
- It will show which data source is being used
- The system will fall back to mock data if the configured source fails

**Problem:** Changes not taking effect
- **Solution:** Always restart the Flask server after changing `.env`:
  ```bash
  Ctrl+C  # Stop server
  python app.py  # Start server
  ```

---

## Data Management Page

Access at: **http://127.0.0.1:5000/data-management**

Features:
- ✅ View current data source and record count
- ✅ Upload CSV files with validation
- ✅ Download CSV template
- ✅ Refresh data from configured source
- ✅ Export current data to CSV
- ✅ Configuration examples for all source types

---

## Best Practices

1. **Start with Mock Data** - Test the dashboard before connecting real data
2. **Use CSV Templates** - Always download and use the official template
3. **Test Uploads** - Upload a small test file before bulk uploads
4. **Backup Data** - Export data regularly using the export feature
5. **Monitor Logs** - Check Flask console for data loading status
6. **Validate Data** - Ensure dates, coordinates, and scores are in valid ranges

---

## Support

For technical issues:
1. Check the console output for error messages
2. Review this guide's troubleshooting section
3. Verify `.env` configuration
4. Check file permissions for CSV uploads

---

Last Updated: {{ current_date }}
