"""
Professional E-commerce Analytics Dashboard
Converted from EDA_Refactored.ipynb with exact layout specifications
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
from datetime import datetime, date
from data_loader import EcommerceDataLoader, load_and_process_data
from business_metrics import BusinessMetricsCalculator

# Configure page
st.set_page_config(
    page_title="E-commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e9ecef;
        height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-title {
        font-size: 0.875rem;
        color: #6c757d;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #212529;
        margin-bottom: 0.25rem;
    }
    
    .trend-indicator {
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .trend-positive {
        color: #28a745;
    }
    
    .trend-negative {
        color: #dc3545;
    }
    
    .chart-container {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e9ecef;
        margin-bottom: 1rem;
    }
    
    .bottom-card {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 0.5rem;
        border: 1px solid #e9ecef;
        height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
    }
    
    .star-rating {
        color: #ffc107;
        font-size: 1.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

@st.cache_data
def load_dashboard_data():
    """Load and cache dashboard data"""
    loader = EcommerceDataLoader('ecommerce_data/')
    loader.load_raw_data()
    processed_data = loader.process_all_data()
    sales_data = loader.create_sales_dataset(
        year_filter=None,
        month_filter=None,
        status_filter='delivered'
    )
    return sales_data

def format_currency(value, compact=True):
    """Format currency values"""
    if compact:
        if value >= 1_000_000:
            return f"${value/1_000_000:.1f}M"
        elif value >= 1_000:
            return f"${value/1_000:.0f}K"
        else:
            return f"${value:.0f}"
    else:
        return f"${value:,.2f}"

def format_trend_indicator(current, previous):
    """Format trend indicator with arrow and color"""
    if previous == 0:
        return "N/A", "color: #6c757d;"
    
    change = ((current - previous) / previous) * 100
    arrow = "↑" if change >= 0 else "↓"
    color = "color: #28a745;" if change >= 0 else "color: #dc3545;"
    
    return f"{arrow} {change:.2f}%", color

def create_revenue_trend_chart(sales_data, current_year, previous_year):
    """Create revenue trend line chart"""
    # Current year data
    current_data = sales_data[sales_data['purchase_year'] == current_year]
    current_monthly = current_data.groupby('purchase_month')['price'].sum().reset_index()
    current_monthly.columns = ['Month', 'Revenue']
    
    # Previous year data
    previous_data = sales_data[sales_data['purchase_year'] == previous_year]
    previous_monthly = previous_data.groupby('purchase_month')['price'].sum().reset_index()
    previous_monthly.columns = ['Month', 'Revenue']
    
    fig = go.Figure()
    
    # Current year (solid line)
    fig.add_trace(go.Scatter(
        x=current_monthly['Month'],
        y=current_monthly['Revenue'],
        mode='lines+markers',
        name=f'{current_year}',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))
    
    # Previous year (dashed line)
    fig.add_trace(go.Scatter(
        x=previous_monthly['Month'],
        y=previous_monthly['Revenue'],
        mode='lines+markers',
        name=f'{previous_year}',
        line=dict(color='#ff7f0e', width=3, dash='dash'),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='Monthly Revenue Trend',
        xaxis_title='Month',
        yaxis_title='Revenue',
        showlegend=True,
        height=400,
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(
            showgrid=True, 
            gridcolor='rgba(0,0,0,0.1)',
            tickformat='$,.0s'
        ),
        plot_bgcolor='white'
    )
    
    return fig

def create_top_categories_chart(sales_data, year):
    """Create top 10 categories pie chart"""
    year_data = sales_data[sales_data['purchase_year'] == year]
    
    if 'product_category_name' not in year_data.columns:
        fig = go.Figure()
        fig.add_annotation(text="Product category data not available", 
                          x=0.5, y=0.5, showarrow=False)
        return fig
    
    category_revenue = year_data.groupby('product_category_name')['price'].sum().sort_values(ascending=False).head(10)
    
    # Create labels with formatted category names
    labels = [cat.replace('_', ' ').title() for cat in category_revenue.index]
    
    # Create diverse color palette for pie chart
    colors = px.colors.qualitative.Set3[:len(category_revenue)]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=category_revenue.values,
        marker=dict(colors=colors),
        textinfo='label+percent',
        textposition='auto',
        hovertemplate='<b>%{label}</b><br>Revenue: %{customdata}<br>Percentage: %{percent}<extra></extra>',
        customdata=[format_currency(val) for val in category_revenue.values]
    )])
    
    fig.update_layout(
        title='Top 10 Product Categories by Revenue',
        height=400,
        showlegend=False,  # Remove legend since labels are on the pie slices
        plot_bgcolor='white'
    )
    
    return fig

def create_state_map(sales_data, year):
    """Create US choropleth map"""
    year_data = sales_data[sales_data['purchase_year'] == year]
    
    if 'customer_state' not in year_data.columns:
        fig = go.Figure()
        fig.add_annotation(text="Geographic data not available", 
                          x=0.5, y=0.5, showarrow=False)
        return fig
    
    state_revenue = year_data.groupby('customer_state')['price'].sum().reset_index()
    state_revenue.columns = ['State', 'Revenue']
    
    fig = px.choropleth(
        state_revenue,
        locations='State',
        color='Revenue',
        locationmode='USA-states',
        scope='usa',
        title='Revenue by State',
        color_continuous_scale='Blues',
        labels={'Revenue': 'Revenue ($)'}
    )
    
    fig.update_layout(
        height=400,
        geo=dict(showframe=False, showcoastlines=True)
    )
    
    return fig

def create_satisfaction_delivery_chart(sales_data, year):
    """Create satisfaction vs delivery time chart"""
    year_data = sales_data[sales_data['purchase_year'] == year]
    
    if 'review_score' not in year_data.columns or 'delivery_days' not in year_data.columns:
        fig = go.Figure()
        fig.add_annotation(text="Review or delivery data not available", 
                          x=0.5, y=0.5, showarrow=False)
        return fig
    
    # Remove duplicates for order-level analysis
    order_data = year_data.drop_duplicates('order_id').copy()
    order_data = order_data.dropna(subset=['delivery_days', 'review_score'])
    
    # Create delivery time buckets
    order_data['delivery_bucket'] = pd.cut(
        order_data['delivery_days'], 
        bins=[0, 3, 7, float('inf')], 
        labels=['1-3 days', '4-7 days', '8+ days']
    )
    
    satisfaction_by_speed = order_data.groupby('delivery_bucket')['review_score'].mean().reset_index()
    
    fig = go.Figure(go.Bar(
        x=satisfaction_by_speed['delivery_bucket'],
        y=satisfaction_by_speed['review_score'],
        marker_color=['#2ca02c', '#ff7f0e', '#d62728'],
        text=[f'{score:.2f}' for score in satisfaction_by_speed['review_score']],
        textposition='outside'
    ))
    
    fig.update_layout(
        title='Average Review Score by Delivery Speed',
        xaxis_title='Delivery Time',
        yaxis_title='Average Review Score',
        height=400,
        yaxis=dict(range=[0, 5]),
        plot_bgcolor='white'
    )
    
    return fig

def main():
    # Load data
    if not st.session_state.data_loaded:
        with st.spinner("Loading data..."):
            sales_data = load_dashboard_data()
            st.session_state.sales_data = sales_data
            st.session_state.data_loaded = True
    
    sales_data = st.session_state.sales_data
    
    # Available years for filtering
    available_years = sorted(sales_data['purchase_year'].unique(), reverse=True)
    
    # Header with title and date filter
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown('<div class="main-header">E-commerce Analytics Dashboard</div>', unsafe_allow_html=True)
    
    with col2:
        # Set 2023 as default year
        default_index = 0
        if 2023 in available_years:
            default_index = available_years.index(2023)
        
        selected_year = st.selectbox(
            "Select Year",
            available_years,
            index=default_index,
            key="year_filter"
        )
    
    current_year = selected_year
    previous_year = current_year - 1 if current_year - 1 in available_years else None
    
    # Initialize metrics calculator
    metrics_calculator = BusinessMetricsCalculator(sales_data)
    
    # Calculate metrics
    revenue_metrics = metrics_calculator.calculate_revenue_metrics(current_year, previous_year)
    monthly_trends = metrics_calculator.calculate_monthly_trends(current_year)
    satisfaction_metrics = metrics_calculator.analyze_customer_satisfaction(current_year)
    delivery_metrics = metrics_calculator.analyze_delivery_performance(current_year)
    
    # KPI Row - 4 cards
    st.markdown("### Key Performance Indicators")
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    with kpi_col1:
        trend_text, trend_color = format_trend_indicator(
            revenue_metrics['total_revenue'], 
            revenue_metrics.get('previous_year_revenue', 0)
        ) if previous_year else ("N/A", "color: #6c757d;")
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Revenue</div>
            <div class="metric-value">{format_currency(revenue_metrics['total_revenue'])}</div>
            <div class="trend-indicator" style="{trend_color}">{trend_text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col2:
        avg_growth = monthly_trends['revenue_growth'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Monthly Growth</div>
            <div class="metric-value">{avg_growth:.2f}%</div>
            <div class="trend-indicator" style="color: #6c757d;">Average</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col3:
        trend_text, trend_color = format_trend_indicator(
            revenue_metrics['average_order_value'], 
            revenue_metrics.get('previous_year_aov', 0)
        ) if previous_year else ("N/A", "color: #6c757d;")
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Average Order Value</div>
            <div class="metric-value">{format_currency(revenue_metrics['average_order_value'], False)}</div>
            <div class="trend-indicator" style="{trend_color}">{trend_text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col4:
        trend_text, trend_color = format_trend_indicator(
            revenue_metrics['total_orders'], 
            revenue_metrics.get('previous_year_orders', 0)
        ) if previous_year else ("N/A", "color: #6c757d;")
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Orders</div>
            <div class="metric-value">{revenue_metrics['total_orders']:,}</div>
            <div class="trend-indicator" style="{trend_color}">{trend_text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Grid - 2x2 layout
    st.markdown("### Performance Analytics")
    
    chart_row1_col1, chart_row1_col2 = st.columns(2)
    chart_row2_col1, chart_row2_col2 = st.columns(2)
    
    with chart_row1_col1:
        if previous_year:
            fig_revenue = create_revenue_trend_chart(sales_data, current_year, previous_year)
            st.plotly_chart(fig_revenue, use_container_width=True)
        else:
            st.info("Previous year data not available for trend comparison")
    
    with chart_row1_col2:
        fig_categories = create_top_categories_chart(sales_data, current_year)
        st.plotly_chart(fig_categories, use_container_width=True)
    
    with chart_row2_col1:
        fig_map = create_state_map(sales_data, current_year)
        st.plotly_chart(fig_map, use_container_width=True)
    
    with chart_row2_col2:
        fig_satisfaction = create_satisfaction_delivery_chart(sales_data, current_year)
        st.plotly_chart(fig_satisfaction, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bottom Row - 2 cards
    st.markdown("### Customer Experience Metrics")
    bottom_col1, bottom_col2 = st.columns(2)
    
    with bottom_col1:
        if 'error' not in delivery_metrics:
            # Calculate trend for delivery time (assuming previous year comparison)
            if previous_year:
                prev_delivery = metrics_calculator.analyze_delivery_performance(previous_year)
                if 'error' not in prev_delivery:
                    trend_text, trend_color = format_trend_indicator(
                        delivery_metrics['avg_delivery_days'],
                        prev_delivery['avg_delivery_days']
                    )
                else:
                    trend_text, trend_color = "N/A", "color: #6c757d;"
            else:
                trend_text, trend_color = "N/A", "color: #6c757d;"
            
            st.markdown(f"""
            <div class="bottom-card">
                <div class="metric-title">Average Delivery Time</div>
                <div class="metric-value">{delivery_metrics['avg_delivery_days']:.1f} days</div>
                <div class="trend-indicator" style="{trend_color}">{trend_text}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="bottom-card">
                <div class="metric-title">Average Delivery Time</div>
                <div class="metric-value">N/A</div>
                <div class="trend-indicator" style="color: #6c757d;">Data not available</div>
            </div>
            """, unsafe_allow_html=True)
    
    with bottom_col2:
        if 'error' not in satisfaction_metrics:
            # Create star rating display
            score = satisfaction_metrics['avg_review_score']
            full_stars = int(score)
            partial_star = score - full_stars
            stars = "★" * full_stars
            if partial_star >= 0.5:
                stars += "☆"
            
            st.markdown(f"""
            <div class="bottom-card">
                <div class="metric-value">{score:.2f}</div>
                <div class="star-rating">{stars}</div>
                <div class="metric-title">Average Review Score</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="bottom-card">
                <div class="metric-value">N/A</div>
                <div class="star-rating">☆☆☆☆☆</div>
                <div class="metric-title">Average Review Score</div>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()