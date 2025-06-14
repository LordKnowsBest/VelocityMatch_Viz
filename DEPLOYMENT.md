# VelocityMatch Dashboard - Git Commands & Deployment Guide

## 🚀 Complete Deployment Workflow

### Step 1: Initialize Git Repository
```bash
cd "C:\Users\nolan\Desktop\05_Education\PURDUE MSAI\575\velocitymatch-dashboard"
git init
git add .
git commit -m "Initial commit: VelocityMatch Carrier Intelligence Dashboard - CGT 575 Strategic Implementation"
```

### Step 2: Connect to Your GitHub Repository
```bash
git remote add origin https://github.com/LordKnowsBest/VelocityMatch_Viz.git
git branch -M main
git push -u origin main
```

### Step 3: Verify Local Development
```bash
pip install -r requirements.txt
streamlit run src/main.py
```
Dashboard should be accessible at: `http://localhost:8501`

### Step 4: Deploy to Render (Web Service)
1. **Login to Render:** https://render.com/dashboard
2. **New Web Service:** Click "New +" → "Web Service"
3. **Connect Repository:** Select `LordKnowsBest/VelocityMatch_Viz`
4. **Configuration Settings:**
   - **Name:** `velocitymatch-viz`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run src/main.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`
   - **Plan:** Select your preferred paid tier for optimal performance
5. **Environment Variables (Optional):**
   - `STREAMLIT_SERVER_HEADLESS=true`
   - `STREAMLIT_BROWSER_GATHER_USAGE_STATS=false`
6. **Deploy:** Click "Create Web Service"

### Step 5: Access Live Dashboard
Your dashboard will be live at: `https://velocitymatch-viz.onrender.com`

### Step 6: Update Assignment Documentation
Add live demo URL to:
- Week 6 assignment submission
- Design review meeting materials
- Portfolio documentation

## 🔄 Future Updates Workflow

For any changes to your dashboard:
```bash
# Make changes to your files
git add .
git commit -m "Update: [describe your changes]"
git push origin main
```

Render will automatically redeploy with your latest changes.

## 🎯 Strategic Validation Checklist

Before design review meeting:
- [ ] Dashboard loads without errors
- [ ] All three tabs function correctly
- [ ] Interactive filters work smoothly
- [ ] Heat map displays properly
- [ ] Charts render with realistic data
- [ ] Mobile responsiveness verified
- [ ] Performance acceptable on paid Render tier

## 📱 Demo Preparation

**Key talking points for design review:**
1. **Real-time interactivity** - demonstrate state filtering and carrier drill-down
2. **Business intelligence integration** - show how federal data becomes sales ammunition
3. **Scalability demonstration** - explain how this expands to real FMCSA API integration
4. **ROI quantification** - highlight specific dollar amounts and savings calculations

Your live dashboard URL transforms your Week 6 storyboard into a functional demonstration of technical execution capability.
