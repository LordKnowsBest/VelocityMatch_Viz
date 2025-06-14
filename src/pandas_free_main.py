import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import json
from datetime import datetime, timedelta
import random

# Set random seed for reproducible data
np.random.seed(42)
random.seed(42)

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

def generate_carrier_data(n_carriers=500):
    """Generate realistic carrier data without pandas dependency"""
    
    # State data with regional clustering
    states = ['GA', 'FL', 'TX', 'NC', 'TN', 'SC', 'AL', 'MS', 'LA', 'AR', 'OK', 'KY', 'VA', 'WV']
    cities = {
        'GA': ['Atlanta', 'Savannah', 'Augusta', 'Columbus'],
        'FL': ['Miami', 'Jacksonville', 'Tampa', 'Orlando'],
        'TX': ['Houston', 'Dallas', 'Austin', 'San Antonio'],
        'NC': ['Charlotte', 'Raleigh', 'Greensboro', 'Asheville'],
        'TN': ['Nashville', 'Memphis', 'Knoxville', 'Chattanooga'],
        'SC': ['Charleston', 'Columbia', 'Greenville', 'Spartanburg'],
        'AL': ['Birmingham', 'Mobile', 'Montgomery', 'Huntsville'],
        'MS': ['Jackson', 'Gulfport', 'Meridian', 'Hattiesburg'],
        'LA': ['New Orleans', 'Baton Rouge', 'Shreveport', 'Lafayette'],
        'AR': ['Little Rock', 'Fort Smith', 'Fayetteville', 'Pine Bluff'],
        'OK': ['Oklahoma City', 'Tulsa', 'Norman', 'Broken Arrow'],
        'KY': ['Louisville', 'Lexington', 'Bowling Green', 'Owensboro'],
        'VA': ['Richmond', 'Norfolk', 'Virginia Beach', 'Newport News'],
        'WV': ['Charleston', 'Huntington', 'Parkersburg', 'Morgantown']
    }
    
    # Company name components
    company_types = ['Transport', 'Logistics', 'Freight', 'Trucking', 'Express', 'Cargo', 'Hauling']
    company_modifiers = ['Southern', 'Regional', 'Interstate', 'Metro', 'Premier', 'Elite', 'Swift']
    
    carriers = []
    
    for i in range(n_carriers):
        state = np.random.choice(states)
        city = np.random.choice(cities[state])
        
        # Generate company name
        modifier = np.random.choice(company_modifiers)
        company_type = np.random.choice(company_types)
        company_name = f"{modifier} {company_type} Co."
        
        # Fleet size with realistic distribution
        fleet_size = int(np.random.lognormal(mean=3.5, sigma=0.8))
        fleet_size = max(10, min(500, fleet_size))  # Cap between 10-500
        
        # Safety metrics with correlations
        base_violation_rate = np.random.exponential(2.5)
        
        # Wage percentile (correlated with safety - worse safety often = lower wages)
        wage_percentile = max(5, min(95, 70 - (base_violation_rate * 8) + np.random.normal(0, 15)))
        
        # Out-of-service rate
        out_of_service_rate = max(0.1, base_violation_rate + np.random.normal(0, 1))
        
        # Crash rate (per million miles)
        crash_rate = max(0.1, np.random.exponential(1.2) + (base_violation_rate * 0.3))
        
        # Safety violations per year
        safety_violations = max(0, int(fleet_size * 0.1 * base_violation_rate + np.random.poisson(2)))
        
        # Calculate risk score (1-10 scale)
        risk_components = [
            min(10, out_of_service_rate / 2),  # Out-of-service contribution
            min(10, crash_rate),  # Crash rate contribution
            min(10, safety_violations / fleet_size * 10),  # Violations per truck
            min(10, (100 - wage_percentile) / 10)  # Wage competitiveness (inverse)
        ]
        risk_score = np.mean(risk_components)
        
        # Annual savings potential (based on fleet size and risk)
        base_savings_per_truck = 25000  # Industry average driver replacement cost
        churn_multiplier = 1 + (risk_score - 5) * 0.1  # Higher risk = higher churn
        annual_savings_potential = fleet_size * base_savings_per_truck * churn_multiplier * 0.4  # 40% reduction
        
        carriers.append({
            'carrier_id': f"USDOT{100000 + i}",
            'carrier_name': company_name,
            'state': state,
            'city': city,
            'fleet_size': fleet_size,
            'wage_percentile': wage_percentile,
            'out_of_service_rate': out_of_service_rate,
            'crash_rate': crash_rate,
            'safety_violations': safety_violations,
            'risk_score': risk_score,
            'annual_savings_potential': annual_savings_potential
        })
    
    return carriers

