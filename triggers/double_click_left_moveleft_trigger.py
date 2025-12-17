# triggers/double_click_left_moveleft_trigger.py

from .trigger_base import TriggerBase
import time

class DoubleClickLeftMoveLeftTrigger(TriggerBase):
    """
    双击左键后，整体向左移动（方向为主，不要求直线），触发回调
    """
    def __init__(self, max_double_click_interval=0.45, gesture_timeout=1.2, min_left_move=300, callback=None):
        self.max_double_click_interval = max_double_click_interval
        self.gesture_timeout = gesture_timeout
        self.min_left_move = min_left_move
        self.callback = callback

        self.state = 0  # 0:等待第一次点击，1:等待第二次点击，2:等待向左移动
        self.last_down_time = 0
        self.first_up_time = 0
        self.start_pos = None
        self.last_pos = None

    def update(self, state):
        mouse_x = state['mouse_x']
        mouse_y = state['mouse_y']
        left_down = state['left_button']

        now = time.time()

        if self.state == 0:
            if left_down:
                self.state = 1
                self.last_down_time = now
        elif self.state == 1:
            if not left_down:
                self.first_up_time = now
                self.state = 2
                self.last_pos = (mouse_x, mouse_y)
                self.start_pos = (mouse_x, mouse_y)
        elif self.state == 2:
            # 等待第二次按下
            if left_down:
                if now - self.first_up_time < self.max_double_click_interval:
                    self.state = 3
                    self.last_down_time = now
                else:
                    self.state = 0
            elif now - self.first_up_time > self.max_double_click_interval:
                self.state = 0
        elif self.state == 3:
            # 第二次松开
            if not left_down:
                self.state = 4
                self.start_pos = (mouse_x, mouse_y)
                self.last_pos = (mouse_x, mouse_y)
                self.gesture_start_time = now
        elif self.state == 4:
            # 检测向左移动趋势
            if now - self.gesture_start_time > self.gesture_timeout:
                self.state = 0
            else:
                move_x = mouse_x - self.start_pos[0]
                if move_x < -self.min_left_move:
                    self.on_trigger()
                    self.state = 0

    def on_trigger(self):
        if self.callback:
            self.callback()