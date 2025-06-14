import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_risk_heatmap(state_summary):
    """Create choropleth map showing carrier risk by state"""
    
    fig = px.choropleth(
        state_summary,
        locations='state',
        color='avg_risk_score',
        locationmode='USA-states',
        scope='usa',
        color_continuous_scale='Reds',
        hover_data={
            'carrier_count': True,
            'total_savings_potential': ':,.0f',
            'avg_risk_score': ':.1f'
        },
        labels={
            'avg_risk_score': 'Risk Score',
            'carrier_count': 'Carrier Count',
            'total_savings_potential': 'Savings Potential ($)'
        },
        title="Carrier Churn Risk by State"
    )
    
    fig.update_layout(
        height=500,
        showlegend=True,
        coloraxis_colorbar=dict(
            title="Risk Score (1-10)",
            titleside="top",
            tickmode="linear",
            tick0=1,
            dtick=1
        )
    )
    
    return fig

def create_safety_trends(carrier_data, months=12):
    """Create time series showing safety violation trends"""
    
    # Generate sample time series data for top 5 riskiest carriers
    top_carriers = carrier_data.nlargest(5, 'risk_score')
    
    fig = go.Figure()
    
    colors = ['#ef4444', '#f97316', '#eab308', '#22c55e', '#3b82f6']
    
    for i, (_, carrier) in enumerate(top_carriers.iterrows()):
        # Generate monthly data
        dates = pd.date_range(start=datetime.now() - timedelta(days=365), periods=months, freq='M')
        
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
        hovermode='x unified',
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        )
    )
    
    return fig

def create_savings_ranking(carrier_data):
    """Create horizontal bar chart ranking carriers by savings potential"""
    
    # Sort by savings potential
    ranked_carriers = carrier_data.nlargest(20, 'annual_savings_potential').copy()
    
    # Create risk-based color scale
    colors = ['#dc2626' if risk >= 8 else '#ea580c' if risk >= 6.5 else '#ca8a04' 
              for risk in ranked_carriers['risk_score']]
    
    fig = go.Figure(data=[
        go.Bar(
            x=ranked_carriers['annual_savings_potential'],
            y=ranked_carriers['carrier_name'],
            orientation='h',
            marker_color=colors,
            text=[f"${x/1000:.0f}K" for x in ranked_carriers['annual_savings_potential']],
            textposition='inside',
            textfont=dict(color='white', weight='bold'),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Savings Potential: $%{x:,.0f}<br>"
                "Risk Score: %{customdata[0]:.1f}/10<br>"
                "Fleet Size: %{customdata[1]} trucks<br>"
                "<extra></extra>"
            ),
            customdata=list(zip(ranked_carriers['risk_score'], ranked_carriers['fleet_size']))
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
    
    # Add risk score annotation
    fig.add_annotation(
        text="🔴 High Risk (8+) | 🟠 Medium Risk (6.5-8) | 🟡 Moderate Risk (<6.5)",
        xref="paper", yref="paper",
        x=0.5, y=-0.1,
        showarrow=False,
        font=dict(size=10)
    )
    
    return fig

def create_correlation_matrix(carrier_data):
    """Create correlation heatmap of key metrics"""
    
    metrics = ['risk_score', 'out_of_service_rate', 'crash_rate', 'safety_violations', 
               'wage_percentile', 'fleet_size', 'annual_savings_potential']
    
    corr_matrix = carrier_data[metrics].corr()
    
    fig = px.imshow(
        corr_matrix,
        title="Carrier Metrics Correlation Matrix",
        color_continuous_scale='RdBu_r',
        aspect='auto'
    )
    
    fig.update_layout(height=500)
    
    return fig

def create_fleet_size_distribution(carrier_data):
    """Create histogram showing fleet size distribution"""
    
    fig = px.histogram(
        carrier_data,
        x='fleet_size',
        nbins=30,
        title="Fleet Size Distribution",
        labels={'fleet_size': 'Fleet Size (Number of Trucks)', 'count': 'Number of Carriers'},
        color_discrete_sequence=['#3b82f6']
    )
    
    fig.update_layout(
        height=400,
        showlegend=False
    )
    
    return fig

def create_risk_vs_savings_scatter(carrier_data):
    """Create scatter plot showing risk score vs savings potential"""
    
    fig = px.scatter(
        carrier_data,
        x='risk_score',
        y='annual_savings_potential',
        size='fleet_size',
        color='wage_percentile',
        hover_data=['carrier_name', 'state'],
        title="Risk Score vs. Savings Potential",
        labels={
            'risk_score': 'Risk Score (1-10)',
            'annual_savings_potential': 'Annual Savings Potential ($)',
            'wage_percentile': 'Wage Percentile',
            'fleet_size': 'Fleet Size'
        },
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(height=500)
    
    return fig
