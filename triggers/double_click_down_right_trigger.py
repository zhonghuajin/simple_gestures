import time
from .trigger_base import TriggerBase

class DoubleClickDownRightTrigger(TriggerBase):
    """
    触发条件：连续两次左键点击（双击）后，鼠标整体趋势先向下再向右移动，每段只要位移趋势达标即可，不要求直线。
    参数：
        - max_double_click_interval: 两次点击最大间隔（秒）
        - gesture_timeout: 手势完成最大允许时长（秒）
        - min_move: 每段最小趋势位移像素
        - callback: 触发回调
    """
    def __init__(
        self,
        max_double_click_interval=0.4,
        gesture_timeout=1.2,
        min_move=80,
        callback=None
    ):
        self.max_double_click_interval = max_double_click_interval
        self.gesture_timeout = gesture_timeout
        self.min_move = min_move
        self.callback = callback

        self.click_times = []
        self.last_left_state = False
        self.gesture_stage = 0
        self.gesture_start_time = None
        self.ref_pos = None
        self.last_pos = None

    def update(self, state):
        mouse_x = state.get('mouse_x', 0)
        mouse_y = state.get('mouse_y', 0)
        left_button = state.get('left_button', False)
        cur_time = time.time()

        # 1. 检测双击
        if self.last_left_state and not left_button:
            self.click_times.append(cur_time)
            if len(self.click_times) > 2:
                self.click_times = self.click_times[-2:]
            if (len(self.click_times) == 2 and
                self.click_times[1] - self.click_times[0] <= self.max_double_click_interval):
                print(">>> 检测到双击，准备检测手势")
                self.gesture_stage = 1  # 进入第一段
                self.gesture_start_time = cur_time
                self.ref_pos = (mouse_x, mouse_y)
                self.last_pos = (mouse_x, mouse_y)
                self.click_times = []
            else:
                if len(self.click_times) == 2:
                    self.click_times = [self.click_times[-1]]
        self.last_left_state = left_button

        # 2. 手势过程
        if self.gesture_stage > 0:
            if cur_time - self.gesture_start_time > self.gesture_timeout:
                print(">>> 手势超时，重置")
                self.gesture_stage = 0
                return

            x0, y0 = self.ref_pos
            dx = mouse_x - x0
            dy = mouse_y - y0

            if self.gesture_stage == 1:
                # 向下趋势，y轴增加即可
                if dy > self.min_move:
                    print(">>> 手势1/2 向下趋势达成")
                    self.gesture_stage = 2
                    self.ref_pos = (mouse_x, mouse_y)
            elif self.gesture_stage == 2:
                # 向右趋势，x轴增加即可
                if dx > self.min_move:
                    print(">>> 手势2/2 向右趋势达成，全部手势完成，触发回调")
                    self.gesture_stage = 0
                    self.on_trigger()
            # 若逆向移动太多，重置
            elif abs(dx) > self.min_move * 2 or abs(dy) > self.min_move * 2:
                print(">>> 手势方向错误，重置")
                self.gesture_stage = 0

    def on_trigger(self):
        if self.callback:
            self.callback()
        else:
            print("DoubleClickDownRightTrigger: 触发事件")