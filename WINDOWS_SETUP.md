# VelocityMatch Windows Development Setup

## 🛡️ Strategic Solution for Windows Development

Your pandas compilation error is a common Windows challenge. Here's the battle-tested deployment strategy:

### Option 1: Virtual Environment Reset (Recommended)
```bash
# Navigate to project directory
cd "C:\Users\nolan\Desktop\05_Education\PURDUE MSAI\575\velocitymatch-dashboard"

# Create fresh virtual environment
python -m venv venv

# Activate virtual environment
# For PowerShell:
.venv\Scripts\Activate.ps1
# For Command Prompt:
.venv\Scripts\activate.bat

# Upgrade pip first
python -m pip install --upgrade pip

# Install requirements (optimized for Windows)
pip install -r requirements.txt

# Test Streamlit installation
python -m streamlit hello
```

### Option 2: Direct Streamlit Installation (If Option 1 Fails)
```bash
# Install core dependencies individually
pip install streamlit
pip install plotly
pip install numpy

# Test with minimal app
python -m streamlit run src/main.py
```

### Option 3: Alternative Pandas Installation
```bash
# If pandas compilation still fails, try pre-compiled wheel
pip install --only-binary=all pandas

# Or use conda for pre-compiled packages
conda install pandas numpy plotly streamlit
```

## 🚀 Quick Validation Commands

```bash
# Test Python modules individually
python -c "import streamlit; print('Streamlit:', streamlit.__version__)"
python -c "import pandas; print('Pandas:', pandas.__version__)"
python -c "import plotly; print('Plotly:', plotly.__version__)"

# Run Streamlit hello app
python -m streamlit hello

# Run your dashboard
python -m streamlit run src/main.py
```

## 🎯 Deployment Strategy

Once local testing works:

### GitHub Push:
```bash
git init
git add .
git commit -m "VelocityMatch Dashboard - CGT 575 Implementation"
git remote add origin https://github.com/LordKnowsBest/VelocityMatch_Viz.git
git branch -M main
git push -u origin main
```

### Render Deployment:
- Render uses Linux containers (no Windows compilation issues)
- Your optimized requirements.txt will install cleanly
- Live dashboard at: `https://velocitymatch-viz.onrender.com`

## 🔧 Troubleshooting

If you continue to see compilation errors:

1. **Use Python 3.9-3.11** (most stable for data science packages)
2. **Clear pip cache:** `pip cache purge`
3. **Update Visual Studio Build Tools** (if needed for other packages)
4. **Skip to Render deployment** (Linux environment handles compilation automatically)

The key insight: Render's Linux environment will compile everything cleanly, so local Windows issues won't affect your final deployment.

Your dashboard will work perfectly once deployed, regardless of local compilation challenges.
