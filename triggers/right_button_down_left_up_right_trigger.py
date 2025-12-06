# triggers/right_button_down_left_up_right_trigger.py
from .trigger_base import TriggerBase

class RightButtonDownLeftUpRightTrigger(TriggerBase):
    """右键按下，向左→上→右，触发 F5"""
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
                # 向左
                if self.x0 - x > self.min_dist:
                    self.x1 = x
                    self.y1 = y
                    self.state = 2
            elif self.state == 2:
                # 向上
                if self.y1 - y > self.min_dist:
                    self.x2 = x
                    self.y2 = y
                    self.state = 3
            elif self.state == 3:
                # 向右
                if x - self.x2 > self.min_dist:
                    if not self.triggered:
                        self.on_trigger()
                        self.triggered = True
                    self.state = 4
        else:
            self.state = 0
            self.x0 = None
            self.y0 = None
            self.triggered = False

    def on_trigger(self):
        self.callback()