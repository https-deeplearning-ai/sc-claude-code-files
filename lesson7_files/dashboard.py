"""
E-commerce Business Analytics Dashboard
A professional Streamlit dashboard for business performance analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings

# Import custom modules
from data_loader import EcommerceDataLoader, load_and_process_data
from business_metrics import BusinessMetricsCalculator

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="E-commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0;
        color: #1f1f1f;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin: 0;
        margin-bottom: 0.5rem;
    }
    
    .metric-trend {
        font-size: 0.8rem;
        margin: 0;
    }
    
    .trend-positive {
        color: #28a745;
    }
    
    .trend-negative {
        color: #dc3545;
    }
    
    
    .bottom-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
    }
    
    .stSelectbox > div > div > div {
        background-color: white;
    }
    
    .stars {
        color: #ffc107;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_dashboard_data():
    """Load and cache data for dashboard"""
    try:
        loader, processed_data = load_and_process_data('ecommerce_data/')
        return loader, processed_data
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None


def format_currency(value):
    """Format currency values with K/M suffixes"""
    if abs(value) >= 1e6:
        return f"${value/1e6:.1f}M"
    elif abs(value) >= 1e3:
        return f"${value/1e3:.0f}K"
    else:
        return f"${value:.0f}"


def format_trend(current, previous):
    """Format trend indicators with arrows and colors"""
    if previous == 0:
        return "N/A"
    
    change_pct = ((current - previous) / previous) * 100
    arrow = "↗" if change_pct > 0 else "↘"
    color_class = "trend-positive" if change_pct > 0 else "trend-negative"
    
    return f'<span class="{color_class}">{arrow} {abs(change_pct):.2f}%</span>'


def create_revenue_trend_chart(current_data, previous_data, current_year, previous_year):
    """Create revenue trend line chart"""
    fig = go.Figure()
    
    # Check if we have multiple months of data
    current_months = current_data['purchase_month'].nunique()
    
    if current_months > 1:
        # Multiple months - show monthly trend
        current_monthly = current_data.groupby('purchase_month')['price'].sum().reset_index()
        fig.add_trace(go.Scatter(
            x=current_monthly['purchase_month'],
            y=current_monthly['price'],
            mode='lines+markers',
            name=f'{current_year}',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8)
        ))
        
        # Previous period line (dashed)
        if previous_data is not None and not previous_data.empty:
            previous_monthly = previous_data.groupby('purchase_month')['price'].sum().reset_index()
            fig.add_trace(go.Scatter(
                x=previous_monthly['purchase_month'],
                y=previous_monthly['price'],
                mode='lines+markers',
                name=f'{previous_year}',
                line=dict(color='#ff7f0e', width=3, dash='dash'),
                marker=dict(size=8)
            ))
        
        fig.update_layout(
            title="Monthly Revenue Trend",
            xaxis_title="Month",
            yaxis_title="Revenue"
        )
    else:
        # Single month - show daily trend if available, otherwise show comparison bar
        current_revenue = current_data['price'].sum()
        previous_revenue = previous_data['price'].sum() if previous_data is not None and not previous_data.empty else 0
        
        fig.add_trace(go.Bar(
            x=[f'{current_year}', f'{previous_year}'],
            y=[current_revenue, previous_revenue],
            marker=dict(color=['#1f77b4', '#ff7f0e']),
            text=[format_currency(current_revenue), format_currency(previous_revenue)],
            textposition='outside'
        ))
        
        fig.update_layout(
            title="Revenue Comparison",
            xaxis_title="Year",
            yaxis_title="Revenue"
        )
    
    # Custom Y-axis formatting function
    def format_yticks(value):
        if value >= 1e6:
            return f"${value/1e6:.0f}M"
        elif value >= 1e3:
            return f"${value/1e3:.0f}K"
        else:
            return f"${value:.0f}"
    
    fig.update_layout(
        showlegend=True,
        hovermode='x unified',
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
        yaxis=dict(
            showgrid=True, 
            gridcolor='#f0f0f0',
            tickformat='$,.0s'  # This will format as K/M
        ),
        height=350,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig


def create_category_chart(sales_data):
    """Create top 10 categories bar chart"""
    if 'product_category_name' not in sales_data.columns:
        return go.Figure().add_annotation(
            text="Product category data not available",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
        )
    
    category_revenue = sales_data.groupby('product_category_name')['price'].sum().sort_values(ascending=True).tail(10)
    
    fig = go.Figure(data=[
        go.Bar(
            y=category_revenue.index,
            x=category_revenue.values,
            orientation='h',
            marker=dict(
                color=category_revenue.values,
                colorscale='Blues',
                showscale=False
            ),
            text=[format_currency(x) for x in category_revenue.values],
            textposition='outside',
            hovertemplate='%{y}<br>Revenue: %{text}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Top 10 Product Categories",
        xaxis_title="Revenue",
        yaxis_title="",
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='#f0f0f0', tickformat='$,.0s'),
        yaxis=dict(showgrid=False),
        height=350,
        margin=dict(t=50, b=50, l=150, r=50)
    )
    
    return fig


def create_state_map(sales_data):
    """Create US choropleth map"""
    if 'customer_state' not in sales_data.columns:
        return go.Figure().add_annotation(
            text="Geographic data not available",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
        )
    
    state_revenue = sales_data.groupby('customer_state')['price'].sum().reset_index()
    state_revenue.columns = ['state', 'revenue']
    
    fig = go.Figure(data=go.Choropleth(
        locations=state_revenue['state'],
        z=state_revenue['revenue'],
        locationmode='USA-states',
        colorscale='Blues',
        showscale=True,
        colorbar=dict(title="Revenue", tickformat='$,.0f')
    ))
    
    fig.update_layout(
        title="Revenue by State",
        geo_scope='usa',
        height=350,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig


def create_satisfaction_delivery_chart(sales_data):
    """Create satisfaction vs delivery time chart"""
    if 'delivery_days' not in sales_data.columns or 'review_score' not in sales_data.columns:
        return go.Figure().add_annotation(
            text="Delivery or review data not available",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
        )
    
    # Categorize delivery days
    def categorize_delivery(days):
        if pd.isna(days):
            return 'Unknown'
        elif days <= 3:
            return '1-3 days'
        elif days <= 7:
            return '4-7 days'
        else:
            return '8+ days'
    
    sales_data['delivery_category'] = sales_data['delivery_days'].apply(categorize_delivery)
    
    # Calculate average review score by delivery category
    delivery_satisfaction = sales_data.groupby('delivery_category')['review_score'].mean().reset_index()
    delivery_satisfaction = delivery_satisfaction[delivery_satisfaction['delivery_category'] != 'Unknown']
    
    # Order categories properly
    category_order = ['1-3 days', '4-7 days', '8+ days']
    delivery_satisfaction['delivery_category'] = pd.Categorical(
        delivery_satisfaction['delivery_category'], 
        categories=category_order, 
        ordered=True
    )
    delivery_satisfaction = delivery_satisfaction.sort_values('delivery_category')
    
    fig = go.Figure(data=[
        go.Bar(
            x=delivery_satisfaction['delivery_category'],
            y=delivery_satisfaction['review_score'],
            marker=dict(color='#1f77b4'),
            text=[f'{x:.2f}' for x in delivery_satisfaction['review_score']],
            textposition='outside',
        )
    ])
    
    fig.update_layout(
        title="Customer Satisfaction vs Delivery Time",
        xaxis_title="Delivery Time",
        yaxis_title="Average Review Score",
        plot_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', range=[0, 5]),
        height=350,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig


def main():
    """Main dashboard function"""
    
    # Load data
    loader, processed_data = load_dashboard_data()
    
    if loader is None:
        st.error("Failed to load data. Please check your data files.")
        return
    
    # Header with title and date filters - aligned as requested
    col1, spacer, col2 = st.columns([3, 1, 2])
    
    with col1:
        st.title("E-commerce Analytics Dashboard")
    
    with col2:
        # Year filter aligned to the right
        orders_data = processed_data['orders']
        available_years = sorted(orders_data['purchase_year'].unique(), reverse=True)
        
        # Set default year to 2023 if available, otherwise use the first year
        default_year_index = 0
        if 2023 in available_years:
            default_year_index = available_years.index(2023)
        
        selected_year = st.selectbox(
            "Select Year",
            options=available_years,
            index=default_year_index,
            key="year_filter"
        )
        
        # Month filter removed as per requirements - using year only
        selected_month = None
    
    # Create datasets based on selected year and month
    current_data = loader.create_sales_dataset(
        year_filter=selected_year,
        month_filter=selected_month,
        status_filter='delivered'
    )
    
    previous_year = selected_year - 1
    previous_data = None
    if previous_year in available_years:
        previous_data = loader.create_sales_dataset(
            year_filter=previous_year,
            month_filter=selected_month,
            status_filter='delivered'
        )
    
    # Calculate metrics
    total_revenue = current_data['price'].sum()
    total_orders = current_data['order_id'].nunique()
    avg_order_value = current_data.groupby('order_id')['price'].sum().mean()
    
    # Calculate previous year metrics for trends
    prev_revenue = previous_data['price'].sum() if previous_data is not None else 0
    prev_orders = previous_data['order_id'].nunique() if previous_data is not None else 0
    prev_aov = previous_data.groupby('order_id')['price'].sum().mean() if previous_data is not None else 0
    
    # Monthly growth calculation
    monthly_data = current_data.groupby('purchase_month')['price'].sum()
    monthly_growth = monthly_data.pct_change().mean() * 100 if len(monthly_data) > 1 else 0
    
    # KPI Row - 4 cards
    st.markdown("### Key Performance Indicators")
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        trend_html = format_trend(total_revenue, prev_revenue)
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Total Revenue</p>
            <p class="metric-value">{format_currency(total_revenue)}</p>
            <p class="metric-trend">{trend_html}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi2:
        color_class = "trend-positive" if monthly_growth > 0 else "trend-negative"
        arrow = "↗" if monthly_growth > 0 else "↘"
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Monthly Growth</p>
            <p class="metric-value">{monthly_growth:.2f}%</p>
            <p class="metric-trend"><span class="{color_class}">{arrow}</span></p>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi3:
        trend_html = format_trend(avg_order_value, prev_aov)
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Average Order Value</p>
            <p class="metric-value">{format_currency(avg_order_value)}</p>
            <p class="metric-trend">{trend_html}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi4:
        trend_html = format_trend(total_orders, prev_orders)
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Total Orders</p>
            <p class="metric-value">{total_orders:,}</p>
            <p class="metric-trend">{trend_html}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Grid - 2x2 layout
    st.markdown("### Performance Analytics")
    
    chart_row1_col1, chart_row1_col2 = st.columns(2)
    chart_row2_col1, chart_row2_col2 = st.columns(2)
    
    with chart_row1_col1:
        revenue_fig = create_revenue_trend_chart(current_data, previous_data, selected_year, previous_year)
        st.plotly_chart(revenue_fig, use_container_width=True)
    
    with chart_row1_col2:
        category_fig = create_category_chart(current_data)
        st.plotly_chart(category_fig, use_container_width=True)
    
    with chart_row2_col1:
        map_fig = create_state_map(current_data)
        st.plotly_chart(map_fig, use_container_width=True)
    
    with chart_row2_col2:
        satisfaction_fig = create_satisfaction_delivery_chart(current_data)
        st.plotly_chart(satisfaction_fig, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bottom Row - 2 cards
    st.markdown("### Customer Experience Metrics")
    
    bottom_col1, bottom_col2 = st.columns(2)
    
    with bottom_col1:
        # Average delivery time
        if 'delivery_days' in current_data.columns:
            avg_delivery = current_data['delivery_days'].mean()
            prev_delivery = previous_data['delivery_days'].mean() if previous_data is not None else 0
            delivery_trend = format_trend(avg_delivery, prev_delivery)
            
            st.markdown(f"""
            <div class="bottom-card">
                <p class="metric-label">Average Delivery Time</p>
                <p class="metric-value">{avg_delivery:.1f} days</p>
                <p class="metric-trend">{delivery_trend}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="bottom-card">
                <p class="metric-label">Average Delivery Time</p>
                <p class="metric-value">N/A</p>
                <p class="metric-trend">Data not available</p>
            </div>
            """, unsafe_allow_html=True)
    
    with bottom_col2:
        # Review Score with large number and stars as specified
        if 'review_score' in current_data.columns:
            avg_review = current_data['review_score'].mean()
            stars = "★" * int(round(avg_review)) + "☆" * (5 - int(round(avg_review)))
            
            st.markdown(f"""
            <div class="bottom-card">
                <p class="metric-value" style="font-size: 3rem; margin-bottom: 0.5rem;">{avg_review:.1f}</p>
                <p class="stars" style="font-size: 1.5rem; margin: 0.5rem 0;">{stars}</p>
                <p class="metric-label" style="margin-top: 0.5rem;">Average Review Score</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="bottom-card">
                <p class="metric-label">Average Review Score</p>
                <p class="metric-value">N/A</p>
                <p class="metric-trend">Data not available</p>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()