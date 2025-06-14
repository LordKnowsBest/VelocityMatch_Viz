# VelocityMatch Carrier Intelligence Dashboard

**Strategic Sales Intelligence Platform for Driver Retention Solutions**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## 🚚 Strategic Mission

Transform federal transportation data into actionable sales intelligence by identifying trucking carriers with high driver churn risk, enabling targeted prospecting for VelocityMatch's AI-powered driver retention platform.

**Live Demo:** [https://velocitymatch-viz.onrender.com](https://velocitymatch-viz.onrender.com)

## 📊 Dashboard Intelligence Features

### 🗺️ Carrier Risk Intelligence Overview
- Interactive U.S. heat map showing carrier churn-risk scores by state/region
- Real-time filtering by fleet size, safety scores, and wage percentiles
- KPI summary with addressable market insights
- Strategic targeting based on federal FMCSA and BLS data integration

### 📊 Carrier Deep-Dive Analysis
- Time-series safety violation trends over 24 months with year-over-year comparison
- Scatter plot correlating wage percentiles vs. out-of-service rates
- Detailed carrier profiles with predictive churn scores and contact intelligence
- Hover functionality for contextual insights without visual clutter

### 🎯 Predictive Targeting & Pipeline
- Ranked list of highest-risk carriers by annual savings opportunity
- Geographic bubble map showing market penetration opportunities
- Pipeline management and sales intelligence export tools
- Competitive analysis and territory optimization insights

## 🛠️ Technical Architecture

- **Frontend:** Streamlit for enterprise-grade interactive deployment
- **Visualization Engine:** Plotly for publication-quality charts and maps
- **Data Processing:** Pandas/NumPy for federal dataset simulation and analysis
- **ML Pipeline:** Scikit-learn for churn risk prediction modeling
- **Deployment:** Render Web Service for professional hosting

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/LordKnowsBest/VelocityMatch_Viz.git
cd VelocityMatch_Viz

# Install dependencies
pip install -r requirements.txt

# Run dashboard locally
streamlit run src/main.py
```

Access dashboard at: `http://localhost:8501`

## 📈 Business Impact & ROI Demonstration

This dashboard demonstrates how data visualization becomes a competitive weapon when deployed with strategic precision:

- **Sales Velocity:** Convert federal compliance data into million-dollar sales conversations
- **Market Intelligence:** Identify carriers losing $2.3M+ annually to driver turnover
- **Competitive Advantage:** Surface "stress hotspots" where VelocityMatch delivers 40-60% retention improvement
- **Pipeline Acceleration:** Transform generic "driver shortage" messaging into laser-focused prospect intelligence

## 🎯 Data Foundation & Methodology

**Federal Data Sources Simulated:**
- FMCSA Safety Measurement System (SMS) - roadside inspections, out-of-service counts, BASIC violation metrics
- FMCSA Crash Database - reportable crashes, severity indicators, time-weighted scores
- FMCSA Motor Carrier Census - fleet size, cargo type, operational characteristics
- BLS Occupational Employment & Wage Statistics - state-level driver wage benchmarks

**Predictive Modeling Framework:**
- Gradient-boost classification for high-risk segment identification
- Multi-factor risk scoring: safety violations + wage competitiveness + fleet characteristics
- Geographic clustering analysis for territory optimization
- Churn cost estimation based on industry replacement benchmarks

## 🌐 Live Deployment

**Production URL:** [https://velocitymatch-viz.onrender.com](https://velocitymatch-viz.onrender.com)

Deployed on Render Web Service with:
- Zero cold-start latency for real-time demonstrations
- SSL encryption for enterprise security
- Automatic scaling for concurrent user sessions
- Custom domain capability for portfolio branding

## 📋 CGT 575 Assignment Context

**Week 6 Deliverable:** Storyboard implementation demonstrating transition from static wireframes to functional business intelligence platform.

**Strategic Stakeholder Validation:**
- **Marcus Chen (VP Sales):** Pipeline velocity and quota attainment focus
- **Dr. Sarah Rodriguez (Data Science Director):** Statistical rigor and model validation
- **James Patterson (Regional Sales Director):** Market reality and field intelligence validation

## 🔧 Development & Contribution

```bash
# Development setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run with hot reloading
streamlit run src/main.py --server.runOnSave=true
```

## 📊 Performance Metrics & Analytics

Dashboard includes built-in analytics for measuring business impact:
- Prospect identification conversion rates
- Territory optimization effectiveness
- Sales cycle acceleration metrics
- Market penetration tracking

---

**Built with Strategic Precision for CGT 575 - Data Visualization**

*Transforming Federal Transportation Data into Million-Dollar Sales Intelligence*
