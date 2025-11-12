# 🚀 Quick Start: Option B (Automatic API Extraction)

## One-Command Setup

```bash
cd C:\vanuatu-survey-dashboard
python configure_api.py
```

This will prompt you for:
- Survey Solutions API username
- Survey Solutions API password

Then automatically configure the `.env` file.

---

## Manual Setup (Alternative)

Edit `.env` file:

```bash
DATA_SOURCE=api
SS_API_USER=your_username_here
SS_API_PASSWORD=your_password_here
```

---

## Start the Dashboard

```bash
python app.py
```

Look for this in console:
```
✅ Successfully loaded X records from API
```

---

## Access Dashboard

Open browser: **http://127.0.0.1:5000**

---

## Refresh Data Anytime

1. Go to: http://127.0.0.1:5000/data-management
2. Click **"Fetch from API"** button

---

## Troubleshooting

### ❌ Authentication Failed
- Check username/password in `.env`
- Contact Survey Solutions admin

### ❌ Cannot Connect
- Check internet connection
- Verify server is online: https://vnsocapi.gov.vu/

### ⚠️ Falls Back to Mock Data
- Dashboard will work with test data
- Fix credentials and refresh

---

## Server Information

- **URL**: https://vnsocapi.gov.vu/
- **Version**: Survey Solutions 24.09
- **Auth**: HTTP Basic Authentication
- **API Docs**: https://docs.mysurvey.solutions/headquarters/api/

---

## Get API Credentials

Contact your Survey Solutions administrator or:

1. Login to Survey Solutions
2. Go to **Admin** → **Users**
3. Create new user with **"API User"** role
4. Save username and password

---

## Need Help?

📚 **Full Guide**: See `OPTION_B_API_SETUP.md`
📖 **Data Upload Guide**: See `DATA_UPLOAD_GUIDE.md`
🌐 **Web Interface**: http://127.0.0.1:5000/data-management

---

**Status**: ✅ Option B Configured
**Mode**: Automatic API Extraction
**Server**: https://vnsocapi.gov.vu/
