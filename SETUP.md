# Quick Setup Guide

## 1. Initialize Git Repository
```bash
cd "C:\Users\nolan\Desktop\05_Education\PURDUE MSAI\575\velocitymatch-dashboard"
git init
git add .
git commit -m "Initial commit: VelocityMatch Carrier Intelligence Dashboard"
```

## 2. Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `velocitymatch-dashboard`
3. Description: `Strategic carrier intelligence dashboard for VelocityMatch - CGT 575 Data Visualization Project`
4. Set to Public
5. Don't initialize with README (we have one)
6. Click "Create repository"

## 3. Connect Local to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/velocitymatch-dashboard.git
git branch -M main
git push -u origin main
```

## 4. Test Locally
```bash
pip install -r requirements.txt
streamlit run src/main.py
```

## 5. Deploy to Render
1. Go to https://render.com
2. Sign up/Login with GitHub
3. Click "New +" → "Web Service"
4. Connect GitHub repository: `velocitymatch-dashboard`
5. Configuration:
   - Name: `velocitymatch-dashboard`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run src/main.py --server.port=$PORT --server.address=0.0.0.0`
6. Click "Create Web Service"

## 6. Update Assignment with Live Demo
Once deployed, add the live URL to your README and assignment submission.

Your dashboard will be live at: `https://velocitymatch-dashboard.onrender.com`
