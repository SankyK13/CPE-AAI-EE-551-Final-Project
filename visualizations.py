"""
visualizations.py
Generates and saves all matplotlib figures for the report.
By: Pal Sanjaybhai Anghan
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

FIGURES_DIR = "figures"

def _save(fig, filename):
    #Helper to save a figure and close it
    os.makedirs(FIGURES_DIR, exist_ok=True)
    path = os.path.join(FIGURES_DIR, filename)
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"  Saved {path}")
    return path

def plot_delay_distribution(df):
    #Histogram of departure delays with mean line
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df["actual_departure_delay_min"], bins=25,
            edgecolor="white", color="#4C72B0", alpha=0.85)

    mean_val = df["actual_departure_delay_min"].mean()
    ax.axvline(mean_val, color="red", linestyle="--",
               label=f"Mean = {mean_val:.1f} min")

    ax.set_title("Distribution of Departure Delays")
    ax.set_xlabel("Delay (minutes)")
    ax.set_ylabel("Number of Trips")
    ax.legend()
    return _save(fig, "delay_distribution.png")

def plot_delay_by_transport(df):
    #Bar chart — average delay per transport type
    means = df.groupby("transport_type")["actual_departure_delay_min"].mean().sort_values()
    colors = ["#55A868", "#4C72B0", "#C44E52", "#8172B2"]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(means.index, means.values,
                  color=colors[:len(means)], edgecolor="white")

    # label each bar with its value
    for bar, val in zip(bars, means.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
                f"{val:.1f}", ha="center", fontsize=10)

    ax.set_title("Average Delay by Transport Type")
    ax.set_ylabel("Avg Delay (min)")
    return _save(fig, "delay_by_transport.png")

def plot_peak_vs_offpeak(df):
    #Overlapping histograms for peak vs off-peak
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df[df["peak_hour"] == 1]["actual_departure_delay_min"],
            bins=20, alpha=0.6, label="Peak Hour", color="#C44E52")
    ax.hist(df[df["peak_hour"] == 0]["actual_departure_delay_min"],
            bins=20, alpha=0.6, label="Off-Peak", color="#4C72B0")
    ax.set_title("Peak vs Off-Peak Delay Distribution")
    ax.set_xlabel("Delay (minutes)")
    ax.set_ylabel("Frequency")
    ax.legend()
    return _save(fig, "peak_vs_offpeak.png")

def plot_delay_by_congestion(df):
    #Box plot of delays grouped by traffic congestion level
    if "traffic_congestion_index" not in df.columns:
        return None
    df = df.copy()
    df["congestion_level"] = pd.cut(
        df["traffic_congestion_index"],
        bins=[0, 3, 6, 10],
        labels=["Low (0-3)", "Medium (3-6)", "High (6-10)"],
        include_lowest=True,
    )
    levels = ["Low (0-3)", "Medium (3-6)", "High (6-10)"]
    data = [df[df["congestion_level"] == lv]["actual_departure_delay_min"].dropna().values
            for lv in levels]

    fig, ax = plt.subplots(figsize=(10, 6))
    bp = ax.boxplot(data, labels=levels, patch_artist=True)

    palette = ["#55A868", "#FFD700", "#C44E52"]
    for patch, color in zip(bp["boxes"], palette):
        patch.set_facecolor(color)

    ax.set_title("Delay Spread by Traffic Congestion Level")
    ax.set_ylabel("Delay (minutes)")
    ax.set_xlabel("Congestion Level")
    return _save(fig, "delay_by_congestion.png")

def plot_delay_category_breakdown(df):
    #Stacked bar chart, delay category counts per transport type
    if "delay_category" not in df.columns:
        return None

    cat_order = ["On Time", "Minor", "Moderate", "Severe"]
    ct = pd.crosstab(df["transport_type"], df["delay_category"])
    # reindex to ensure consistent ordering
    ct = ct.reindex(columns=cat_order, fill_value=0)

    fig, ax = plt.subplots(figsize=(10, 6))
    ct.plot(kind="bar", stacked=True, ax=ax, edgecolor="white",
            color=["#55A868", "#FFD700", "#FF8C00", "#C44E52"])
    ax.set_title("Delay Category Breakdown by Transport Type")
    ax.set_ylabel("Number of Trips")
    ax.set_xlabel("")
    ax.legend(title="Category")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    return _save(fig, "delay_category_breakdown.png")

def plot_correlation_heatmap(corr):
    #Heatmap of the correlation matrix
    fig, ax = plt.subplots(figsize=(9, 7))
    cax = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
    fig.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)

    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(corr.columns, fontsize=9)
    ax.set_title("Feature Correlation Matrix")

    for i in range(len(corr)):
        for j in range(len(corr)):
            val = corr.values[i, j]
            color = "white" if abs(val) > 0.5 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                    fontsize=8, color=color)

    return _save(fig, "correlation_heatmap.png")

def plot_feature_importance(importance: dict):
    #Horizontal bar chart of model feature coefficients
    sorted_items = sorted(importance.items(), key=lambda kv: kv[1], reverse=True)
    names = [k for k, _ in sorted_items]
    values = [v for _, v in sorted_items]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(names, values, color="#4C72B0", edgecolor="white")
    ax.set_xlabel("Absolute Coefficient")
    ax.set_title("Logistic Regression — Feature Importance")
    ax.invert_yaxis()
    return _save(fig, "feature_importance.png")

def generate_all_plots(df, corr, importance):
    #Run all visualizations, return list of saved paths
    plots = [
        plot_delay_distribution(df),
        plot_delay_by_transport(df),
        plot_peak_vs_offpeak(df),
        plot_delay_by_congestion(df),
        plot_delay_category_breakdown(df),
        plot_correlation_heatmap(corr),
        plot_feature_importance(importance),
    ]
    return [p for p in plots if p is not None]
