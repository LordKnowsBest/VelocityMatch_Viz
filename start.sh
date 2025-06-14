#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run src/main.py --server.port=$PORT --server.address=0.0.0.0
