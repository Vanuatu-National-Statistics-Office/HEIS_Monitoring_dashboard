# Option B: Automatic Survey Solutions API Setup

## 🌐 Automatic Data Extraction from Survey Solutions Server

This guide will help you configure the dashboard to automatically extract survey data from the Survey Solutions server at **https://vnsocapi.gov.vu/**

---

## ⚙️ Configuration Steps

### Step 1: Get API Credentials

You need API credentials from your Survey Solutions administrator:

1. **Username**: Your Survey Solutions API user account
2. **Password**: API password (not your regular login password)

**How to get credentials:**
- Contact your Survey Solutions administrator
- Or create an API user in Survey Solutions:
  - Go to Survey Solutions admin panel
  - Navigate to "Users" section
  - Create a new user with "API User" role
  - Save the username and password

### Step 2: Update .env File

Open the `.env` file in the project root directory and update these lines:

```bash
# Set data source to API
DATA_SOURCE=api

# Enter your Survey Solutions credentials
SS_API_USER=your_actual_username
SS_API_PASSWORD=your_actual_password
```

**Example:**
```bash
DATA_SOURCE=api
SS_API_USER=vanuatu_api_user
SS_API_PASSWORD=SecurePassword123!
```

### Step 3: Restart the Flask Server

Stop the current server (press `Ctrl+C` in the terminal) and restart:

```bash
cd C:\vanuatu-survey-dashboard
python app.py
```

You should see:
```
============================================================
🚀 VANUATU HIES SURVEY DASHBOARD - DATA SOURCE
============================================================
📡 Loading data from SURVEY SOLUTIONS API...
✅ Successfully loaded 150 records from API
============================================================
```

---

## 🔄 Data Refresh

The dashboard automatically fetches fresh data from the Survey Solutions server when:

1. **Server starts** - Fresh data loaded on startup
2. **Manual refresh** - Click "Refresh" button in Data Management page
3. **API call** - POST request to `/api/refresh-data`

### Manual Refresh Options

**Option 1: Web Interface**
1. Navigate to: http://127.0.0.1:5000/data-management
2. Click the **"Fetch from API"** button under "Survey Solutions API"
3. Or click **"Refresh Current Source"** button

**Option 2: API Endpoint**
```bash
curl -X POST http://127.0.0.1:5000/api/refresh-data
```

**Option 3: Python Script**
```python
import requests
response = requests.post('http://127.0.0.1:5000/api/refresh-data')
print(response.json())
```

---

## 📊 What Data Gets Extracted

The system automatically extracts:

### Interview Data
- Survey ID and interview status
- Assignment information
- Interview dates and timestamps
- Quality metrics

### Geographic Information
- Province, island, area council
- Enumeration area codes
- GPS coordinates (if available)

### Team Information
- Interviewer details (ID, name)
- Supervisor details (ID, name)
- Team assignments

### Survey Solutions Specific
- Interview status (completed, in progress, rejected)
- Question counts (total, answered, invalid)
- Synchronization status
- Last sync timestamp

### Device Information
- Device/tablet ID
- Tablet model
- Battery level
- Data collection method (CAPI/CAWI)

---

## 🔐 Security & Permissions

### API User Requirements

Your Survey Solutions API user needs these permissions:
- ✅ Read access to interviews
- ✅ Read access to assignments
- ✅ Read access to interview statistics
- ❌ Write access not required

### API Endpoints Used

The dashboard connects to these Survey Solutions endpoints:
```
GET /api/v1/questionnaires
GET /api/v1/interviews
GET /api/v1/assignments
GET /api/v1/interviews/{id}
GET /api/v1/interviews/{id}/stats
```

### Connection Security

