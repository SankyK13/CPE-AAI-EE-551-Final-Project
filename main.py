"""
main.py
Runs the full transit delay analysis pipeline.
By: Pal Sanjaybhai Anghan

Note: This should be converted to a Jupyter Notebook (main.ipynb). 
Each section below maps to a notebook cell.
"""

from data_loader import load_data, clean_data, data_summary
from analytics import (
    compute_statistics, compute_rms_delay, compute_percentiles,
    get_high_delays, delays_by_group, delay_generator,
    correlation_matrix, peak_hour_delay_summary, traffic_delay_summary,
)
from delay_predictor import RuleBasedPredictor, LogisticDelayPredictor
from visualizations import generate_all_plots

DATA_FILE = "public_transport_delays.csv"
THRESHOLD = 5.0


def print_section(title):
    #Print a section header
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


def main():
    #1. Load and clean
    print_section("1. Data Loading & Cleaning")

    raw = load_data(DATA_FILE)
    print(f"  Raw rows: {len(raw)}")

    df = clean_data(raw)
    print(f"  After cleaning: {len(df)}")

    info = data_summary(df)
    print(f"  Date range: {info['date_range'][0]} to {info['date_range'][1]}")
    print(f"  Transport types: {', '.join(info['transport_types'])}")
    print(f"  Unique routes: {info['unique_routes']}")
    print(f"  Avg delay: {info['avg_delay']} min")
    print(f"  % delayed: {info['delayed_pct']}%")

    #2. Descriptive stats
    print_section("2. Descriptive Statistics")

    delays = list(delay_generator(df))
    mean, std, median = compute_statistics(delays)
    rms = compute_rms_delay(delays)
    pcts = compute_percentiles(delays)

    print(f"  Mean:   {mean:.2f} min")
    print(f"  Std:    {std:.2f} min")
    print(f"  Median: {median:.1f} min")
    print(f"  RMS:    {rms:.2f} min")
    print(f"  Percentiles: {pcts}")

    high = get_high_delays(delays, 10)
    print(f"  Trips > 10 min delay: {len(high)} ({len(high)/len(delays)*100:.1f}%)")

    #3. Group analysis
    print_section("3. Group Analysis")

    print("\n  -- By Transport Type --")
    for transport, avg in sorted(delays_by_group(df, "transport_type").items()):
        print(f"    {transport:<8} {avg:.2f} min")

    print("\n  -- By Peak Hour --")
    peak_df = peak_hour_delay_summary(df)
    print(peak_df.to_string())

    print("\n  -- By Traffic Congestion --")
    traffic_df = traffic_delay_summary(df)
    print(traffic_df.to_string())

    print("\n  -- By Delay Category --")
    for cat, avg in sorted(delays_by_group(df, "delay_category").items()):
        print(f"    {cat:<10} {avg:.2f} min")

    #4. Rule-based prediction
    print_section("4. Rule-Based Prediction")

    rule_pred = RuleBasedPredictor(threshold=THRESHOLD)
    rule_pred.fit(df)

    risky = rule_pred.high_risk_routes()
    print(f"  Threshold: {THRESHOLD} min")
    print(f"  Total routes: {len(rule_pred.network)}")
    print(f"  High-risk routes: {len(risky)}")

    # show top 10 by avg delay using enumerate
    summary = rule_pred.route_summary()
    top10 = sorted(summary.items(), key=lambda kv: kv[1]["avg_delay"], reverse=True)[:10]
    print("\n  -- Top 10 Routes by Avg Delay --")
    for i, (route_id, info) in enumerate(top10, start=1):
        flag = "!!" if info["high_risk"] else "  "
        print(f"  {i:>3}. {flag} {route_id}  avg={info['avg_delay']:.1f}  "
              f"max={info['max_delay']}  trips={info['trips']}")

    # demonstrate set operations
    print("\n  -- Set Operations (Delay Categories) --")
    all_cats = rule_pred.network.all_delay_categories()
    print(f"  All delay categories across network: {all_cats}")

    ids = list(rule_pred.network.route_ids)
    if len(ids) >= 2:
        common = rule_pred.network.common_categories(ids[0], ids[1])
        print(f"  Categories shared by {ids[0]} & {ids[1]}: {common}")
        unique = rule_pred.network.unique_categories(ids[0])
        print(f"  Categories unique to {ids[0]}: {unique if unique else 'none (all shared)'}")

    #5. Logistic regression
    print_section("5. Logistic Regression Model")

    lr = LogisticDelayPredictor()
    results = lr.train(df)

    print(f"  Train: {results['train_size']}  Test: {results['test_size']}")
    print(f"  Accuracy: {results['accuracy']:.2%}")
    print(f"\n{results['report']}")

    importance = lr.feature_importance()
    print("  Feature importance:")
    for feat, coef in sorted(importance.items(), key=lambda x: x[1], reverse=True):
        print(f"    {feat:<35} {coef:.4f}")

    #6. Correlation
    print_section("6. Correlation Matrix")
    corr = correlation_matrix(df)
    print(corr.to_string())

    #7. Visualizations
    print_section("7. Generating Figures")
    paths = generate_all_plots(df, corr, importance)
    print(f"\n  {len(paths)} figures saved to figures/")

    print_section("Done")


if __name__ == "__main__":
    main()
