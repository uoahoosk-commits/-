"""
Visualization Module
Visualizes temperature data with anomalies highlighted
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


def visualize_temperatures():
    """
    Creates a visualization of temperature data with anomalies
    Normal temperatures: blue line
    Anomalies: red points
    Includes statistics box with summary information
    """
    
    try:
        # Load the data with anomalies
        df = pd.read_csv("weather_with_anomalies.csv")
        df["date"] = pd.to_datetime(df["date"])
        
        if df.empty:
            print("✗ No data found in weather_with_anomalies.csv")
            print("  Please run detect.py first.")
            return
        
        print("Creating visualization...")
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # Separate normal and anomaly data
        normal_data = df[~df["is_anomaly"]]
        anomaly_data = df[df["is_anomaly"]]
        
        # Plot normal temperatures as a blue line
        ax.plot(normal_data["date"], normal_data["max_temp"], 
                color="blue", linewidth=2, label="Normal Temperature", alpha=0.7)
        
        # Plot anomalies as red points
        ax.scatter(anomaly_data["date"], anomaly_data["max_temp"], 
                   color="red", s=100, label="Anomaly (Heat Wave/Cold Snap)", 
                   marker="o", zorder=5, edgecolors="darkred", linewidth=1.5)
        
        # Add moving average (7-day)
        df_sorted = df.sort_values("date")
        moving_avg = df_sorted["max_temp"].rolling(window=7, center=True).mean()
        ax.plot(df_sorted["date"], moving_avg, 
                color="orange", linewidth=2, label="7-day Moving Average", 
                linestyle="--", alpha=0.6)
        
        # Formatting
        ax.set_xlabel("Date", fontsize=12, fontweight="bold")
        ax.set_ylabel("Maximum Temperature (°C)", fontsize=12, fontweight="bold")
        ax.set_title("Seoul Temperature Analysis - Anomaly Detection", 
                     fontsize=14, fontweight="bold", pad=20)
        
        # Format x-axis to show dates nicely
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        plt.xticks(rotation=45, ha="right")
        
        # Add grid
        ax.grid(True, alpha=0.3, linestyle="--")
        
        # Add legend
        ax.legend(loc="upper left", fontsize=10, framealpha=0.95)
        
        # Calculate statistics
        total_records = len(df)
        anomaly_count = len(anomaly_data)
        normal_count = len(normal_data)
        avg_temp = df["max_temp"].mean()
        min_temp = df["max_temp"].min()
        max_temp = df["max_temp"].max()
        
        # Add statistics box
        stats_text = (
            f"📊 Statistics\n"
            f"─────────────────\n"
            f"Total Records: {total_records}\n"
            f"Anomalies: {anomaly_count} ({100*anomaly_count/total_records:.1f}%)\n"
            f"Normal: {normal_count}\n"
            f"─────────────────\n"
            f"Avg Temp: {avg_temp:.1f}°C\n"
            f"Min Temp: {min_temp:.1f}°C\n"
            f"Max Temp: {max_temp:.1f}°C"
        )
        
        props = dict(boxstyle="round", facecolor="wheat", alpha=0.8)
        ax.text(0.02, 0.97, stats_text, transform=ax.transAxes, 
                fontsize=10, verticalalignment="top", bbox=props, 
                family="monospace")
        
        # Tight layout
        plt.tight_layout()
        
        # Save figure
        output_file = "temperature_analysis.png"
        plt.savefig(output_file, dpi=300, bbox_inches="tight")
        print(f"✓ Visualization saved to {output_file}")
        
        # Display the plot
        plt.show()
        
    except FileNotFoundError:
        print("✗ weather_with_anomalies.csv not found.")
        print("  Please run detect.py first.")
    except Exception as e:
        print(f"✗ Error during visualization: {e}")


if __name__ == "__main__":
    visualize_temperatures()
