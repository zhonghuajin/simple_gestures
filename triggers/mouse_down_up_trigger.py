# triggers/mouse_down_up_trigger.py

from .trigger_base import TriggerBase
import time

class MouseDownUpTrigger(TriggerBase):
    """
    鼠标按住左键时，先下移再上移，触发回调
    """
    def __init__(self, min_move=60, max_time=1.0, callback=None):
        self.min_move = min_move      # 需要的最小移动距离
        self.max_time = max_time      # 最大识别时间（秒）
        self.callback = callback
        self.reset()

    def reset(self):
        self.state = "idle"
        self.start_y = None
        self.min_y = None
        self.max_y = None
        self.start_time = None

    def update(self, state):
        y = state['mouse_y']
        left = state.get('left_button', False)
        now = time.time()

        if self.state == "idle":
            if left:
                # 按下左键，初始化
                self.start_time = now
                self.start_y = y
                self.min_y = y
                self.max_y = y
                self.state = "down"
        elif self.state == "down":
            if left:
                # 检查下移
                if y > self.max_y:
                    self.max_y = y
                if y < self.min_y:
                    self.min_y = y
                # 判断是否下移达到阈值
                if (self.max_y - self.start_y) > self.min_move:
                    self.state = "up"
            else:
                self.reset()
        elif self.state == "up":
            if left:
                # 检查回升
                if y < self.min_y:
                    self.min_y = y
                # 判断是否上移达到阈值
                if (self.max_y - y) > self.min_move:
                    # 满足先下再上
                    self.on_trigger()
                    self.reset()
                # 超时重置
                elif (now - self.start_time) > self.max_time:
                    self.reset()
            else:
                self.reset()

    def on_trigger(self):
        if self.callback:
            self.callback()