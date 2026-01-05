# 🚀 SkillLens AI - Quick Start Guide

Get up and running in **5 minutes**!

---

## 📋 Prerequisites

- **Python 3.8+** installed ([Download here](https://www.python.org/downloads/))
- **Windows, Mac, or Linux**
- **PDF Resume** ready to upload

---

## 🎯 Quick Installation

### Windows Users

1. **Open Command Prompt** in the project folder
2. **Run the startup script:**
   ```cmd
   start.bat
   ```

The script will automatically:
- Create a virtual environment
- Install all dependencies
- Start the server

### Mac/Linux Users

1. **Open Terminal** in the project folder
2. **Make the script executable:**
   ```bash
   chmod +x start.sh
   ```
3. **Run the startup script:**
   ```bash
   ./start.sh
   ```

---

## 🌐 Access the Application

Once the server starts, open your browser and go to:

```
http://127.0.0.1:5000
```

You'll see the SkillLens AI landing page! 🎉

---

## 📝 First Time Usage

### Step 1: Create Account
1. Click **"Sign Up"** button
2. Enter your details:
   - Full Name
   - Email
   - Password (min 6 characters)
3. Click **"Create Account"**

### Step 2: Upload Resume
1. You'll be redirected to the dashboard
2. Click **"Upload Resume"** in the sidebar
3. Drag & drop your PDF resume or click to browse
4. Wait 5-10 seconds for AI to extract skills

### Step 3: Select Career Role
1. Click **"Skill Analysis"** in the sidebar
2. Choose your target role (e.g., "Data Analyst")
3. AI will analyze your skill gap instantly

### Step 4: View Results
You'll see:
- **Skill Score** (0-100%)
- **Skills you have** ✅
- **Critical missing skills** ❌
- **Important missing skills** ⚠️
- **Nice-to-have skills** ⭐

### Step 5: Get Your Roadmap
1. Click **"Learning Roadmap"** in the sidebar
2. View your personalized 3-phase learning plan:
   - **Beginner** (0-4 weeks)
   - **Intermediate** (1-3 months)
   - **Advanced** (3-6 months)

### Step 6: Learn
1. Click **"Recommendations"** in the sidebar
2. Get course recommendations for each missing skill
3. Start learning!

---

## 🎓 Example Workflow

**Scenario:** You want to become a Data Analyst

1. **Upload Resume** → AI finds: Python, Excel
2. **Select "Data Analyst"** → Score: 45%
3. **View Gap Analysis:**
   - ✅ Have: Python, Excel
   - ❌ Missing: SQL, Pandas, Power BI, Statistics
4. **Follow Roadmap:**
   - Week 1-2: Learn SQL basics
   - Week 3-4: Master Pandas for data manipulation
   - Month 2: Practice with Power BI dashboards
5. **Take Courses:**
   - SQL: SQLBolt (free)
   - Pandas: Kaggle Learn (free)
   - Power BI: Microsoft Learn (free)

---

## 🐛 Troubleshooting

### Problem: Server won't start
**Solution:**
```bash
# Check if port 5000 is in use
# Windows:
netstat -ano | findstr :5000

# Mac/Linux:
lsof -i :5000
```

### Problem: "Python not found"
**Solution:**
- Install Python 3.8+ from [python.org](https://www.python.org/)
- Make sure to check "Add Python to PATH" during installation

### Problem: Resume upload fails
**Solution:**
- Ensure file is PDF format (not image or Word)
- Check file size is under 16MB
- Use text-based PDF (not scanned images)

### Problem: No skills extracted
**Solution:**
- Make sure your resume has clear skill sections
- List technologies and tools explicitly
- Use common skill names (e.g., "Python" not "Py")

---

## 💡 Tips for Best Results

### Resume Tips
- ✅ Use ATS-friendly format (simple, clean layout)
- ✅ Include a dedicated "Skills" section
- ✅ List programming languages, tools, frameworks
- ✅ Mention projects and technologies used
- ❌ Avoid graphics-heavy or scanned resumes

### Analysis Tips
- 🎯 Be realistic about your target role
- 📚 Focus on critical missing skills first
- 🔄 Update and re-upload resume as you learn
- 📊 Track your progress over time
- 🚀 Practice with recommended projects

---

## 🔥 Popular Career Paths

### For Beginners
1. **Data Analyst** - High demand, good entry point
2. **Frontend Developer** - Creative, visual projects
3. **Backend Developer** - Logic and systems

### For Intermediate
1. **Full Stack Developer** - Complete web applications
2. **Data Scientist** - Advanced analytics & ML
3. **DevOps Engineer** - Infrastructure & automation

### For Advanced
1. **Machine Learning Engineer** - AI/ML systems
2. **Cloud Engineer** - Scalable cloud solutions
3. **Cybersecurity Analyst** - Security & protection

---

## 📊 Dashboard Overview

### Overview Tab
- Total resumes analyzed
- Average skill score
- Skills mastered count
- Recent analyses history

### Upload Tab
- Drag & drop resume upload
- Progress indicator
- Skill extraction preview

### Analysis Tab
- 10 career roles to choose from
- Real-time skill gap analysis
- Visual score representation
- Detailed skill breakdown

### Roadmap Tab
- 3-phase learning plan
- Skill prioritization
- Project recommendations
- Time estimates

### Recommendations Tab
- Course suggestions per skill
- Platform recommendations
- Free vs. paid options
- Learning resources

### History Tab
- Past analyses
- Score tracking
- Progress over time
- Re-access old results

---

## 🎯 Success Metrics

After using SkillLens AI for **1 month**, you should have:
- ✅ Clear understanding of skill gaps
- ✅ Started learning 2-3 critical skills
- ✅ Completed at least 1 beginner project
- ✅ Updated resume with new skills

After **3 months**:
- ✅ Mastered 5-7 key skills
- ✅ Built 3-5 portfolio projects
- ✅ Skill score improved by 30-40%
- ✅ Ready to apply for junior roles

After **6 months**:
- ✅ Advanced proficiency in target role
- ✅ 10+ portfolio projects
- ✅ Skill score 80%+
- ✅ Job-ready!

---

## 🆘 Need Help?

### Common Issues
- **Login issues?** Clear browser cookies and try again
- **Slow upload?** Check your internet connection
- **Wrong skills extracted?** Ensure resume has clear text

### Resources
- 📖 Read the full [README.md](README.md)
- 💻 Check the code in `/backend` and `/frontend`
- 🐛 Report bugs by creating an issue

---

## 🎉 You're All Set!

**Your journey to career success starts now!**

1. ✅ Server running
2. ✅ Account created
3. ✅ Resume uploaded
4. ✅ Skills analyzed
5. ✅ Roadmap received

**Next Steps:**
- Follow your personalized roadmap
- Take recommended courses
- Build projects
- Update your skills
- Apply for jobs

---

## 🌟 Pro Tips

1. **Upload Multiple Resumes** - Try different versions to see what works best
2. **Explore All Roles** - Discover skills that overlap between roles
3. **Regular Updates** - Re-analyze every month to track progress
4. **Use Projects** - Recommended projects are designed for real learning
5. **Free Resources** - Focus on free courses first before paid ones

---

## 📱 Stay Connected

- 🌐 **Website:** Your SkillLens AI instance
- 📧 **Support:** Check the main README
- 🐦 **Updates:** Follow development progress

---

**Happy Learning! 🚀**

*Made with ❤️ for Indian Students*