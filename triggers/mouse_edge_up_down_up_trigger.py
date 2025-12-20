# triggers/mouse_edge_up_down_up_trigger.py

from .trigger_base import TriggerBase
import time

class MouseEdgeUpDownUpTrigger(TriggerBase):
    """
    鼠标上移到上边缘 -> 再下移到下边缘 -> 再上移到上边缘，触发回调
    """

    STATE_WAIT_TOP1 = 0
    STATE_WAIT_BOTTOM = 1
    STATE_WAIT_TOP2 = 2

    def __init__(self, edge_size=5, max_time=2.0, callback=None):
        self.edge_size = edge_size
        self.max_time = max_time
        self.callback = callback
        self.state = self.STATE_WAIT_TOP1
        self._last_time = None

    def update(self, state):
        mouse_y = state.get('mouse_y', 0)
        screen_height = state.get('screen_height', 1080)  # 需主程序传递
        now = time.time()
        if self.state == self.STATE_WAIT_TOP1:
            if mouse_y <= self.edge_size:
                self.state = self.STATE_WAIT_BOTTOM
                self._last_time = now
        elif self.state == self.STATE_WAIT_BOTTOM:
            if now - self._last_time > self.max_time:
                self.reset()
                return
            if mouse_y >= screen_height - self.edge_size:
                self.state = self.STATE_WAIT_TOP2
                self._last_time = now
        elif self.state == self.STATE_WAIT_TOP2:
            if now - self._last_time > self.max_time:
                self.reset()
                return
            if mouse_y <= self.edge_size:
                self.on_trigger()
                self.reset()

    def on_trigger(self):
        if self.callback:
            self.callback()

    def reset(self):
        self.state = self.STATE_WAIT_TOP1
        self._last_time = None