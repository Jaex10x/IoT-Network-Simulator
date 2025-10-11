import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

def create_plots(received_packets, parent_window=None):
    """
    Create and return Matplotlib figures.
    If parent_window is provided, embed in Tkinter.
    """
    if not received_packets:
        print("No packets received!")
        return None
    
    times = [p["received_at"] - p["timestamp"] for p in received_packets]  # Latency
    values = [p["value"] for p in received_packets]
    timestamps = [p["timestamp"] for p in received_packets]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    
    ax1.hist(times, bins=20, edgecolor='black')
    ax1.set_title('Packet Latency Distribution')
    ax1.set_xlabel('Latency (seconds)')
    
    ax2.plot(timestamps, values, 'o-')
    ax2.set_title('Received Sensor Data Over Time')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Temperature (°C)')
    
    plt.tight_layout()
    
    if parent_window:
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        return canvas
    else:
        plt.show()
        return fig

# Standalone call (for non-GUI)
if __name__ == "__main__":
    # Dummy data for testing
    dummy_packets = [{"timestamp": i, "received_at": i + 0.2, "value": 25 + i*0.1} for i in range(10)]
    create_plots(dummy_packets)
