# E-commerce Business Analytics Dashboard

A comprehensive business intelligence solution featuring both Jupyter notebook analysis and a professional Streamlit dashboard for e-commerce sales data with configurable time periods and reusable business metrics calculations.

## Overview

This project transforms a basic exploratory data analysis into a professional, maintainable business intelligence framework. The refactored solution provides:

- **Configurable Analysis**: Easily analyze any time period or compare different years
- **Modular Architecture**: Reusable data loading and metrics calculation modules
- **Professional Visualizations**: Business-oriented charts with proper formatting
- **Strategic Insights**: Automated generation of business recommendations

## Project Structure

```
data_analysis/
├── EDA_Refactored.ipynb     # Main analysis notebook
├── dashboard.py             # Streamlit dashboard application
├── data_loader.py           # Data loading and processing module
├── business_metrics.py      # Business metrics calculation module
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── ecommerce_data/         # Data directory
    ├── orders_dataset.csv
    ├── order_items_dataset.csv
    ├── products_dataset.csv
    ├── customers_dataset.csv
    ├── order_reviews_dataset.csv
    └── order_payments_dataset.csv
```

## Features

### 1. Configurable Analysis Framework
- Set analysis year, comparison year, and month filters
- Flexible time period analysis without code changes
- Automatic handling of missing data periods

### 2. Comprehensive Business Metrics
- **Revenue Analysis**: Total revenue, growth rates, average order value
- **Product Performance**: Category analysis, revenue share, top performers
- **Geographic Insights**: State-level revenue and order analysis
- **Customer Satisfaction**: Review scores, satisfaction distribution
- **Delivery Performance**: Delivery times, speed categorization

### 3. Professional Visualizations
- Monthly revenue trend charts
- Product category performance bars
- Interactive geographic heatmaps
- Customer satisfaction distributions
- Consistent color schemes and formatting

### 4. Automated Insights
- Strategic recommendations based on data patterns
- Performance benchmarking and alerts
- Executive summary generation

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Jupyter Notebook or JupyterLab (for notebook analysis)

### Installation Steps

1. **Clone or download the project files**

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure data files are in place**:
   - Place CSV files in the `ecommerce_data/` directory
   - Verify all required files are present (see Project Structure above)

4. **Run the applications**:

   **For Professional Dashboard (NEW)**:
   ```bash
   streamlit run dashboard_new.py
   ```

   **For Original Dashboard**:
   ```bash
   streamlit run dashboard.py
   ```

   **For Jupyter Notebook Analysis**:
   ```bash
   jupyter notebook EDA_Refactored.ipynb
   ```

## Usage Guide

### Professional Streamlit Dashboard (NEW)

#### dashboard_new.py - Converted from EDA_Refactored.ipynb

1. **Launch the professional dashboard**:
   ```bash
   streamlit run dashboard_new.py
   ```

2. **Professional Dashboard Layout**:
   The new dashboard follows the exact layout specifications with professional styling:
   
   **Header Section**:
   - **Title**: "E-commerce Analytics Dashboard" (left-aligned)
   - **Year Filter**: Dropdown selector (right-aligned) that applies globally to all visualizations
   
   **KPI Row** (4 cards with uniform heights):
   - **Total Revenue**: with trend indicator vs previous year (green/red arrows)
   - **Monthly Growth**: average month-over-month growth percentage  
   - **Average Order Value**: with trend indicator vs previous year (green/red arrows)
   - **Total Orders**: with trend indicator vs previous year (green/red arrows)
   
   **Charts Grid** (2x2 layout):
   - **Revenue Trend**: Line chart with solid line (current year) vs dashed line (previous year), grid lines, Y-axis as $300K format
   - **Top 10 Categories**: Horizontal bar chart with blue gradient, sorted descending, values as $300K/$2M
   - **Revenue by State**: US Choropleth map with blue color scale
   - **Satisfaction vs Delivery**: Bar chart showing review scores by delivery time buckets (1-3 days, 4-7 days, 8+ days)
   
   **Bottom Row** (2 cards with uniform heights):
   - **Average Delivery Time**: Large number with trend indicator
   - **Review Score**: Large number with star rating display and "Average Review Score" subtitle

3. **Professional Features**:
   - **Real-time filtering**: All charts update automatically when year is changed
   - **Trend indicators**: Green/red arrows with two decimal places showing performance changes
   - **Professional styling**: Clean, business-ready interface without icons
   - **Plotly charts**: All visualizations use Plotly for professional presentation
   - **Formatted values**: Currency displayed as $300K, $2M for readability
   - **Grid lines**: Added to charts for easier reading
   - **Uniform card heights**: Consistent sizing across rows
   - **Data caching**: Optimized performance with Streamlit caching

### Original Streamlit Dashboard

#### dashboard.py - Original Implementation

1. **Launch the original dashboard**:
   ```bash
   streamlit run dashboard.py
   ```

