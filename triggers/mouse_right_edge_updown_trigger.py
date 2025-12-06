# triggers/mouse_right_edge_updown_trigger.py

from .trigger_base import TriggerBase
import pyautogui

class MouseRightEdgeUpDownTrigger(TriggerBase):
    """
    鼠标移动到右侧边缘并大幅度上移时，触发回调
    """
    def __init__(self, edge_size, move_threshold, callback):
        self.edge_size = edge_size  # 右侧边缘宽度
        self.move_threshold = move_threshold  # 上移的最小距离
        self.callback = callback
        self._start_y = None
        self._triggered = False

        # 获取屏幕尺寸
        self.screen_width, self.screen_height = pyautogui.size()

    def update(self, state):
        mouse_x = state['mouse_x']
        mouse_y = state['mouse_y']

        # 只检测右侧边缘
        if mouse_x >= self.screen_width - self.edge_size:
            if self._start_y is None:
                self._start_y = mouse_y
                self._triggered = False
                return

            delta_y = mouse_y - self._start_y

            if not self._triggered and delta_y <= -self.move_threshold:
                self._triggered = True
                self.on_trigger()
            elif abs(delta_y) < 5:
                # 防止轻微抖动重复触发
                self._triggered = False
        else:
            self._start_y = None
            self._triggered = False

    def on_trigger(self):
        self.callback()
        print(">>> 已触发 右侧边缘大幅度上移 (Ctrl+W)")