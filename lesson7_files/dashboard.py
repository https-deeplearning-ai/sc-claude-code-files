"""
E-Commerce Business Analytics Dashboard

A professional Streamlit dashboard for analyzing e-commerce business metrics.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import custom modules
from data_loader import (
    load_all_datasets,
    prepare_orders_data,
    prepare_reviews_data,
    create_sales_dataset,
    enrich_sales_with_products,
    enrich_sales_with_geography,
    enrich_sales_with_reviews
)
from business_metrics import (
    calculate_revenue_metrics,
    calculate_monthly_revenue,
    calculate_average_mom_growth,
    calculate_order_metrics,
    calculate_product_category_performance,
    calculate_geographic_sales,
    calculate_review_metrics,
    calculate_delivery_speed_vs_reviews,
    calculate_avg_delivery_time
)

# Page configuration
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
    <style>
    /* Force light mode */
    .stApp {
        background-color: #FAFAFA;
    }

    /* Main container */
    .main {
        padding: 0rem 1rem;
    }

    /* KPI Card Styling */
    .kpi-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .kpi-title {
        font-size: 14px;
        color: #666666;
        font-weight: 500;
        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 32px;
        font-weight: bold;
        color: #1f1f1f;
        margin-bottom: 8px;
    }

    .kpi-trend {
        font-size: 14px;
        font-weight: 600;
    }

    .trend-positive {
        color: #06A77D;
    }

    .trend-negative {
        color: #D62828;
    }

    /* Bottom Card Styling */
    .bottom-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 25px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .bottom-card-title {
        font-size: 14px;
        color: #666666;
        font-weight: 500;
        margin-bottom: 10px;
    }

    .bottom-card-value {
        font-size: 48px;
        font-weight: bold;
        color: #1f1f1f;
        margin-bottom: 8px;
    }

    .stars {
        font-size: 24px;
        color: #FFB800;
        margin-top: 5px;
    }

    /* Header */
    .header-container {
        padding: 20px 0;
        margin-bottom: 10px;
    }

    .header-title {
        font-size: 48px;
        font-weight: 800;
        background: linear-gradient(135deg, #2E86AB 0%, #06A77D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }

    .header-subtitle {
        font-size: 16px;
        color: #666666;
        font-weight: 400;
        margin-top: 0;
        padding-left: 2px;
    }

    .header-divider {
        height: 4px;
        background: linear-gradient(90deg, #2E86AB 0%, #06A77D 50%, transparent 100%);
        border-radius: 2px;
        margin-top: 10px;
        margin-bottom: 20px;
    }

    /* Chart container */
    .chart-container {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 400px;
    }

    /* Remove streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load and prepare all datasets."""
    # Load datasets
    datasets = load_all_datasets('ecommerce_data')

    # Prepare datasets
    orders = prepare_orders_data(datasets['orders'])
    reviews = prepare_reviews_data(datasets['reviews'])

    # Create sales dataset
    sales_data = create_sales_dataset(orders, datasets['order_items'], status_filter='delivered')

    # Enrich with additional information
    sales_data = enrich_sales_with_products(sales_data, datasets['products'])
    sales_data = enrich_sales_with_geography(sales_data, orders, datasets['customers'])
    sales_data = enrich_sales_with_reviews(sales_data, reviews)

    return sales_data, orders


def format_currency(value):
    """Format currency values with K/M suffix."""
    if value >= 1_000_000:
        return f"${value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"${value/1_000:.0f}K"
    else:
        return f"${value:.0f}"


