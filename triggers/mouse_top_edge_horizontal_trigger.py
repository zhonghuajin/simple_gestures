# triggers/mouse_top_edge_horizontal_trigger.py

from .trigger_base import TriggerBase
import pyautogui

class MouseTopEdgeHorizontalTrigger(TriggerBase):
    """
    鼠标在屏幕上边缘大幅度水平移动，触发回调
    direction: 'right' 或 'left'
    """
    def __init__(self, edge_size, move_threshold, direction, callback):
        self.edge_size = edge_size  # 上边缘高度
        self.move_threshold = move_threshold  # 水平移动阈值
        self.direction = direction  # 'right' 或 'left'
        self.callback = callback
        self._start_x = None
        self._triggered = False

        # 屏幕尺寸
        self.screen_width, self.screen_height = pyautogui.size()

    def update(self, state):
        mouse_x = state['mouse_x']
        mouse_y = state['mouse_y']

        # 只检测上边缘
        if mouse_y <= self.edge_size:
            if self._start_x is None:
                self._start_x = mouse_x
                self._triggered = False
                return

            delta_x = mouse_x - self._start_x

            if self.direction == 'right':
                if not self._triggered and delta_x >= self.move_threshold:
                    self._triggered = True
                    self.on_trigger()
            elif self.direction == 'left':
                if not self._triggered and delta_x <= -self.move_threshold:
                    self._triggered = True
                    self.on_trigger()

            # 防止轻微抖动重复触发
            if abs(delta_x) < 5:
                self._triggered = False

        else:
            self._start_x = None
            self._triggered = False

    def on_trigger(self):
        self.callback()
        print(f">>> 已触发 上边缘大幅度{'右移' if self.direction == 'right' else '左移'}")