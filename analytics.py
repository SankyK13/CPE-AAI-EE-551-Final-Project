"""
analytics.py
This file includes all of the statistical analysis functions for delay data.
Provides utility functions for loading, processing, and
analyzing transportation delay data using Pandas, NumPy,
and other Python libraries.

Includes filtering and generator-based data processing functions.
By: Rakshita Singh
"""
import math
import numpy as np
import pandas as pd

def compute_statistics(delays: list) -> tuple:
    # Returns (mean, std_dev, median) as a tuple.
    if not delays:
        return (0.0, 0.0, 0.0)
    return (
        float(np.mean(delays)),
        float(np.std(delays, ddof=1)),
        float(np.median(delays)),
    )

def compute_rms_delay(delays: list) -> float:
    # Root,mean,square of delay values. Uses math.sqrt.
    if not delays:
        return 0.0
    squared = [d ** 2 for d in delays]
    return math.sqrt(sum(squared) / len(squared))

def compute_percentiles(delays: list, percentiles=(25, 50, 75, 90, 95)) -> dict:
    #Dict comprehension maps each percentile to its value.
    arr = np.array(delays)
    return {p: round(float(np.percentile(arr, p)), 2) for p in percentiles}

def get_high_delays(delays: list, threshold: float) -> list:
    # Filter delays above threshold using filter and lambda.
    return list(filter(lambda d: d > threshold, delays))

def delays_by_group(df: pd.DataFrame, group_col: str) -> dict:
    # Average delay grouped by a column. Returns a plain dict.
    return df.groupby(group_col)["actual_departure_delay_min"].mean().to_dict()

def delay_generator(df: pd.DataFrame):
    #Generator yields delay values one at a time in a memory efficient fashion
    for val in df["actual_departure_delay_min"]:
        if not pd.isna(val):
            yield float(val)

def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    # Correlation matrix for the key numeric columns.
    cols = [
        "actual_departure_delay_min", "temperature_C",
        "humidity_percent", "wind_speed_kmh", "precipitation_mm",
        "traffic_congestion_index", "peak_hour", "holiday",
    ]
    available = [c for c in cols if c in df.columns]
    return df[available].corr()

def peak_hour_delay_summary(df: pd.DataFrame) -> pd.DataFrame:
    # Avg delay and count broken out by peak vs off-peak hours.
    if "peak_hour" not in df.columns:
        return pd.DataFrame()
    df = df.copy()
    df["hour_type"] = df["peak_hour"].map(lambda x: "Peak" if x == 1 else "Off-Peak")
    return (
        df.groupby("hour_type")["actual_departure_delay_min"]
        .agg(["mean", "std", "count"])
        .rename(columns={"mean": "avg_delay", "std": "std_delay", "count": "trips"})
        .sort_values("avg_delay", ascending=False)
    )

def traffic_delay_summary(df: pd.DataFrame) -> pd.DataFrame:
    #Avg delay broken out by traffic congestion level (binned).
    if "traffic_congestion_index" not in df.columns:
        return pd.DataFrame()
    df = df.copy()
    df["congestion_level"] = pd.cut(
        df["traffic_congestion_index"],
        bins=[0, 3, 6, 10],
        labels=["Low (0-3)", "Medium (3-6)", "High (6-10)"],
        include_lowest=True,
    )
    return (
        df.groupby("congestion_level")["actual_departure_delay_min"]
        .agg(["mean", "std", "count"])
        .rename(columns={"mean": "avg_delay", "std": "std_delay", "count": "trips"})
        .sort_values("avg_delay", ascending=False)
    )

if __name__ == "__main__":
    print("analytics module — run main.py to use")
