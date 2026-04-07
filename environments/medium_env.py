from .base_ev_model import BaseEVModel

class MediumEVEnv(BaseEVModel):
    def __init__(self):
        super().__init__(battery_capacity=50, route_length=40, traffic_factor=0.8)