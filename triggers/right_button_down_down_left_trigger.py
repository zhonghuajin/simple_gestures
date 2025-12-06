# triggers/right_button_down_down_left_trigger.py
from .trigger_base import TriggerBase

class RightButtonDownDownLeftTrigger(TriggerBase):
    """右键按下，向下再向左，触发 Ctrl+W"""
    def __init__(self, min_dist, callback):
        self.min_dist = min_dist
        self.callback = callback
        self.state = 0
        self.x0 = None
        self.y0 = None
        self.triggered = False

    def update(self, state):
        x = state['mouse_x']
        y = state['mouse_y']
        if state['right_button']:
            if self.state == 0:
                self.x0 = x
                self.y0 = y
                self.state = 1
                self.triggered = False
            elif self.state == 1:
                # 向下
                if y - self.y0 > self.min_dist:
                    self.y1 = y
                    self.x1 = x
                    self.state = 2
            elif self.state == 2:
                # 向左
                if self.x1 - x > self.min_dist:
                    if not self.triggered:
                        self.on_trigger()
                        self.triggered = True
                    self.state = 3
        else:
            self.state = 0
            self.x0 = None
            self.y0 = None
            self.triggered = False

    def on_trigger(self):
        self.callback()