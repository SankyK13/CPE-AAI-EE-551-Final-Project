"""
data_loader.py
Thid program handles reading/loading, validating, and cleaning the transit delay CSV.
By: Sankalp Khira
"""
import pandas as pd

def load_data(file_path: str) -> pd.DataFrame:
    #Load CSV file and do basic validation on required columns
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: could not find '{file_path}'")
        raise

    df.columns = df.columns.str.strip()

    # make sure the columns we actually need are present
    required = {"trip_id", "route_id", "transport_type",
                "actual_departure_delay_min"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing columns: {missing}")

    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    #Drop bad rows and add a delay category column.
    df = df.copy()

    # drop rows missing critical fields
    df = df.dropna(subset=["actual_departure_delay_min", "route_id"])

    # toss negative delays (probably data errors)
    df = df[df["actual_departure_delay_min"] >= 0]

    # parse dates if the column exists
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # categorize delays using a lambda + map
    categorize = lambda d: (
        "On Time" if d <= 2 else
        "Minor" if d <= 5 else
        "Moderate" if d <= 10 else
        "Severe"
    )
    df["delay_category"] = df["actual_departure_delay_min"].map(categorize)

    # fill missing event types
    if "event_type" in df.columns:
        df["event_type"] = df["event_type"].fillna("None")

    return df.reset_index(drop=True)

def data_summary(df: pd.DataFrame) -> dict:
    # Quick summary of the cleaned dataset. Returns a dict.
    date_range = ("N/A", "N/A")
    if "date" in df.columns:
        date_range = (str(df["date"].min().date()), str(df["date"].max().date()))

    return {
        "total_trips":     len(df),
        "date_range":      date_range,                       # tuple (immutable)
        "transport_types": sorted(df["transport_type"].unique().tolist()),
        "unique_routes":   df["route_id"].nunique(),
        "avg_delay":       round(df["actual_departure_delay_min"].mean(), 2),
        "delayed_pct":     round(df["delayed"].mean() * 100, 1) if "delayed" in df.columns else None,
    }

if __name__ == "__main__":
    df = load_data("public_transport_delays.csv")
    df = clean_data(df)
    print(data_summary(df))
