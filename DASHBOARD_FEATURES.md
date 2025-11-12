# Vanuatu HIES Survey Progress Monitoring Dashboard
## Comprehensive Field Monitoring System

### 📋 **Dashboard Features**

## **🗂️ Basic Identification Fields**
All surveys capture the following identification information:
- **Province**: One of 6 provinces (Malampa, Penama, Sanma, Shefa, Tafea, Torba)
- **Island**: Specific island within the province
- **Area Council / Enumeration Area (EA)**: Administrative subdivision
- **Village / Community Name**: 15+ villages tracked
- **Household ID / Listing Number**: Unique identifier (format: HH-XXXXXX)
- **Enumerator Name / ID**: 24 trained field staff (INT-001 to INT-024)
- **Supervisor Name / ID**: 6 supervisors (SUP-001 to SUP-006), one per team
- **Date of Interview / Visit**: Timestamp of data collection

## **📊 Progress Tracking Metrics**
Each Enumeration Area (EA) tracks:
- **Total Households in EA**: Target number of households to survey
- **Households Completed**: Successfully finished interviews
- **Households Refused**: Households that declined participation
- **Households Not Found / Absent**: Households unavailable during visits
- **Partially Completed Interviews**: In-progress surveys
- **Remaining Households**: Outstanding surveys needed
- **Completion Rate (%)**: Auto-calculated percentage complete

## **🕐 Timing and Duration**
Time-based metrics include:
- **Start Date of Enumeration in EA**: When fieldwork began
- **Expected End Date**: Target completion date
- **Actual End Date**: When EA survey completed
- **Average Interview Duration (minutes)**: 30-120 minutes per household
- **Enumerator Daily Progress (HH per day)**: 3-8 households per day average

## **📋 Data Quality Checks**
Quality assurance metrics:
- **Number of Incomplete Forms**: Forms missing required data
- **Number of Rejected / Corrected Forms**: Forms sent back for correction
- **Supervisor Review Status**: 
  - Pending: Awaiting supervisor review
  - Approved: Validated by supervisor
  - Sent Back: Requires corrections
- **GPS Coordinates Captured?**: Yes/No flag for location data
- **Photo / Document Evidence Attached?**: Yes/No flag for supporting documentation
- **Quality Score**: 0-100 rating based on completeness and accuracy

## **🧭 Logistics and Field Issues**
Field conditions tracking:
- **Transport Availability**: Good / Poor / None
- **Network Coverage**: Good / Poor / None  
- **Tablet / Device Status**: OK / Faulty / Replaced
- **Power Supply Situation**: Good / Poor
- **Comments / Field Notes**: Free text for enumerator/supervisor remarks

---

## **📈 Dashboard-Level Indicators**

### **Main Dashboard** (`/dashboard`)
- Overall progress gauge (completed vs target 5,000 surveys)
- Daily progress line chart (trend over time)
- Survey status distribution (pie chart)
- Province progress (stacked bar chart)
- Team performance comparison
- Top interviewer leaderboard (top 15 performers)
- Island geographic heatmap
- Quality score trends
- Time efficiency by team

### **Advanced Analytics Dashboard** (`/analytics`)
- **Data Quality Metrics**:
  - Average quality score gauge
  - GPS capture rate (%)
  - Photo attachment rate (%)
  - Error rate by team
  - Incomplete/rejected forms count
  - Supervisor review status

- **Logistics & Field Conditions**:
  - Transport availability status
  - Network coverage analysis
  - Device status tracking
  - Power supply conditions
  - Stacked bar visualization

- **Household Status Breakdown**:
  - Total households targeted
  - Completed vs Refused vs Not Found
  - Remaining households pie chart

- **EA Completion by Province**:
  - % of EAs fully completed per province
  - Bar chart comparison

- **Supervisor Review Summary**:
  - Reviews by supervisor
  - Approval vs rejection rates
  - Quality scores by supervisor

