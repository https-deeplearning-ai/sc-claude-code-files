# Streamlit Dashboard Conversion Requirements

Convert @EDA_Refactored.ipynb into a professional Streamlit dashboard with the following exact layout.


## Layout Structure

### **Header**
- Title + date range filter (applies globally)
  - **Title**: aligned left
  - **Date range filter**: aligned right

### **KPI Row**
- 4 cards: **Total Revenue**, **Monthly Growth**, **Average Order Value**, **Total Orders**
- Trend indicators for:
  - Total Revenue
  - Average Order Value
  - Total Orders
- Color coding:
  - Red for negative trends
  - Green for positive trends

### **Charts Grid** (2x2 layout)

#### Revenue Trend Line Chart
- Solid line for the current period
- Dashed line for the previous period
- Add grid lines for easier reading
- Y-axis formatting: `$300K` instead of `$300,000`

#### Top 10 Categories Bar Chart
- Sorted descending
- Blue gradient (light shade for lower values)
- Value formatting: `$300K` and `$2M`

#### Revenue by State (US Choropleth Map)
- Color-coded by revenue amount
- Blue gradient

#### Satisfaction vs Delivery Time (Bar Chart)
- **X-axis**: Delivery time buckets (1–3 days, 4–7 days, etc.)
- **Y-axis**: Average review score

### **Bottom Row**
- **Average Delivery Time** with trend indicator
- **Review Score**:
  - Large number with stars
  - Subtitle: `"Average Review Score"`


## Key Requirements
- Use **Plotly** for all charts
- Ensure charts update correctly when filters change
- Apply professional styling with trend arrows and colors
- **Do not use icons**
- Maintain **uniform card heights** for each row
- Show **two decimal places** for each trend indicator
- Include:
  - `requirements.txt`
  - `README.md`