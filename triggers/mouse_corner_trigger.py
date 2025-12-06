# triggers/mouse_corner_trigger.py
from .trigger_base import TriggerBase

class MouseCornerTrigger(TriggerBase):
    """鼠标移动到左上角触发"""
    def __init__(self, corner_size, callback):
        self.corner_size = corner_size
        self.callback = callback
        self.triggered = False

    def update(self, state):
        x = state['mouse_x']
        y = state['mouse_y']
        if x < self.corner_size and y < self.corner_size:
            if not self.triggered:
                self.on_trigger()
                self.triggered = True
        else:
            self.triggered = False

    def on_trigger(self):
        self.callback()