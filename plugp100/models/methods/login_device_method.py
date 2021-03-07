from models.methods import method
from typing import Any

class LoginDeviceMethod(method.Method):
    def __init__(self, params: Any):
        super().__init__("login_device", params)
        self.requestTimeMils = 0

    def set_request_time_milis(self, t: float):
        self.requestTimeMils = t

