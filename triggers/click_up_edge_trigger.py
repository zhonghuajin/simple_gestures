from .trigger_base import TriggerBase
import time

class ClickUpEdgeTrigger(TriggerBase):
    def __init__(self, min_up_dist=150, max_click_time=0.3, max_gesture_time=2.0, callback_left=None, callback_right=None):
        """
        手势：点击左键 -> 向上移动 -> 撞击左边缘或右边缘
        :param min_up_dist: 向上移动的最小像素距离
        :param max_click_time: 判定为点击的最大按下时间
        :param max_gesture_time: 整个手势的最大耗时
        :param callback_left: 撞击左边缘触发的回调 (Home)
        :param callback_right: 撞击右边缘触发的回调 (End)
        """
        self.min_up_dist = min_up_dist
        self.max_click_time = max_click_time
        self.max_gesture_time = max_gesture_time
        self.callback_left = callback_left
        self.callback_right = callback_right
        
        # 状态机
        # 0: 空闲
        # 1: 鼠标按下
        # 2: 鼠标抬起（完成点击），等待上移
        # 3: 已经上移足够距离，等待撞墙
        self.state = 0
        self.start_time = 0
        self.click_pos = (0, 0)

    def update(self, state):
        curr_time = time.time()
        x, y = state['mouse_x'], state['mouse_y']
        lb = state['left_button']
        w = state['screen_width']

        # 超时重置机制 (除了空闲状态)
        if self.state != 0 and (curr_time - self.start_time > self.max_gesture_time):
            self.reset()
            return

        # 状态 0: 等待按下
        if self.state == 0:
            if lb:
                self.state = 1
                self.start_time = curr_time
                self.click_pos = (x, y)
        
        # 状态 1: 等待抬起
        elif self.state == 1:
            if not lb:
                # 检查按键时间，确保是点击而不是长按
                if curr_time - self.start_time <= self.max_click_time:
                    self.state = 2
                else:
                    self.reset()
        
        # 状态 2: 等待上移
        elif self.state == 2:
            if lb: # 如果中途又按下了鼠标，重置
                self.reset()
                return
            
            # 检查是否向上移动了足够的距离 (y 减小)
            if self.click_pos[1] - y > self.min_up_dist:
                self.state = 3
        
        # 状态 3: 等待撞墙
        elif self.state == 3:
            if lb:
                self.reset()
                return

            # 撞左墙
            if x <= 5:
                if self.callback_left:
                    self.callback_left()
                self.reset()
            
            # 撞右墙
            elif x >= w - 5:
                if self.callback_right:
                    self.callback_right()
                self.reset()

    def reset(self):
        self.state = 0