import threading
import random
from device import IoTDevice
from network import IoTNetwork

def run_simulation(num_devices=5, sim_time=30, log_callback=None):
    """
    Run the simulation. 
    - log_callback: Optional function to append logs (e.g., for GUI).
    Returns: (received_packets, total_logs)
    """
    env = simpy.Environment()
    network = IoTNetwork(env)
    logs = []  # Mo store sa logs
    
    def log_message(msg):
        logs.append(f"[{env.now:.2f}] {msg}")
        if log_callback:
            log_callback(logs[-1])
    
    # use log_message instead of print 
    original_print = print
    def custom_print(*args, **kwargs):
        msg = ' '.join(map(str, args))
        log_message(msg)
        original_print(*args, **kwargs)  # Still print to console if needed
    
    # Monkey-patch print globally for this run (or inject into classes)
    import builtins
    builtins.print = custom_print
    
    # Create and start devices
    devices = [IoTDevice(env, f"Sensor_{i}", data_rate=random.uniform(0.5, 2.0)) for i in range(num_devices)]
    for device in devices:
        env.process(device.generate_data())
        env.process(device.send_data(network))
    env.process(network.simulate_interference())
    
    # Run simulation
    env.run(until=sim_time)
    
    # Restore original print
    builtins.print = original_print
    
    return network.received_packets, logs

# For backward compatibility: Run standalone
if __name__ == "__main__":
    packets, logs = run_simulation()
    print("\nSimulation complete. Logs:")
    for log in logs:
        print(log)
