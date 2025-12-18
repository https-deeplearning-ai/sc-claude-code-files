"""
Data Loading and Preprocessing Module

This module handles loading e-commerce datasets and performing
initial data cleaning and transformation operations.
"""

import pandas as pd
from typing import Dict, Tuple
import warnings
warnings.filterwarnings('ignore')


def load_all_datasets(data_dir: str = 'ecommerce_data') -> Dict[str, pd.DataFrame]:
    """
    Load all e-commerce datasets from CSV files.

    Parameters
    ----------
    data_dir : str
        Directory containing the CSV files

    Returns
    -------
    Dict[str, pd.DataFrame]
        Dictionary containing all loaded datasets with keys:
        'orders', 'order_items', 'products', 'customers', 'reviews'
    """
    datasets = {}

    # Load each dataset
    datasets['orders'] = pd.read_csv(f'{data_dir}/orders_dataset.csv')
    datasets['order_items'] = pd.read_csv(f'{data_dir}/order_items_dataset.csv')
    datasets['products'] = pd.read_csv(f'{data_dir}/products_dataset.csv')
    datasets['customers'] = pd.read_csv(f'{data_dir}/customers_dataset.csv')
    datasets['reviews'] = pd.read_csv(f'{data_dir}/order_reviews_dataset.csv')

    return datasets


def prepare_orders_data(orders: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare orders dataset by converting date columns and extracting time features.

    Parameters
    ----------
    orders : pd.DataFrame
        Raw orders dataset

    Returns
    -------
    pd.DataFrame
        Processed orders dataset with datetime columns and extracted features
    """
    orders_clean = orders.copy()

    # Convert date columns to datetime
    date_columns = [
        'order_purchase_timestamp',
        'order_approved_at',
        'order_delivered_carrier_date',
        'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]

    for col in date_columns:
        orders_clean[col] = pd.to_datetime(orders_clean[col])

    # Extract year and month from purchase timestamp
    orders_clean['year'] = orders_clean['order_purchase_timestamp'].dt.year
    orders_clean['month'] = orders_clean['order_purchase_timestamp'].dt.month

    return orders_clean


def prepare_reviews_data(reviews: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare reviews dataset by converting date columns.

    Parameters
    ----------
    reviews : pd.DataFrame
        Raw reviews dataset

    Returns
    -------
    pd.DataFrame
        Processed reviews dataset
    """
    reviews_clean = reviews.copy()

    # Convert date columns to datetime
    reviews_clean['review_creation_date'] = pd.to_datetime(reviews_clean['review_creation_date'])
    reviews_clean['review_answer_timestamp'] = pd.to_datetime(reviews_clean['review_answer_timestamp'])

    return reviews_clean


def create_sales_dataset(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    status_filter: str = 'delivered'
) -> pd.DataFrame:
    """
    Create a combined sales dataset by merging orders and order items.
    Filters for delivered orders by default.

    Parameters
    ----------
    orders : pd.DataFrame
        Processed orders dataset
    order_items : pd.DataFrame
        Order items dataset
    status_filter : str
        Order status to filter for (default: 'delivered')

    Returns
    -------
    pd.DataFrame
        Combined sales dataset with order and item information
    """
    # Merge order items with order information
    sales_data = pd.merge(
        left=order_items[['order_id', 'order_item_id', 'product_id', 'price', 'freight_value']],
        right=orders[[
            'order_id', 'order_status', 'order_purchase_timestamp',
            'order_delivered_customer_date', 'year', 'month'
        ]],
        on='order_id',
        how='left'
    )

    # Filter by order status
    if status_filter:
        sales_data = sales_data[sales_data['order_status'] == status_filter].copy()

    # Calculate delivery speed in days
    sales_data['delivery_speed_days'] = (
        sales_data['order_delivered_customer_date'] -
        sales_data['order_purchase_timestamp']
    ).dt.days

    return sales_data


def filter_by_date_range(
    df: pd.DataFrame,
    year: int = None,
    month: int = None,
    date_column: str = 'order_purchase_timestamp'
) -> pd.DataFrame:
    """
    Filter dataframe by year and/or month.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe to filter
    year : int, optional
        Year to filter for
    month : int, optional
        Month to filter for (1-12)
    date_column : str
        Name of the date column to use for filtering

    Returns
    -------
    pd.DataFrame
        Filtered dataframe
    """
    filtered_df = df.copy()

    if year is not None:
        if 'year' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['year'] == year]
        else:
            filtered_df = filtered_df[filtered_df[date_column].dt.year == year]

    if month is not None:
        if 'month' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['month'] == month]
        else:
            filtered_df = filtered_df[filtered_df[date_column].dt.month == month]

    return filtered_df


def enrich_sales_with_products(
    sales_data: pd.DataFrame,
    products: pd.DataFrame
) -> pd.DataFrame:
    """
    Enrich sales data with product category information.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset
    products : pd.DataFrame
        Products dataset

    Returns
    -------
    pd.DataFrame
        Sales data enriched with product information
    """
    return pd.merge(
        left=sales_data,
        right=products[['product_id', 'product_category_name']],
        on='product_id',
        how='left'
    )


def enrich_sales_with_geography(
    sales_data: pd.DataFrame,
    orders: pd.DataFrame,
    customers: pd.DataFrame
) -> pd.DataFrame:
    """
    Enrich sales data with customer geographic information.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset
    orders : pd.DataFrame
        Orders dataset
    customers : pd.DataFrame
        Customers dataset

    Returns
    -------
    pd.DataFrame
        Sales data enriched with geographic information
    """
    # First merge with orders to get customer_id
    sales_with_customer = pd.merge(
        left=sales_data,
        right=orders[['order_id', 'customer_id']],
        on='order_id',
        how='left'
    )

    # Then merge with customers to get location info
    sales_with_geo = pd.merge(
        left=sales_with_customer,
        right=customers[['customer_id', 'customer_state', 'customer_city']],
        on='customer_id',
        how='left'
    )

    return sales_with_geo


def enrich_sales_with_reviews(
    sales_data: pd.DataFrame,
    reviews: pd.DataFrame
) -> pd.DataFrame:
    """
    Enrich sales data with review information.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset
    reviews : pd.DataFrame
        Reviews dataset

    Returns
    -------
    pd.DataFrame
        Sales data enriched with review scores
    """
    return pd.merge(
        left=sales_data,
        right=reviews[['order_id', 'review_score']],
        on='order_id',
        how='left'
    )
