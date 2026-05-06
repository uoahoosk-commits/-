"""
Visualization Module
Creates a graph showing temperature trends with anomalies highlighted
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams
import warnings

warnings.filterwarnings("ignore")

# Set Korean font support
rcParams['font.family'] = 'DejaVu Sans'
rcParams['axes.unicode_minus'] = False


def visualize_temperatures():
    """
    Visualizes temperature data with normal temperatures as a blue line
    and detected anomalies as red points
    """
    
    try:
        # Load the data with anomalies
        df = pd.read_csv("weather_with_anomalies.csv")
        df["date"] = pd.to_datetime(df["date"])
        
        if df.empty:
            print("✗ No data found. Please run detect.py first.")
            return
        
        # Sort by date
        df = df.sort_values("date")
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # Plot normal temperatures as blue line
        normal_data = df[df["is_anomaly"] == False]
        ax.plot(normal_data["date"], normal_data["max_temp"], 
                color="blue", linewidth=1.5, label="Normal Temperature", alpha=0.8)
        
        # Plot anomalies as red points
        anomalies = df[df["is_anomaly"] == True]
        if len(anomalies) > 0:
            ax.scatter(anomalies["date"], anomalies["max_temp"], 
                      color="red", s=100, label="Anomaly", marker="o", zorder=5, alpha=0.8)
        
        # Formatting
        ax.set_xlabel("Date", fontsize=12, fontweight="bold")
        ax.set_ylabel("Maximum Temperature (°C)", fontsize=12, fontweight="bold")
        ax.set_title("Seoul Temperature Analysis - Daily Maximum Temperature\n(Anomaly Detection: Heat Waves and Cold Snaps)", 
                    fontsize=14, fontweight="bold", pad=20)
        
        # Format x-axis to show dates nicely
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        plt.xticks(rotation=45, ha="right")
        
        # Add grid
        ax.grid(True, alpha=0.3, linestyle="--")
        
        # Add legend
        ax.legend(loc="best", fontsize=11, framealpha=0.9)
        
        # Add statistics box
        stats_text = f"Total records: {len(df)}\nAnomalies: {len(anomalies)}\n"
        stats_text += f"Avg temp: {df['max_temp'].mean():.1f}°C\n"
        stats_text += f"Min temp: {df['max_temp'].min():.1f}°C\n"
        stats_text += f"Max temp: {df['max_temp'].max():.1f}°C"
        
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
               fontsize=10, verticalalignment="top", 
               bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))
        
        # Adjust layout and save
        plt.tight_layout()
        plt.savefig("temperature_analysis.png", dpi=300, bbox_inches="tight")
        print(f"✓ Visualization saved to temperature_analysis.png")
        
        plt.show()
    
    except FileNotFoundError:
        print("✗ weather_with_anomalies.csv not found. Please run detect.py first.")
    except Exception as e:
        print(f"✗ Error during visualization: {e}")


if __name__ == "__main__":
    visualize_temperatures()
