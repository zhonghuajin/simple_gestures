import time
from .trigger_base import TriggerBase

class DoubleClickDownUpTrigger(TriggerBase):
    def __init__(self, max_double_click_interval=0.4, gesture_timeout=2.0, min_down=500, callback=None):
        self.max_double_click_interval = max_double_click_interval
        self.gesture_timeout = gesture_timeout
        self.min_down = min_down
        self.callback = callback

        # 内部状态
        self.last_click_time = 0
        self.click_count = 0
        self.is_gesture_active = False
        self.gesture_start_time = 0
        self.start_y = 0
        self.max_y = 0
        self.was_down = False
        self.down_threshold_met = False

    def update(self, state):
        curr_time = time.time()
        left_down = state['left_button']
        # 我们只关心 Y 轴 (垂直方向)，忽略 X 轴 (水平方向)，所以不用走直线
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
                self.max_y = y # 初始化最大深度为当前点
                self.down_threshold_met = False
                self.click_count = 0 # 重置点击计数，防止连续触发

        self.was_down = left_down

        # 2. 追踪手势移动 (Track Gesture Movement)
        if self.is_gesture_active:
            # 超时检查
            if curr_time - self.gesture_start_time > self.gesture_timeout:
                self.is_gesture_active = False
                return

            # 追踪最低点（屏幕坐标 Y 值越大越靠下）
            if y > self.max_y:
                self.max_y = y

            # 计算向下移动的深度
            down_dist = self.max_y - self.start_y

            # 检查是否满足最小向下深度要求
            if down_dist > self.min_down:
                self.down_threshold_met = True

            # 如果向下深度已达标，检测回拉
            if self.down_threshold_met:
                # 逻辑：当前 Y 坐标 <= 起始 Y 坐标
                # 这意味着鼠标已经回到了起始高度，或者拉得更高
                # 也就是：向上回拉距离 >= 向下移动距离
                if y <= self.start_y:
                    self.on_trigger()
                    self.is_gesture_active = False # 触发后重置

    def on_trigger(self):
        if self.callback:
            self.callback()