2. **Original Dashboard Layout**:
   The dashboard follows a professional layout with these sections:
   
   **Header Row**:
   - **Title**: "E-commerce Analytics Dashboard" (left-aligned)
   - **Year Filter**: Dropdown selector (right-aligned) that applies globally to all visualizations
   
   **KPI Row** (4 cards):
   - **Total Revenue**: with trend indicator vs previous year
   - **Monthly Growth**: average month-over-month growth percentage  
   - **Average Order Value**: with trend indicator vs previous year
   - **Total Orders**: with trend indicator vs previous year
   
   **Charts Grid** (2x2 layout):
   - **Revenue Trend**: Line chart showing current year (solid line) vs previous year (dashed line)
   - **Top 10 Categories**: Horizontal bar chart with blue gradient, sorted descending
   - **Revenue by State**: US Choropleth map with blue color scale
   - **Satisfaction vs Delivery**: Bar chart showing review scores by delivery time buckets
   
   **Bottom Row** (2 cards):
   - **Average Delivery Time**: with trend indicator
   - **Review Score**: Large number with star rating display

3. **Dashboard Features**:
   - **Real-time filtering**: All charts update automatically when year is changed
   - **Professional styling**: Clean, business-ready interface with uniform card heights
   - **Trend indicators**: Green/red arrows with two decimal places showing performance changes
   - **Formatted values**: Currency displayed as $300K, $2M for readability (no icons used)
   - **Interactive charts**: All visualizations built with Plotly for professional presentation
   - **Grid lines**: Added to charts for easier reading as specified

### Notebook Analysis

1. **Open the refactored notebook**: `EDA_Refactored.ipynb`

2. **Configure analysis parameters** in the Configuration & Setup section:
   ```python
   ANALYSIS_YEAR = 2023        # Year to analyze
   COMPARISON_YEAR = 2022      # Comparison year (optional)
   ANALYSIS_MONTH = None       # Specific month or None for full year
   DATA_PATH = 'ecommerce_data/'
   ```

3. **Run all cells** to generate the complete analysis

#### EDA_Refactored.ipynb Features

The refactored notebook provides a professional, well-structured analysis with:

**Notebook Structure:**
- **Table of Contents**: Clickable navigation between sections
- **Introduction & Business Objectives**: Clear analysis goals and KPIs
- **Configuration & Setup**: Flexible parameters for any time period
- **Data Dictionary**: Comprehensive explanation of business terms and metrics
- **Modular Analysis Sections**: Revenue, Product, Geographic, and Customer Experience
- **Executive Summary**: Strategic recommendations and actionable insights

**Technical Improvements:**
- **Configurable Framework**: Easily analyze any year/month combination
- **Module Integration**: Uses existing data_loader.py and business_metrics.py
- **Clean Code**: Eliminates pandas warnings and follows best practices
- **Professional Visualizations**: Business-ready charts with proper formatting
- **Comprehensive Documentation**: Detailed explanations and insights

**Analysis Sections:**
1. **Revenue Performance**: Total revenue, growth rates, monthly trends, AOV analysis
2. **Product Categories**: Top performers, revenue share, market analysis
3. **Geographic Performance**: State-level revenue, market penetration, choropleth maps
4. **Customer Experience**: Satisfaction scores, delivery performance, correlation analysis

**Key Benefits:**
- **Reusable**: Works with any date range without code modifications
- **Maintainable**: Clear structure for future analysts
- **Business-Oriented**: Focuses on actionable insights rather than technical details
- **Professional Output**: Publication-ready visualizations and reports

### Advanced Configuration

#### Analyzing Specific Time Periods
```python
# Analyze only Q4 2023
for month in [10, 11, 12]:
    ANALYSIS_MONTH = month
    # Run analysis
```

#### Custom Data Paths
```python
# Use different data location
DATA_PATH = '/path/to/your/data/'
```

#### Filtering by Order Status
```python
# Modify in data_loader.py create_sales_dataset method
status_filter = 'delivered'  # or 'shipped', 'processing', etc.
```

### Module Usage

#### Data Loading Module
```python
from data_loader import EcommerceDataLoader, load_and_process_data

# Quick start
loader, processed_data = load_and_process_data('ecommerce_data/')

# Advanced usage
loader = EcommerceDataLoader('ecommerce_data/')
loader.load_raw_data()
processed_data = loader.process_all_data()

# Create filtered dataset
sales_data = loader.create_sales_dataset(
    year_filter=2023,
    month_filter=None,
    status_filter='delivered'
)
```

#### Business Metrics Module
```python
from business_metrics import BusinessMetricsCalculator, MetricsVisualizer

# Calculate metrics
metrics_calc = BusinessMetricsCalculator(sales_data)
report = metrics_calc.generate_comprehensive_report(
    current_year=2023,
    previous_year=2022
)

# Create visualizations
visualizer = MetricsVisualizer(report)
revenue_fig = visualizer.plot_revenue_trend()
category_fig = visualizer.plot_category_performance()
```

