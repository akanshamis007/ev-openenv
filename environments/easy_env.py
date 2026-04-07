from .base_ev_model import BaseEVModel

class EasyEVEnv(BaseEVModel):
    def __init__(self):
        super().__init__(
            battery_capacity=120,
            max_speed=80,
            traffic_factor=0.05
        )