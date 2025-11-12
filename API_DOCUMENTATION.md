# API Documentation
## Vanuatu HIES Survey Progress Monitoring API

Base URL: `http://localhost:5000` (or your deployed domain)

---

## **Endpoints**

### **1. Overall Progress**
```
GET /api/progress
```

**Response:**
```json
{
  "total_surveys": 1200,
  "target_surveys": 5000,
  "completed": 985,
  "in_progress": 156,
  "pending_review": 59,
  "completion_rate": 19.7,
  "avg_quality_score": 85.3,
  "daily_average": 27.9
}
```

---

### **2. Data Quality Metrics**
```
GET /api/quality
```

**Response:**
```json
{
  "total_incomplete_forms": 42,
  "total_rejected_forms": 18,
  "forms_pending_review": 59,
  "forms_approved": 985,
  "forms_sent_back": 23,
  "gps_capture_rate": 87.5,
  "photo_attach_rate": 72.3,
  "avg_quality_score": 85.3,
  "error_rate": 5.0
}
```

---

### **3. Logistics Status**
```
GET /api/logistics
```

**Response:**
```json
{
  "transport_good": 850,
  "transport_poor": 280,
  "transport_none": 70,
  "network_good": 720,
  "network_poor": 380,
  "network_none": 100,
  "devices_ok": 1050,
  "devices_faulty": 120,
  "devices_replaced": 30,
  "power_good": 900,
  "power_poor": 300
}
```

---

### **4. EA Statistics**
```
GET /api/ea-stats
```

**Response:** Array of enumeration area objects
```json
[
  {
    "enumeration_area": "EA-001",
    "ea_total_households": 85,
    "ea_completed": 72,
    "ea_refused": 3,
    "ea_not_found": 2,
    "ea_remaining": 8,
    "completion_rate_ea": 84.7,
    "province": "Shefa",
    "area_council": "Port Vila"
  },
  ...
]
```

---

### **5. Supervisor Review Summary**
```
GET /api/supervisors
```

**Response:** Object with team/supervisor data
```json
{
  "Team A": {
    "supervisor_name": "Wilson Tari",
    "total_reviews": 198,
    "approved": 175,
    "total_rejected": 8,
    "quality_score": 86.5
  },
  ...
}
```

---

### **6. Detailed Interviewer Performance**
```
GET /api/interviewer-detailed
```

**Response:** Object with interviewer performance metrics
```json
{
  "INT-001": {
    "interviewer_name": "John Tari",
    "team": "Team A",
    "total_surveys": 58,
    "completed_surveys": 52,
    "avg_duration": 67.3,
    "avg_daily_progress": 5.8,
    "avg_quality": 88.2,
    "incomplete_forms": 2,
    "rejected_forms": 1,
    "gps_capture_rate": 93.1
  },
  ...
}
```

---

### **7. Province EA Completion Rate**
```
GET /api/province-ea-completion
```

**Response:** Object with province-level EA completion
```json
{
  "Shefa": {
    "total_eas": 12,
    "completed_eas": 8,
    "ea_completion_percentage": 66.7
  },
  ...
}
```

---

### **8. Province Statistics**
```
GET /api/provinces
```

**Response:** Object with province breakdown
```json
{
  "Malampa": {
    "total_surveys": 187,
    "completed_surveys": 152,
    "quality_score": 84.5,
    "time_taken_minutes": 72.3
  },
  ...
}
```

---

### **9. Team Statistics**
```
GET /api/teams
```

**Response:** Object with team performance
```json
{
  "Team A": {
    "total_surveys": 215,
    "completed_surveys": 189,
    "quality_score": 86.2,
    "time_taken_minutes": 68.5
  },
  ...
}
```

---

### **10. Interviewer Statistics**
```
GET /api/interviewers
```

**Response:** Object with interviewer data
```json
{
  "INT-001": {
    "interviewer_name": "John Tari",
    "team": "Team A",
    "total_surveys": 58,
    "completed_surveys": 52,
    "quality_score": 88.2,
    "time_taken_minutes": 67.3
  },
  ...
}
```

---

### **11. Daily Progress**
```
GET /api/daily
```

**Response:** Object with daily survey counts
```json
{
  "2025-10-01": {
    "total": 15,
    "completed": 12
  },
  "2025-10-02": {
    "total": 23,
    "completed": 19
  },
  ...
}
```

---

### **12. Filtered Data**
```
GET /api/filter?province=Shefa&team=Team A
```

**Query Parameters:**
- `province`: Filter by province name
- `island`: Filter by island name
- `team`: Filter by team name
- `interviewer`: Filter by interviewer ID

**Response:** Same as `/api/progress` but filtered

---

## **Authentication**
Currently: **No authentication required** (development mode)

For production deployment, implement:
- API key authentication
- OAuth2 / JWT tokens
- Rate limiting
- CORS configuration

---

## **Rate Limits**
Currently: **No rate limits** (development mode)

Recommended production limits:
- 100 requests per minute per IP
- 1000 requests per hour per API key

---

## **Error Codes**

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid parameters) |
| 404 | Not Found (invalid endpoint) |
| 500 | Internal Server Error |

**Error Response Format:**
```json
{
  "error": "Error message description",
  "code": 400
}
```

---

## **Sample cURL Requests**

### Get Overall Progress
```bash
curl http://localhost:5000/api/progress
```

### Get Quality Metrics
```bash
curl http://localhost:5000/api/quality
```

### Get Filtered Data
```bash
curl "http://localhost:5000/api/filter?province=Shefa&team=Team%20A"
```

---

## **Sample JavaScript Fetch**

```javascript
// Get overall progress
fetch('http://localhost:5000/api/progress')
  .then(response => response.json())
  .then(data => {
    console.log('Total Surveys:', data.total_surveys);
    console.log('Completion Rate:', data.completion_rate + '%');
  })
  .catch(error => console.error('Error:', error));

// Get data quality metrics
fetch('http://localhost:5000/api/quality')
  .then(response => response.json())
  .then(data => {
    console.log('Quality Score:', data.avg_quality_score);
    console.log('GPS Capture Rate:', data.gps_capture_rate + '%');
  });
```

---

## **Sample Python Request**

```python
import requests

# Get overall progress
response = requests.get('http://localhost:5000/api/progress')
data = response.json()

print(f"Total Surveys: {data['total_surveys']}")
print(f"Completion Rate: {data['completion_rate']}%")

# Get quality metrics
response = requests.get('http://localhost:5000/api/quality')
quality = response.json()

print(f"Quality Score: {quality['avg_quality_score']}")
print(f"Error Rate: {quality['error_rate']}%")
```

---

## **Webhook Support** (Future Feature)
Configure webhooks to receive notifications:
- When EA reaches 100% completion
- When quality score drops below threshold
- When device faults reported
- Daily progress summaries

---

## **Data Update Frequency**
- Real-time updates (reflects current data)
- Auto-refresh: Every 5 minutes (recommended)
- Database sync: As data is collected

---

## **Contact**
For API support and integration assistance:
- Email: support@vnso.gov.vu
- Website: https://vnso.gov.vu
- Dashboard Admin: dashboard@vnso.gov.vu

---

**API Version**: 2.0  
**Last Updated**: November 12, 2025