def generate_state_summary(carrier_data):
    """Generate state-level summary statistics using native Python"""
    
    # Group by state
    state_groups = {}
    for carrier in carrier_data:
        state = carrier['state']
        if state not in state_groups:
            state_groups[state] = []
        state_groups[state].append(carrier)
    
    # Calculate aggregates
    state_summary = []
    for state, carriers in state_groups.items():
        carrier_count = len(carriers)
        avg_risk_score = np.mean([c['risk_score'] for c in carriers])
        total_savings_potential = sum([c['annual_savings_potential'] for c in carriers])
        avg_fleet_size = np.mean([c['fleet_size'] for c in carriers])
        avg_wage_percentile = np.mean([c['wage_percentile'] for c in carriers])
        avg_out_of_service_rate = np.mean([c['out_of_service_rate'] for c in carriers])
        
        state_summary.append({
            'state': state,
            'carrier_count': carrier_count,
            'avg_risk_score': avg_risk_score,
            'total_savings_potential': total_savings_potential,
            'avg_fleet_size': avg_fleet_size,
            'avg_wage_percentile': avg_wage_percentile,
            'avg_out_of_service_rate': avg_out_of_service_rate
        })
    
    return state_summary

def create_risk_heatmap(state_summary):
    """Create choropleth map showing carrier risk by state"""
    
    # Extract data for plotting
    states = [s['state'] for s in state_summary]
    risk_scores = [s['avg_risk_score'] for s in state_summary]
    carrier_counts = [s['carrier_count'] for s in state_summary]
    savings_potential = [s['total_savings_potential'] for s in state_summary]
    
    fig = go.Figure(data=go.Choropleth(
        locations=states,
        z=risk_scores,
        locationmode='USA-states',
        colorscale='Reds',
        text=[f"Carriers: {cc}<br>Savings: ${sp:,.0f}" for cc, sp in zip(carrier_counts, savings_potential)],
        hovertemplate="<b>%{location}</b><br>Risk Score: %{z:.1f}<br>%{text}<extra></extra>",
        colorbar_title="Risk Score (1-10)"
    ))
    
    fig.update_layout(
        title="Carrier Churn Risk by State",
        geo_scope='usa',
        height=500
    )
    
    return fig

def create_safety_trends(carrier_data, months=12):
    """Create time series showing safety violation trends"""
    
    # Get top 5 riskiest carriers
    sorted_carriers = sorted(carrier_data, key=lambda x: x['risk_score'], reverse=True)
    top_carriers = sorted_carriers[:5]
    
    fig = go.Figure()
    
    colors = ['#ef4444', '#f97316', '#eab308', '#22c55e', '#3b82f6']
    
    for i, carrier in enumerate(top_carriers):
        # Generate monthly data
        base_date = datetime.now() - timedelta(days=365)
        dates = [base_date + timedelta(days=30*j) for j in range(months)]
        
        # Base violations with trend
        base_level = carrier['safety_violations'] / 12  # Monthly average
        trend = np.random.normal(0, 0.1, months).cumsum()
        seasonal = [0.2 * np.sin(2 * np.pi * j / 12) for j in range(months)]
        
        violations_current = [max(0, base_level + t + s + np.random.normal(0, 0.5)) 
                            for t, s in zip(trend, seasonal)]
        violations_prior = [max(0, v + np.random.normal(0, 0.3)) for v in violations_current]
        
        # Current year (solid line)
        fig.add_trace(go.Scatter(
            x=dates,
            y=violations_current,
            mode='lines+markers',
            name=f"{carrier['carrier_name']} (Current)",
            line=dict(color=colors[i], width=3),
            marker=dict(size=6)
        ))
        
        # Prior year (dotted line)
        fig.add_trace(go.Scatter(
            x=dates,
            y=violations_prior,
            mode='lines',
            name=f"{carrier['carrier_name']} (Prior Year)",
            line=dict(color=colors[i], width=2, dash='dot'),
            opacity=0.6,
            showlegend=False
        ))
    
    fig.update_layout(
        title="Safety Violation Trends - Top Risk Carriers",
        xaxis_title="Month",
        yaxis_title="Monthly Safety Violations",
        height=400,
        hovermode='x unified'
    )
    
    return fig