def create_kpi_card(title, value, trend_value=None, is_currency=True, is_percentage=False):
    """Create a KPI card with trend indicator."""
    if is_currency:
        formatted_value = format_currency(value)
    elif is_percentage:
        formatted_value = f"{value:.2f}%"
    else:
        formatted_value = f"{value:,.0f}"

    trend_html = ""
    if trend_value is not None:
        trend_color = "trend-positive" if trend_value >= 0 else "trend-negative"
        trend_arrow = "↑" if trend_value >= 0 else "↓"
        trend_html = f'<div class="kpi-trend {trend_color}">{trend_arrow} {abs(trend_value):.2f}% vs last year</div>'

    card_html = f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{formatted_value}</div>
        {trend_html}
    </div>
    """
    return card_html


def create_bottom_card(title, value, subtitle="", is_trend=False, trend_value=None):
    """Create a bottom row card."""
    trend_html = ""
    if is_trend and trend_value is not None:
        trend_color = "trend-positive" if trend_value >= 0 else "trend-negative"
        trend_arrow = "↑" if trend_value >= 0 else "↓"
        trend_html = f'<div class="kpi-trend {trend_color}" style="margin-top: 8px;">{trend_arrow} {abs(trend_value):.2f}% vs last year</div>'

    card_html = f"""
    <div class="bottom-card">
        <div class="bottom-card-title">{subtitle if subtitle else title}</div>
        <div class="bottom-card-value">{value}</div>
        {trend_html}
    </div>
    """
    return card_html


def create_revenue_trend_chart(sales_data, current_year, previous_year):
    """Create revenue trend line chart comparing current vs previous year."""
    # Get monthly data for both years
    current_monthly = calculate_monthly_revenue(sales_data, current_year)
    previous_monthly = calculate_monthly_revenue(sales_data, previous_year)

    # Create figure
    fig = go.Figure()

    # Add current year line (solid)
    fig.add_trace(go.Scatter(
        x=current_monthly['month'],
        y=current_monthly['revenue'],
        mode='lines+markers',
        name=str(current_year),
        line=dict(color='#2E86AB', width=3),
        marker=dict(size=8)
    ))

    # Add previous year line (dashed)
    fig.add_trace(go.Scatter(
        x=previous_monthly['month'],
        y=previous_monthly['revenue'],
        mode='lines+markers',
        name=str(previous_year),
        line=dict(color='#A9A9A9', width=2, dash='dash'),
        marker=dict(size=6)
    ))

    # Update layout
    fig.update_layout(
        title="Monthly Revenue Trend",
        xaxis_title="Month",
        yaxis_title="Revenue",
        hovermode='x unified',
        plot_bgcolor='white',
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            showgrid=True,
            gridcolor='#f0f0f0'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#f0f0f0',
            tickformat='$,.0f',
            tickprefix='$',
            ticksuffix='K',
            tickmode='linear',
        )
    )

    # Format y-axis to show K/M
    fig.update_yaxes(tickvals=None)

    return fig


def create_category_chart(sales_data, year):
    """Create top 10 categories bar chart."""
    category_data = calculate_product_category_performance(sales_data, year, top_n=10)

    # Create gradient colors (lighter for lower values)
    colors = [f'rgba(46, 134, 171, {0.4 + (i * 0.06)})'
              for i in range(len(category_data)-1, -1, -1)]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=category_data['product_category_name'],
        x=category_data['revenue'],
        orientation='h',
        marker=dict(color=colors),
        text=[format_currency(v) for v in category_data['revenue']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Revenue: $%{x:,.0f}<extra></extra>'
    ))

    fig.update_layout(
        title="Top 10 Product Categories",
        xaxis_title="Revenue",
        yaxis_title="",
        plot_bgcolor='white',
        height=350,
        margin=dict(l=20, r=80, t=40, b=20),
        xaxis=dict(showgrid=False),
        yaxis=dict(autorange="reversed")
    )

    return fig


def create_state_map(sales_data, year):
    """Create US choropleth map for revenue by state."""
    state_data = calculate_geographic_sales(sales_data, year)

    fig = px.choropleth(
        state_data,
        locations='customer_state',
        color='revenue',
        locationmode='USA-states',
        scope='usa',
        title='Revenue by State',
        color_continuous_scale='Blues',
        labels={'revenue': 'Revenue', 'customer_state': 'State'}
    )

    fig.update_layout(
        height=350,
        margin=dict(l=0, r=0, t=40, b=0),
        geo=dict(bgcolor='rgba(0,0,0,0)')
    )

    return fig


def create_delivery_satisfaction_chart(sales_data, year):
    """Create delivery time vs satisfaction bar chart."""
    delivery_data = calculate_delivery_speed_vs_reviews(sales_data, year)

    # Filter out 'Unknown' if present
    delivery_data = delivery_data[delivery_data['delivery_time'] != 'Unknown']

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=delivery_data['delivery_time'],
        y=delivery_data['avg_review_score'],
        marker=dict(color='#2E86AB'),
        text=[f"{v:.2f}" for v in delivery_data['avg_review_score']],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Avg Review: %{y:.2f}<extra></extra>'
    ))

    fig.update_layout(
        title="Customer Satisfaction by Delivery Speed",
        xaxis_title="Delivery Time",
        yaxis_title="Average Review Score",
        plot_bgcolor='white',
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
        yaxis=dict(range=[0, 5], showgrid=True, gridcolor='#f0f0f0'),
        xaxis=dict(showgrid=False)
    )

    return fig


# Main app
def main():
    # Load data
    sales_data, orders = load_data()

    # Get available years
    available_years = sorted(sales_data['year'].unique(), reverse=True)

    # Header section
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.markdown('''
            <div class="header-container">
                <h1 class="header-title">E-Commerce Analytics Dashboard</h1>
                <p class="header-subtitle">Real-time business insights and performance metrics</p>
            </div>
        ''', unsafe_allow_html=True)

    with col2:
        # Set default to 2023 if available, otherwise use most recent year
        default_year_index = available_years.index(2023) if 2023 in available_years else 0
        selected_year = st.selectbox(
            "Select Year",
            options=available_years,
            index=default_year_index,
            key="year_filter"
        )

    with col3:
        month_options = ["All Months"] + [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        selected_month = st.selectbox(
            "Select Month",
            options=month_options,
            index=0,
            key="month_filter"
        )

    # Add visual divider
    st.markdown('<div class="header-divider"></div>', unsafe_allow_html=True)

    # Convert month selection to number (None for "All Months")
    month_num = None if selected_month == "All Months" else month_options.index(selected_month)

    # Filter data by selected year and month
    filtered_sales = sales_data[sales_data['year'] == selected_year].copy()
    if month_num is not None:
        filtered_sales = filtered_sales[filtered_sales['month'] == month_num]

    # Filter previous year data for comparison
    current_year = selected_year
    previous_year = selected_year - 1 if (selected_year - 1) in available_years else None

    if previous_year:
        prev_filtered_sales = sales_data[sales_data['year'] == previous_year].copy()
        if month_num is not None:
            prev_filtered_sales = prev_filtered_sales[prev_filtered_sales['month'] == month_num]
        # Combine for metrics that need both years
        comparison_sales = pd.concat([filtered_sales, prev_filtered_sales])
    else:
        comparison_sales = filtered_sales

    # Calculate all metrics using filtered data
    revenue_metrics = calculate_revenue_metrics(comparison_sales, current_year, previous_year)
    order_metrics = calculate_order_metrics(comparison_sales, current_year, previous_year)

    # Only calculate MoM growth if viewing all months
    if month_num is None:
        mom_growth = calculate_average_mom_growth(filtered_sales, current_year)
    else:
        mom_growth = 0  # Not applicable for single month

    review_metrics = calculate_review_metrics(filtered_sales, current_year)
    avg_delivery = calculate_avg_delivery_time(filtered_sales, current_year)

    # Calculate previous year metrics for trends
    if previous_year:
        prev_delivery = calculate_avg_delivery_time(prev_filtered_sales, previous_year)
        prev_review = calculate_review_metrics(prev_filtered_sales, previous_year)
        delivery_trend = ((avg_delivery - prev_delivery) / prev_delivery) * 100 if prev_delivery > 0 else None
        review_trend = ((review_metrics['avg_review_score'] - prev_review['avg_review_score']) / prev_review['avg_review_score']) * 100 if prev_review['avg_review_score'] > 0 else None
    else:
        delivery_trend = None
        review_trend = None

    # KPI Row
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

    with kpi_col1:
        st.markdown(
            create_kpi_card(
                "Total Revenue",
                revenue_metrics['total_revenue'],
                revenue_metrics.get('revenue_growth_pct')
            ),
            unsafe_allow_html=True
        )

    with kpi_col2:
        st.markdown(
            create_kpi_card(
                "Monthly Growth",
                mom_growth,
                is_currency=False,
                is_percentage=True
            ),
            unsafe_allow_html=True
        )

    with kpi_col3:
        st.markdown(
            create_kpi_card(
                "Average Order Value",
                order_metrics['avg_order_value'],
                order_metrics.get('aov_growth_pct')
            ),
            unsafe_allow_html=True
        )

    with kpi_col4:
        st.markdown(
            create_kpi_card(
                "Total Orders",
                order_metrics['total_orders'],
                order_metrics.get('order_growth_pct'),
                is_currency=False
            ),
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts Grid (2x2)
    chart_row1_col1, chart_row1_col2 = st.columns(2)

    with chart_row1_col1:
        if previous_year and month_num is None:
            fig = create_revenue_trend_chart(sales_data, current_year, previous_year)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            if month_num is not None:
                st.info("Revenue trend comparison is only available when viewing all months")
            else:
                st.info("Previous year data not available for comparison")

    with chart_row1_col2:
        fig = create_category_chart(filtered_sales, current_year)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    chart_row2_col1, chart_row2_col2 = st.columns(2)

    with chart_row2_col1:
        fig = create_state_map(filtered_sales, current_year)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with chart_row2_col2:
        fig = create_delivery_satisfaction_chart(filtered_sales, current_year)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<br>", unsafe_allow_html=True)

    # Bottom Row
    bottom_col1, bottom_col2 = st.columns(2)

    with bottom_col1:
        st.markdown(
            create_bottom_card(
                "Average Delivery Time",
                f"{avg_delivery:.1f} days",
                subtitle="Average Delivery Time",
                is_trend=True,
                trend_value=delivery_trend
            ),
            unsafe_allow_html=True
        )

    with bottom_col2:
        # Create stars based on review score
        full_stars = int(review_metrics['avg_review_score'])
        partial_star = review_metrics['avg_review_score'] - full_stars
        stars = "★" * full_stars
        if partial_star >= 0.5:
            stars += "☆"

        card_html = f"""
        <div class="bottom-card">
            <div class="bottom-card-title">Average Review Score</div>
            <div class="bottom-card-value">{review_metrics['avg_review_score']:.2f}</div>
            <div class="stars">{stars}</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
