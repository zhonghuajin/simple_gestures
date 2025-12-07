# triggers/mouse_bottom_edge_zigzag_trigger.py

from .trigger_base import TriggerBase
import time
import pyautogui

class MouseBottomEdgeZigzagTrigger(TriggerBase):
    def __init__(self, edge_size=5, min_zigzag_dist=300, max_interval=1.2, callback=None):
        """
        edge_size: 底部边缘判定区域高度
        min_zigzag_dist: 左右来回移动的最小距离
        max_interval: 来回移动的最大时间（秒）
        callback: 触发回调
        """
        self.edge_size = edge_size
        self.min_zigzag_dist = min_zigzag_dist
        self.max_interval = max_interval
        self.callback = callback

        self.last_positions = []
        self.last_trigger_time = 0

        # 获取屏幕高度
        self.screen_height = pyautogui.size().height

    def update(self, state):
        mouse_x = state.get('mouse_x', 0)
        mouse_y = state.get('mouse_y', 0)
        now = time.time()

        # 在屏幕底部边缘
        if mouse_y >= self.screen_height - self.edge_size:
            self.last_positions.append((mouse_x, now))
            # 只保留最近 max_interval 秒内的记录
            self.last_positions = [
                (x, t) for x, t in self.last_positions if now - t <= self.max_interval
            ]

            # 检查“左到右到左”或“右到左到右”的zigzag
            if len(self.last_positions) >= 3:
                xs = [p[0] for p in self.last_positions]
                min_x = min(xs)
                max_x = max(xs)
                if max_x - min_x >= self.min_zigzag_dist:
                    # 检查是否有过往返
                    if (xs[0] < xs[-1] and xs[-1] - min_x > self.min_zigzag_dist // 2) or \
                       (xs[0] > xs[-1] and max_x - xs[-1] > self.min_zigzag_dist // 2):
                        if now - self.last_trigger_time > self.max_interval:
                            self.on_trigger()
                            self.last_trigger_time = now
                            self.last_positions.clear()
        else:
            # 离开底边缘时清空
            self.last_positions.clear()

    def on_trigger(self):
        if self.callback:
            self.callback()