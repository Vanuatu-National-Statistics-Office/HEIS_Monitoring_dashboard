# API Quick Reference

## 🚀 Quick Start

### View API Documentation
```
http://127.0.0.1:5000/api/docs
```

### Test API Endpoint
```bash
curl http://127.0.0.1:5000/api/progress
```

## 📋 Core Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/docs` | API documentation |
| `/api/progress` | Overall progress |
| `/api/provinces` | Province stats |
| `/api/teams` | Team performance |
| `/api/quality` | Quality metrics |
| `/api/survey-solutions-sync` | Sync status |

## 🔑 Authentication (Optional - Disabled by Default)

### Enable in `.env`:
```bash
API_KEY_REQUIRED=True
API_KEY=your-secret-key
```

### Use with header:
```bash
curl -H "X-API-Key: your-key" http://127.0.0.1:5000/api/progress
```

## 🌐 CORS (Enabled by Default)

Configure in `.env`:
```bash
CORS_ORIGINS=*  # Allow all (dev)
CORS_ORIGINS=https://yourdomain.com  # Production
```

## 📊 Response Format

```json
{
  "status": "success",
  "message": "Survey progress retrieved successfully",
  "data": { ...actual data... },
  "metadata": {
    "timestamp": "2025-11-12T10:30:00",
    "version": "1.0.0",
    "total_records": 4
  }
}
```

## 🔧 Configuration Files

- `.env.example` - Environment template
- `config.py` - API settings
- `API_CONFIG_GUIDE.md` - Full documentation

## 📝 Current Settings

- **Authentication:** Disabled (development mode)
- **CORS:** Enabled for all origins
- **Rate Limit:** 100 requests/minute
- **Response Format:** JSON with metadata
- **Server:** http://127.0.0.1:5000

## 🎯 Common Use Cases

### Get Progress Data
```python
import requests
response = requests.get('http://127.0.0.1:5000/api/progress')
data = response.json()['data']
```

### Filter by Province
```bash
curl http://127.0.0.1:5000/api/filter?province=Shefa
```

### Embed in Joomla
```html
<iframe src="http://127.0.0.1:5000/embed" width="100%" height="800"></iframe>
```

## 📚 Documentation

Full details: `API_CONFIG_GUIDE.md`
