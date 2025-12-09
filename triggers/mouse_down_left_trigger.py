# triggers/mouse_down_left_trigger.py

from .trigger_base import TriggerBase
import time

class MouseDownLeftTrigger(TriggerBase):
    def __init__(self, min_down=100, min_left=100, max_time=1.0, callback=None):
        """
        min_down: 向下移动的最小像素
        min_left: 向左移动的最小像素
        max_time: 必须在多少秒内完成
        callback: 触发时调用的函数
        """
        self.min_down = min_down
        self.min_left = min_left
        self.max_time = max_time
        self.callback = callback

        self.reset()

    def reset(self):
        self.state = 0
        self.start_time = None
        self.start_pos = None
        self.down_pos = None

    def update(self, state):
        x = state['mouse_x']
        y = state['mouse_y']
        right_down = state['right_button']

        t = time.time()

        if self.state == 0:
            if right_down:
                self.state = 1
                self.start_time = t
                self.start_pos = (x, y)
        elif self.state == 1:
            if not right_down:
                self.reset()
                return
            if abs(y - self.start_pos[1]) >= self.min_down:
                self.state = 2
                self.down_pos = (x, y)
        elif self.state == 2:
            if not right_down:
                self.reset()
                return
            if abs(x - self.down_pos[0]) >= self.min_left and (x - self.down_pos[0]) < 0:
                if t - self.start_time <= self.max_time:
                    self.on_trigger()
                self.reset()
            elif t - self.start_time > self.max_time:
                self.reset()

    def on_trigger(self):
        if self.callback:
            self.callback()