# Vanuatu Household Income & Expenditure Survey Dashboard

A comprehensive Python-based dashboard for monitoring and analyzing household income and expenditure survey data in Vanuatu.

## Features

- 📊 **Interactive Visualizations**: Built with Plotly for dynamic, responsive charts
- 🌍 **Provincial Analysis**: Compare data across all 6 provinces of Vanuatu
- 💰 **Income & Expenditure Tracking**: Monitor household financial patterns
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices
- 🔌 **REST API**: Programmatic access to survey data
- 🎨 **Embeddable Widget**: Easy integration into Joomla websites

## Dashboard Components

### Key Metrics
- Total households surveyed
- Average monthly income
- Average monthly expenditure
- Average savings
- Household size statistics

### Visualizations
1. **Income vs Expenditure Scatter Plot**: Compare household income against expenditure
2. **Provincial Comparison**: Bar charts showing averages across provinces
3. **Expenditure Breakdown**: Pie chart of spending categories
4. **Income Sources**: Bar chart of income source distribution
5. **Income Distribution**: Histogram of household income brackets
6. **Savings Rate Analysis**: Savings rates by income bracket

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or extract the project**
   ```powershell
   cd C:\vanuatu-survey-dashboard
   ```

2. **Create a virtual environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```powershell
   Copy-Item .env.example .env
   ```
   Edit `.env` file and set your configuration:
   - `SECRET_KEY`: Your Flask secret key
   - `PORT`: Port number (default: 5000)
   - `FLASK_ENV`: development or production

5. **Run the application**
   ```powershell
   python app.py
   ```

6. **Access the dashboard**
   - Main page: http://localhost:5000/
   - Full dashboard: http://localhost:5000/dashboard
   - Embed page: http://localhost:5000/embed

## API Endpoints

The dashboard provides RESTful API endpoints for data access:

### GET /api/summary
Returns summary statistics
```json
{
  "total_households": 500,
  "avg_household_size": 4.8,
  "avg_income": 123456.78,
  "median_income": 98765.43,
  "avg_expenditure": 109876.54,
  "median_expenditure": 87654.32,
  "avg_savings": 13580.24,
  "provinces_covered": 6
}
```

### GET /api/provinces
Returns statistics grouped by province

### GET /api/expenditure
Returns expenditure breakdown by category

### GET /api/income-sources
Returns income aggregated by source

### GET /api/filter?province=Shefa&urban_rural=Urban
Returns filtered statistics based on query parameters

## Integrating into Joomla

There are multiple ways to integrate this dashboard into your Joomla website:

### Method 1: IFrame Embed (Recommended for Quick Integration)

1. **Keep the Flask app running** on your server
   ```powershell
   python app.py
   ```

2. **In Joomla, create a new article or custom HTML module**

3. **Add the following HTML code**:
   ```html
   <iframe src="http://your-server:5000/embed" 
           width="100%" 
           height="1200px" 
           frameborder="0"
           style="border: none;">
   </iframe>
   ```

4. **Adjust the height** as needed to fit your content

### Method 2: Joomla Custom Component (Advanced)

1. **Deploy Flask as a REST API backend**
   - Run Flask on a separate port or subdomain
   - Use gunicorn for production deployment
   
2. **Create Joomla component** that:
   - Fetches data from Flask API endpoints
   - Renders visualizations using JavaScript libraries
   - Displays in Joomla template

3. **Example Joomla PHP code**:
   ```php
   <?php
   // Fetch data from Flask API
   $apiUrl = 'http://your-server:5000/api/summary';
   $data = json_decode(file_get_contents($apiUrl), true);
   
   // Display in Joomla
   echo '<div class="survey-stats">';
   echo '<h3>Survey Statistics</h3>';
   echo '<p>Total Households: ' . $data['total_households'] . '</p>';
   echo '<p>Average Income: ' . number_format($data['avg_income']) . ' VUV</p>';
   echo '</div>';
   ?>
   ```

### Method 3: Reverse Proxy (Production Deployment)

1. **Configure Apache/Nginx** to proxy requests to Flask

2. **Apache example** (.htaccess or VirtualHost):
   ```apache
   ProxyPass /survey http://localhost:5000
   ProxyPassReverse /survey http://localhost:5000
   ```

3. **Nginx example**:
   ```nginx
   location /survey {
       proxy_pass http://localhost:5000;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
   }
   ```

4. **Access in Joomla** via relative path: `/survey/embed`

## Production Deployment

### Using Gunicorn (Recommended)

1. **Install Gunicorn** (already in requirements.txt)

2. **Run with Gunicorn**:
   ```powershell
   gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
   ```

3. **Create Windows Service** (using NSSM):
   ```powershell
   nssm install VanuatuSurveyDashboard "C:\path\to\venv\Scripts\gunicorn.exe" "--bind 0.0.0.0:5000 --workers 4 app:app"
   nssm set VanuatuSurveyDashboard AppDirectory "C:\vanuatu-survey-dashboard"
   nssm start VanuatuSurveyDashboard
   ```

### Security Considerations

1. **Change SECRET_KEY** in production
2. **Set FLASK_ENV=production** in .env
3. **Use HTTPS** for production deployment
4. **Implement authentication** if needed
5. **Configure CORS** if accessing from different domain:
   ```python
   from flask_cors import CORS
   CORS(app)
   ```

## Customization

### Adding Real Data

Replace the sample data generator in `app.py`:

```python
# Instead of:
survey_data = SurveyDataGenerator.generate_sample_data(num_households=500)

# Load from database or CSV:
import pandas as pd
survey_data = pd.read_csv('your_survey_data.csv')
```

### Modifying Provinces

Edit `config.py` to match your specific regions:

```python
PROVINCES = [
    'Your Province 1',
    'Your Province 2',
    # ... add all provinces
]
```

### Customizing Colors

Modify the color scheme in `visualizations.py`:

```python
COLORS = {
    'primary': '#YOUR_COLOR',
    'secondary': '#YOUR_COLOR',
    # ... more colors
}
```

## Data Structure

The survey data should have the following structure:

```python
{
    'household_id': str,          # Unique identifier
    'province': str,              # Province name
    'household_size': int,        # Number of people
    'survey_date': datetime,      # Survey date
    'total_income': float,        # Monthly income in VUV
    'total_expenditure': float,   # Monthly expenditure in VUV
    'savings': float,             # Monthly savings in VUV
    'income_sources': dict,       # {source: amount}
    'expenditure_breakdown': dict, # {category: amount}
    'urban_rural': str            # 'Urban' or 'Rural'
}
```

## Troubleshooting

### Port Already in Use
```powershell
# Find process using port 5000
netstat -ano | findstr :5000
# Kill the process
taskkill /PID <process_id> /F
```

### Import Errors
```powershell
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1
# Reinstall dependencies
pip install -r requirements.txt
```

### IFrame Not Loading in Joomla
- Check if your server allows iframe embedding
- Verify Flask app is running and accessible
- Check browser console for errors
- Add CORS headers if needed

## Support

For issues or questions:
- Check the Flask documentation: https://flask.palletsprojects.com/
- Plotly documentation: https://plotly.com/python/
- Joomla documentation: https://docs.joomla.org/

## License

This project is provided as-is for use by Vanuatu National Statistics Office.

## Contributing

To add new features:
1. Add routes in `app.py`
2. Add analytics in `data_models.py`
3. Add visualizations in `visualizations.py`
4. Create templates in `templates/`

## Version History

- **v1.0.0** (2025-11-12): Initial release
  - Basic dashboard functionality
  - 6 visualization types
  - REST API endpoints
  - Joomla embed support
