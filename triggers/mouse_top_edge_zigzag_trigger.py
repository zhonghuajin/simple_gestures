# triggers/mouse_top_edge_zigzag_trigger.py

from .trigger_base import TriggerBase
import time

class MouseTopEdgeZigzagTrigger(TriggerBase):
    def __init__(
        self,
        edge_size=5,
        min_move_dist=80,
        max_interval=1.2,
        callback_left=None,
        callback_right=None
    ):
        """
        edge_size: 顶部边缘判定区域高度
        min_move_dist: 触发的最小水平移动距离
        max_interval: 检测移动的最大时间（秒）
        callback_left: 向左移动回调
        callback_right: 向右移动回调
        """
        self.edge_size = edge_size
        self.min_move_dist = min_move_dist
        self.max_interval = max_interval
        self.callback_left = callback_left
        self.callback_right = callback_right

        self.last_x = None
        self.last_time = None
        self.last_trigger_time = 0

    def update(self, state):
        mouse_x = state.get('mouse_x', 0)
        mouse_y = state.get('mouse_y', 0)
        now = time.time()

        if mouse_y <= self.edge_size:
            if self.last_x is None:
                self.last_x = mouse_x
                self.last_time = now
                return

            dx = mouse_x - self.last_x
            dt = now - self.last_time

            # 向右
            if dx > self.min_move_dist and dt <= self.max_interval:
                if now - self.last_trigger_time > self.max_interval:
                    self.on_trigger('right')
                    self.last_trigger_time = now
                self.last_x = mouse_x
                self.last_time = now
            # 向左
            elif dx < -self.min_move_dist and dt <= self.max_interval:
                if now - self.last_trigger_time > self.max_interval:
                    self.on_trigger('left')
                    self.last_trigger_time = now
                self.last_x = mouse_x
                self.last_time = now
            elif dt > self.max_interval:
                self.last_x = mouse_x
                self.last_time = now
        else:
            self.last_x = None
            self.last_time = None

    def on_trigger(self, direction):
        if direction == 'right' and self.callback_right:
            self.callback_right()
        elif direction == 'left' and self.callback_left:
            self.callback_left()