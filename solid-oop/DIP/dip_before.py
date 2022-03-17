from collections import namedtuple
from dataclasses import dataclass

RGB = namedtuple('RGB', ['R', 'G', 'B'])


@dataclass
class LEDLight:
    color: RGB

    def set_rgb(self, color: RGB):
        self.color = color
        print(f'Color({color.R}, {color.G}, {color.B}) is set for a LED light')


class ToggleButton:
    def __init__(self):
        self._is_on = False
        self._led_indicator = LEDLight(RGB(0, 0, 0))

    def click(self):
        if self._is_on:
            self._is_on = False
            self._led_indicator.set_rgb(RGB(0, 0, 0))
        else:
            self._is_on = True
            self._led_indicator.set_rgb(RGB(255, 255, 255))


if __name__ == "__main__":
    btn = ToggleButton()
    btn.click()
    btn.click()
    btn.click()
    btn.click()
