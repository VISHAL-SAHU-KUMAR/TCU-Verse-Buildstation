# 🛠️ SkillLens AI - Complete Installation Guide

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Methods](#installation-methods)
3. [Step-by-Step Setup](#step-by-step-setup)
4. [Verification](#verification)
5. [Usage Instructions](#usage-instructions)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Configuration](#advanced-configuration)

---

## 📋 System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: Version 3.8 or higher
- **RAM**: 2GB minimum
- **Storage**: 500MB free space
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, or Edge 90+
- **Internet**: Required for initial setup and course recommendations

### Recommended Requirements
- **Python**: Version 3.10+
- **RAM**: 4GB or more
- **Storage**: 1GB free space
- **Browser**: Latest version of Chrome or Firefox

---

## 🚀 Installation Methods

### Method 1: Automated Setup (Recommended)

#### For Windows Users
1. Open Command Prompt or PowerShell in the project folder
2. Run:
   ```cmd
   start.bat
   ```

#### For macOS/Linux Users
1. Open Terminal in the project folder
2. Make script executable:
   ```bash
   chmod +x start.sh
   ```
3. Run:
   ```bash
   ./start.sh
   ```

The automated script will:
- ✅ Check Python installation
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Create necessary directories
- ✅ Start the server

### Method 2: Manual Setup

#### Step 1: Verify Python Installation
```bash
python --version
# or
python3 --version
```

Should output: `Python 3.8.x` or higher

#### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv

# macOS/Linux
python3 -m venv venv
```

#### Step 3: Activate Virtual Environment
```bash
# Windows Command Prompt
venv\Scripts\activate.bat

# Windows PowerShell
venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal.

#### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

Expected output: Successfully installed Flask, Flask-CORS, PyPDF2, Werkzeug, python-dotenv

#### Step 5: Create Required Directories
```bash
# Windows
mkdir database uploads models

# macOS/Linux
mkdir -p database uploads models
```

#### Step 6: Start the Server
```bash
cd backend
python app.py
```

---

## 🔍 Step-by-Step Setup

### 1. Python Installation (If Not Installed)

#### Windows
1. Download from [python.org](https://www.python.org/downloads/)
2. Run installer
3. ✅ **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify: Open Command Prompt and type `python --version`

#### macOS
```bash
# Using Homebrew
brew install python3

# Verify
python3 --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Verify
python3 --version
```

### 2. Download Project
```bash
# If using git
git clone <repository-url>
cd tcu

# Or download and extract ZIP file
cd tcu
```

### 3. Virtual Environment Setup
**Why virtual environment?**
- Isolates project dependencies
- Prevents conflicts with system Python
- Easy to manage and delete

```bash
# Create
python -m venv venv

# Activate (do this every time you work on the project)
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# You'll see (venv) in your terminal prompt
```

### 4. Dependency Installation
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Dependencies installed:**
- Flask 2.3.3 - Web framework
- Flask-CORS 4.0.0 - Cross-origin support
- PyPDF2 3.0.1 - PDF processing
- Werkzeug 2.3.7 - Security utilities
- python-dotenv 1.0.0 - Environment variables

### 5. Directory Structure Verification
```bash
# Windows
dir

# macOS/Linux
ls -la
```

Should show:
```
backend/
frontend/
static/
database/
uploads/
models/
requirements.txt
start.bat
start.sh
README.md
```

### 6. Launch Application
```bash
cd backend
python app.py
```

**Expected Output:**
```
==================================================
🧠 SkillLens AI - Career Intelligence Platform
==================================================

✅ Server starting...
📍 Open your browser and navigate to:
   http://127.0.0.1:5000

📝 Press Ctrl+C to stop the server

==================================================
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

---

## ✅ Verification

### 1. Server Running Check
- Terminal shows "Running on http://0.0.0.0:5000"
- No error messages
- Debug mode is ON

### 2. Browser Access Test
1. Open browser
2. Navigate to: `http://127.0.0.1:5000`
3. Should see SkillLens AI landing page
4. Check for:
   - Hero section with animations
   - "Sign Up" and "Login" buttons visible
   - Smooth animations on scroll

### 3. Database Creation Check
```bash
# In a new terminal (don't close server)
cd database
dir  # Windows
ls -la  # macOS/Linux
```

Should see: `skilllens.db` file created automatically

### 4. API Endpoint Test
Open browser console (F12) and run:
```javascript
fetch('http://127.0.0.1:5000/api/check-auth', {
    credentials: 'include'
}).then(r => r.json()).then(console.log)
```

Should return: `{ authenticated: false }`

---

## 📱 Usage Instructions

### First-Time User Flow

#### 1. Create Account (Registration)
1. Click **"Sign Up"** button on homepage
2. Fill in form:
   - **Full Name**: Your name
   - **Email**: Valid email address
   - **Password**: Minimum 6 characters
3. Click **"Create Account"**
4. Automatic redirect to dashboard

#### 2. Upload Resume
1. In dashboard sidebar, click **"Upload Resume"**
2. Upload methods:
   - **Drag & Drop**: Drag PDF file to upload area
   - **Click to Browse**: Click "Browse Files" button
3. Wait 5-10 seconds for processing
4. View extracted skills preview
5. Click **"Proceed to Analysis"**

**Resume Requirements:**
- ✅ PDF format only
- ✅ Text-based (not scanned images)
- ✅ Maximum 16MB size
- ✅ Clear skill sections
- ✅ English language

#### 3. Analyze Skills
1. Click **"Skill Analysis"** in sidebar
2. View 10 career role options
3. Click your target role (e.g., "Data Analyst")
4. Wait for AI analysis (1-2 seconds)
5. View results:
   - **Skill Score**: 0-100% match
   - **Present Skills**: What you already have
   - **Critical Missing**: Must-learn skills
   - **Important Missing**: High-value skills
   - **Nice-to-Have**: Optional skills

#### 4. Get Learning Roadmap
1. Click **"Learning Roadmap"** in sidebar
2. View 3-phase plan:
   - **Beginner Phase** (0-4 weeks): Foundation skills
   - **Intermediate Phase** (1-3 months): Core skills
   - **Advanced Phase** (3-6 months): Expert skills
3. Each phase includes:
   - Skills to learn
   - Practice projects
   - Time estimates

#### 5. Access Course Recommendations
1. Click **"Recommendations"** in sidebar
2. View curated courses for each missing skill
3. Each recommendation shows:
   - Skill name
   - Platform (Coursera, Udemy, FreeCodeCamp, etc.)
   - Why it's useful
4. Click "Learn More" to explore

#### 6. Track Progress
1. Click **"Overview"** to see dashboard
2. View statistics:
   - Total resumes analyzed
   - Average skill score
   - Skills mastered count
   - Courses recommended
3. Check **"History"** for past analyses

---

## 🐛 Troubleshooting

### Problem 1: Python Not Found
**Error**: `'python' is not recognized as an internal or external command`

**Solutions:**
```bash
# Try python3 instead
python3 --version

# Reinstall Python with PATH option checked
# Windows: Download from python.org and check "Add to PATH"

# Verify PATH (Windows)
echo %PATH%

# Verify PATH (macOS/Linux)
echo $PATH
```

### Problem 2: Port Already in Use
**Error**: `Address already in use`

**Solutions:**
```bash
# Find process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <process_id> /F

# macOS/Linux:
lsof -ti:5000
kill -9 <process_id>

# Or change port in app.py (last line):
app.run(debug=True, host="0.0.0.0", port=8080)
```

### Problem 3: Module Not Found
**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solutions:**
```bash
# Ensure virtual environment is activated
# You should see (venv) in prompt

# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt

# If still failing, delete venv and recreate
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows
python -m venv venv
```

### Problem 4: Permission Denied
**Error**: `Permission denied: 'uploads'`

**Solutions:**
```bash
# Windows (run as Administrator)
Right-click Command Prompt -> Run as Administrator

# Linux/macOS
sudo chmod 755 uploads database
sudo chown -R $USER:$USER uploads database
```

### Problem 5: Resume Upload Fails
**Error**: File upload returns error

**Solutions:**
1. Check file is PDF format
2. Ensure file size < 16MB
3. Verify `uploads/` folder exists
4. Check file is text-based PDF, not scanned image
5. Try different PDF (generate from Word/Google Docs)

### Problem 6: Database Locked
**Error**: `database is locked`

**Solutions:**
```bash
# Close all connections and restart server
# Delete database and let it recreate
rm database/skilllens.db  # Linux/Mac
del database\skilllens.db  # Windows

# Restart server - database will be recreated
```

### Problem 7: Skills Not Extracted
**Issue**: Resume uploaded but no skills found

**Solutions:**
1. Ensure resume has clear "Skills" section
2. List skills explicitly (e.g., "Python", "SQL", "Excel")
3. Use common skill names, not abbreviations
4. Check PDF is text-based (try copying text from PDF)
5. Regenerate resume from editable format

### Problem 8: Browser Can't Connect
**Error**: `This site can't be reached`

**Solutions:**
1. Check server is running (terminal shows no errors)
2. Try `http://localhost:5000` instead of `127.0.0.1`
3. Clear browser cache
4. Try different browser
5. Check firewall settings
6. Disable VPN temporarily

---

## ⚙️ Advanced Configuration

### Change Port Number
Edit `backend/app.py`, last line:
```python
# Change from port 5000 to 8080
app.run(debug=True, host="0.0.0.0", port=8080)
```

### Increase Upload Limit
Edit `backend/app.py`, line 16:
```python
# Change from 16MB to 32MB
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024
```

### Extend Session Duration
Edit `backend/app.py`, line 17:
```python
# Change from 7 days to 30 days
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
```

### Add New Career Role
Edit `backend/app.py`, add to `ROLE_REQUIREMENTS`:
```python
'Your New Role': {
    'critical': ['Skill1', 'Skill2', 'Skill3'],
    'important': ['Skill4', 'Skill5'],
    'nice_to_have': ['Skill6', 'Skill7']
}
```

### Database Configuration (PostgreSQL)
```python
# Install psycopg2
pip install psycopg2-binary

# Update connection in app.py
import psycopg2
DATABASE_URL = 'postgresql://user:password@localhost/skilllens'
```

### Enable HTTPS
```python
# Generate SSL certificate
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Update app.run()
app.run(debug=True, host="0.0.0.0", port=5000, 
        ssl_context=('cert.pem', 'key.pem'))
```

---

## 🔒 Security Best Practices

### For Production Deployment
1. **Change Secret Key**
   ```python
   # Generate new secret key
   import secrets
   print(secrets.token_hex(32))
   
   # Update in app.py
   app.secret_key = 'your-generated-secret-key'
   ```

2. **Disable Debug Mode**
   ```python
   app.run(debug=False, host="0.0.0.0", port=5000)
   ```

3. **Use Environment Variables**
   ```bash
   # Create .env file
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///database/skilllens.db
   UPLOAD_FOLDER=uploads
   ```

4. **Set Up HTTPS** (see above)

5. **Enable Rate Limiting**
   ```bash
   pip install Flask-Limiter
   ```

---

## 📊 Performance Optimization

### For Large User Base
1. **Migrate to PostgreSQL**
   - SQLite limited to ~100 concurrent users
   - PostgreSQL handles thousands

2. **Add Redis Caching**
   ```bash
   pip install redis flask-caching
   ```

3. **Use Gunicorn**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
   ```

4. **Enable Compression**
   ```bash
   pip install flask-compress
   ```

---

## 🎓 Next Steps

After installation:
1. ✅ Read [QUICKSTART.md](QUICKSTART.md) for usage guide
2. ✅ Check [README.md](README.md) for features
3. ✅ Review [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for architecture
4. ✅ Start using the application!

---

## 💬 Getting Help

### Resources
- 📖 **README.md** - Full documentation
- 🚀 **QUICKSTART.md** - 5-minute guide
- 📊 **PROJECT_SUMMARY.md** - Technical details
- 🐛 **GitHub Issues** - Report bugs

### Common Questions

**Q: Can I use this offline?**
A: Yes, after initial setup. Course recommendations require internet.

**Q: Is my data secure?**
A: Yes, stored locally in SQLite database on your machine.

**Q: Can I analyze multiple resumes?**
A: Yes, upload as many as you want and compare results.

**Q: Does it work with non-technical resumes?**
A: Optimized for tech roles, but works with any resume.

**Q: Can I export my roadmap?**
A: Currently view-only, export feature coming soon.

---

## 🎉 Installation Complete!

Your SkillLens AI instance is now ready!

**Next:** Open http://127.0.0.1:5000 and create your account.

**Happy Learning! 🚀**

---

*Made with ❤️ for Indian Students*