## Key Business Metrics

### Revenue Metrics
- **Total Revenue**: Sum of all delivered order item prices
- **Revenue Growth Rate**: Year-over-year percentage change
- **Average Order Value (AOV)**: Average total value per order
- **Monthly Growth Trends**: Month-over-month performance

### Product Performance
- **Category Revenue**: Revenue by product category
- **Market Share**: Percentage of total revenue by category
- **Category Diversity**: Distribution across product lines

### Geographic Analysis
- **State Performance**: Revenue and order count by state
- **Market Penetration**: Number of active markets
- **Regional AOV**: Average order value by geographic region

### Customer Experience
- **Review Scores**: Average satisfaction rating (1-5 scale)
- **Satisfaction Distribution**: Percentage of high/low ratings
- **Delivery Performance**: Average delivery time and speed metrics

## Output Examples

### Console Output
```
BUSINESS METRICS SUMMARY - 2023
============================================================

REVENUE PERFORMANCE:
  Total Revenue: $3,360,294.74
  Total Orders: 4,635
  Average Order Value: $724.98
  Revenue Growth: -2.5%

CUSTOMER SATISFACTION:
  Average Review Score: 4.10/5.0
  High Satisfaction (4+): 84.2%

DELIVERY PERFORMANCE:
  Average Delivery Time: 8.0 days
  Fast Delivery (≤3 days): 28.5%
```

### Generated Visualizations
- Monthly revenue trend line charts
- Top product category horizontal bar charts
- Interactive US state choropleth maps
- Customer satisfaction distribution charts

## Customization Options

### Adding New Metrics
1. Extend the `BusinessMetricsCalculator` class in `business_metrics.py`
2. Add visualization methods to `MetricsVisualizer` class
3. Update the notebook to display new metrics

### Custom Visualizations
```python
# Example: Custom visualization
def plot_custom_metric(self, data):
    fig, ax = plt.subplots(figsize=(12, 6))
    # Your visualization code
    return fig
```

### Data Source Modifications
- Modify `data_loader.py` to handle different CSV structures
- Update column mappings in the `EcommerceDataLoader` class
- Add new data validation rules

## Troubleshooting

### Common Issues

1. **Module Import Errors**:
   - Ensure all files are in the same directory
   - Check Python path configuration

2. **Missing Data Files**:
   - Verify CSV files are in the `ecommerce_data/` directory
   - Check file naming matches expected patterns

3. **Empty Results**:
   - Verify date filters match available data
   - Check order status filtering

4. **Visualization Issues**:
   - Ensure all required packages are installed
   - Check Plotly version compatibility for interactive maps

### Performance Optimization
- For large datasets, consider chunked processing
- Use data sampling for initial exploration
- Implement caching for repeated analysis

## Dashboard Features

### Layout Structure (Exact Implementation)
- **Header**: Title left-aligned, Year filter right-aligned (applies globally to all charts)
- **KPI Row**: 4 metric cards with trend indicators showing two decimal places
  - Total Revenue, Monthly Growth, Average Order Value, Total Orders
  - Color-coded trends (green for positive, red for negative)
  - Uniform card heights maintained across the row
- **Charts Grid**: 2x2 interactive Plotly visualization layout
  - Revenue trend with solid line (current) and dashed line (previous year)  
  - Top 10 product categories horizontal bar chart with blue gradient
  - US state choropleth map with blue color scale
  - Customer satisfaction vs delivery time bar chart (1-3 days, 4-7 days, 8+ days buckets)
- **Bottom Row**: Customer experience metrics with uniform card heights
  - Average delivery time with trend indicator
  - Review score with large number display and star rating

### Technical Features
- **Y-axis Formatting**: Currency values formatted as $300K, $2M instead of $300,000
- **No Icons**: Professional styling without icon usage as specified
- **Grid Lines**: Added to charts for easier reading
- **Real-time Filtering**: All visualizations update automatically when year filter changes
- **Professional Styling**: Business-ready interface with consistent formatting
- **Plotly Charts**: Interactive, publication-quality visualizations
- **Error Handling**: Graceful handling of missing data with appropriate fallbacks

## Future Enhancements

### Planned Features
- Real-time data connections
- Predictive analytics and forecasting
- Customer segmentation analysis
- A/B testing framework
- Automated report scheduling
- Export functionality (PDF reports)

### Extension Ideas
- Integration with business intelligence tools
- API endpoints for metrics access
- Machine learning model integration
- Advanced statistical analysis
- Mobile-responsive improvements

## Contributing

To extend this analysis framework:

1. Follow the existing code structure and documentation patterns
2. Add comprehensive docstrings to new functions
3. Include unit tests for new business logic
4. Update this README with new features

## License

This project is provided as-is for educational and business analysis purposes.

---

**Note**: This framework is designed to be easily maintained and extended for ongoing business intelligence needs. The modular architecture ensures that updates to data sources or metric calculations can be made without affecting the overall analysis structure.