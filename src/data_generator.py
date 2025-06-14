import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducible data
np.random.seed(42)
random.seed(42)

def generate_carrier_data(n_carriers=500):
    """Generate realistic carrier data simulating FMCSA and BLS datasets"""
    
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
    
    return pd.DataFrame(carriers)

def generate_state_summary():
    """Generate state-level summary statistics"""
    
    carrier_data = generate_carrier_data()
    
    state_summary = carrier_data.groupby('state').agg({
        'carrier_id': 'count',
        'risk_score': 'mean',
        'annual_savings_potential': 'sum',
        'fleet_size': 'mean',
        'wage_percentile': 'mean',
        'out_of_service_rate': 'mean'
    }).reset_index()
    
    state_summary.columns = [
        'state', 'carrier_count', 'avg_risk_score', 'total_savings_potential',
        'avg_fleet_size', 'avg_wage_percentile', 'avg_out_of_service_rate'
    ]
    
    return state_summary

def generate_time_series_data(carrier_id, months=24):
    """Generate monthly safety violation data for trend analysis"""
    
    start_date = datetime.now() - timedelta(days=months*30)
    dates = [start_date + timedelta(days=30*i) for i in range(months)]
    
    # Base trend with seasonal variation
    base_violations = np.random.poisson(3, months)
    seasonal_factor = [1 + 0.3 * np.sin(2 * np.pi * i / 12) for i in range(months)]
    
    violations = [max(0, int(base * seasonal)) for base, seasonal in zip(base_violations, seasonal_factor)]
    
    return pd.DataFrame({
        'date': dates,
        'carrier_id': carrier_id,
        'safety_violations': violations,
        'month_year': [d.strftime('%Y-%m') for d in dates]
    })

if __name__ == "__main__":
    # Test data generation
    carriers = generate_carrier_data(100)
    print("Sample carrier data:")
    print(carriers.head())
    
    state_summary = generate_state_summary()
    print("\nState summary:")
    print(state_summary.head())
