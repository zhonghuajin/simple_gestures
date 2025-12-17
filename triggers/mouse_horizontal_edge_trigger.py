# triggers/mouse_horizontal_edge_trigger.py

from .trigger_base import TriggerBase
import time

class MouseHorizontalEdgeTrigger(TriggerBase):
    """
    鼠标从左边缘移动到右边缘触发callback_right。
    鼠标从右边缘移动到左边缘可触发callback_left（本需求只用右）。
    """

    def __init__(self, edge_size=5, min_move=400, max_time=1.0, callback_left=None, callback_right=None):
        self.edge_size = edge_size
        self.min_move = min_move
        self.max_time = max_time
        self.callback_left = callback_left
        self.callback_right = callback_right
        self._state = None

    def update(self, state):
        mouse_x = state['mouse_x']
        mouse_y = state['mouse_y']
        screen_width, screen_height = self._get_screen_size()
        now = time.time()

        if self._state is None:
            if mouse_x <= self.edge_size:
                # 左边缘起点
                self._state = {
                    'start_x': mouse_x,
                    'start_time': now,
                    'from': 'left'
                }
            elif mouse_x >= screen_width - self.edge_size:
                # 右边缘起点
                self._state = {
                    'start_x': mouse_x,
                    'start_time': now,
                    'from': 'right'
                }
        else:
            start_x = self._state['start_x']
            start_time = self._state['start_time']
            from_where = self._state['from']

            if from_where == 'left':
                # 到达右边缘
                if mouse_x >= screen_width - self.edge_size:
                    if (now - start_time) <= self.max_time and (mouse_x - start_x) >= self.min_move:
                        if self.callback_right:
                            self.callback_right()
                    self._state = None
                elif (now - start_time) > self.max_time or mouse_x <= self.edge_size + 2:
                    self._state = None
            elif from_where == 'right':
                # 到达左边缘
                if mouse_x <= self.edge_size:
                    if (now - start_time) <= self.max_time and (start_x - mouse_x) >= self.min_move:
                        if self.callback_left:
                            self.callback_left()
                    self._state = None
                elif (now - start_time) > self.max_time or mouse_x >= screen_width - self.edge_size - 2:
                    self._state = None

    def _get_screen_size(self):
        import pyautogui
        return pyautogui.size()

    def on_trigger(self):
        pass