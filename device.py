import random
import simpy

class IoTDevice:
    def __init__(self, env, name, data_rate=1.0):  # data_rate in packets/sec
        self.env = env
        self.name = name
        self.data_rate = data_rate
        self.data_buffer = []  # Simulated data queue
        
    def generate_data(self):
        """Simulate data generation (e.g., sensor readings)."""
        while True:
            # Generate random data (e.g., temp between 20-30°C)
            data = {"timestamp": self.env.now, "value": random.uniform(20, 30), "device": self.name}
            self.data_buffer.append(data)
            print(f"[{self.env.now:.2f}] {self.name} generated: {data['value']}°C")
            yield self.env.timeout(1 / self.data_rate)  # Time between generations
    
    def send_data(self, network):
        """Send data to network (simplified; in reality, use MQTT/CoAP)."""
        while True:
            if self.data_buffer:
                packet = self.data_buffer.pop(0)
                # Simulate transmission delay and possible loss
                delay = random.uniform(0.1, 0.5)  # Network delay
                loss_prob = 0.1  # 10% packet loss
                if random.random() > loss_prob:
                    yield self.env.timeout(delay)
                    network.receive_packet(packet)
                    print(f"[{self.env.now:.2f}] {self.name} sent packet to gateway")
                else:
                    print(f"[{self.env.now:.2f}] Packet from {self.name} lost!")
            else:
                yield self.env.timeout(0.1)  # Check buffer periodically
