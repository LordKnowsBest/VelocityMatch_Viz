import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_generator import generate_carrier_data, generate_state_summary
from visualizations import create_risk_heatmap, create_safety_trends, create_savings_ranking

# Page configuration
st.set_page_config(
    page_title="VelocityMatch | Carrier Intelligence Dashboard",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enterprise styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
        text-align: center;
    }
    .insight-box {
        background-color: #f3f4f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🚚 VelocityMatch Carrier Intelligence Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #6b7280; font-size: 1.1rem;">Strategic Sales Intelligence Platform for Driver Retention Solutions</p>', unsafe_allow_html=True)
    
    # Sidebar filters
    st.sidebar.markdown("## 🎛️ Intelligence Filters")
    
    # Generate sample data
    carrier_data = generate_carrier_data()
    state_summary = generate_state_summary()
    
    # Sidebar filter controls
    selected_states = st.sidebar.multiselect(
        "Select States",
        options=list(state_summary['state'].unique()),
        default=['GA', 'FL', 'TX', 'NC', 'TN']
    )
    
    fleet_size_range = st.sidebar.slider(
        "Fleet Size Range",
        min_value=10,
        max_value=500,
        value=(25, 150),
        step=5
    )
    
    risk_threshold = st.sidebar.slider(
        "Minimum Risk Score",
        min_value=1.0,
        max_value=10.0,
        value=6.0,
        step=0.5
    )
    
    # Filter data
    filtered_carriers = carrier_data[
        (carrier_data['state'].isin(selected_states)) &
        (carrier_data['fleet_size'] >= fleet_size_range[0]) &
        (carrier_data['fleet_size'] <= fleet_size_range[1]) &
        (carrier_data['risk_score'] >= risk_threshold)
    ]
    
    # Main dashboard tabs
    tab1, tab2, tab3 = st.tabs(["🗺️ Risk Intelligence Overview", "📊 Carrier Deep-Dive", "🎯 Predictive Targeting"])
    
    with tab1:
        # KPI Summary
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{len(filtered_carriers)}</h3>
                <p>High-Risk Carriers</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_savings = filtered_carriers['annual_savings_potential'].sum()
            st.markdown(f"""
            <div class="metric-card">
                <h3>${total_savings/1e6:.1f}M</h3>
                <p>Total Savings Potential</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_risk = filtered_carriers['risk_score'].mean()
            st.markdown(f"""
            <div class="metric-card">
                <h3>{avg_risk:.1f}/10</h3>
                <p>Average Risk Score</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            market_penetration = len(filtered_carriers) / len(carrier_data) * 100
            st.markdown(f"""
            <div class="metric-card">
                <h3>{market_penetration:.1f}%</h3>
                <p>Market Penetration</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Risk heatmap
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown('<h3 class="sub-header">Carrier Risk Intelligence by State</h3>', unsafe_allow_html=True)
            risk_map = create_risk_heatmap(state_summary)
            st.plotly_chart(risk_map, use_container_width=True)
        
        with col2:
            st.markdown('<h3 class="sub-header">Key Insights</h3>', unsafe_allow_html=True)
            
            # Top risk states
            top_risk_states = state_summary.nlargest(5, 'avg_risk_score')[['state', 'avg_risk_score']]
            
            for _, row in top_risk_states.iterrows():
                st.markdown(f"""
                <div class="insight-box">
                    <strong>{row['state']}</strong><br>
                    Risk Score: {row['avg_risk_score']:.1f}/10
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<h3 class="sub-header">Safety Violation Trends Analysis</h3>', unsafe_allow_html=True)
        
        # Safety trends chart
        safety_chart = create_safety_trends(filtered_carriers)
        st.plotly_chart(safety_chart, use_container_width=True)
        
        # Carrier selection
        st.markdown("---")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<h3 class="sub-header">Carrier Risk vs. Wage Correlation</h3>', unsafe_allow_html=True)
            
            scatter_fig = px.scatter(
                filtered_carriers,
                x='wage_percentile',
                y='out_of_service_rate',
                size='fleet_size',
                color='risk_score',
                hover_data=['carrier_name', 'annual_savings_potential'],
                title="Out-of-Service Rate vs. Wage Percentile",
                labels={
                    'wage_percentile': 'Driver Wage Percentile',
                    'out_of_service_rate': 'Out-of-Service Rate (%)',
                    'risk_score': 'Risk Score'
                },
                color_continuous_scale='Reds'
            )
            st.plotly_chart(scatter_fig, use_container_width=True)
        
        with col2:
            st.markdown('<h3 class="sub-header">Carrier Profile</h3>', unsafe_allow_html=True)
            
            if not filtered_carriers.empty:
                selected_carrier = filtered_carriers.iloc[0]
                
                st.markdown(f"""
                **{selected_carrier['carrier_name']}**
                
                📍 **Location:** {selected_carrier['city']}, {selected_carrier['state']}
                
                🚛 **Fleet Size:** {selected_carrier['fleet_size']} trucks
                
                ⚠️ **Risk Score:** {selected_carrier['risk_score']:.1f}/10
                
                💰 **Savings Potential:** ${selected_carrier['annual_savings_potential']:,.0f}
                
                📊 **Key Metrics:**
                - Out-of-Service Rate: {selected_carrier['out_of_service_rate']:.1f}%
                - Wage Percentile: {selected_carrier['wage_percentile']:.0f}%
                - Safety Violations: {selected_carrier['safety_violations']:.0f}/year
                """)
    
    with tab3:
        st.markdown('<h3 class="sub-header">Top Priority Prospects by Savings Potential</h3>', unsafe_allow_html=True)
        
        # Rankings chart
        ranking_chart = create_savings_ranking(filtered_carriers.head(20))
        st.plotly_chart(ranking_chart, use_container_width=True)
        
        st.markdown("---")
        
        # Action panel
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<h3 class="sub-header">Geographic Market Opportunities</h3>', unsafe_allow_html=True)
            
            # Bubble map
            bubble_fig = px.scatter_geo(
                state_summary,
                locations='state',
                locationmode='USA-states',
                size='carrier_count',
                color='avg_risk_score',
                hover_data=['total_savings_potential'],
                scope='usa',
                title="Market Concentration and Risk Distribution",
                color_continuous_scale='Reds'
            )
            bubble_fig.update_layout(height=400)
            st.plotly_chart(bubble_fig, use_container_width=True)
        
        with col2:
            st.markdown('<h3 class="sub-header">Sales Intelligence</h3>', unsafe_allow_html=True)
            
            # Action buttons
            if st.button("📊 Export Top 50 Prospects", type="primary"):
                st.success("Prospect list exported to CRM!")
            
            if st.button("📈 Generate Territory Battle Cards"):
                st.success("Territory intelligence generated!")
            
            if st.button("🔔 Set Risk Score Alerts"):
                st.success("Alert system activated!")
            
            # Market intelligence
            st.markdown("---")
            st.markdown("**📈 Market Intelligence:**")
            
            high_risk_count = len(filtered_carriers[filtered_carriers['risk_score'] >= 7.5])
            st.metric("Critical Risk Carriers", high_risk_count)
            
            avg_fleet_size = filtered_carriers['fleet_size'].mean()
            st.metric("Average Fleet Size", f"{avg_fleet_size:.0f} trucks")
            
            competitive_density = np.random.choice(['Low', 'Medium', 'High'], p=[0.4, 0.4, 0.2])
            st.metric("Competitive Density", competitive_density)

if __name__ == "__main__":
    main()
