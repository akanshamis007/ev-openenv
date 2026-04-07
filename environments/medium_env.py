from .base_ev_model import BaseEVModel

class MediumEVEnv(BaseEVModel):
    """Balanced task: medium distance, medium traffic, mixed weather."""
    def __init__(self):
        super().__init__(
            battery_capacity=80,
            max_speed=70,
            traffic_factor=0.15,
            total_distance=50
        )