import pyautogui
import time
from collections import deque
from .trigger_base import TriggerBase

class MouseDiagonalToTopRightTrigger(TriggerBase):
    def __init__(self, corner_size, min_dist, max_time, callback):
        self.corner_size = corner_size
        self.min_dist = min_dist
        self.max_time = max_time
        self.callback = callback
        self.history = deque(maxlen=50)  # 存储最近50帧的轨迹点
        screen = pyautogui.size()
        self.screen_width = screen.width
        self.screen_height = screen.height
        self.triggered = False

    def update(self, state):
        x, y = state['mouse_x'], state['mouse_y']
        t = time.time()
        self.history.append((x, y, t))

        # 判断是否在右上角
        if x >= self.screen_width - self.corner_size and y <= self.corner_size:
            # 查找历史轨迹中，max_time 秒内距离最远的点
            for hx, hy, ht in list(self.history):
                dt = t - ht
                if dt > self.max_time:
                    continue
                dx = x - hx
                dy = y - hy
                dist = (dx ** 2 + dy ** 2) ** 0.5
                # 斜向右上：dx>0, dy<0
                if dist >= self.min_dist and dx > 0 and dy < 0:
                    if not self.triggered:
                        print(">>> 触发：鼠标大幅斜向上移动到右上角")
                        self.triggered = True
                        self.on_trigger()
                    break
            else:
                self.triggered = False  # 没触发则下次可继续
        else:
            self.triggered = False  # 离开右上角则允许再次触发

    def on_trigger(self):
        if self.callback:
            self.callback()