def create_savings_ranking(carrier_data):
    """Create horizontal bar chart ranking carriers by savings potential"""
    
    # Sort by savings potential and take top 20
    sorted_carriers = sorted(carrier_data, key=lambda x: x['annual_savings_potential'], reverse=True)
    top_carriers = sorted_carriers[:20]
    
    # Extract data
    carrier_names = [c['carrier_name'] for c in top_carriers]
    savings = [c['annual_savings_potential'] for c in top_carriers]
    risk_scores = [c['risk_score'] for c in top_carriers]
    fleet_sizes = [c['fleet_size'] for c in top_carriers]
    
    # Create risk-based color scale
    colors = ['#dc2626' if risk >= 8 else '#ea580c' if risk >= 6.5 else '#ca8a04' 
              for risk in risk_scores]
    
    fig = go.Figure(data=[
        go.Bar(
            x=savings,
            y=carrier_names,
            orientation='h',
            marker_color=colors,
            text=[f"${x/1000:.0f}K" for x in savings],
            textposition='inside',
            textfont=dict(color='white', weight='bold'),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Savings Potential: $%{x:,.0f}<br>"
                "Risk Score: %{customdata[0]:.1f}/10<br>"
                "Fleet Size: %{customdata[1]} trucks<br>"
                "<extra></extra>"
            ),
            customdata=list(zip(risk_scores, fleet_sizes))
        )
    ])
    
    fig.update_layout(
        title="Top 20 Prospects by Annual Savings Potential",
        xaxis_title="Annual Savings Potential ($)",
        yaxis_title="",
        height=600,
        showlegend=False,
        yaxis=dict(autorange="reversed"),  # Highest values at top
        margin=dict(l=200)  # More space for carrier names
    )
    
    return fig

def filter_carriers(carriers, selected_states, fleet_size_range, risk_threshold):
    """Filter carriers based on user selections"""
    filtered = []
    for carrier in carriers:
        if (carrier['state'] in selected_states and
            fleet_size_range[0] <= carrier['fleet_size'] <= fleet_size_range[1] and
            carrier['risk_score'] >= risk_threshold):
            filtered.append(carrier)
    return filtered

