"""
Anomaly Detection Module
Detects anomalous temperatures (heat waves or cold snaps) using Isolation Forest
"""

import pandas as pd
from sklearn.ensemble import IsolationForest
import warnings

warnings.filterwarnings("ignore")


def detect_anomalies():
    """
    Detects temperature anomalies from weather.csv using Isolation Forest
    Anomalies represent extreme temperatures (heat waves or cold snaps)
    Prints detected anomalies with dates and temperatures
    """
    
    try:
        # Load the CSV file
        df = pd.read_csv("weather.csv")
        df["date"] = pd.to_datetime(df["date"])
        
        if df.empty:
            print("✗ No data found in weather.csv")
            return None
        
        print(f"Loaded {len(df)} temperature records")
        
        # Prepare data for Isolation Forest
        X = df[["max_temp"]].values
        
        # Initialize Isolation Forest
        # contamination: expected proportion of anomalies (adjust as needed)
        iso_forest = IsolationForest(
            contamination=0.05,  # Expect ~5% anomalies
            random_state=42,
            n_estimators=100
        )
        
        # Predict anomalies (-1 = anomaly, 1 = normal)
        predictions = iso_forest.fit_predict(X)
        
        # Add predictions to dataframe
        df["anomaly"] = predictions
        df["is_anomaly"] = df["anomaly"] == -1
        
        # Extract anomalies
        anomalies = df[df["is_anomaly"]]
        
        # Print results
        print(f"\n{'='*60}")
        print(f"Anomaly Detection Results (Isolation Forest)")
        print(f"{'='*60}")
        print(f"Total anomalies detected: {len(anomalies)}")
        print(f"Normal records: {len(df) - len(anomalies)}")
        print(f"\n{'Date':<15} {'Temperature (°C)':<20} {'Type':<20}")
        print(f"{'-'*55}")
        
        if len(anomalies) > 0:
            for idx, row in anomalies.iterrows():
                date_str = row["date"].strftime("%Y-%m-%d")
                temp = row["max_temp"]
                
                # Determine type of anomaly
                mean_temp = df["max_temp"].mean()
                if temp > mean_temp:
                    anomaly_type = "Heat Wave 🔥"
                else:
                    anomaly_type = "Cold Snap ❄️"
                
                print(f"{date_str:<15} {temp:>18.1f}°C  {anomaly_type:<20}")
        else:
            print("No anomalies detected")
        
        print(f"{'='*60}\n")
        
        # Save results
        df.to_csv("weather_with_anomalies.csv", index=False, encoding="utf-8")
        print(f"✓ Results saved to weather_with_anomalies.csv")
        
        return df
    
    except FileNotFoundError:
        print("✗ weather.csv not found. Please run collect_data.py first.")
        return None
    except Exception as e:
        print(f"✗ Error during anomaly detection: {e}")
        return None


if __name__ == "__main__":
    detect_anomalies()
