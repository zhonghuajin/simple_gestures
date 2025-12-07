# triggers/mouse_left_down_left_right_trigger.py

import time
from .trigger_base import TriggerBase

class MouseLeftDownLeftRightTrigger(TriggerBase):
    def __init__(self, min_move=100, max_time=1.2, callback_left=None, callback_right=None):
        self.min_move = min_move
        self.max_time = max_time
        self.callback_left = callback_left
        self.callback_right = callback_right
        self.active = False
        self.start_x = None
        self.start_time = None
        self.already_triggered = False

    def update(self, state):
        left_down = state.get('left_button', False)
        x = state.get('mouse_x', 0)

        if left_down and not self.active:
            # 鼠标左键按下，开始监控
            self.active = True
            self.start_x = x
            self.start_time = time.time()
            self.already_triggered = False

        elif not left_down and self.active:
            # 鼠标左键松开，重置状态
            self.active = False
            self.start_x = None
            self.start_time = None
            self.already_triggered = False

        elif self.active and not self.already_triggered:
            # 监控移动距离和方向
            delta_x = x - self.start_x
            duration = time.time() - self.start_time

            if abs(delta_x) >= self.min_move and duration <= self.max_time:
                if delta_x < 0 and self.callback_left:
                    self.on_trigger('left')
                elif delta_x > 0 and self.callback_right:
                    self.on_trigger('right')
                self.already_triggered = True

    def on_trigger(self, direction):
        if direction == 'left' and self.callback_left:
            self.callback_left()
        elif direction == 'right' and self.callback_right:
            self.callback_right()