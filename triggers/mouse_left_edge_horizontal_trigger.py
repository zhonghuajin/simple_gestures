# triggers/mouse_left_edge_horizontal_trigger.py

from .trigger_base import TriggerBase
import pyautogui

class MouseLeftEdgeHorizontalTrigger(TriggerBase):
    """
    鼠标在屏幕左边缘大幅度水平移动，触发回调
    direction: 'down' 或 'up'
    """
    def __init__(self, edge_size, move_threshold, direction, callback):
        self.edge_size = edge_size  # 左边缘宽度
        self.move_threshold = move_threshold  # 垂直移动阈值
        self.direction = direction  # 'down' 或 'up'
        self.callback = callback
        self._start_y = None
        self._triggered = False

        # 屏幕尺寸
        self.screen_width, self.screen_height = pyautogui.size()

    def update(self, state):
        mouse_x = state['mouse_x']
        mouse_y = state['mouse_y']

        # 只检测左边缘
        if mouse_x <= self.edge_size:
            if self._start_y is None:
                self._start_y = mouse_y
                self._triggered = False
                return

            delta_y = mouse_y - self._start_y

            if self.direction == 'down':
                if not self._triggered and delta_y >= self.move_threshold:
                    self._triggered = True
                    self.on_trigger()
            elif self.direction == 'up':
                if not self._triggered and delta_y <= -self.move_threshold:
                    self._triggered = True
                    self.on_trigger()

            # 防止轻微抖动重复触发
            if abs(delta_y) < 5:
                self._triggered = False

        else:
            self._start_y = None
            self._triggered = False

    def on_trigger(self):
        self.callback()
        print(f">>> 已触发 左边缘大幅度{'下移' if self.direction == 'down' else '上移'}")