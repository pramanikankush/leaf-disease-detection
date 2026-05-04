# 🚀 Quick Start Guide (Windows)

## Step 1: Install Python
- Download from: https://www.python.org/downloads/
- **Important**: Check "Add Python to PATH" during installation
- Verify: Open PowerShell and type `python --version`

## Step 2: Install Dependencies

**PowerShell (Recommended):**
```powershell
cd C:\Users\YourUsername\Desktop\Plant-Health-Analyzer
pip install -r requirements.txt
```

## Step 3: Get API Key

1. Visit: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the generated key (looks like: `AQ.Ab8RN...`)

## Step 4: Configure API Key

### Option A: PowerShell (Temporary - Current Session Only)
```powershell
$env:GEMINI_API_KEY = "paste_your_key_here"
streamlit run app.py
```

### Option B: PowerShell (Permanent - All Sessions)
```powershell
[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', 'paste_your_key_here', 'User')
```
Then **restart PowerShell** and run:
```powershell
streamlit run app.py
```

### Option C: Command Prompt (Temporary)
```cmd
set GEMINI_API_KEY=paste_your_key_here
streamlit run app.py
```

### Option D: Edit Config File (Development)
1. Open: `Plant-Health-Analyzer\utils\config.py`
2. Find: `DEFAULT_GEMINI_KEY = "AQ.Ab8R..."`
3. Replace with your key
4. Save and run: `streamlit run app.py`

## Step 5: Verify Setup

**Run verification script:**
```powershell
python verify_setup.py
```

Should show:
```
✅ PASS - Python Version
✅ PASS - Dependencies
✅ PASS - File Structure
✅ PASS - Data Directory
✅ PASS - API Configuration
```

## Step 6: Start Application

```powershell
streamlit run app.py
```

Opens at: `http://localhost:8501`

---

## 📋 Troubleshooting

### PowerShell Error: "streamlit: The term is not recognized"
**Solution:**
```powershell
# Use full path
python -m streamlit run app.py
```

### PowerShell Error: "Cannot be loaded because running scripts is disabled"
**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Type 'Y' and Enter to confirm
```

### API Key Not Working
**Check:**
1. Copy entire key (no spaces before/after)
2. Key starts with `AQ.` or `sk-`
3. Verify in Google AI Studio it's still active
4. Check: `echo $env:GEMINI_API_KEY`

### "Cannot find module" errors
**Solution:**
```powershell
pip install -r requirements.txt --upgrade
```

### Port 8501 already in use
**Solution:**
```powershell
streamlit run app.py --server.port=8502
```

---

## 🔑 API Key Best Practices

✅ **DO:**
- Keep API key private
- Use environment variables
- Rotate keys regularly
- Monitor usage in Google Cloud Console

❌ **DON'T:**
- Share API key on social media
- Commit to Git/GitHub
- Use in public URLs
- Reuse same key across projects

---

## 📁 Folder Structure

```
C:\Users\YourUsername\Desktop\Plant-Health-Analyzer\
├── app.py                    ← Main application
├── verify_setup.py           ← Run this to check setup
├── requirements.txt          ← Dependencies
├── README.md                 ← Full documentation
├── .env.example              ← Copy to .env
├── .gitignore               ← Don't commit these files
│
├── utils/
│   ├── config.py            ← API configuration
│   └── ...
│
├── services/
│   └── gemini_service.py     ← Gemini API
│
└── pages/                    ← Feature pages
    ├── 1_📰_Crop_News.py
    ├── 2_🕒_History.py
    └── ...
```

---

## ✅ You're Ready!

1. ✅ Python installed
2. ✅ Dependencies installed
3. ✅ API key configured
4. ✅ Verification passed
5. 🚀 Run `streamlit run app.py`

---

## 🆘 Still Having Issues?

1. Check ⚙️ Settings page in the app (shows diagnostics)
2. Run `verify_setup.py` for detailed error messages
3. Check README.md for full documentation
4. Restart PowerShell/IDE completely

---

**Enjoy analyzing plant diseases! 🌿**
