import random


class IoTDevice:
    def __init__(self, env, name, data_rate=3.0):  
        self.env = env
        self.name = name
        self.data_rate = data_rate
        self.data_buffer = []  
        
    def generate_data(self):
        """Simulate data generation (e.g., sensor readings)."""
        while True:
            
            data = {"timestamp": self.env.now, "value": random.uniform(30, 40), "device": self.name}
            self.data_buffer.append(data)
            print(f"[{self.env.now:.2f}] {self.name} generated: {data['value']}°C")
            yield self.env.timeout(1 / self.data_rate)  
    
    def send_data(self, network):
        """Send data to network (simplified; in reality, use MQTT/CoAP)."""
        while True:
            if self.data_buffer:
                packet = self.data_buffer.pop(0)
                
                delay = random.uniform(0.1, 0.5)  
                loss_prob = 0.01  
                if random.random() > loss_prob:
                    yield self.env.timeout(delay)
                    network.receive_packet(packet)
                    print(f"[{self.env.now:.2f}] {self.name} sent packet to gateway")
                else:
                    print(f"[{self.env.now:.2f}] Packet from {self.name} lost!")
            else:
                yield self.env.timeout(0.1)  
