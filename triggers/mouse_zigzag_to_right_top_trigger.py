from .trigger_base import TriggerBase
import pyautogui
import time

class MouseZigzagToRightTopTrigger(TriggerBase):
    """
    检测鼠标是否先明显向下，再明显向右移动，如果满足则将鼠标移动到屏幕右上角。
    """

    def __init__(self, move_threshold=80, callback=None, timeout=1.2):
        self.move_threshold = move_threshold
        self.callback = callback
        self.timeout = timeout
        self.reset()

    def reset(self):
        self.stage = 0
        self.last_pos = None
        self.last_time = None

    def update(self, state):
        x, y = state['mouse_x'], state['mouse_y']
        now = time.time()

        if self.last_pos is None:
            self.last_pos = (x, y)
            self.last_time = now
            return

        dx = x - self.last_pos[0]
        dy = y - self.last_pos[1]

        # 超时自动重置
        if now - self.last_time > self.timeout:
            self.reset()
            self.last_pos = (x, y)
            self.last_time = now
            return

        # 阶段0：检测向下
        if self.stage == 0 and dy > self.move_threshold and abs(dx) < self.move_threshold // 2:
            self.stage = 1
            self.last_pos = (x, y)
            self.last_time = now
            # print("检测到向下")
            return

        # 阶段1：检测向右
        if self.stage == 1 and dx > self.move_threshold and abs(dy) < self.move_threshold // 2:
            self.stage = 2
            self.last_pos = (x, y)
            self.last_time = now
            # print("检测到向右")
            self.on_trigger()
            self.reset()
            return

        # 允许小范围位置抖动更新
        if abs(dx) > 2 or abs(dy) > 2:
            self.last_pos = (x, y)
            self.last_time = now

    def on_trigger(self):
        screen_width, screen_height = pyautogui.size()
        pyautogui.moveTo(screen_width - 1, 1, duration=0.15)
        print(">>> 检测到先下后右，已将鼠标移动到屏幕右上角。")
        if self.callback:
            self.callback()