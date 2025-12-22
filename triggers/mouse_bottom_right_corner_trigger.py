# triggers/mouse_bottom_right_corner_trigger.py

from .trigger_base import TriggerBase

class MouseBottomRightCornerTrigger(TriggerBase):
    def __init__(self, corner_size, callback):
        self.corner_size = corner_size
        self.callback = callback
        self.triggered = False  # 防止重复触发

    def update(self, state):
        mouse_x = state['mouse_x']
        mouse_y = state['mouse_y']
        screen_w = state['screen_width']
        screen_h = state['screen_height']

        # 判断是否在右下角区域
        # x 坐标 > 屏幕宽度 - 角落大小
        # y 坐标 > 屏幕高度 - 角落大小
        in_corner = (mouse_x >= screen_w - self.corner_size) and \
                    (mouse_y >= screen_h - self.corner_size)

        if in_corner:
            if not self.triggered:
                self.on_trigger()
                self.triggered = True
        else:
            # 离开角落后重置状态，以便下次再次触发
            self.triggered = False

    def on_trigger(self):
        if self.callback:
            self.callback()