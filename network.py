import simpy
import random
class IoTNetwork:
    def __init__(self, env):
        self.env = env
        self.received_packets = []
        self.gateway = "Central Gateway"
        
    def receive_packet(self, packet):
        """Process incoming packet at gateway."""
        packet["received_at"] = self.env.now
        self.received_packets.append(packet)
        print(f"[{self.env.now:.2f}] Gateway received: {packet['value']}°C from {packet['device']}")
        
    def simulate_interference(self):
        """Optional: Add background interference events."""
        while True:
            yield self.env.timeout(random.uniform(5, 10))  
            print(f"[{self.env.now:.2f}] Network interference detected!")
            