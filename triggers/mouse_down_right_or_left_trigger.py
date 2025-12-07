# triggers/mouse_down_right_or_left_trigger.py

from .trigger_base import TriggerBase
import time

class MouseDownRightOrLeftTrigger(TriggerBase):
    """
    按下左键，先向下再向右，触发A，否则向下再向左触发B
    """
    def __init__(self, min_down=40, min_side=40, callback_right=None, callback_left=None):
        self.min_down = min_down  # 最小向下距离
        self.min_side = min_side  # 最小左右距离
        self.callback_right = callback_right
        self.callback_left = callback_left
        self.state = 0  # 0:等待按下左键  1:检测向下  2:检测左右
        self.start_pos = None
        self.down_pos = None
        self.last_left_down = False

    def update(self, state):
        left_down = state['left_button']
        x, y = state['mouse_x'], state['mouse_y']

        if self.state == 0:
            if left_down and not self.last_left_down:
                # 按下左键，记录起始位置
                self.start_pos = (x, y)
                self.state = 1
            elif not left_down:
                self.start_pos = None
                self.down_pos = None

        elif self.state == 1:
            if not left_down:
                # 按钮松开，重置
                self.state = 0
                self.start_pos = None
                self.down_pos = None
            else:
                # 检查向下移动
                if self.start_pos and (y - self.start_pos[1]) > self.min_down:
                    self.down_pos = (x, y)
                    self.state = 2

        elif self.state == 2:
            if not left_down:
                # 按钮松开，检查左右移动
                if self.down_pos:
                    dx = x - self.down_pos[0]
                    if dx > self.min_side:
                        # 向右
                        if self.callback_right:
                            self.callback_right()
                    elif dx < -self.min_side:
                        # 向左
                        if self.callback_left:
                            self.callback_left()
                # 重置
                self.state = 0
                self.start_pos = None
                self.down_pos = None

        self.last_left_down = left_down