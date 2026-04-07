from .base_ev_model import BaseEVModel

class EasyEVEnv(BaseEVModel):
    """Simplest task: reach destination without dying."""
    def __init__(self):
        super().__init__(battery_capacity=50, max_speed=60, traffic_factor=0.1)