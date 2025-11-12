# Quick Start Guide

## Running the Dashboard

1. **Open PowerShell and navigate to the project directory**:
   ```powershell
   cd C:\vanuatu-survey-dashboard
   ```

2. **Create and activate virtual environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Copy and configure environment file**:
   ```powershell
   Copy-Item .env.example .env
   ```

5. **Run the application**:
   ```powershell
   python app.py
   ```

6. **Open in browser**:
   - Main page: http://localhost:5000
   - Dashboard: http://localhost:5000/dashboard
   - Embed view: http://localhost:5000/embed

## Embedding in Joomla

**Simple IFrame Method:**

1. In Joomla, create a new article
2. Switch to HTML mode
3. Paste this code:
   ```html
   <iframe src="http://YOUR-SERVER:5000/embed" 
           width="100%" 
           height="1400px" 
           frameborder="0">
   </iframe>
   ```
4. Replace `YOUR-SERVER` with your actual server address
5. Save and publish

## Key Files

- `app.py` - Main Flask application
- `config.py` - Configuration settings
- `data_models.py` - Data generation and analytics
- `visualizations.py` - Chart generation
- `templates/` - HTML templates
- `README.md` - Full documentation
- `JOOMLA_INTEGRATION.md` - Detailed Joomla integration guide

## Next Steps

1. Replace sample data with your actual survey data
2. Customize provinces in `config.py`
3. Adjust visualizations in `visualizations.py`
4. Deploy to production server
5. Integrate with Joomla following JOOMLA_INTEGRATION.md

## Support

Check README.md for troubleshooting and detailed configuration options.
