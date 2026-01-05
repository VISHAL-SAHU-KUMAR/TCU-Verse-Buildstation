# 🚀 SkillLens AI - Complete Deployment Guide

## 📋 Table of Contents
1. [Platform Options](#platform-options)
2. [Netlify Deployment (Frontend Only)](#netlify-deployment)
3. [Render.com Deployment (Full Stack)](#rendercom-deployment)
4. [Railway.app Deployment (Full Stack)](#railwayapp-deployment)
5. [Heroku Deployment (Full Stack)](#heroku-deployment)
6. [Vercel Deployment (Frontend Only)](#vercel-deployment)
7. [Environment Variables](#environment-variables)
8. [Post-Deployment](#post-deployment)

---

## 🎯 Platform Options

### **Static Hosting (Frontend Only)**
- ✅ **Netlify** - Best for static sites, free tier
- ✅ **Vercel** - Fast deployment, free tier
- ✅ **GitHub Pages** - Simple, free
- ⚠️ **Limitation**: Backend features won't work (no resume upload, no analysis)

### **Full Stack Hosting (Frontend + Backend)**
- ✅ **Render.com** - Free tier, Python support, recommended
- ✅ **Railway.app** - Easy deployment, $5 free credit
- ✅ **Heroku** - Popular, paid plans
- ✅ **PythonAnywhere** - Python-specific hosting
- ✅ **DigitalOcean App Platform** - Scalable, starts at $5/month

---

## 🌐 Netlify Deployment (Frontend Only)

### **What You'll Get:**
- ✅ Beautiful landing page
- ✅ Login/Signup UI
- ❌ No backend functionality
- ❌ Resume upload won't work
- ❌ Skill analysis won't work

### **Step-by-Step:**

#### **Option 1: Deploy via Web UI**

1. **Go to Netlify**: https://app.netlify.com/
2. **Sign in** with GitHub
3. **Click "Add new site" → "Import an existing project"**
4. **Select your repository**: `TCU-Verse-Buildstation`
5. **Configure build settings**:
   ```
   Branch to deploy: main
   Base directory: (leave empty)
   Build command: (leave empty)
   Publish directory: frontend
   Functions directory: (leave empty)
   ```
6. **Click "Deploy site"**

#### **Option 2: Deploy via Netlify CLI**

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Initialize Netlify
netlify init

# Deploy
netlify deploy --prod
```

### **Netlify Configuration**

The `netlify.toml` file is already configured:

```toml
[build]
  publish = "frontend"
  command = ""

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### **After Deployment:**

Your site will be live at: `https://your-site-name.netlify.app`

⚠️ **Important**: To enable backend features, you need to deploy backend separately (see Render.com section).

---

## 🔷 Render.com Deployment (Full Stack - RECOMMENDED)

### **What You'll Get:**
- ✅ Complete application
- ✅ Resume upload works
- ✅ AI analysis works
- ✅ All features functional
- ✅ Free tier available

### **Step-by-Step:**

1. **Go to Render**: https://render.com/
2. **Sign up** with GitHub
3. **Click "New +" → "Web Service"**
4. **Connect your repository**: `TCU-Verse-Buildstation`
5. **Configure settings**:

   ```
   Name: skilllens-ai
   Region: Singapore (or closest to you)
   Branch: main
   Root Directory: (leave empty)
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: cd backend && gunicorn app:app --bind 0.0.0.0:$PORT
   ```

6. **Select Plan**: Free
7. **Environment Variables** (click "Advanced"):
   ```
   PYTHON_VERSION = 3.10.0
   FLASK_ENV = production
   SECRET_KEY = (auto-generated)
   ```

8. **Click "Create Web Service"**

### **Using render.yaml (Recommended)**

The `render.yaml` file is already configured. Just:

1. Go to Render Dashboard
2. Click "New +" → "Blueprint"
3. Connect repository
4. Render will auto-detect `render.yaml`
5. Click "Apply"

### **After Deployment:**

Your app will be live at: `https://skilllens-ai.onrender.com`

⚠️ **Note**: Free tier spins down after inactivity. First request may take 30-60 seconds.

---

## 🚂 Railway.app Deployment (Full Stack)

### **What You'll Get:**
- ✅ Complete application
- ✅ All features work
- ✅ Fast deployment
- ✅ $5 free credit

### **Step-by-Step:**

1. **Go to Railway**: https://railway.app/
2. **Sign in** with GitHub
3. **Click "New Project" → "Deploy from GitHub repo"**
4. **Select repository**: `TCU-Verse-Buildstation`
5. **Railway auto-detects** Python app
6. **Add Environment Variables**:
   ```
   PYTHON_VERSION = 3.10
   FLASK_ENV = production
   PORT = 5000
   ```

7. **Deploy** - Railway handles everything automatically

### **Using railway.json (Optional)**

The `railway.json` file is already configured. Railway will auto-detect it.

### **After Deployment:**

Your app will be at: `https://your-project.up.railway.app`

### **Custom Domain:**

1. Go to project settings
2. Click "Generate Domain"
3. Or add your custom domain

---

## 🟪 Heroku Deployment (Full Stack)

### **Prerequisites:**
- Heroku account
- Heroku CLI installed

### **Step-by-Step:**

```bash
# 1. Install Heroku CLI
# Windows: Download from https://devcenter.heroku.com/articles/heroku-cli
# Mac: brew tap heroku/brew && brew install heroku
# Linux: curl https://cli-assets.heroku.com/install.sh | sh

# 2. Login to Heroku
heroku login

# 3. Create Heroku app
heroku create skilllens-ai

# 4. Add Python buildpack
heroku buildpacks:set heroku/python

# 5. Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(openssl rand -hex 32)

# 6. Deploy
git push heroku main

# 7. Open app
heroku open
```

### **Procfile Configuration:**

The `Procfile` is already configured:

```
web: cd backend && gunicorn app:app --bind 0.0.0.0:$PORT
```

### **After Deployment:**

Your app will be at: `https://skilllens-ai.herokuapp.com`

---

## ▲ Vercel Deployment (Frontend Only)

### **Step-by-Step:**

1. **Go to Vercel**: https://vercel.com/
2. **Import Project** from GitHub
3. **Select repository**: `TCU-Verse-Buildstation`
4. **Configure**:
   ```
   Framework Preset: Other
   Root Directory: frontend
   Build Command: (leave empty)
   Output Directory: ./
   ```
5. **Deploy**

### **vercel.json Configuration:**

Create `vercel.json` in root:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ]
}
```

---

## 🔐 Environment Variables

### **Required Variables:**

```bash
# Production
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
PYTHON_VERSION=3.10

# Optional
PORT=5000
DATABASE_URL=sqlite:///database/skilllens.db
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
```

### **Generate Secret Key:**

```bash
# Python
python -c "import secrets; print(secrets.token_hex(32))"

# OpenSSL
openssl rand -hex 32
```

---

## 📝 Post-Deployment Checklist

### **1. Test Basic Functionality:**
- [ ] Homepage loads correctly
- [ ] Sign up works
- [ ] Login works
- [ ] Dashboard accessible

### **2. Test Core Features:**
- [ ] Resume upload works
- [ ] PDF parsing works
- [ ] Skill extraction works
- [ ] Role selection works
- [ ] Analysis generates correctly
- [ ] Roadmap displays
- [ ] Course recommendations show

### **3. Test Profile Features:**
- [ ] View profile works
- [ ] Edit profile works
- [ ] Change password works
- [ ] Avatar displays

### **4. Performance Checks:**
- [ ] Page load time < 3 seconds
- [ ] API responses < 2 seconds
- [ ] File upload works smoothly
- [ ] No console errors

### **5. Security Checks:**
- [ ] HTTPS enabled
- [ ] Sessions work correctly
- [ ] Password hashing works
- [ ] File validation works

---

## 🔧 Troubleshooting

### **Issue: Application Crashes**

**Solution:**
```bash
# Check logs
render logs          # Render.com
railway logs         # Railway.app
heroku logs --tail   # Heroku

# Check if all dependencies installed
pip freeze > requirements.txt
```

### **Issue: Database Errors**

**Solution:**
```bash
# Ensure database directory exists
mkdir -p database

# Set proper permissions
chmod 755 database
```

### **Issue: Static Files Not Loading**

**Solution:**
- Check `static_folder` path in `app.py`
- Ensure paths start with `/static/`
- Check CORS settings

### **Issue: Resume Upload Fails**

**Solution:**
- Check file size limits
- Ensure `uploads/` directory exists
- Check file permissions
- Verify PyPDF2 is installed

---

## 📊 Performance Optimization

### **1. Enable Caching:**

```python
# Add to app.py
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})
```

### **2. Use Production Server:**

Already configured with Gunicorn:
```bash
gunicorn app:app --workers 4 --bind 0.0.0.0:$PORT
```

### **3. Optimize Database:**

For production, migrate to PostgreSQL:
```bash
# Install
pip install psycopg2-binary

# Update connection string
DATABASE_URL = os.getenv('DATABASE_URL')
```

### **4. Enable Compression:**

```python
# Add to app.py
from flask_compress import Compress

Compress(app)
```

---

## 🌍 Custom Domain Setup

### **Render.com:**
1. Go to Settings
2. Add Custom Domain
3. Add DNS records (provided by Render)

### **Railway.app:**
1. Project Settings → Domains
2. Add Custom Domain
3. Configure DNS

### **Netlify:**
1. Domain Settings
2. Add Custom Domain
3. Configure DNS automatically

---

## 📈 Monitoring & Analytics

### **1. Application Monitoring:**

**Sentry** (Error Tracking):
```bash
pip install sentry-sdk[flask]
```

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()]
)
```

### **2. Usage Analytics:**

Add Google Analytics to `index.html` and `dashboard.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

---

## 🎯 Recommended Deployment Strategy

### **For Development/Testing:**
- Use **Render.com Free Tier**
- Fast deployment
- All features work
- Free forever

### **For Production:**
- **Option 1**: Render.com Paid Plan ($7/month)
- **Option 2**: Railway.app ($5/month)
- **Option 3**: DigitalOcean App Platform ($5/month)
- **Option 4**: Self-hosted VPS (DigitalOcean Droplet, AWS EC2)

### **For Static Frontend Only:**
- **Netlify** or **Vercel**
- Perfect for landing page
- CDN included
- Free forever

---

## 📞 Support

### **Deployment Issues:**
- Check platform-specific logs
- Review this guide
- Check GitHub Issues
- Contact platform support

### **Application Issues:**
- Check server logs
- Test locally first
- Review error messages
- Create GitHub issue

---

## ✅ Quick Reference

### **Netlify (Frontend Only):**
```bash
Publish directory: frontend
Build command: (empty)
```

### **Render.com (Full Stack):**
```bash
Build: pip install -r requirements.txt
Start: cd backend && gunicorn app:app --bind 0.0.0.0:$PORT
```

### **Railway.app (Full Stack):**
```bash
Auto-detected, uses railway.json
```

### **Heroku (Full Stack):**
```bash
heroku create skilllens-ai
git push heroku main
```

---

**Made with ❤️ for Easy Deployment**

**Choose your platform and deploy in minutes!** 🚀