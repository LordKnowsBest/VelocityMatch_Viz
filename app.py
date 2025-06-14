import os

# Streamlit configuration for deployment
os.environ['STREAMLIT_SERVER_PORT'] = os.environ.get('PORT', '8501')
os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'

# Import and run the main app
from src.main import main

if __name__ == "__main__":
    main()
