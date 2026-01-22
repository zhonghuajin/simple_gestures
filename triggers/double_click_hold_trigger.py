# triggers/double_click_hold_trigger.py
import time
from .trigger_base import TriggerBase

class DoubleClickHoldTrigger(TriggerBase):
    def __init__(self, 
                 max_double_click_interval=0.3, 
                 hold_duration=0.5, 
                 move_threshold=5, 
                 callback=None):
        """
        :param max_double_click_interval: 双击两下之间的最大间隔（秒）
        :param hold_duration: 双击后需要保持静止的时长（秒）
        :param move_threshold: 静止期间允许的微小移动像素（防抖）
        :param callback: 触发后的回调函数
        """
        self.max_double_click_interval = max_double_click_interval
        self.hold_duration = hold_duration
        self.move_threshold = move_threshold
        self.callback = callback

        # 状态机定义
        # 0: IDLE (空闲)
        # 1: FIRST_DOWN (第一次按下)
        # 2: FIRST_UP (第一次抬起)
        # 3: SECOND_DOWN (第二次按下)
        # 4: WAITING_FOR_HOLD (第二次抬起，开始等待静止时间)
        self.state = 0
        
        self.last_event_time = 0
        self.hold_start_time = 0
        self.anchor_x = 0
        self.anchor_y = 0

    def update(self, state):
        curr_time = time.time()
        left_down = state['left_button']
        x, y = state['mouse_x'], state['mouse_y']

        # 状态机逻辑
        if self.state == 0:  # IDLE
            if left_down:
                self.state = 1
                self.last_event_time = curr_time

        elif self.state == 1:  # FIRST_DOWN
            if not left_down:
                self.state = 2
                self.last_event_time = curr_time

        elif self.state == 2:  # FIRST_UP
            # 超时重置
            if curr_time - self.last_event_time > self.max_double_click_interval:
                self.state = 0
                return

            if left_down:
                self.state = 3
                self.last_event_time = curr_time

        elif self.state == 3:  # SECOND_DOWN
            if not left_down:
                # 双击完成，进入静止检测阶段
                self.state = 4
                self.hold_start_time = curr_time
                self.anchor_x = x
                self.anchor_y = y

        elif self.state == 4:  # WAITING_FOR_HOLD
            # 如果期间又按下了鼠标，或者移动幅度过大，则取消
            if left_down:
                self.state = 1 # 视为新的一轮点击开始
                self.last_event_time = curr_time
                return
            
            dist_sq = (x - self.anchor_x)**2 + (y - self.anchor_y)**2
            if dist_sq > self.move_threshold**2:
                self.state = 0 # 移动了，取消
                return

            # 检查时间是否满足
            if curr_time - self.hold_start_time >= self.hold_duration:
                self.on_trigger()
                self.state = 0 # 触发后重置

    def on_trigger(self):
        if self.callback:
            self.callback()