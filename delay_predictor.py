"""
delay_predictor.py
For this program two approaches are used to predict delays:
  1.RueBasedPredictor: simple threshold on historical avg
  2. LogisticDelayPredictor:sklearn logistic regression
By: Rakshita Singh
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler

from transit_data import TransitNetwork


class RuleBasedPredictor:
    """
    This portion flags routes as high-risk if their historical avg delay exceeds a threshold.
    Uses TransitNetwork internally (composition).
    """

    def __init__(self, threshold=5.0):
        self.threshold = threshold
        self.network = TransitNetwork()

    def fit(self, df: pd.DataFrame):
        #Populate the network from a DataFrame
        for _, row in df.iterrows():
            self.network.add_record(
                row["route_id"],
                row["actual_departure_delay_min"],
            )

    def predict_route(self, route_id: str) -> bool:
        #True if the route's avg delay is above threshold.
        route = self.network.get_route(route_id)
        if route is None:
            return False
        return route.average_delay > self.threshold

    def high_risk_routes(self) -> list:
        #List comp to get all risky route IDs
        return [r.route_id for r in self.network.all_routes
                if r.average_delay > self.threshold]

    def route_summary(self) -> dict:
        #Dict comp, {route_id: {avg, max, trips, high_risk}}
        return {
            r.route_id: {
                "avg_delay": round(r.average_delay, 2),
                "max_delay": r.max_delay,
                "trips": len(r),
                "high_risk": r.average_delay > self.threshold,
            }
            for r in self.network.all_routes
        }

class LogisticDelayPredictor:
    #Sklearn logistic regression to predict the binary 'delayed' column

    FEATURES = [
        "actual_departure_delay_min", "temperature_C",
        "humidity_percent", "wind_speed_kmh", "precipitation_mm",
        "traffic_congestion_index", "peak_hour", "holiday",
    ]

    def __init__(self):
        self.scaler = StandardScaler()
        self.model = LogisticRegression(max_iter=1000, random_state=42)
        self._fitted = False

    def train(self, df: pd.DataFrame, test_size=0.2) -> dict:

        #Train the model and return accuracy + classification report
        available = [c for c in self.FEATURES if c in df.columns]
        X = df[available].values
        y = df["delayed"].values

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )

        X_train = self.scaler.fit_transform(X_train)
        X_test = self.scaler.transform(X_test)

        self.model.fit(X_train, y_train)
        self._fitted = True

        preds = self.model.predict(X_test)
        acc = accuracy_score(y_test, preds)

        return {
            "accuracy": round(acc, 4),
            "report": classification_report(y_test, preds, zero_division=0),
            "train_size": len(X_train),
            "test_size": len(X_test),
        }

    def predict(self, df: pd.DataFrame):
        #Predict on new data. Raises RuntimeError if not trained yet
        if not self._fitted:
            raise RuntimeError("Model not trained yet — call train() first")
        available = [c for c in self.FEATURES if c in df.columns]
        X = self.scaler.transform(df[available].values)
        return self.model.predict(X)

    def feature_importance(self) -> dict:
        #Absolute coefficient per feature
        if not self._fitted:
            return {}
        coefs = self.model.coef_[0]
        available = [c for c in self.FEATURES if c in
                     ["actual_departure_delay_min", "temperature_C",
                      "humidity_percent", "wind_speed_kmh", "precipitation_mm",
                      "traffic_congestion_index", "peak_hour", "holiday"]]
        return {
            name: round(abs(float(c)), 4)
            for name, c in zip(available, coefs)
        }

if __name__ == "__main__":
    print("delay_predictor module — run main.py to use")
