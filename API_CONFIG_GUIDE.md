# API Configuration Guide

## Overview
The Vanuatu HIES Survey Progress API provides RESTful endpoints for accessing survey monitoring data. The API supports optional authentication, CORS, and standardized response formats.

## Base URL
```
http://127.0.0.1:5000/api/
```

## Authentication
The API supports optional API key authentication. By default, authentication is **disabled** for development.

### Enabling API Authentication
1. Create a `.env` file in the project root (copy from `.env.example`)
2. Set `API_KEY_REQUIRED=True`
3. Set `API_KEY=your-secure-api-key-here`

### Using API Keys
Include the API key in requests using either method:

**Header (Recommended):**
```bash
curl -H "X-API-Key: your-api-key" http://127.0.0.1:5000/api/progress
```

**Query Parameter:**
```bash
curl http://127.0.0.1:5000/api/progress?api_key=your-api-key
```

## CORS Configuration
Cross-Origin Resource Sharing (CORS) is enabled by default to allow API access from web applications.

### Configure Allowed Origins
In `.env` file:
```bash
CORS_ORIGINS=*  # Allow all origins (development)
# OR
CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com  # Production
```

## API Endpoints

### Documentation
- **GET** `/api` or `/api/docs` - API documentation and endpoint reference

### Core Progress Endpoints
| Endpoint | Description | Response Fields |
|----------|-------------|-----------------|
| `/api/progress` | Overall survey progress | total_surveys, completed, in_progress, completion_rate |
| `/api/provinces` | Province-level statistics | province, total, completed, completion_rate |
| `/api/teams` | Team performance data | team, supervisor, total, completed, avg_quality |
| `/api/interviewers` | Interviewer statistics | interviewer_id, name, team, total, completed |
| `/api/daily` | Daily progress tracking | date, surveys_completed, cumulative_total |

### Quality & Logistics Endpoints
| Endpoint | Description | Response Fields |
|----------|-------------|-----------------|
| `/api/quality` | Data quality metrics | avg_quality_score, error_rate, gps_capture_rate |
| `/api/logistics` | Equipment & logistics status | tablets_active, tablets_issues, transport_available |
| `/api/ea-stats` | Enumeration Area statistics | ea_code, province, island, households, completed |
| `/api/supervisors` | Supervisor review summary | supervisor, team, approved, rejected, pending |
| `/api/interviewer-detailed` | Detailed interviewer performance | All performance metrics |
| `/api/province-ea-completion` | EA completion by province | Province-wise EA completion rates |

### Survey Solutions Endpoints
| Endpoint | Description | Response Fields |
|----------|-------------|-----------------|
| `/api/survey-solutions-sync` | Tablet sync status | synced, pending, failed, sync_rate |
| `/api/survey-solutions-interview-status` | Interview workflow status | status_counts by workflow stage |
| `/api/device-sync-performance` | Device sync performance | interviewer, device_id, sync_success_rate |

### Filter Endpoint
**GET** `/api/filter`

Filter survey data by multiple criteria:
- `province` - Filter by province name
- `island` - Filter by island name
- `team` - Filter by team name
- `interviewer` - Filter by interviewer ID

Example:
```bash
curl http://127.0.0.1:5000/api/filter?province=Shefa&team=Team-A
```

## Response Format

### Success Response
```json
{
  "status": "success",
  "message": "Survey progress retrieved successfully",
  "data": {
    "total_surveys": 1200,
    "completed": 850,
    "in_progress": 250,
    "completion_rate": 70.83
  },
  "metadata": {
    "timestamp": "2025-11-12T10:30:00",
    "version": "1.0.0",
    "total_records": 4
  }
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Invalid or missing API key",
  "data": null
}
```

## Rate Limiting
Default rate limit: **100 requests per minute**

Configure in `.env`:
```bash
API_RATE_LIMIT=100
```

## Usage Examples

### Python
```python
import requests

# Without authentication
response = requests.get('http://127.0.0.1:5000/api/progress')
data = response.json()

# With API key
headers = {'X-API-Key': 'your-api-key'}
response = requests.get('http://127.0.0.1:5000/api/progress', headers=headers)
data = response.json()

# Access the actual data
progress_data = data['data']
print(f"Completed: {progress_data['completed']}")
```

