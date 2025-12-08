# triggers/mouse_left_bottom_corner_trigger.py

from .trigger_base import TriggerBase
import pyautogui

class MouseLeftBottomCornerTrigger(TriggerBase):
    def __init__(self, corner_size, callback):
        self.corner_size = corner_size
        self.callback = callback
        self.triggered = False

    def update(self, state):
        screen_width, screen_height = pyautogui.size()
        x = state['mouse_x']
        y = state['mouse_y']

        if (x <= self.corner_size and
                y >= screen_height - self.corner_size):
            if not self.triggered:
                self.on_trigger()
                self.triggered = True
        else:
            self.triggered = False

    def on_trigger(self):
        self.callback()