- **Data Error Rate by Team**:
  - Percentage of forms with errors
  - Team-by-team comparison

- **Daily Progress per Enumerator**:
  - Average households per day
  - Top 15 performers ranked

- **EA Progress Details Table**:
  - Searchable/sortable table with all EAs
  - Province, Area Council, EA breakdown
  - Total/Completed/Refused/Not Found/Remaining counts
  - Color-coded completion rate badges

---

## **🌐 API Endpoints**

Access real-time data programmatically:

| Endpoint | Description |
|----------|-------------|
| `/api/progress` | Overall survey progress statistics |
| `/api/quality` | Data quality metrics |
| `/api/logistics` | Field logistics status |
| `/api/ea-stats` | Enumeration area statistics |
| `/api/supervisors` | Supervisor review summary |
| `/api/interviewer-detailed` | Detailed interviewer performance |
| `/api/province-ea-completion` | EA completion rates by province |
| `/api/provinces` | Province-level breakdown |
| `/api/teams` | Team statistics |
| `/api/interviewers` | Interviewer performance data |
| `/api/daily` | Daily progress trends |
| `/api/filter` | Filtered data (by province/island/team/interviewer) |

---

## **🎯 Key Performance Indicators (KPIs)**

### **Progress KPIs**
- **Target Surveys**: 5,000 households
- **Current Progress**: Real-time count
- **Completion Rate**: % toward target
- **Daily Average**: Surveys conducted per day
- **Projected Completion**: Based on current rate

### **Quality KPIs**
- **Average Quality Score**: 70-100 scale
- **GPS Capture Rate**: % of surveys with location data
- **Photo Attachment Rate**: % with supporting evidence
- **Error Rate**: % of forms with issues
- **Approval Rate**: % approved on first submission

### **Efficiency KPIs**
- **Average Interview Duration**: Time per household
- **Daily Progress per Enumerator**: HH/day
- **Team Performance**: Comparative rankings
- **EA Completion Rate**: % of areas finished

### **Logistics KPIs**
- **Transport Availability**: % with good access
- **Network Coverage**: % with connectivity
- **Device Functionality**: % operational equipment
- **Power Supply**: % with reliable power

---

## **🔗 Integration for Joomla Website**

### **Embed Options**
1. **Full Dashboard Embed**: 
   - URL: `http://your-domain:5000/embed`
   - Use iframe integration
   
2. **API Integration**:
   - Pull data via REST API endpoints
   - Build custom Joomla components
   - Real-time data updates (auto-refresh every 5 minutes)

### **Sample Joomla IFrame Code**
```html
<iframe 
  src="http://your-domain:5000/embed" 
  width="100%" 
  height="1200px" 
  frameborder="0"
  style="border: none;">
</iframe>
```

---

## **📊 Data Generation**
- Sample data includes 1,200+ survey records
- 24 interviewers across 6 teams
- 6 provinces with multiple islands
- 50+ enumeration areas
- Realistic timing, quality, and logistics data
- Date range: October 2025 - November 2025

---

## **🚀 Running the Dashboard**

### **Start Server**
```powershell
cd C:\vanuatu-survey-dashboard
python app.py
```

### **Access Points**
- Homepage: `http://localhost:5000/`
- Main Dashboard: `http://localhost:5000/dashboard`
- Advanced Analytics: `http://localhost:5000/analytics`
- Embeddable Version: `http://localhost:5000/embed`

---

## **📝 Future Enhancements**
- Connect to real database (PostgreSQL/MySQL)
- User authentication and role-based access
- Export to Excel/PDF reports
- SMS/email alerts for supervisors
- Mobile-responsive data entry forms
- Offline data collection with sync
- Map visualization of survey locations
- Time-series forecasting for completion dates

---

**Dashboard Version**: 2.0 (Enhanced with Comprehensive Field Monitoring)  
**Last Updated**: November 12, 2025  
**Maintained by**: Vanuatu National Statistics Office