def main():
    # Header
    st.markdown('<h1 class="main-header">🚚 VelocityMatch Carrier Intelligence Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #6b7280; font-size: 1.1rem;">Strategic Sales Intelligence Platform for Driver Retention Solutions</p>', unsafe_allow_html=True)
    
    # Sidebar filters
    st.sidebar.markdown("## 🎛️ Intelligence Filters")
    
    # Generate sample data
    carrier_data = generate_carrier_data()
    state_summary = generate_state_summary(carrier_data)
    
    # Get unique states
    unique_states = list(set([c['state'] for c in carrier_data]))
    
    # Sidebar filter controls
    selected_states = st.sidebar.multiselect(
        "Select States",
        options=unique_states,
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
    filtered_carriers = filter_carriers(carrier_data, selected_states, fleet_size_range, risk_threshold)
    
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
            total_savings = sum([c['annual_savings_potential'] for c in filtered_carriers])
            st.markdown(f"""
            <div class="metric-card">
                <h3>${total_savings/1e6:.1f}M</h3>
                <p>Total Savings Potential</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_risk = np.mean([c['risk_score'] for c in filtered_carriers]) if filtered_carriers else 0
            st.markdown(f"""
            <div class="metric-card">
                <h3>{avg_risk:.1f}/10</h3>
                <p>Average Risk Score</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            market_penetration = len(filtered_carriers) / len(carrier_data) * 100 if carrier_data else 0
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
            top_risk_states = sorted(state_summary, key=lambda x: x['avg_risk_score'], reverse=True)[:5]
            
            for state_data in top_risk_states:
                st.markdown(f"""
                <div class="insight-box">
                    <strong>{state_data['state']}</strong><br>
                    Risk Score: {state_data['avg_risk_score']:.1f}/10
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
            
            if filtered_carriers:
                # Extract data for scatter plot
                wage_percentiles = [c['wage_percentile'] for c in filtered_carriers]
                out_of_service_rates = [c['out_of_service_rate'] for c in filtered_carriers]
                fleet_sizes = [c['fleet_size'] for c in filtered_carriers]
                risk_scores = [c['risk_score'] for c in filtered_carriers]
                carrier_names = [c['carrier_name'] for c in filtered_carriers]
                savings_potential = [c['annual_savings_potential'] for c in filtered_carriers]
                
                scatter_fig = go.Figure(data=go.Scatter(
                    x=wage_percentiles,
                    y=out_of_service_rates,
                    mode='markers',
                    marker=dict(
                        size=[f/10 for f in fleet_sizes],  # Scale fleet size for visibility
                        color=risk_scores,
                        colorscale='Reds',
                        showscale=True,
                        colorbar=dict(title="Risk Score")
                    ),
                    text=[f"{name}<br>Savings: ${sp:,.0f}" for name, sp in zip(carrier_names, savings_potential)],
                    hovertemplate="<b>%{text}</b><br>Wage Percentile: %{x:.0f}%<br>Out-of-Service Rate: %{y:.1f}%<extra></extra>"
                ))
                
                scatter_fig.update_layout(
                    title="Out-of-Service Rate vs. Wage Percentile",
                    xaxis_title="Driver Wage Percentile",
                    yaxis_title="Out-of-Service Rate (%)",
                    height=400
                )
                
                st.plotly_chart(scatter_fig, use_container_width=True)
        
        with col2:
            st.markdown('<h3 class="sub-header">Carrier Profile</h3>', unsafe_allow_html=True)
            
            if filtered_carriers:
                selected_carrier = filtered_carriers[0]
                
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
        ranking_chart = create_savings_ranking(filtered_carriers)
        st.plotly_chart(ranking_chart, use_container_width=True)
        
        st.markdown("---")
        
        # Action panel
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<h3 class="sub-header">Geographic Market Opportunities</h3>', unsafe_allow_html=True)
            
            # Bubble map using state summary
            states = [s['state'] for s in state_summary]
            carrier_counts = [s['carrier_count'] for s in state_summary]
            risk_scores = [s['avg_risk_score'] for s in state_summary]
            savings_potential = [s['total_savings_potential'] for s in state_summary]
            
            bubble_fig = go.Figure(data=go.Scattergeo(
                locations=states,
                locationmode='USA-states',
                mode='markers',
                marker=dict(
                    size=[cc/2 for cc in carrier_counts],  # Scale for visibility
                    color=risk_scores,
                    colorscale='Reds',
                    showscale=True,
                    colorbar=dict(title="Risk Score")
                ),
                text=[f"Carriers: {cc}<br>Total Savings: ${sp:,.0f}" for cc, sp in zip(carrier_counts, savings_potential)],
                hovertemplate="<b>%{location}</b><br>%{text}<br>Risk Score: %{marker.color:.1f}<extra></extra>"
            ))
            
            bubble_fig.update_layout(
                title="Market Concentration and Risk Distribution",
                geo=dict(scope='usa'),
                height=400
            )
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
            
            high_risk_count = len([c for c in filtered_carriers if c['risk_score'] >= 7.5])
            st.metric("Critical Risk Carriers", high_risk_count)
            
            avg_fleet_size = np.mean([c['fleet_size'] for c in filtered_carriers]) if filtered_carriers else 0
            st.metric("Average Fleet Size", f"{avg_fleet_size:.0f} trucks")
            
            competitive_density = np.random.choice(['Low', 'Medium', 'High'], p=[0.4, 0.4, 0.2])
            st.metric("Competitive Density", competitive_density)

if __name__ == "__main__":
    main()
