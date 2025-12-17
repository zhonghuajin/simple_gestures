# triggers/mouse_vertical_edge_trigger.py

from .trigger_base import TriggerBase
import time

class MouseVerticalEdgeTrigger(TriggerBase):
    """
    鼠标从底部边缘移动到顶部边缘触发callback_up，
    从顶部边缘移动到底部边缘触发callback_down。
    """

    def __init__(self, edge_size=5, min_move=400, max_time=1.0, callback_up=None, callback_down=None):
        self.edge_size = edge_size
        self.min_move = min_move
        self.max_time = max_time
        self.callback_up = callback_up
        self.callback_down = callback_down
        self._state = None

    def update(self, state):
        mouse_x = state['mouse_x']
        mouse_y = state['mouse_y']
        screen_width, screen_height = self._get_screen_size()

        now = time.time()

        if self._state is None:
            # 检查是否处于顶部或底部
            if mouse_y >= screen_height - self.edge_size:
                # 记录起点：底部
                self._state = {
                    'start_y': mouse_y,
                    'start_time': now,
                    'from': 'bottom'
                }
            elif mouse_y <= self.edge_size:
                # 记录起点：顶部
                self._state = {
                    'start_y': mouse_y,
                    'start_time': now,
                    'from': 'top'
                }
        else:
            # 已经有起点
            start_y = self._state['start_y']
            start_time = self._state['start_time']
            from_where = self._state['from']

            if from_where == 'bottom':
                # 看看是否到达顶部
                if mouse_y <= self.edge_size:
                    if (now - start_time) <= self.max_time and (start_y - mouse_y) >= self.min_move:
                        if self.callback_up:
                            self.callback_up()
                    self._state = None
                # 超时或大幅移动回底部则重置
                elif (now - start_time) > self.max_time or mouse_y >= screen_height - self.edge_size - 2:
                    self._state = None
            elif from_where == 'top':
                # 到达底部
                if mouse_y >= screen_height - self.edge_size:
                    if (now - start_time) <= self.max_time and (mouse_y - start_y) >= self.min_move:
                        if self.callback_down:
                            self.callback_down()
                    self._state = None
                elif (now - start_time) > self.max_time or mouse_y <= self.edge_size + 2:
                    self._state = None

    def _get_screen_size(self):
        import pyautogui
        return pyautogui.size()

    def on_trigger(self):
        pass