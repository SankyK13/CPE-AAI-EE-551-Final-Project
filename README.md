# Public Transport Delay Analysis
# Team Members

| Sankalp Khira | skhira@stevens.edu | 20023909 |
| Rakshita Singh | rsingh39@stevens.edu | 20024023 |
| Pal Sanjaybhai Anghan | panghan@stevens.edu | 2004515 |

# Project Description
Our choosen real-world engineering/science problem 

# Overview
This code itself analyzes a dataset of 2,000 public-transport trips to understand delay patterns and predict whether a trip will be delayed. We explore how factors like time of day, transport type, traffic congestion, and holidays affect departure delays across buses, trams, trains, and metro lines.

The program:
- Loads and cleans real-world transit data from a CSV file
- Computes descriptive statistics (mean, median, RMS, percentiles)
- Groups and compares delays by transport type, peak hours, and traffic congestion
- Predicts delays using a rule-based threshold approach and a logistic regression model
- Generates 7 visualizations saved as PNG charts

# Dependencies / Libraries
- pandas: data loading, cleaning, grouping
- numpy: statistical calculations
- matplotlib: all charts and plots
- scikit-learn: logistic regression model, train/test split, scaling
- math: RMS calculation
- pytest: test framework

Install with:
pip install pandas numpy matplotlib scikit-learn pytest

# File / Module Structure

project/
├── main.py                 # Runs the full analysis pipeline
├── transit_data.py          # TransitRoute and TransitNetwork classes (Member 1)
├── data_loader.py           # CSV loading, cleaning, validation (Member 1)
├── analytics.py             # Statistical analysis functions (Member 2)
├── delay_predictor.py       # Rule-based + logistic regression predictors (Member 2)
├── visualizations.py        # Matplotlib chart generation (Member 3)
├── test_project.py          # Pytest test cases
├── public_transport_delays.csv
├── figures/                 # Generated charts (created on run)
└── README.md


# How to Run

1. Make sure Python 3.12+ is installed
2. Install dependencies:
   pip install pandas numpy matplotlib scikit-learn pytest
3. Run the analysis:
   python main.py
4. Run the tests:
   pytest test_project.py -v

Charts are saved to the `figures/` folder.

# Main Contributions

# Sankalp Khira — Data Engineering
Files: `transit_data.py`, `data_loader.py`

- Designed the `TransitRoute` and `TransitNetwork` classes (composition relationship)
- Implemented dunder methods: `__str__`, `__len__`, `__eq__`, `__hash__`, `__getattr__`, `__contains__`, `__iter__`
- Built CSV loading with exception handling (FileNotFoundError, ValueError)
- Data cleaning pipeline with lambda-based delay categorization
- Set operations on delay category data (union, intersection, difference)
- Generator function for memory-efficient delay iteration

# Rakshita Singh — Analysis & Prediction
Files: `analytics.py`, `delay_predictor.py`

- Statistical functions: mean, std, RMS, percentiles, grouped averages
- Correlation analysis between delays and environmental factors
- Peak hour and traffic congestion delay summaries
- Rule-based delay predictor using historical route averages
- Logistic regression model with train/test split and feature importance
- Used filter + lambda for delay thresholding
- Dict and list comprehensions throughout

# Pal Sanjaybhai Anghan — Visualization & Reporting
Files: `visualizations.py`, `main.py`, `test_project.py`

- Created 7 matplotlib visualizations (histogram, bar, box plot, stacked bar, heatmap, overlaid histogram, horizontal bar)
- Built the main pipeline script orchestrating all modules
- Wrote pytest test suite with 13 test cases
- Debugged the code and helped other members with error managing

# Requirements Checklist
# Part 1
1. Two classes with relationship - `TransitRoute` and `TransitNetwork` (composition)
2. Two meaningful functions - `compute_statistics`, `compute_rms_delay`, `delays_by_group`, etc.
3. Two advanced libraries - pandas, numpy, matplotlib, scikit-learn
4. Exception handling + tests - FileNotFoundError and ValueError in `data_loader.py`; RuntimeError in `delay_predictor.py`; 13 pytest cases in `test_project.py`
5. Data I/O - CSV file reading via pandas
6. Loops and conditionals - for/while loops and if statements throughout all modules
7. Mutable + immutable types - list, dict, set (mutable); int, float, str, tuple (immutable)
8. `__str__` + operator overloads - `__str__`, `__len__`, `__eq__`, `__hash__` on TransitRoute
9. Docstrings and comments - present on every class and function
10. README - this file

# Part 2 (4+ required, we have 6)
1. Special functions - `filter`, `lambda`, `enumerate`, `zip` used across modules
2. Comprehensions - list and dict comprehensions in multiple files
3. Built-in module - `math` (sqrt in RMS calculation)
4. Generator - `delay_generator()` in both `analytics.py` and `transit_data.py`
5. Set operations - union, intersection, difference in `TransitNetwork` (on delay categories)
6. `__name__` - `if __name__ == "__main__"` guards in all .py modules
