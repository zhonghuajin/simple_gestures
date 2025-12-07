# triggers/mouse_bottom_edge_side_zigzag_trigger.py

from .trigger_base import TriggerBase
import time
import pyautogui

class MouseBottomEdgeZigzagTrigger(TriggerBase):
    def __init__(
        self,
        edge_size=5,
        min_zigzag_dist=150,
        max_interval=1.2,
        side_width_ratio=0.3,
        callback_left=None,
        callback_right=None
    ):
        """
        edge_size: 底部边缘判定区域高度
        min_zigzag_dist: 左右来回移动的最小距离
        max_interval: 来回移动的最大时间（秒）
        side_width_ratio: 屏幕宽度的多少算做左/右侧（如0.3为左/右各30%）
        callback_left: 左侧回调
        callback_right: 右侧回调
        """
        self.edge_size = edge_size
        self.min_zigzag_dist = min_zigzag_dist
        self.max_interval = max_interval
        self.callback_left = callback_left
        self.callback_right = callback_right

        self.last_positions_left = []
        self.last_positions_right = []
        self.last_trigger_time_left = 0
        self.last_trigger_time_right = 0

        screen = pyautogui.size()
        self.screen_width = screen.width
        self.screen_height = screen.height
        self.left_max_x = int(self.screen_width * side_width_ratio)
        self.right_min_x = int(self.screen_width * (1 - side_width_ratio))

    def update(self, state):
        mouse_x = state.get('mouse_x', 0)
        mouse_y = state.get('mouse_y', 0)
        now = time.time()

        # 在屏幕底部边缘
        if mouse_y >= self.screen_height - self.edge_size:
            # 左侧区域
            if mouse_x <= self.left_max_x:
                self.last_positions_left.append((mouse_x, now))
                # 只保留最近 max_interval 秒内的记录
                self.last_positions_left = [
                    (x, t) for x, t in self.last_positions_left if now - t <= self.max_interval
                ]
                if self._detect_zigzag(self.last_positions_left):
                    if now - self.last_trigger_time_left > self.max_interval:
                        self.on_trigger_left()
                        self.last_trigger_time_left = now
                        self.last_positions_left.clear()
            else:
                self.last_positions_left.clear()

            # 右侧区域
            if mouse_x >= self.right_min_x:
                self.last_positions_right.append((mouse_x, now))
                self.last_positions_right = [
                    (x, t) for x, t in self.last_positions_right if now - t <= self.max_interval
                ]
                if self._detect_zigzag(self.last_positions_right):
                    if now - self.last_trigger_time_right > self.max_interval:
                        self.on_trigger_right()
                        self.last_trigger_time_right = now
                        self.last_positions_right.clear()
            else:
                self.last_positions_right.clear()
        else:
            self.last_positions_left.clear()
            self.last_positions_right.clear()

    def _detect_zigzag(self, positions):
        # 检查是否有足够的Z字形移动
        if len(positions) >= 3:
            xs = [p[0] for p in positions]
            min_x = min(xs)
            max_x = max(xs)
            if max_x - min_x >= self.min_zigzag_dist:
                # 检查是否有过往返（从左到右又回左，或相反）
                if (xs[0] < xs[-1] and xs[-1] - min_x > self.min_zigzag_dist // 2) or \
                   (xs[0] > xs[-1] and max_x - xs[-1] > self.min_zigzag_dist // 2):
                    return True
        return False

    def on_trigger_left(self):
        if self.callback_left:
            self.callback_left()

    def on_trigger_right(self):
        if self.callback_right:
            self.callback_right()