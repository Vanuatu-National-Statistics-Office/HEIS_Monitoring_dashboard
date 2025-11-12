# Joomla Integration Guide

## Quick Start - IFrame Method

The easiest way to integrate the Vanuatu Survey Dashboard into your Joomla website is using an iframe.

### Step 1: Deploy the Flask Application

1. Upload the dashboard files to your server
2. Install dependencies and run the Flask app:
   ```bash
   cd /path/to/vanuatu-survey-dashboard
   pip install -r requirements.txt
   python app.py
   ```

### Step 2: Create a Joomla Menu Item

1. Log into Joomla Administrator
2. Go to **Menus → Main Menu → Add New Menu Item**
3. Set **Menu Title**: "Survey Dashboard"
4. Set **Menu Item Type**: Select "Single Article"

### Step 3: Create the Article with IFrame

1. Go to **Content → Articles → New Article**
2. Enter a title: "Household Survey Dashboard"
3. In the content editor, switch to **HTML mode**
4. Paste this code:

```html
<div class="survey-dashboard-container">
    <iframe 
        src="http://YOUR-SERVER-IP:5000/embed" 
        width="100%" 
        height="1400px" 
        frameborder="0"
        scrolling="auto"
        style="border: none; min-height: 1400px;">
        <p>Your browser does not support iframes. Please visit the 
        <a href="http://YOUR-SERVER-IP:5000/dashboard">dashboard directly</a>.</p>
    </iframe>
</div>

<style>
.survey-dashboard-container {
    margin: 0;
    padding: 0;
    width: 100%;
}
</style>
```

5. Replace `YOUR-SERVER-IP` with your actual server address
6. Save the article

### Step 4: Assign to Menu

1. Go back to your menu item from Step 2
2. Select the article you just created
3. Save and close

## Advanced Integration Methods

### Method 1: Custom Joomla Module

Create a custom module for better integration:

1. **Create module folder**: `/modules/mod_vanuatu_survey/`

2. **Create mod_vanuatu_survey.xml**:
```xml
<?xml version="1.0" encoding="utf-8"?>
<extension type="module" version="4.0" client="site" method="upgrade">
    <name>Vanuatu Survey Dashboard</name>
    <author>Your Name</author>
    <version>1.0.0</version>
    <description>Displays household income and expenditure survey data</description>
    <files>
        <filename module="mod_vanuatu_survey">mod_vanuatu_survey.php</filename>
        <folder>tmpl</folder>
    </files>
    <config>
        <fields name="params">
            <fieldset name="basic">
                <field
                    name="api_url"
                    type="text"
                    label="API Base URL"
                    description="Base URL for the Flask API"
                    default="http://localhost:5000"
                />
                <field
                    name="display_mode"
                    type="list"
                    label="Display Mode"
                    default="embed">
                    <option value="embed">Embed</option>
                    <option value="summary">Summary Only</option>
                    <option value="charts">Charts Only</option>
                </field>
            </fieldset>
        </fields>
    </config>
</extension>
```

3. **Create mod_vanuatu_survey.php**:
```php
<?php
defined('_JEXEC') or die;

use Joomla\CMS\Helper\ModuleHelper;

// Get module parameters
$apiUrl = $params->get('api_url', 'http://localhost:5000');
$displayMode = $params->get('display_mode', 'embed');

// Load the template
require ModuleHelper::getLayoutPath('mod_vanuatu_survey', $displayMode);
```

4. **Create tmpl/embed.php**:
```php
<?php
defined('_JEXEC') or die;
?>
<div class="vanuatu-survey-module">
    <iframe 
        src="<?php echo $apiUrl; ?>/embed" 
        width="100%" 
        height="1200px" 
        frameborder="0"
        style="border: none;">
    </iframe>
</div>
```

5. **Create tmpl/summary.php**:
```php
<?php
defined('_JEXEC') or die;

// Fetch data from API
$summaryData = @file_get_contents($apiUrl . '/api/summary');
$data = json_decode($summaryData, true);

if ($data) {
?>
<div class="survey-summary">
    <h3>Survey Statistics</h3>
    <div class="row">
        <div class="col-md-3">
            <div class="stat-box">
                <div class="stat-value"><?php echo number_format($data['total_households']); ?></div>
                <div class="stat-label">Total Households</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stat-box">
                <div class="stat-value"><?php echo number_format($data['avg_income']); ?> VUV</div>
                <div class="stat-label">Average Income</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stat-box">
                <div class="stat-value"><?php echo number_format($data['avg_expenditure']); ?> VUV</div>
                <div class="stat-label">Average Expenditure</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stat-box">
                <div class="stat-value"><?php echo number_format($data['avg_savings']); ?> VUV</div>
                <div class="stat-label">Average Savings</div>
            </div>
        </div>
    </div>
    <p class="text-center mt-3">
        <a href="<?php echo $apiUrl; ?>/dashboard" target="_blank" class="btn btn-primary">
            View Full Dashboard
        </a>
    </p>
</div>

<style>
.survey-summary {
    padding: 20px;
    background: #f9f9f9;
    border-radius: 8px;
}
.stat-box {
    background: white;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
    margin-bottom: 15px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.stat-value {
    font-size: 1.8em;
    font-weight: bold;
    color: #2E86AB;
}
.stat-label {
    color: #666;
    font-size: 0.9em;
    margin-top: 5px;
}
</style>
<?php
} else {
    echo '<p class="alert alert-warning">Unable to load survey data. Please try again later.</p>';
}
?>
```

