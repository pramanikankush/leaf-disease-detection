# 🌿 Plant Health Analyzer

AI-powered plant disease detection using Google Gemini Vision API.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- Google Gemini API Key (free)

### 2. Installation

```bash
# Clone or navigate to project directory
cd Plant-Health-Analyzer

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Key

#### Option A: Environment Variable (Recommended)

**Windows PowerShell:**
```powershell
$env:GEMINI_API_KEY = "your_api_key_here"
streamlit run app.py
```

**Windows Command Prompt:**
```cmd
set GEMINI_API_KEY=your_api_key_here
streamlit run app.py
```

**Linux/Mac:**
```bash
export GEMINI_API_KEY="your_api_key_here"
streamlit run app.py
```

#### Option B: .env File

1. Copy `.env.example` to `.env`
2. Update with your API key
3. Run: `streamlit run app.py`

#### Option C: Direct Config Update (Development)

Edit `utils/config.py` and set:
```python
DEFAULT_GEMINI_KEY = "your_api_key_here"
```

### 4. Get Your API Key

1. Visit: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy and paste in configuration above

### 5. Run Application

```bash
streamlit run app.py
```

App opens at: `http://localhost:8501`

---

## 📋 Features

### Main Analysis
- **🔬 Real-time Leaf Analysis** - Upload or capture leaf photos
- **📸 Instant Diagnosis** - AI-powered disease detection
- **💬 Follow-up Questions** - Ask specific questions about results
- **🌐 Multi-Language Support** - Results in Hindi, Marathi, Spanish, French

### Tools & Guides
- **🌱 Prevention Tips** - Disease-specific prevention strategies
- **🔄 Compare Diseases** - Side-by-side disease comparison
- **📊 Disease Timeline** - Track severity progression over time
- **🌤️ Weather Guide** - Optimal treatment timing based on weather
- **📚 Disease Library** - Offline reference database

### Record Keeping
- **🕒 Scan History** - View all past diagnoses
- **📥 PDF Reports** - Download professional reports
- **📰 Latest News** - Agricultural news updates
- **📅 Treatment Planner** - Day-by-day treatment schedules

### Admin
- **⚙️ Settings** - API configuration and diagnostics

---

## 📁 Project Structure

```
Plant-Health-Analyzer/
├── app.py                          # Main Streamlit app
├── requirements.txt                # Dependencies
├── .env.example                    # Example environment config
│
├── services/
│   ├── __init__.py
│   └── gemini_service.py           # Google Gemini API integration
│
├── utils/
│   ├── __init__.py
│   ├── config.py                   # Centralized API key management
│   ├── history_manager.py          # Scan history storage
│   ├── disease_library.py          # Offline disease database
│   ├── weather_service.py          # Weather forecast & analysis
│   ├── parser.py                   # JSON response parsing
│   └── pdf_generator.py            # PDF report generation
│
├── pages/                          # Streamlit multi-page app
│   ├── 1_📰_Crop_News.py
│   ├── 2_🕒_History.py
│   ├── 3_📅_Treatment_Planner.py
│   ├── 4_🌱_Prevention_Tips.py
│   ├── 5_🔄_Compare_Diseases.py
│   ├── 6_📊_Disease_Timeline.py
│   ├── 7_🌤️_Weather_Guide.py
│   ├── 8_📚_Disease_Library.py
│   └── 9_⚙️_Settings.py
│
└── data/                           # User data (history, reports)
    └── history.json                # Scan history archive
```

---

## 🔒 Security

### API Key Safety

1. **Never commit API keys** to version control
2. **Use environment variables** for production
3. **Rotate keys regularly** in Google AI Studio
4. **Monitor API usage** in Google Cloud Console

### Data Privacy

- Scan history stored locally in `data/history.json`
- No data sent to external services except Google Gemini
- Weather data from free public API (Open-Meteo)
- News feeds from public RSS sources

---

## 🐛 Troubleshooting

### API Key Issues

```
Error: "API key too short or empty"
→ Check environment variable is set correctly
→ Verify entire key was copied

Error: "Could not analyze leaf - API Error"
→ Check internet connection
→ Verify API key is active in Google AI Studio
→ Check API quota/usage limits
```

### Windows Environment Variable

```powershell
# Set variable
$env:GEMINI_API_KEY = "your_key"

# Verify it's set
echo $env:GEMINI_API_KEY

# For permanent (all sessions)
[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', 'your_key', 'User')
# Then restart PowerShell
```

### Streamlit Issues

```bash
# Clear cache
streamlit cache clear

# Verbose output
streamlit run app.py --logger.level=debug

# Force restart
streamlit run app.py --client.showErrorDetails=true
```

---

## 📚 Usage Examples

### Basic Workflow

1. **Upload Leaf Photo** → Main page
2. **View Diagnosis** → Disease name, confidence, symptoms
3. **Check Prevention** → 4_🌱_Prevention_Tips page
4. **Plan Treatment** → 3_📅_Treatment_Planner page
5. **Track Progress** → 6_📊_Disease_Timeline page
6. **Check Weather** → 7_🌤️_Weather_Guide for treatment timing

### Compare Similar Diseases

1. Go to **5_🔄_Compare_Diseases**
2. Select 2-3 diseases to compare
3. View side-by-side prevention/treatment strategies
4. Identify key differences

### Historical Analysis

1. Go to **2_🕒_History**
2. Browse past diagnoses
3. Generate PDF reports
4. Check **6_📊_Disease_Timeline** for progression tracking

---

## 🤝 Contributing

Found a bug? Have a feature idea?
- Check existing pages for similar functionality
- Test changes before committing
- Update documentation

---

## 📄 License

This project uses Google Gemini API and is subject to Google's terms of service.

---

## ✅ Verification Checklist

Before first use:

- [ ] Python 3.8+ installed
- [ ] `pip install -r requirements.txt` completed
- [ ] API key obtained from Google AI Studio
- [ ] Environment variable or config file set
- [ ] `streamlit run app.py` runs without errors
- [ ] Settings page shows "✅ Gemini API Status"
- [ ] Can upload and analyze a test image

---

## 📞 Support

1. **Check Settings Page** → ⚙️_Settings.py has troubleshooting
2. **Check Disease Library** → 8_📚_Disease_Library for references
3. **Review Error Messages** → Usually have actionable solutions

---

**Made with 🌿 for plant health!**
