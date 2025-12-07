# triggers/mouse_left_up_down_up_trigger.py

from .trigger_base import TriggerBase

class MouseLeftUpDownUpTrigger(TriggerBase):
    """
    检测左键按下时，鼠标依次移动：上->下->上，触发回调
    """
    def __init__(self, min_move=30, max_time=1.0, callback=None):
        self.min_move = min_move
        self.max_time = max_time
        self.callback = callback
        self.reset()

    def reset(self):
        self.state = 0
        self.start_time = None
        self.last_y = None

    def update(self, state):
        left_down = state.get("left_button")
        y = state.get("mouse_y")
        now = __import__('time').time()

        if not left_down:
            self.reset()
            return

        if self.state == 0:
            # 第一次按下，记录起点
            self.start_time = now
            self.last_y = y
            self.state = 1
            return

        if self.state == 1:
            # 检测向上
            if y < self.last_y - self.min_move:
                self.last_y = y
                self.state = 2
            elif now - self.start_time > self.max_time:
                self.reset()
            return

        if self.state == 2:
            # 检测向下
            if y > self.last_y + self.min_move:
                self.last_y = y
                self.state = 3
            elif now - self.start_time > self.max_time:
                self.reset()
            return

        if self.state == 3:
            # 再次检测向上
            if y < self.last_y - self.min_move:
                self.on_trigger()
                self.reset()
            elif now - self.start_time > self.max_time:
                self.reset()

    def on_trigger(self):
        if self.callback:
            self.callback()