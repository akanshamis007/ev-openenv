from .base_ev_model import BaseEVModel

class EasyEVEnv(BaseEVModel):
    def __init__(self):
        super().__init__(battery_capacity=60, route_length=25, traffic_factor=0.5)