- Uses HTTPS encryption (https://vnsocapi.gov.vu/)
- HTTP Basic Authentication
- Credentials stored in `.env` (never in code)
- `.env` file excluded from version control

---

## 🧪 Testing the Connection

### Test 1: Check Server Connectivity

```bash
curl https://vnsocapi.gov.vu/
```

Expected: Connection successful (even if authentication required)

### Test 2: Test Authentication

```bash
curl -u username:password https://vnsocapi.gov.vu/api/v1/questionnaires
```

Replace `username` and `password` with your credentials.

Expected: JSON response with questionnaire list

### Test 3: View Dashboard Startup

When you start the Flask app, watch the console output:

**Success:**
```
📡 Loading data from SURVEY SOLUTIONS API...
✅ Successfully loaded 150 records from API
```

**Authentication Error:**
```
📡 Loading data from SURVEY SOLUTIONS API...
❌ Authentication failed. Check credentials.
⚠️ Falling back to MOCK data for testing
```

**Connection Error:**
```
📡 Loading data from SURVEY SOLUTIONS API...
❌ Cannot connect to server. Check network connection.
⚠️ Falling back to MOCK data for testing
```

---

## 🛠️ Troubleshooting

### Issue: Authentication Failed

**Symptoms:**
- Console shows "Authentication failed"
- Dashboard falls back to mock data

**Solutions:**
1. Verify credentials in `.env` file
2. Ensure API user exists in Survey Solutions
3. Check user has API role (not interviewer/supervisor)
4. Try credentials manually with curl (see Test 2 above)

### Issue: Cannot Connect to Server

**Symptoms:**
- Console shows "Cannot connect to server"
- Timeout errors

**Solutions:**
1. Check internet connection
2. Verify server URL: https://vnsocapi.gov.vu/
3. Check if Survey Solutions server is running
4. Try accessing the URL in a web browser
5. Check firewall settings

### Issue: No Data / Empty Response

**Symptoms:**
- Connection successful but 0 records
- Dashboard shows empty charts

**Solutions:**
1. Verify surveys exist in Survey Solutions
2. Check if API user has permission to view surveys
3. Check questionnaire assignment status
4. Review Survey Solutions logs

### Issue: Partial Data / Missing Fields

**Symptoms:**
- Some fields are empty or null
- GPS coordinates missing

**Solutions:**
1. These fields may not be available in all interviews
2. Check Survey Solutions questionnaire design
3. GPS data only available if enabled in survey
4. Some fields populate only after interview completion

---

## 📈 Data Sync Schedule

### Automatic Sync Options

Currently, data refreshes on:
- ✅ Server startup
- ✅ Manual refresh

**Future Enhancement Ideas:**
```python
# Add to app.py for automatic periodic refresh
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(
    func=lambda: data_loader.refresh_data(),
    trigger="interval",
    minutes=30  # Refresh every 30 minutes
)
scheduler.start()
```

---

## 📋 Checklist

Before going live with API mode:

- [ ] API credentials obtained from administrator
- [ ] Credentials added to `.env` file
- [ ] `.env` file not committed to version control
- [ ] Test connection with curl
- [ ] Verify API user permissions
- [ ] Restart Flask server
- [ ] Check console for successful data load
- [ ] View dashboard to verify data appears
- [ ] Test manual refresh from Data Management page
- [ ] Verify all charts display correct data
- [ ] Check GPS coordinates if using map features
- [ ] Export data to verify all fields populated

---

## 🆘 Getting Help

If you encounter issues:

1. **Check Console Output**: Most errors show detailed messages
2. **Review Logs**: Look for error messages in terminal
3. **Test with curl**: Verify API access independently
4. **Try Mock Data**: Change `DATA_SOURCE=mock` to verify dashboard works
5. **Contact Survey Solutions Admin**: For credential or permission issues

---

## 📞 Survey Solutions API Resources

- **Server**: https://vnsocapi.gov.vu/
- **API Documentation**: https://docs.mysurvey.solutions/headquarters/api/
- **Version**: 24.09
- **Authentication**: HTTP Basic Auth
- **Format**: JSON

---

## ✅ You're All Set!

Once configured, your dashboard will:
- ✅ Automatically fetch fresh data from Survey Solutions
- ✅ Display real-time survey progress
- ✅ Update when you click refresh
- ✅ Fall back to mock data if connection fails
- ✅ Show detailed status in console

**Next Steps:**
1. Enter your credentials in `.env`
2. Restart the server
3. Navigate to http://127.0.0.1:5000
4. Monitor your survey in real-time! 🎉

---

Last Updated: November 12, 2025
