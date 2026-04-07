from .base_ev_model import BaseEVModel

class HardEVEnv(BaseEVModel):
    def __init__(self):
        super().__init__(battery_capacity=40, route_length=70, traffic_factor=1.2)