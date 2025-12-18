# E-Commerce Business Analytics

A comprehensive, configurable analytics framework for e-commerce business performance analysis. This project provides structured exploratory data analysis with reusable modules for calculating business metrics and generating insights, plus an interactive Streamlit dashboard for real-time data exploration.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Modules](#modules)
- [Customization](#customization)
- [Key Metrics](#key-metrics)

## Overview

This analytics framework analyzes e-commerce data across multiple dimensions:
- Revenue trends and growth analysis
- Order volume and average order value tracking
- Product category performance
- Geographic sales distribution
- Customer experience metrics (reviews and delivery)

The refactored codebase separates data loading, business logic, and presentation to make the analysis maintainable, reusable, and easy to extend.

## Features

- **Interactive Dashboard**: Professional Streamlit dashboard with real-time filtering and visualizations
- **Configurable Analysis**: Easily analyze any time period by changing configuration parameters
- **Modular Design**: Separate modules for data loading and business metrics calculation
- **Comprehensive Visualizations**: Professional charts with proper labels, titles, and styling
- **Year-over-Year Comparisons**: Built-in support for comparing current vs previous periods
- **Rich Documentation**: Detailed markdown cells explaining each analysis section
- **Reusable Functions**: Well-documented functions with clear parameters and return values

## Project Structure

```
lesson7_files/
├── .streamlit/                  # Streamlit configuration
│   └── config.toml              # Dashboard theme settings (light mode)
├── ecommerce_data/              # Data directory
│   ├── orders_dataset.csv
│   ├── order_items_dataset.csv
│   ├── products_dataset.csv
│   ├── customers_dataset.csv
│   └── order_reviews_dataset.csv
├── data_loader.py               # Data loading and preprocessing module
├── business_metrics.py          # Business metrics calculation module
├── dashboard.py                 # Interactive Streamlit dashboard
├── EDA_Refactored.ipynb         # Main analysis notebook
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup Steps

1. Clone or navigate to the project directory:
```bash
cd lesson7_files
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Launch Jupyter Notebook:
```bash
jupyter notebook
```

4. Open `EDA_Refactored.ipynb` in your browser

## Usage

### Quick Start

1. Open `EDA_Refactored.ipynb` in Jupyter Notebook
2. Modify the configuration parameters in Section 1:
   ```python
   CURRENT_YEAR = 2023
   PREVIOUS_YEAR = 2022
   MONTH_FILTER = None  # Set to 1-12 for specific month
   ```
3. Run all cells (Cell > Run All)
4. Review the analysis results and visualizations

### Analyzing Different Time Periods

To analyze different time periods, simply modify the configuration:

**Analyze a specific year:**
```python
CURRENT_YEAR = 2023
PREVIOUS_YEAR = None  # No comparison
```

**Compare two years:**
```python
CURRENT_YEAR = 2023
PREVIOUS_YEAR = 2022
```

**Analyze a specific month:**
```python
CURRENT_YEAR = 2023
MONTH_FILTER = 6  # June only
```

### Using the Modules Independently

You can use the modules in your own Python scripts:

```python
from data_loader import load_all_datasets, prepare_orders_data
from business_metrics import calculate_revenue_metrics

# Load data
datasets = load_all_datasets('ecommerce_data')
orders = prepare_orders_data(datasets['orders'])

# Calculate metrics
revenue_metrics = calculate_revenue_metrics(sales_data, 2023, 2022)
print(f"Revenue: ${revenue_metrics['total_revenue']:,.2f}")
```

### Running the Interactive Dashboard

Launch the Streamlit dashboard for an interactive, web-based analytics experience:

```bash
streamlit run dashboard.py
```

The dashboard will open in your default web browser at `http://localhost:8501`.

#### Dashboard Features

The dashboard provides a professional, interactive interface with:

**Header Section:**
- Title and year filter (applies globally to all visualizations)
- Clean, professional layout

**KPI Cards (Row 1):**
- Total Revenue with year-over-year trend indicator
- Monthly Growth Rate
- Average Order Value with trend indicator
- Total Orders with trend indicator
- Color-coded trends (green for positive, red for negative)

**Analytics Grid (2x2 Layout):**
- **Revenue Trend Chart**: Line chart comparing current year (solid line) vs previous year (dashed line)
- **Top 10 Categories**: Horizontal bar chart with blue gradient, sorted by revenue
- **Geographic Distribution**: Interactive US choropleth map showing revenue by state
- **Delivery Satisfaction**: Bar chart showing review scores by delivery speed

**Bottom Metrics (Row 3):**
- Average Delivery Time with trend indicator
- Average Review Score with star rating visualization

**Interactive Features:**
- Year filter in header updates all charts dynamically
- Hover tooltips on all charts for detailed information
- Professional styling with consistent colors and formatting
- Responsive layout that adapts to screen size

#### Dashboard Usage Tips

1. **Filtering by Year**: Use the dropdown in the top-right to switch between years
2. **Chart Interactions**: Hover over any chart element for detailed values
3. **Trend Indicators**: All metrics show percentage change vs previous year (when available)
4. **Value Formatting**: Large numbers are automatically formatted (e.g., $2.5M, $300K)

## Modules

### data_loader.py

Handles all data loading and preprocessing operations:

**Key Functions:**
- `load_all_datasets(data_dir)`: Load all CSV files
- `prepare_orders_data(orders)`: Clean and enhance orders data
- `create_sales_dataset(orders, order_items)`: Merge orders and items
- `enrich_sales_with_products(sales_data, products)`: Add product info
- `enrich_sales_with_geography(sales_data, orders, customers)`: Add location data
- `enrich_sales_with_reviews(sales_data, reviews)`: Add review scores
- `filter_by_date_range(df, year, month)`: Filter by time period

**Example:**
```python
from data_loader import load_all_datasets, create_sales_dataset

# Load datasets
datasets = load_all_datasets('ecommerce_data')

# Create sales dataset
sales_data = create_sales_dataset(
    datasets['orders'],
    datasets['order_items'],
    status_filter='delivered'
)
```

### business_metrics.py

Contains all business metric calculation functions:

**Revenue Metrics:**
- `calculate_revenue_metrics(sales_data, current_year, previous_year)`: Total revenue and YoY growth
- `calculate_monthly_revenue(sales_data, year)`: Revenue by month
- `calculate_month_over_month_growth(sales_data, year)`: MoM growth rates
- `calculate_average_mom_growth(sales_data, year)`: Average MoM growth

**Order Metrics:**
- `calculate_order_metrics(sales_data, current_year, previous_year)`: Order volume and AOV
- `calculate_order_status_distribution(orders, year)`: Order status breakdown

**Product Metrics:**
- `calculate_product_category_performance(sales_data, year, top_n)`: Revenue by category

**Geographic Metrics:**
- `calculate_geographic_sales(sales_data, year, top_n)`: Revenue by state

**Customer Experience Metrics:**
- `calculate_review_metrics(sales_data, year)`: Average review score
- `calculate_delivery_speed_vs_reviews(sales_data, year)`: Delivery vs satisfaction
- `calculate_avg_delivery_time(sales_data, year)`: Average delivery days
- `calculate_review_distribution(sales_data, year)`: Review score breakdown

**Example:**
```python
from business_metrics import calculate_revenue_metrics, calculate_order_metrics

# Calculate revenue metrics
revenue = calculate_revenue_metrics(sales_data, 2023, 2022)
print(f"YoY Growth: {revenue['revenue_growth_pct']:.2f}%")

# Calculate order metrics
orders = calculate_order_metrics(sales_data, 2023, 2022)
print(f"Average Order Value: ${orders['avg_order_value']:.2f}")
```

## Customization

### Adding New Metrics

To add a new business metric:

1. Add the calculation function to `business_metrics.py`:
```python
def calculate_new_metric(sales_data, year=None):
    """
    Calculate your new metric.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales dataset
    year : int, optional
        Filter for specific year

    Returns
    -------
    float or pd.DataFrame
        Calculated metric
    """
    # Your calculation logic here
    pass
```

2. Import and use in the notebook:
```python
from business_metrics import calculate_new_metric

result = calculate_new_metric(sales_data, CURRENT_YEAR)
```

### Adding New Visualizations

Follow the pattern in the notebook:
```python
# Calculate data
metric_data = calculate_some_metric(sales_data, CURRENT_YEAR)

# Create visualization
plt.figure(figsize=(12, 6))
plt.plot(metric_data['x'], metric_data['y'])
plt.title('Your Metric Title - {}'.format(CURRENT_YEAR),
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('X Label', fontsize=12, fontweight='bold')
plt.ylabel('Y Label', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.show()
```

## Key Metrics

### Revenue Metrics
- **Total Revenue**: Sum of all delivered order item prices
- **YoY Revenue Growth**: Percentage change vs same period last year
- **Month-over-Month Growth**: Monthly revenue change percentage
- **Average MoM Growth**: Mean of monthly growth rates

### Order Metrics
- **Total Orders**: Count of unique delivered orders
- **Average Order Value (AOV)**: Average total price per order
- **YoY Order Growth**: Percentage change in order count vs last year
- **Order Status Distribution**: Breakdown by status (delivered, canceled, etc.)

### Product Metrics
- **Category Revenue**: Total revenue by product category
- **Top Categories**: Highest-performing product categories

### Geographic Metrics
- **State Revenue**: Total revenue by US state
- **Top Markets**: Highest-revenue geographic locations

### Customer Experience Metrics
- **Average Review Score**: Mean customer rating (1-5 scale)
- **Review Distribution**: Percentage breakdown by rating
- **Average Delivery Time**: Mean days from purchase to delivery
- **Delivery Speed vs Reviews**: Satisfaction by delivery time bucket

## Data Dictionary

### Orders Dataset
- `order_id`: Unique order identifier
- `customer_id`: Unique customer identifier
- `order_status`: delivered, shipped, canceled, processing, pending, returned
- `order_purchase_timestamp`: When order was placed
- `order_delivered_customer_date`: When delivered to customer

### Order Items Dataset
- `order_id`: Links to orders
- `product_id`: Links to products
- `price`: Item price (USD)
- `freight_value`: Shipping cost (USD)

### Products Dataset
- `product_id`: Unique product identifier
- `product_category_name`: Product category

### Customers Dataset
- `customer_id`: Unique customer identifier
- `customer_state`: US state code
- `customer_city`: City name

### Reviews Dataset
- `order_id`: Links to orders
- `review_score`: Rating 1 (worst) to 5 (best)
- `review_comment_title`: Review title
- `review_comment_message`: Review text

## Best Practices

1. **Always filter for delivered orders** when calculating revenue metrics
2. **Use unique order IDs** when calculating review metrics to avoid duplicates
3. **Specify time periods clearly** in analysis titles and labels
4. **Compare year-over-year** for seasonal businesses
5. **Document assumptions** when adding custom metrics
6. **Test with different date ranges** to ensure configurability works

## Troubleshooting

### Common Issues

**Module import errors:**
```bash
# Make sure you're in the correct directory
cd lesson7_files

# Reinstall requirements
pip install -r requirements.txt
```

**Data file not found:**
```python
# Check the data directory path in configuration
DATA_DIR = 'ecommerce_data'  # Update if your data is elsewhere
```

**Empty results for a year:**
```python
# Check available years in your data
print(orders['year'].unique())
```

**Dashboard not loading:**
```bash
# Ensure Streamlit is installed
pip install streamlit>=1.28.0

# Run from the correct directory
cd lesson7_files
streamlit run dashboard.py
```

**Port already in use:**
```bash
# Run on a different port
streamlit run dashboard.py --server.port 8502
```

## Future Enhancements

Potential improvements for future versions:
- Add customer cohort analysis
- Include product-level profitability metrics
- Add forecasting capabilities
- Create automated report generation
- Add statistical significance testing for comparisons
- Include seasonality analysis
- Add customer lifetime value calculations

## License

This project is for educational and analytical purposes.

## Support

For issues or questions, please review the inline documentation in the modules and notebook cells.
