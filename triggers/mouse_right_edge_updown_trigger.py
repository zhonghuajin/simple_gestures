# triggers/mouse_right_edge_updown_trigger.py

from .trigger_base import TriggerBase
import pyautogui

class MouseRightEdgeUpDownTrigger(TriggerBase):
    """
    鼠标移动到右侧边缘并上下移动一次，触发回调
    """
    def __init__(self, edge_size, move_threshold, callback):
        self.edge_size = edge_size  # 右侧边缘宽度
        self.move_threshold = move_threshold  # 上下移动的最小距离
        self.callback = callback
        self._pre_y = None
        self._state = 0  # 0:初始, 1:检测到向上, 2:检测到向下

        # 获取屏幕宽度
        self.screen_width, self.screen_height = pyautogui.size()

    def update(self, state):
        mouse_x = state['mouse_x']
        mouse_y = state['mouse_y']

        # 只在鼠标位于右侧边缘时检测
        if mouse_x >= self.screen_width - self.edge_size:
            if self._pre_y is None:
                self._pre_y = mouse_y
                self._state = 0
                return

            delta_y = mouse_y - self._pre_y

            if self._state == 0 and delta_y <= -self.move_threshold:
                # 先向上
                self._state = 1
                self._pre_y = mouse_y
            elif self._state == 1 and delta_y >= self.move_threshold:
                # 再向下
                self._state = 2
                self._pre_y = mouse_y
                self.on_trigger()
            elif abs(delta_y) > 0:
                # 更新_y，避免小抖动干扰
                self._pre_y = mouse_y
        else:
            self._pre_y = None
            self._state = 0

    def on_trigger(self):
        self.callback()
        print(">>> 已触发 右侧边缘上下移动 (Ctrl+W)")