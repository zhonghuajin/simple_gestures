# triggers/double_click_up_move_trigger.py
import time
from .trigger_base import TriggerBase

class DoubleClickUpMoveTrigger(TriggerBase):
    def __init__(self, 
                 max_double_click_interval=0.4, 
                 gesture_timeout=1.2,
                 min_up_move=500,
                 callback=None):
        """
        :param max_double_click_interval: 双击两下之间的最大间隔（秒）
        :param gesture_timeout: 双击后上移的最大时间窗口（秒）
        :param min_up_move: 上移的最小像素距离
        :param callback: 触发后的回调函数
        """
        self.max_double_click_interval = max_double_click_interval
        self.gesture_timeout = gesture_timeout
        self.min_up_move = min_up_move
        self.callback = callback

        # 状态机定义
        # 0: IDLE
        # 1: FIRST_DOWN
        # 2: FIRST_UP
        # 3: SECOND_DOWN
        # 4: READY_FOR_UP_MOVE
        self.state = 0
        self.last_event_time = 0
        self.gesture_start_time = 0
        self.anchor_x = 0
        self.anchor_y = 0

    def update(self, state):
        curr_time = time.time()
        left_down = state['left_button']
        x, y = state['mouse_x'], state['mouse_y']

        if self.state == 0:  # IDLE
            if left_down:
                self.state = 1
                self.last_event_time = curr_time

        elif self.state == 1:  # FIRST_DOWN
            if not left_down:
                self.state = 2
                self.last_event_time = curr_time

        elif self.state == 2:  # FIRST_UP
            if curr_time - self.last_event_time > self.max_double_click_interval:
                self.state = 0
                return
            if left_down:
                self.state = 3
                self.last_event_time = curr_time

        elif self.state == 3:  # SECOND_DOWN
            if not left_down:
                # 双击完成，准备检测上提
                self.state = 4
                self.gesture_start_time = curr_time
                self.anchor_x = x
                self.anchor_y = y

        elif self.state == 4:  # READY_FOR_UP_MOVE
            if curr_time - self.gesture_start_time > self.gesture_timeout:
                # 超时
                self.state = 0
                return
            # 计算Y方向上移
            delta_y = self.anchor_y - y
            if delta_y >= self.min_up_move:
                self.on_trigger()
                self.state = 0
                return
            # 若此时用户又按下鼠标，重新开始
            if left_down:
                self.state = 1
                self.last_event_time = curr_time

    def on_trigger(self):
        if self.callback:
            self.callback()