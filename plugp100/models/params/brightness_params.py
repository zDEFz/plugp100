class BrightnessParams(object):
    def __init__(self):
        self.brightness: bool = 100

    def set_brightness(self, new_value: int):
        self.brightness = new_value

    def get_brightness(self):
        return self.brightness
