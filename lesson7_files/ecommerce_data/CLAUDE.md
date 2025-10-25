# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an e-commerce business analytics project with a modular architecture for analyzing sales data. The project provides both Jupyter notebook analysis and a Streamlit dashboard for business intelligence.

**Note**: This directory (`ecommerce_data/`) contains only the CSV datasets. The main Python modules and notebooks are in the parent directory.

## Data Structure

This directory contains 6 CSV datasets representing different aspects of e-commerce operations:

- `customers_dataset.csv` (8,001 records): Customer information including unique IDs, zip codes, cities, and states
- `orders_dataset.csv` (10,001 records): Order lifecycle data with timestamps for purchase, approval, delivery dates, and order status
- `order_items_dataset.csv` (16,048 records): Individual line items with product IDs, seller IDs, prices, and freight values
- `order_payments_dataset.csv` (14,092 records): Payment details including payment type, installments, and values (multiple payments per order possible)
- `order_reviews_dataset.csv` (9,426 records): Customer reviews with scores (1-5), comments, and timestamps
- `products_dataset.csv` (6,001 records): Product catalog with categories, dimensions, and descriptions

### Key Relationships

The datasets connect through these relationships:
- `orders.order_id` joins to `order_items.order_id`, `order_payments.order_id`, and `order_reviews.order_id`
- `orders.customer_id` joins to `customers.customer_id`
- `order_items.product_id` joins to `products.product_id`

## Common Development Commands

### Running the Streamlit Dashboard

From the parent directory:
```bash
streamlit run dashboard.py
```

The dashboard provides interactive filtering by year and displays KPI cards, revenue trends, product performance, geographic heatmaps, and customer satisfaction metrics.

### Running Jupyter Notebooks

From the parent directory:
```bash
jupyter notebook EDA_Refactored.ipynb
```

Or for the original exploratory analysis:
```bash
jupyter notebook EDA.ipynb
```

### Installing Dependencies

From the parent directory:
```bash
pip install -r requirements.txt
```

Required packages: pandas, numpy, matplotlib, seaborn, plotly, streamlit, jupyter, ipykernel

## Architecture and Key Modules

The project follows a modular design with three main Python modules in the parent directory:

### 1. data_loader.py

Handles all data loading and preprocessing:

- **EcommerceDataLoader class**: Main data loading interface
  - `load_raw_data()`: Loads all 6 CSV files into raw_data dictionary
  - `process_all_data()`: Cleans data, converts timestamps, extracts date components
  - `create_sales_dataset(year_filter, month_filter, status_filter)`: Creates comprehensive sales dataset by joining orders, order_items, products, customers, and reviews
  - `get_data_summary()`: Returns row counts, memory usage, and date ranges

- **Key functions**:
  - `load_and_process_data(data_path)`: Convenience function that loads and processes all data
  - `categorize_delivery_speed(days)`: Categorizes delivery into '1-3 days', '4-7 days', '8+ days'

The loader automatically:
- Converts timestamp columns to datetime objects
- Extracts `purchase_year`, `purchase_month`, `purchase_date` from order timestamps
- Calculates `total_item_value` (price + freight)
- Computes `delivery_days` (time between purchase and delivery)

### 2. business_metrics.py

Calculates business metrics and creates visualizations:

- **BusinessMetricsCalculator class**: Core metrics calculation
  - `calculate_revenue_metrics(current_year, previous_year)`: Total revenue, orders, AOV, and growth rates
  - `calculate_monthly_trends(year)`: Month-over-month revenue, orders, and AOV with growth percentages
  - `analyze_product_performance(year, top_n)`: Category-level revenue, share, and rankings
  - `analyze_geographic_performance(year)`: State-level revenue and order metrics
  - `analyze_customer_satisfaction(year)`: Review scores and satisfaction percentages
  - `analyze_delivery_performance(year)`: Delivery time averages and speed distributions
  - `generate_comprehensive_report(current_year, previous_year)`: Combines all metrics into single report

- **MetricsVisualizer class**: Professional visualizations
  - `plot_revenue_trend()`: Monthly revenue line chart with matplotlib
  - `plot_category_performance(top_n)`: Horizontal bar chart of top categories
  - `plot_geographic_heatmap()`: US state choropleth map using Plotly
  - `plot_review_distribution()`: Customer satisfaction bar chart

- **Helper functions**:
  - `format_currency(value)`: Formats numbers as currency ($1,234.56)
  - `format_percentage(value, decimals)`: Formats percentages with specified precision
  - `print_metrics_summary(report)`: Prints formatted console summary of all metrics

### 3. dashboard.py

Streamlit application that provides:
- Year filter in sidebar (dynamically populated from available data years)
- 4 KPI cards: Total Revenue, Monthly Growth, Average Order Value, Total Orders with trend indicators
- 2x2 grid of interactive charts: Revenue trend, Top 10 categories, State map, Satisfaction vs. Delivery
- Bottom row: Delivery time and review score metrics

## Working with the Data

### Configurable Analysis Approach

The project is designed for flexible time-period analysis without code changes:

```python
# In notebooks or scripts
from data_loader import load_and_process_data
from business_metrics import BusinessMetricsCalculator

# Load all data
loader, processed_data = load_and_process_data('ecommerce_data/')

# Create filtered dataset
sales_data = loader.create_sales_dataset(
    year_filter=2023,           # Analyze specific year
    month_filter=None,          # None for full year, or 1-12 for specific month
    status_filter='delivered'   # Only delivered orders (can be 'shipped', 'canceled', etc.)
)

# Calculate metrics
metrics_calc = BusinessMetricsCalculator(sales_data)
report = metrics_calc.generate_comprehensive_report(
    current_year=2023,
    previous_year=2022  # Optional: for growth calculations
)
```

### Important Data Characteristics

- **Order Status**: The datasets include various order statuses (delivered, canceled, etc.). Most analyses filter to `status_filter='delivered'` to analyze completed transactions only.

- **Multiple Payments**: Some orders have multiple payment records (sequential payments). When analyzing order-level metrics, be careful to avoid double-counting.

- **Review Deduplication**: Reviews are at the order level, not the order-item level. Use `drop_duplicates('order_id')` when calculating review-based metrics to avoid inflating review counts.

- **Delivery Days**: Calculated as the difference between `order_delivered_customer_date` and `order_purchase_timestamp`. Some orders may not have delivery dates (e.g., canceled orders), so filter for non-null values.

- **Product Categories**: Stored in `product_category_name` field with values like 'electronics', 'books_media', 'sports_outdoors', 'grocery_gourmet_food'.

### Data Path Configuration

The default data path is `'ecommerce_data/'` (relative to parent directory). When working from within the `ecommerce_data/` directory, use `DATA_PATH = './'` or absolute paths.

## Tips for Development

### When Adding New Metrics

1. Add calculation method to `BusinessMetricsCalculator` class in `business_metrics.py`
2. Add visualization method to `MetricsVisualizer` class if needed
3. Update `generate_comprehensive_report()` to include new metric
4. Update dashboard.py if the metric should be displayed in the Streamlit app

### When Modifying Data Schema

1. Update column mappings in `data_loader.py`'s `EcommerceDataLoader` class methods
2. Update `_validate_data()` in `BusinessMetricsCalculator` if new required columns are added
3. Test with `get_data_summary()` to ensure all data loads correctly

### Performance Considerations

- The full dataset is ~10,000 orders with ~16,000 line items
- Data fits in memory, no need for chunked processing
- The `create_sales_dataset()` method performs multiple joins - cache the result if running multiple analyses
- Streamlit dashboard uses `@st.cache_data` decorator for data loading (in dashboard.py)
