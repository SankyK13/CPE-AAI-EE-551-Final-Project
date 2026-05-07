# Public Transport Delay Analysis

## Team Members

| Name | Email | Student ID |
|---|---|---|
| Sankalp Khira | skhira@stevens.edu | 20023909 |
| Rakshita Singh | rsingh39@stevens.edu | 20024023 |
| Pal Sanjaybhai Anghan | panghan@stevens.edu | 2004515 |

## Project Description

Our chosen real-world engineering/science problem is analyzing public transportation delays and predicting whether a trip will be delayed based on factors such as transport type, time of day, traffic congestion, and holidays.

## Overview

This project analyzes a dataset of 2,000 public-transport trips to understand delay patterns and predict whether a trip will be delayed. We explore how factors like time of day, transport type, traffic congestion, and holidays affect departure delays across buses, trams, trains, and metro lines.

The program:

- Loads and cleans real-world transit data from a CSV file
- Computes descriptive statistics, including mean, median, RMS, and percentiles
- Groups and compares delays by transport type, peak hours, and traffic congestion
- Predicts delays using a rule-based threshold approach and a logistic regression model
- Generates 7 visualizations saved as PNG charts

## Dependencies / Libraries

This project uses the following Python libraries:

- `pandas`: data loading, cleaning, and grouping
- `numpy`: statistical calculations
- `matplotlib`: charts and plots
- `scikit-learn`: logistic regression model, train/test split, and scaling
- `math`: RMS calculation
- `pytest`: test framework

Install dependencies with:

```bash
pip install pandas numpy matplotlib scikit-learn pytest
```

## File / Module Structure

```text
project/
├── main.py                       # Runs the full analysis pipeline
├── transit_data.py                # TransitRoute and TransitNetwork classes
├── data_loader.py                 # CSV loading, cleaning, validation
├── analytics.py                   # Statistical analysis functions
├── delay_predictor.py             # Rule-based and logistic regression predictors
├── visualizations.py              # Matplotlib chart generation
├── test_project.py                # Pytest test cases
├── public_transport_delays.csv    # Dataset
├── figures/                       # Generated charts
└── README.md
```

## How to Run

1. Make sure Python 3.12 or newer is installed.

2. Install dependencies:

```bash
pip install pandas numpy matplotlib scikit-learn pytest
```

3. Run the analysis:

```bash
python main.py
```

4. Run the tests:

```bash
pytest test_project.py -v
```

Charts are saved to the `figures/` folder.

## Main Contributions

### Sankalp Khira — Data Engineering

Files: `transit_data.py`, `data_loader.py`

- Designed the `TransitRoute` and `TransitNetwork` classes using a composition relationship
- Implemented dunder methods: `__str__`, `__len__`, `__eq__`, `__hash__`, `__getattr__`, `__contains__`, and `__iter__`
- Built CSV loading with exception handling, including `FileNotFoundError` and `ValueError`
- Created a data cleaning pipeline with lambda-based delay categorization
- Used set operations on delay category data, including union, intersection, and difference
- Created a generator function for memory-efficient delay iteration

### Rakshita Singh — Analysis & Prediction

Files: `analytics.py`, `delay_predictor.py`

- Implemented statistical functions for mean, standard deviation, RMS, percentiles, and grouped averages
- Performed correlation analysis between delays and environmental factors
- Created peak-hour and traffic-congestion delay summaries
- Built a rule-based delay predictor using historical route averages
- Built a logistic regression model with train/test split and feature importance
- Used `filter` and `lambda` for delay thresholding
- Used dictionary and list comprehensions throughout the project

### Pal Sanjaybhai Anghan — Visualization & Reporting

Files: `visualizations.py`, `main.py`, `test_project.py`

- Created 7 matplotlib visualizations, including histogram, bar chart, box plot, stacked bar chart, heatmap, overlaid histogram, and horizontal bar chart
- Built the main pipeline script that connects and runs all modules
- Wrote a pytest test suite with 13 test cases
- Debugged the code and helped other members with error handling

## Requirements Checklist

### Part 1

1. Two classes with relationship: `TransitRoute` and `TransitNetwork` using composition
2. Two meaningful functions: `compute_statistics`, `compute_rms_delay`, `delays_by_group`, etc.
3. Two advanced libraries: `pandas`, `numpy`, `matplotlib`, and `scikit-learn`
4. Exception handling and tests: `FileNotFoundError` and `ValueError` in `data_loader.py`; `RuntimeError` in `delay_predictor.py`; 13 pytest cases in `test_project.py`
5. Data I/O: CSV file reading using pandas
6. Loops and conditionals: for loops, while loops, and if statements throughout the modules
7. Mutable and immutable types: list, dict, set, int, float, str, and tuple
8. `__str__` and operator overloads: `__str__`, `__len__`, `__eq__`, and `__hash__` on `TransitRoute`
9. Docstrings and comments: present on every class and function
10. README: this file

### Part 2

At least 4 required. This project includes 6.

1. Special functions: `filter`, `lambda`, `enumerate`, and `zip` used across modules
2. Comprehensions: list and dictionary comprehensions in multiple files
3. Built-in module: `math`, used for square root in RMS calculation
4. Generator: `delay_generator()` in both `analytics.py` and `transit_data.py`
5. Set operations: union, intersection, and difference in `TransitNetwork`
6. `__name__`: `if __name__ == "__main__"` guards in all `.py` modules
