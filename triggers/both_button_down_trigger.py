from .trigger_base import TriggerBase

class BothButtonDownTrigger(TriggerBase):
    """同时按下鼠标左右键，触发 Ctrl+T"""
    def __init__(self, callback):
        self.callback = callback
        self.triggered = False

    def update(self, state):
        if state.get('right_button') and state.get('left_button'):
            if not self.triggered:
                self.on_trigger()
                self.triggered = True
        else:
            self.triggered = False

    def on_trigger(self):
        self.callback()