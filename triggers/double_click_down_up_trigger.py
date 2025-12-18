import time
from .trigger_base import TriggerBase

class DoubleClickDownUpTrigger(TriggerBase):
    def __init__(self, max_double_click_interval=0.4, gesture_timeout=2.0, min_down=500, max_horizontal_deviation=150, callback=None):
        """
        :param max_double_click_interval: 双击间隔
        :param gesture_timeout: 手势超时
        :param min_down: 向下移动的最小距离
        :param max_horizontal_deviation: 水平方向允许的最大偏移量（像素）。
                                         如果X轴偏移超过此值，则认为不是纯粹的下上动作（可能是下左/下右），取消触发。
        :param callback: 回调
        """
        self.max_double_click_interval = max_double_click_interval
        self.gesture_timeout = gesture_timeout
        self.min_down = min_down
        self.max_horizontal_deviation = max_horizontal_deviation # 新增参数
        self.callback = callback

        # 内部状态
        self.last_click_time = 0
        self.click_count = 0
        self.is_gesture_active = False
        self.gesture_start_time = 0
        self.start_y = 0
        self.start_x = 0 # 新增：记录起始X
        self.max_y = 0
        self.was_down = False
        self.down_threshold_met = False

    def update(self, state):
        curr_time = time.time()
        left_down = state['left_button']
        x = state['mouse_x']
        y = state['mouse_y']

        # 1. 检测双击 (Detect Double Click)
        if left_down and not self.was_down:
            # 鼠标按下事件
            time_diff = curr_time - self.last_click_time
            
            if time_diff < self.max_double_click_interval:
                self.click_count += 1
            else:
                self.click_count = 1
            
            self.last_click_time = curr_time

            if self.click_count == 2:
                # 双击确认，开始追踪手势
                self.is_gesture_active = True
                self.gesture_start_time = curr_time
                self.start_y = y
                self.start_x = x # 记录起始 X 坐标
                self.max_y = y 
                self.down_threshold_met = False
                self.click_count = 0 

        self.was_down = left_down

        # 2. 追踪手势移动 (Track Gesture Movement)
        if self.is_gesture_active:
            # A. 超时检查
            if curr_time - self.gesture_start_time > self.gesture_timeout:
                self.is_gesture_active = False
                return

            # B. 水平偏移检查 (核心防冲突逻辑)
            # 如果当前的 X 坐标与起始 X 坐标相差太大，说明用户意图不是垂直下上，而是下左或下右
            if abs(x - self.start_x) > self.max_horizontal_deviation:
                # print(f">>> 水平偏移过大 ({abs(x - self.start_x)} > {self.max_horizontal_deviation})，取消下上手势")
                self.is_gesture_active = False
                return

            # C. 追踪最低点
            if y > self.max_y:
                self.max_y = y

            # D. 计算向下移动的深度
            down_dist = self.max_y - self.start_y

            # E. 检查是否满足最小向下深度要求
            if down_dist > self.min_down:
                self.down_threshold_met = True

            # F. 如果向下深度已达标，检测回拉
            if self.down_threshold_met:
                # 逻辑：回到起始高度
                if y <= self.start_y:
                    self.on_trigger()
                    self.is_gesture_active = False # 触发后重置

    def on_trigger(self):
        if self.callback:
            self.callback()