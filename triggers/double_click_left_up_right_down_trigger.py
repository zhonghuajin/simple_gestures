import time
import math
from .trigger_base import TriggerBase

class DoubleClickLeftUpRightDownTrigger(TriggerBase):
    def __init__(self, max_double_click_interval=0.4, gesture_timeout=2.0, min_move=100, callback=None):
        """
        :param max_double_click_interval: 双击判定的最大间隔（秒）
        :param gesture_timeout: 手势完成的最大允许时长（秒）
        :param min_move: 每个方向（左、上、右、下）移动的最小像素距离
        :param callback: 触发后的回调函数
        """
        self.max_double_click_interval = max_double_click_interval
        self.gesture_timeout = gesture_timeout
        self.min_move = min_move
        self.callback = callback

        # 状态变量
        self.last_left_up_time = 0
        self.is_gesture_active = False
        self.gesture_start_time = 0
        self.was_left_down = False
        
        # 手势阶段: 0=等待, 1=向左, 2=向上, 3=向右, 4=向下
        self.phase = 0
        self.ref_pos = (0, 0) # 当前阶段的参考坐标

    def update(self, state):
        curr_time = time.time()
        left_down = state['left_button']
        x, y = state['mouse_x'], state['mouse_y']

        # === 1. 检测双击 ===
        # 检测左键按下瞬间
        if left_down and not self.was_left_down:
            # 如果距离上次松开的时间很短，视为双击的第二次按下
            if (curr_time - self.last_left_up_time) < self.max_double_click_interval:
                self._start_gesture(curr_time, x, y)
            else:
                # 否则只是普通的第一次按下，重置手势
                self._reset_gesture()

        # 检测左键松开瞬间
        if not left_down and self.was_left_down:
            self.last_left_up_time = curr_time

        self.was_left_down = left_down

        # === 2. 手势轨迹检测 ===
        if self.is_gesture_active:
            # 超时检查
            if (curr_time - self.gesture_start_time) > self.gesture_timeout:
                self._reset_gesture()
                return

            # 计算相对于当前阶段起点的位移
            dx = x - self.ref_pos[0]
            dy = y - self.ref_pos[1]

            # 阶段 1: 向左
            if self.phase == 1:
                if dx < -self.min_move:
                    # print(">>> 阶段1完成: 向左")
                    self.phase = 2
                    self.ref_pos = (x, y) # 重置参考点为当前位置，用于判断下一阶段

            # 阶段 2: 向上
            elif self.phase == 2:
                if dy < -self.min_move:
                    # print(">>> 阶段2完成: 向上")
                    self.phase = 3
                    self.ref_pos = (x, y)

            # 阶段 3: 向右
            elif self.phase == 3:
                if dx > self.min_move:
                    # print(">>> 阶段3完成: 向右")
                    self.phase = 4
                    self.ref_pos = (x, y)

            # 阶段 4: 向下 (完成)
            elif self.phase == 4:
                if dy > self.min_move:
                    print(">>> 阶段4完成: 向下 -> 触发动作！")
                    if self.callback:
                        self.callback()
                    self._reset_gesture()

    def _start_gesture(self, time_now, x, y):
        self.is_gesture_active = True
        self.gesture_start_time = time_now
        self.phase = 1 # 开始检测向左
        self.ref_pos = (x, y)
        # print(">>> 双击检测成功，开始检测 左->上->右->下 手势")

    def _reset_gesture(self):
        self.is_gesture_active = False
        self.phase = 0