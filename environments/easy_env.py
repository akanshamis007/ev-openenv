from .base_ev_model import BaseEVModel

class EasyEVEnv(BaseEVModel):
    """Simple environment: small distance, low traffic, mild weather."""
    def __init__(self):
        super().__init__(
            battery_capacity=50,
            max_speed=60,
            traffic_factor=0.05,
            total_distance=20
        )