### JavaScript (Fetch)
```javascript
// Without authentication
fetch('http://127.0.0.1:5000/api/progress')
  .then(response => response.json())
  .then(data => {
    console.log(data.data);  // Access the actual data
  });

// With API key
fetch('http://127.0.0.1:5000/api/progress', {
  headers: {
    'X-API-Key': 'your-api-key'
  }
})
  .then(response => response.json())
  .then(data => {
    console.log(data.data);
  });
```

### cURL
```bash
# Get progress
curl http://127.0.0.1:5000/api/progress

# Get progress with API key
curl -H "X-API-Key: your-api-key" http://127.0.0.1:5000/api/progress

# Filter by province
curl http://127.0.0.1:5000/api/filter?province=Shefa

# Get quality metrics
curl http://127.0.0.1:5000/api/quality
```

### jQuery
```javascript
$.ajax({
  url: 'http://127.0.0.1:5000/api/progress',
  headers: {
    'X-API-Key': 'your-api-key'
  },
  success: function(response) {
    console.log(response.data);
  }
});
```

## Integration with Joomla

### Using the Embed View
The easiest way to integrate with Joomla is using the embeddable view:

```html
<iframe 
  src="http://127.0.0.1:5000/embed" 
  width="100%" 
  height="800" 
  frameborder="0">
</iframe>
```

### Using the API in Joomla
Create a custom Joomla module or component:

```php
<?php
$api_url = 'http://127.0.0.1:5000/api/progress';
$api_key = 'your-api-key';

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $api_url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
    'X-API-Key: ' . $api_key
));

$response = curl_exec($ch);
curl_close($ch);

$data = json_decode($response, true);
$progress = $data['data'];

echo "Completed: " . $progress['completed'] . " surveys";
?>
```

## Security Best Practices

### Production Deployment
1. **Enable API Authentication:**
   ```bash
   API_KEY_REQUIRED=True
   API_KEY=generate-strong-random-key
   ```

2. **Restrict CORS Origins:**
   ```bash
   CORS_ORIGINS=https://yourdomain.com
   ```

3. **Use HTTPS:**
   - Deploy behind a reverse proxy (nginx, Apache)
   - Enable SSL/TLS certificates

4. **Set Strong Secret Key:**
   ```bash
   SECRET_KEY=generate-long-random-secret
   ```

5. **Environment Variables:**
   - Never commit `.env` to version control
   - Use environment-specific configurations

### Generate Secure API Key
```python
import secrets
api_key = secrets.token_urlsafe(32)
print(api_key)
```

## Monitoring & Logging

### View API Usage
Check Flask logs for API requests:
```
127.0.0.1 - - [12/Nov/2025 10:30:00] "GET /api/progress HTTP/1.1" 200 -
```

### Error Handling
The API returns appropriate HTTP status codes:
- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized (invalid API key)
- `404` - Not Found
- `500` - Internal Server Error

## Configuration Reference

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 5000 | Server port |
| `FLASK_ENV` | development | Environment mode |
| `SECRET_KEY` | dev-secret-key | Flask secret key |
| `API_KEY_REQUIRED` | False | Enable API authentication |
| `API_KEY` | - | API key for authentication |
| `API_RATE_LIMIT` | 100 | Requests per minute |
| `CORS_ORIGINS` | * | Allowed CORS origins |
| `SS_API_USER` | api_user | Survey Solutions API user |
| `SS_API_PASSWORD` | - | Survey Solutions password |

## Testing the API

### Test All Endpoints
```bash
# Documentation
curl http://127.0.0.1:5000/api/docs

# Progress
curl http://127.0.0.1:5000/api/progress

# Provinces
curl http://127.0.0.1:5000/api/provinces

# Quality
curl http://127.0.0.1:5000/api/quality

# Survey Solutions Sync
curl http://127.0.0.1:5000/api/survey-solutions-sync
```

### Test with Postman
1. Import the base URL: `http://127.0.0.1:5000/api/`
2. Set header: `X-API-Key: your-api-key`
3. Test each endpoint

## Support
For issues or questions, refer to:
- API Documentation: http://127.0.0.1:5000/api/docs
- Project Documentation: See README.md files
