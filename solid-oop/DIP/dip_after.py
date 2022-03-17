import abc
from collections import namedtuple
from dataclasses import dataclass, field

RGB = namedtuple('RGB', ['R', 'G', 'B'])


@dataclass
class LEDLight:
    color: RGB = field(default=RGB(0, 0, 0))

    def set_rgb(self, color: RGB = RGB(0, 0, 0)):
        self.color = color
        print(f'Color({color.R}, {color.G}, {color.B}) is set for a LED light')


class ISwitch(abc.ABC):
    @abc.abstractmethod
    def on(self):
        pass

    @abc.abstractmethod
    def off(self):
        pass

class LEDSwitch(ISwitch):
    def __init__(self, light):
        self._light = light

    def on(self):
        self._light.set_rgb(RGB(255, 255, 255))

    def off(self):
        self._light.set_rgb(RGB(0, 0, 0))


class ToggleButton:
    def __init__(self, switchable_light=None):
        self._is_on = False
        self._switchable_light = switchable_light if switchable_light else LEDSwitch(
            LEDLight())

    def click(self):
        if self._is_on:
            self._is_on = False
            self._switchable_light.off()
        else:
            self._is_on = True
            self._switchable_light.on()


if __name__ == "__main__":
    btn = ToggleButton()
    btn.click()
    btn.click()
    btn.click()
    btn.click()
