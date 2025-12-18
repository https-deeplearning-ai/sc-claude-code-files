"""
Business Metrics Calculation Module

This module contains functions to calculate key business metrics
for e-commerce analysis including revenue, orders, product performance,
and customer experience metrics.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional


def calculate_revenue_metrics(
    sales_data: pd.DataFrame,
    current_year: int,
    previous_year: int = None
) -> Dict[str, float]:
    """
    Calculate revenue metrics for a given year and compare with previous year.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with 'price' and 'year' columns
    current_year : int
        Year to calculate metrics for
    previous_year : int, optional
        Previous year for comparison

    Returns
    -------
    Dict[str, float]
        Dictionary containing:
        - total_revenue: Total revenue for current year
        - revenue_growth_pct: Year-over-year growth percentage (if previous_year provided)
        - previous_revenue: Total revenue for previous year (if provided)
    """
    current_revenue = sales_data[sales_data['year'] == current_year]['price'].sum()

    metrics = {
        'total_revenue': current_revenue,
        'year': current_year
    }

    if previous_year is not None:
        previous_revenue = sales_data[sales_data['year'] == previous_year]['price'].sum()
        metrics['previous_revenue'] = previous_revenue

        if previous_revenue > 0:
            growth_pct = ((current_revenue - previous_revenue) / previous_revenue) * 100
            metrics['revenue_growth_pct'] = growth_pct
        else:
            metrics['revenue_growth_pct'] = None

    return metrics


def calculate_monthly_revenue(
    sales_data: pd.DataFrame,
    year: int = None
) -> pd.DataFrame:
    """
    Calculate monthly revenue totals.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with 'price', 'year', and 'month' columns
    year : int, optional
        Filter for specific year

    Returns
    -------
    pd.DataFrame
        Monthly revenue totals with columns: year, month, revenue
    """
    data = sales_data.copy()

    if year is not None:
        data = data[data['year'] == year]

    monthly_revenue = (
        data.groupby(['year', 'month'])['price']
        .sum()
        .reset_index()
        .rename(columns={'price': 'revenue'})
    )

    return monthly_revenue


def calculate_month_over_month_growth(
    sales_data: pd.DataFrame,
    year: int
) -> pd.DataFrame:
    """
    Calculate month-over-month growth rates for a given year.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with 'price', 'year', and 'month' columns
    year : int
        Year to calculate growth for

    Returns
    -------
    pd.DataFrame
        Monthly growth rates with columns: month, growth_pct
    """
    year_data = sales_data[sales_data['year'] == year]

    monthly_revenue = (
        year_data.groupby('month')['price']
        .sum()
    )

    growth_pct = monthly_revenue.pct_change() * 100

    result = pd.DataFrame({
        'month': growth_pct.index,
        'growth_pct': growth_pct.values
    })

    return result


def calculate_average_mom_growth(
    sales_data: pd.DataFrame,
    year: int
) -> float:
    """
    Calculate average month-over-month growth rate for a year.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset
    year : int
        Year to calculate for

    Returns
    -------
    float
        Average monthly growth rate as percentage
    """
    mom_growth = calculate_month_over_month_growth(sales_data, year)
    return mom_growth['growth_pct'].mean()


def calculate_order_metrics(
    sales_data: pd.DataFrame,
    current_year: int,
    previous_year: int = None
) -> Dict[str, float]:
    """
    Calculate order-related metrics including count and average order value.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with 'order_id', 'price', and 'year' columns
    current_year : int
        Year to calculate metrics for
    previous_year : int, optional
        Previous year for comparison

    Returns
    -------
    Dict[str, float]
        Dictionary containing:
        - total_orders: Number of unique orders
        - avg_order_value: Average order value
        - order_growth_pct: Year-over-year order count growth (if previous_year provided)
        - aov_growth_pct: Year-over-year AOV growth (if previous_year provided)
    """
    current_data = sales_data[sales_data['year'] == current_year]

    # Calculate current year metrics
    total_orders = current_data['order_id'].nunique()
    avg_order_value = current_data.groupby('order_id')['price'].sum().mean()

    metrics = {
        'total_orders': total_orders,
        'avg_order_value': avg_order_value,
        'year': current_year
    }

    # Calculate comparison metrics if previous year provided
    if previous_year is not None:
        previous_data = sales_data[sales_data['year'] == previous_year]
        previous_orders = previous_data['order_id'].nunique()
        previous_aov = previous_data.groupby('order_id')['price'].sum().mean()

        metrics['previous_orders'] = previous_orders
        metrics['previous_aov'] = previous_aov

        if previous_orders > 0:
            order_growth = ((total_orders - previous_orders) / previous_orders) * 100
            metrics['order_growth_pct'] = order_growth

        if previous_aov > 0:
            aov_growth = ((avg_order_value - previous_aov) / previous_aov) * 100
            metrics['aov_growth_pct'] = aov_growth

    return metrics


def calculate_product_category_performance(
    sales_data: pd.DataFrame,
    year: int = None,
    top_n: int = None
) -> pd.DataFrame:
    """
    Calculate revenue by product category.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with 'product_category_name' and 'price' columns
    year : int, optional
        Filter for specific year
    top_n : int, optional
        Return only top N categories

    Returns
    -------
    pd.DataFrame
        Product category performance with columns: product_category_name, revenue
        Sorted by revenue in descending order
    """
    data = sales_data.copy()

    if year is not None:
        data = data[data['year'] == year]

    category_revenue = (
        data.groupby('product_category_name')['price']
        .sum()
        .reset_index()
        .rename(columns={'price': 'revenue'})
        .sort_values('revenue', ascending=False)
    )

    if top_n is not None:
        category_revenue = category_revenue.head(top_n)

    return category_revenue


def calculate_geographic_sales(
    sales_data: pd.DataFrame,
    year: int = None,
    top_n: int = None
) -> pd.DataFrame:
    """
    Calculate revenue by geographic location (state).

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with 'customer_state' and 'price' columns
    year : int, optional
        Filter for specific year
    top_n : int, optional
        Return only top N states

    Returns
    -------
    pd.DataFrame
        Geographic sales with columns: customer_state, revenue
        Sorted by revenue in descending order
    """
    data = sales_data.copy()

    if year is not None:
        data = data[data['year'] == year]

    state_revenue = (
        data.groupby('customer_state')['price']
        .sum()
        .reset_index()
        .rename(columns={'price': 'revenue'})
        .sort_values('revenue', ascending=False)
    )

    if top_n is not None:
        state_revenue = state_revenue.head(top_n)

    return state_revenue


def calculate_order_status_distribution(
    orders: pd.DataFrame,
    year: int = None
) -> pd.DataFrame:
    """
    Calculate distribution of order statuses.

    Parameters
    ----------
    orders : pd.DataFrame
        Orders dataset with 'order_status' and 'year' columns
    year : int, optional
        Filter for specific year

    Returns
    -------
    pd.DataFrame
        Order status distribution with columns: order_status, count, percentage
    """
    data = orders.copy()

    if year is not None:
        data = data[data['year'] == year]

    status_counts = data['order_status'].value_counts()
    status_pct = data['order_status'].value_counts(normalize=True) * 100

    result = pd.DataFrame({
        'order_status': status_counts.index,
        'count': status_counts.values,
        'percentage': status_pct.values
    })

    return result


def categorize_delivery_speed(days: float) -> str:
    """
    Categorize delivery speed into time buckets.

    Parameters
    ----------
    days : float
        Number of days for delivery

    Returns
    -------
    str
        Category: '1-3 days', '4-7 days', or '8+ days'
    """
    if pd.isna(days):
        return 'Unknown'
    elif days <= 3:
        return '1-3 days'
    elif days <= 7:
        return '4-7 days'
    else:
        return '8+ days'


def calculate_review_metrics(
    sales_data: pd.DataFrame,
    year: int = None
) -> Dict[str, float]:
    """
    Calculate review-related metrics.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with 'review_score' column
    year : int, optional
        Filter for specific year

    Returns
    -------
    Dict[str, float]
        Dictionary containing:
        - avg_review_score: Average review score
        - review_count: Number of reviews
    """
    data = sales_data.copy()

    if year is not None:
        data = data[data['year'] == year]

    # Get unique order reviews (avoid counting same order multiple times)
    unique_reviews = data.drop_duplicates(subset=['order_id'])

    metrics = {
        'avg_review_score': unique_reviews['review_score'].mean(),
        'review_count': len(unique_reviews),
        'year': year
    }

    return metrics


def calculate_delivery_speed_vs_reviews(
    sales_data: pd.DataFrame,
    year: int = None
) -> pd.DataFrame:
    """
    Analyze relationship between delivery speed and review scores.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with 'delivery_speed_days' and 'review_score' columns
    year : int, optional
        Filter for specific year

    Returns
    -------
    pd.DataFrame
        Average review score by delivery time category
        Columns: delivery_time, avg_review_score, order_count
    """
    data = sales_data.copy()

    if year is not None:
        data = data[data['year'] == year]

    # Remove duplicates to avoid counting same order multiple times
    unique_orders = data.drop_duplicates(subset=['order_id'])

    # Categorize delivery speed
    unique_orders['delivery_time'] = unique_orders['delivery_speed_days'].apply(
        categorize_delivery_speed
    )

    # Calculate average review by delivery time
    result = (
        unique_orders.groupby('delivery_time')
        .agg({
            'review_score': 'mean',
            'order_id': 'count'
        })
        .reset_index()
        .rename(columns={
            'review_score': 'avg_review_score',
            'order_id': 'order_count'
        })
    )

    # Sort by delivery time
    category_order = ['1-3 days', '4-7 days', '8+ days', 'Unknown']
    result['delivery_time'] = pd.Categorical(
        result['delivery_time'],
        categories=category_order,
        ordered=True
    )
    result = result.sort_values('delivery_time')

    return result


def calculate_avg_delivery_time(
    sales_data: pd.DataFrame,
    year: int = None
) -> float:
    """
    Calculate average delivery time in days.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with 'delivery_speed_days' column
    year : int, optional
        Filter for specific year

    Returns
    -------
    float
        Average delivery time in days
    """
    data = sales_data.copy()

    if year is not None:
        data = data[data['year'] == year]

    # Use unique orders to avoid counting same order multiple times
    unique_orders = data.drop_duplicates(subset=['order_id'])

    return unique_orders['delivery_speed_days'].mean()


def calculate_review_distribution(
    sales_data: pd.DataFrame,
    year: int = None
) -> pd.DataFrame:
    """
    Calculate distribution of review scores.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset with 'review_score' column
    year : int, optional
        Filter for specific year

    Returns
    -------
    pd.DataFrame
        Review score distribution with columns: review_score, count, percentage
    """
    data = sales_data.copy()

    if year is not None:
        data = data[data['year'] == year]

    # Use unique orders
    unique_reviews = data.drop_duplicates(subset=['order_id'])

    score_counts = unique_reviews['review_score'].value_counts().sort_index()
    score_pct = unique_reviews['review_score'].value_counts(normalize=True).sort_index() * 100

    result = pd.DataFrame({
        'review_score': score_counts.index,
        'count': score_counts.values,
        'percentage': score_pct.values
    })

    return result
