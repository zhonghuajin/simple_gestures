# triggers/right_button_down_up_down_trigger.py
from .trigger_base import TriggerBase

class RightButtonDownUpDownTrigger(TriggerBase):
    """右键按下并做下-上-下移动触发"""
    def __init__(self, min_dist, callback):
        self.min_dist = min_dist
        self.callback = callback
        self.state = 0
        self.y0 = None
        self.triggered = False

    def update(self, state):
        mouse_y = state['mouse_y']
        if state['right_button']:
            if self.state == 0:
                self.y0 = mouse_y
                self.state = 1
                self.triggered = False
            elif self.state == 1:
                if mouse_y - self.y0 > self.min_dist:
                    self.state = 2
                    self.y1 = mouse_y
            elif self.state == 2:
                if self.y1 - mouse_y > self.min_dist:
                    self.state = 3
                    self.y2 = mouse_y
            elif self.state == 3:
                if mouse_y - self.y2 > self.min_dist:
                    if not self.triggered:
                        self.on_trigger()
                        self.triggered = True
                    self.state = 4
        else:
            self.state = 0
            self.y0 = None
            self.triggered = False

    def on_trigger(self):
        self.callback()