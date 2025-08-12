# EDA Notebook Refactoring Plan

The @EDA.ipynb contains exploratory data analysis on e-commerce data in @ecommerce_data, focusing on sales metrics for 2023.  
Keep the same analysis and graphs, and improve the structure and documentation of the notebook. 💡

## Review Checklist

Identify:
- What business metrics are currently calculated
- What visualizations are created
- What data transformations are performed
- Any code quality issues or inefficiencies


## **Refactoring Requirements**

### 1. Notebook Structure & Documentation
- Add proper documentation and markdown cells with clear headers and a brief explanation for each section
- Organize into logical sections:
  1. **Introduction & Business Objectives**
  2. **Data Loading & Configuration**
  3. **Data Preparation & Transformation**
  4. **Business Metrics Calculation** (revenue, product, geographic, customer experience analysis)
  5. **Summary of Observations**
- Add table of contents at the beginning
- Include data dictionary explaining key columns and business terms


### 2. Code Quality Improvements
- Create reusable functions with docstrings
- Implement consistent naming and formatting
- Create separate Python files:
  - `business_metrics.py` → business metric calculations only
  - `data_loader.py` → loading, processing, and cleaning the data


### 3. Enhanced Visualizations
Improve all plots with:
- Clear and descriptive titles
- Proper axis labels with units
- Legends where needed
- Appropriate chart types for the data
- Include date range in plot titles or captions
- Use consistent, business-oriented color schemes


### 4. Configurable Analysis Framework
- Current notebook computes metrics for a fixed date range (entire year of 2023 compared to 2022)
- Refactor to:
  - Filter data by configurable **month** and **year**
  - Implement general-purpose metric calculations


## **Deliverables Expected**
- Refactored Jupyter notebook: `EDA_Refactored.ipynb` with all improvements
- Business metrics module: `business_metrics.py` with documented functions
- Requirements file: `requirements.txt` listing all dependencies
- `README.md` section explaining how to use the refactored analysis