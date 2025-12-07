# triggers/mouse_right_edge_horizontal_trigger.py

from .trigger_base import TriggerBase
import pyautogui

class MouseRightEdgeHorizontalTrigger(TriggerBase):
    """
    鼠标在屏幕右边缘大幅度水平移动，触发回调
    direction: 'right' 或 'left'
    """
    def __init__(self, edge_size, move_threshold, direction, callback):
        self.edge_size = edge_size  # 右边缘宽度
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

        # 只检测右边缘
        if mouse_x >= self.screen_width - self.edge_size:
            if self._start_x is None:
                self._start_x = mouse_y
                self._triggered = False
                return

            delta_y = mouse_y - self._start_x

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
            self._start_x = None
            self._triggered = False

    def on_trigger(self):
        self.callback()
        print(f">>> 已触发 右边缘大幅度{'下移' if self.direction == 'down' else '上移'}")