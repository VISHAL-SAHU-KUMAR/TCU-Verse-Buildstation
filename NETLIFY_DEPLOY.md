# 🌐 Netlify Deployment Guide - SkillLens AI

## ⚡ Quick Deploy (5 Minutes)

### **Step 1: Configure Netlify Settings**

1. Go to: https://app.netlify.com/
2. Click **"Add new site"** → **"Import an existing project"**
3. Select **GitHub** and authorize
4. Choose repository: **`TCU-Verse-Buildstation`**

### **Step 2: Build Settings**

```
Branch to deploy: main
Base directory: (leave empty)
Build command: (leave empty)
Publish directory: public
Functions directory: (leave empty)
```

### **Step 3: Deploy**

Click **"Deploy site"** and wait 1-2 minutes.

---

## ✅ What You'll Get

### **Working Features:**
- ✅ Beautiful landing page
- ✅ Responsive design
- ✅ All animations
- ✅ Feature showcase
- ✅ Career roles display
- ✅ Fast CDN delivery

### **Not Working (Backend Required):**
- ❌ User registration/login
- ❌ Resume upload
- ❌ Skill analysis
- ❌ Learning roadmap generation
- ❌ Course recommendations
- ❌ User profile

---

## ⚠️ Important Notice

This Netlify deployment is a **STATIC DEMO** only. 

The application has a **warning banner** that tells users:
```
⚠️ Note: This is a static demo. Backend features 
(Resume Upload, Skill Analysis) are disabled.
[Deploy Full Version]
```

When users try to login/signup, they get an alert:
```
⚠️ Backend Not Available

This is a static demo on Netlify. 
Login/Signup features require a backend server.

To use full features:
1. Deploy on Render.com (free)
2. Deploy on Railway.app
3. Run locally

See GitHub README for deployment guide.
```

---

## 🚀 For Full Features

To enable ALL features (resume upload, AI analysis, etc.):

### **Option 1: Render.com (Recommended - Free)**

1. Go to: https://render.com/
2. Sign up with GitHub
3. Click **"New +"** → **"Web Service"**
4. Connect repository: `TCU-Verse-Buildstation`
5. Settings:
   ```
   Name: skilllens-ai
   Runtime: Python 3
   Build: pip install -r requirements.txt
   Start: cd backend && gunicorn app:app --bind 0.0.0.0:$PORT
   ```
6. Click **"Create Web Service"**

**Result:** Full working app at `https://skilllens-ai.onrender.com`

### **Option 2: Railway.app ($5 free credit)**

1. Go to: https://railway.app/
2. Sign in with GitHub
3. **"New Project"** → **"Deploy from GitHub"**
4. Select: `TCU-Verse-Buildstation`
5. Railway auto-configures everything
6. Done!

**Result:** Full app at `https://your-project.up.railway.app`

---

## 🔧 Netlify Configuration Files

### **netlify.toml** (Already in repo)
```toml
[build]
  publish = "public"
  command = ""

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### **public/_redirects** (Already in repo)
```
/*    /index.html   200
```

---

## 📁 Folder Structure

```
public/                    # Netlify serves this
├── index.html            # Landing page
├── dashboard.html        # Dashboard (non-functional without backend)
└── static/
    ├── css/              # Stylesheets
    │   ├── style.css
    │   └── dashboard.css
    └── js/               # JavaScript
        ├── main.js
        └── dashboard.js
```

---

## 🎯 Netlify Features Used

- ✅ **Static Hosting** - HTML/CSS/JS served via CDN
- ✅ **Automatic SSL** - HTTPS enabled
- ✅ **Redirects** - SPA routing with `_redirects`
- ✅ **Custom Domain** - Add your own domain
- ✅ **Deploy Previews** - Preview PRs before merge
- ✅ **Continuous Deployment** - Auto-deploy on Git push

---

## 🌟 Custom Domain Setup

1. Go to **Domain settings** in Netlify
2. Click **"Add custom domain"**
3. Enter your domain (e.g., `skilllens.app`)
4. Follow DNS configuration steps
5. Wait for SSL provisioning (automatic)

---

## 📊 Performance

### **Netlify Static Site:**
- Load Time: < 1 second
- Global CDN: Yes
- SSL: Automatic
- Bandwidth: 100GB/month (free tier)

### **Full Stack (Render/Railway):**
- Load Time: 1-3 seconds
- Cold Start: 30-60 seconds (free tier)
- SSL: Automatic
- Always Online: Yes

---

## 🐛 Troubleshooting

### **Issue: 404 Error on refresh**
**Fix:** Already fixed with `_redirects` file
```
/*    /index.html   200
```

### **Issue: CSS/JS not loading**
**Fix:** Check paths use `/static/` not `./static/`
```html
<link rel="stylesheet" href="/static/css/style.css">
<script src="/static/js/main.js"></script>
```

### **Issue: Build fails**
**Fix:** Ensure `public` folder exists
```bash
mkdir -p public
cp -r frontend/* public/
cp -r static public/
```

### **Issue: Login doesn't work**
**Expected:** This is intentional. Static site can't handle auth.
**Solution:** Deploy full stack on Render.com

---

## 📝 Deployment Checklist

- [ ] Repository pushed to GitHub
- [ ] `public` folder exists with all files
- [ ] `netlify.toml` configured
- [ ] `_redirects` file in `public/`
- [ ] Netlify account created
- [ ] Site connected to GitHub repo
- [ ] Build settings configured
- [ ] Site deployed successfully
- [ ] Custom domain added (optional)
- [ ] SSL certificate active

---

## 🎉 Success!

Your SkillLens AI static demo is now live on Netlify!

**Site URL:** `https://your-site-name.netlify.app`

### **What Users See:**
1. Beautiful landing page ✅
2. Warning banner about backend ⚠️
3. Link to deployment guide 📖
4. Alert when trying to login/signup 🚫

### **Next Steps:**
1. Share the Netlify demo link
2. Deploy full version on Render.com
3. Update demo banner with full version URL
4. Add analytics (Google Analytics)
5. Monitor usage via Netlify dashboard

---

## 🔗 Useful Links

- **Netlify Docs:** https://docs.netlify.com/
- **Render Docs:** https://render.com/docs
- **Railway Docs:** https://docs.railway.app/
- **GitHub Repo:** https://github.com/VISHAL-SAHU-KUMAR/TCU-Verse-Buildstation
- **Deployment Guide:** [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 💡 Pro Tips

1. **Free Tier Limits:**
   - Netlify: 100GB bandwidth/month
   - 300 build minutes/month
   - Unlimited sites

2. **Faster Deploys:**
   - Keep `public` folder in repo
   - No build command needed
   - Instant deployment

3. **SEO Optimization:**
   - Add meta tags to `index.html`
   - Create `sitemap.xml`
   - Add `robots.txt`

4. **Analytics:**
   - Enable Netlify Analytics ($9/month)
   - Or add Google Analytics (free)

---

**Made with ❤️ for Easy Deployment**

**Deploy in 5 minutes!** 🚀