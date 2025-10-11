import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from main import run_simulation
from visualize import create_plots

class IoTSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("IoT Network Simulator")
        self.root.geometry("800x600")
        
        # Simulation state
        self.simulation_running = False
        self.simulation_thread = None
        self.received_packets = []
        self.logs = []
        self.log_callback = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Parameters frame
        param_frame = ttk.LabelFrame(self.root, text="Simulation Parameters", padding=10)
        param_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(param_frame, text="Number of Devices:").grid(row=0, column=0, sticky=tk.W)
        self.num_devices_var = tk.StringVar(value="5")
        ttk.Entry(param_frame, textvariable=self.num_devices_var, width=10).grid(row=0, column=1)
        
        ttk.Label(param_frame, text="Simulation Time (seconds):").grid(row=0, column=2, sticky=tk.W)
        self.sim_time_var = tk.StringVar(value="30")
        ttk.Entry(param_frame, textvariable=self.sim_time_var, width=10).grid(row=0, column=3)
        
        # Control buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.start_btn = ttk.Button(btn_frame, text="Start Simulation", command=self.start_simulation)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(btn_frame, text="Stop Simulation", command=self.stop_simulation, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Show Plots", command=self.show_plots).pack(side=tk.LEFT, padx=5)
        
        # Logs area
        log_frame = ttk.LabelFrame(self.root, text="Simulation Logs", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Plots frame (initially empty)
        self.plots_frame = ttk.Frame(self.root)
        self.plots_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Log callback for real-time updates
        def log_cb(msg):
            self.logs.append(msg)
            self.update_logs(msg)
        
        self.log_callback = log_cb
    
    def update_logs(self, msg):
        """Append message to log text area."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update_idletasks()  # Refresh GUI
    
    def start_simulation(self):
        if self.simulation_running:
            return
        
        try:
            num_devices = int(self.num_devices_var.get())
            sim_time = float(self.sim_time_var.get())
        except ValueError:
            self.update_logs("Error: Invalid parameters! Use integers for devices and float for time.")
            return
        
        self.simulation_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.received_packets = []
        self.logs = []
        self.log_text.delete(1.0, tk.END)  # Clear logs
        self.clear_plots()
        
        self.simulation_thread = threading.Thread(
            target=self._run_sim_thread, 
            args=(num_devices, sim_time)
        )
        self.simulation_thread.daemon = True
        self.simulation_thread.start()
    
    def _run_sim_thread(self, num_devices, sim_time):
        """Run simulation in background thread."""
        try:
            self.received_packets, _ = run_simulation(
                num_devices, sim_time, self.log_callback
            )
            self.update_logs("Simulation completed!")
        except Exception as e:
            self.update_logs(f"Simulation error: {str(e)}")
        finally:
            self.simulation_running = False
            self.root.after(0, self._simulation_finished)  # Update GUI on main thread
    
    def _simulation_finished(self):
        """Called after simulation ends to update buttons."""
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
    
    def stop_simulation(self):
        """Basic stop (SimPy doesn't support easy interrupt; this just flags it)."""
        self.simulation_running = False
        self.update_logs("Stop requested. Simulation will end soon.")
        # For full stop, you'd need to use simpy's event interrupts—extend if needed.
    
    def show_plots(self):
        if not self.received_packets:
            self.update_logs("No simulation data to plot!")
            return
        self.clear_plots()
        create_plots(self.received_packets, self.plots_frame)
        self.update_logs("Plots displayed!")
    
    def clear_plots(self):
        """Clear existing plots."""
        for widget in self.plots_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = IoTSimulatorGUI(root)
    root.mainloop()
