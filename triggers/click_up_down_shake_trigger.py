# triggers/click_up_down_shake_trigger.py
import time
from .trigger_base import TriggerBase

class ClickUpDownShakeTrigger(TriggerBase):
    def __init__(self, min_segment_dist=50, max_click_time=0.3, max_gesture_time=2.0, required_shakes=3, callback=None):
        """
        :param min_segment_dist: 每次上下移动的最小像素距离，防止抖动误触
        :param max_click_time: 初始点击的最大持续时间（秒）
        :param max_gesture_time: 整个手势（点击后开始摇晃）的最大允许时间
        :param required_shakes: 需要改变方向的次数（例如：上-下-上 为3次）
        :param callback: 触发后的回调函数
        """
        self.min_segment_dist = min_segment_dist
        self.max_click_time = max_click_time
        self.max_gesture_time = max_gesture_time
        self.required_shakes = required_shakes
        self.callback = callback

        # 状态机
        # 0: IDLE (等待点击)
        # 1: MOUSE_DOWN (左键按下)
        # 2: WATCHING (点击完成，监听移动)
        self.state_code = 0
        
        self.click_start_time = 0
        self.watch_start_time = 0
        self.anchor_y = 0
        
        # 当前移动方向: 0=无, 1=上(Y减小), -1=下(Y增加)
        self.current_dir = 0 
        self.shake_count = 0

    def update(self, state):
        curr_time = time.time()
        mouse_down = state['left_button']
        y = state['mouse_y']

        # 状态 0: 等待点击开始
        if self.state_code == 0:
            if mouse_down:
                self.state_code = 1
                self.click_start_time = curr_time

        # 状态 1: 正在点击（按下状态）
        elif self.state_code == 1:
            if not mouse_down:
                # 鼠标松开
                if curr_time - self.click_start_time < self.max_click_time:
                    # 点击时间短，符合条件，进入监听模式
                    self.state_code = 2
                    self.watch_start_time = curr_time
                    self.anchor_y = y
                    self.current_dir = 0
                    self.shake_count = 0
                else:
                    # 按住时间太长，视为拖拽，重置
                    self.state_code = 0

        # 状态 2: 监听上下摇晃
        elif self.state_code == 2:
            # 如果再次按下鼠标，中断手势
            if mouse_down:
                self.state_code = 1
                self.click_start_time = curr_time
                return
            
            # 超时检查
            if curr_time - self.watch_start_time > self.max_gesture_time:
                self.state_code = 0
                return

            dy = y - self.anchor_y

            # 屏幕坐标系：Y向下增加
            # 向上移动 (dy 为负)
            if dy < -self.min_segment_dist:
                # 如果之前是向下或初始状态
                if self.current_dir != 1:
                    self.shake_count += 1
                    self.current_dir = 1 # 标记为向上
                    self.anchor_y = y    # 更新锚点，准备检测下一次反向
            
            # 向下移动 (dy 为正)
            elif dy > self.min_segment_dist:
                # 如果之前是向上或初始状态
                if self.current_dir != -1:
                    self.shake_count += 1
                    self.current_dir = -1 # 标记为向下
                    self.anchor_y = y     # 更新锚点

            # 检查触发条件
            if self.shake_count >= self.required_shakes:
                if self.callback:
                    self.callback()
                self.state_code = 0