6. **Install the module**:
   - Zip the `mod_vanuatu_survey` folder
   - Go to Joomla Admin → Extensions → Install
   - Upload and install the zip file
   - Go to Extensions → Modules
   - Find and enable "Vanuatu Survey Dashboard"

### Method 2: RESTful Integration with JavaScript

For more dynamic integration, use JavaScript to fetch and display data:

**Create a Custom HTML module in Joomla**:

```html
<div id="vanuatu-dashboard"></div>

<script>
const API_BASE = 'http://YOUR-SERVER:5000/api';

async function loadSurveyData() {
    try {
        const response = await fetch(`${API_BASE}/summary`);
        const data = await response.json();
        
        const html = `
            <div class="survey-stats">
                <h3>Vanuatu Household Survey - Key Metrics</h3>
                <div class="row">
                    <div class="col-md-3">
                        <div class="metric">
                            <span class="value">${data.total_households.toLocaleString()}</span>
                            <span class="label">Households</span>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="metric">
                            <span class="value">${Math.round(data.avg_income).toLocaleString()} VUV</span>
                            <span class="label">Avg Income</span>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="metric">
                            <span class="value">${Math.round(data.avg_expenditure).toLocaleString()} VUV</span>
                            <span class="label">Avg Expenditure</span>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="metric">
                            <span class="value">${Math.round(data.avg_savings).toLocaleString()} VUV</span>
                            <span class="label">Avg Savings</span>
                        </div>
                    </div>
                </div>
                <div class="text-center mt-3">
                    <a href="${API_BASE.replace('/api', '/dashboard')}" target="_blank" class="btn btn-primary">
                        View Full Dashboard
                    </a>
                </div>
            </div>
        `;
        
        document.getElementById('vanuatu-dashboard').innerHTML = html;
        
    } catch (error) {
        console.error('Error loading survey data:', error);
        document.getElementById('vanuatu-dashboard').innerHTML = 
            '<p class="alert alert-danger">Failed to load survey data.</p>';
    }
}

// Load data on page load
document.addEventListener('DOMContentLoaded', loadSurveyData);
</script>

<style>
.survey-stats {
    background: #f5f7fa;
    padding: 30px;
    border-radius: 10px;
    margin: 20px 0;
}
.metric {
    background: white;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}
.metric .value {
    display: block;
    font-size: 2em;
    font-weight: bold;
    color: #2E86AB;
    margin-bottom: 10px;
}
.metric .label {
    display: block;
    color: #666;
    font-size: 0.9em;
}
</style>
```

## Production Deployment

### Using Apache Reverse Proxy

1. **Enable Apache modules**:
```bash
a2enmod proxy
a2enmod proxy_http
systemctl restart apache2
```

2. **Add to your Joomla VirtualHost**:
```apache
<VirtualHost *:80>
    ServerName yoursite.com
    
    # Joomla
    DocumentRoot /var/www/html/joomla
    
    # Survey Dashboard Proxy
    ProxyPreserveHost On
    ProxyPass /survey http://127.0.0.1:5000
    ProxyPassReverse /survey http://127.0.0.1:5000
    
    # Rest of your configuration...
</VirtualHost>
```

3. **Update iframe URL** in Joomla to use `/survey/embed`

### Using Nginx Reverse Proxy

Add to your Nginx configuration:

```nginx
server {
    listen 80;
    server_name yoursite.com;
    
    # Joomla
    root /var/www/html/joomla;
    
    # Survey Dashboard Proxy
    location /survey {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Rest of your configuration...
}
```

## Security Considerations

1. **CORS Configuration**: If API and Joomla are on different domains, add CORS headers to Flask:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://yourjoomlasite.com"}})
```

2. **Authentication**: Add authentication if dashboard contains sensitive data:

```python
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    # Implement your authentication logic
    return username == 'admin' and password == 'secure_password'

@app.route('/dashboard')
@auth.login_required
def dashboard():
    # Your code...
```

3. **SSL/HTTPS**: Always use HTTPS in production
4. **Firewall**: Restrict Flask port access to localhost if using reverse proxy

## Troubleshooting

### IFrame Content Not Showing
- Check browser console for errors
- Verify Flask app is running: `curl http://localhost:5000/embed`
- Check if Joomla has Content Security Policy restrictions
- Try adding to Joomla's `.htaccess`:
  ```
  Header set X-Frame-Options "SAMEORIGIN"
  ```

### CORS Errors
Install flask-cors:
```bash
pip install flask-cors
```

Add to app.py:
```python
from flask_cors import CORS
CORS(app)
```

### Data Not Loading
- Verify API endpoint is accessible
- Check network tab in browser developer tools
- Ensure JSON is valid: `curl http://localhost:5000/api/summary`

## Support

For Joomla-specific questions:
- Joomla Forums: https://forum.joomla.org/
- Joomla Documentation: https://docs.joomla.org/

For Flask integration questions:
- Flask Documentation: https://flask.palletsprojects.com/
