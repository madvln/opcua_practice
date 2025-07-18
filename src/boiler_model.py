class BoilerModel:
    def __init__(self, max_volume=100.0, temp_cold=10.0, temp_hot=90.0, max_flow=1.0):
        self.max_volume = max_volume
        self.temp_cold = temp_cold
        self.temp_hot = temp_hot
        self.max_flow = max_flow

        self.volume = 0.0
        self.temperature = 25.0

        self.valve_hot = 0.5   # 50%
        self.valve_cold = 0.5  # 50%
        self.valve_out = 1.0   # 100%

    def step(self, dt=1.0):
        in_hot = self.valve_hot * self.max_flow * dt
        in_cold = self.valve_cold * self.max_flow * dt
        out = self.valve_out * self.max_flow * dt

        old_volume = self.volume
        incoming = in_hot + in_cold
        total_mass = old_volume + incoming

        if total_mass > 0 and incoming > 0:
            mixed_temp = (in_hot * self.temp_hot + in_cold * self.temp_cold) / (incoming + 1e-6)
            self.temperature = (
                (self.temperature * old_volume + mixed_temp * incoming) /
                (total_mass + 1e-6)
            )

        # Обновляем объём с учётом оттока
        delta = incoming - out
        self.volume = max(0.0, min(old_volume + delta, self.max_volume))

    def get_level_percent(self):
        return (self.volume / self.max_volume) * 100.0

    def get_temperature(self):
        return self.temperature
