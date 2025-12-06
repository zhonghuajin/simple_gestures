from .trigger_base import TriggerBase

class RightButtonDownDownTrigger(TriggerBase):
    """右键按下，向下移动，触发 Ctrl+V"""
    def __init__(self, min_dist, callback):
        self.min_dist = min_dist
        self.callback = callback
        self.state = 0
        self.y0 = None
        self.triggered = False

    def update(self, state):
        y = state['mouse_y']
        if state['right_button']:
            if self.state == 0:
                self.y0 = y
                self.state = 1
                self.triggered = False
            elif self.state == 1:
                # 向下
                if y - self.y0 > self.min_dist:
                    if not self.triggered:
                        self.on_trigger()
                        self.triggered = True
                    self.state = 2
        else:
            self.state = 0
            self.y0 = None
            self.triggered = False

    def on_trigger(self):
        self.callback()