# triggers/mouse_bottom_edge_side_zigzag_trigger.py

from .trigger_base import TriggerBase
import time
import pyautogui

class MouseBottomEdgeZigzagTrigger(TriggerBase):
    def __init__(
        self,
        edge_size=5,
        min_zigzag_dist=150,
        max_interval=1.2,
        side_width_ratio=0.3,
        callback_left=None,
        callback_right=None
    ):
        """
        edge_size: 底部边缘判定区域高度
        min_zigzag_dist: 左右来回移动的最小距离
        max_interval: 来回移动的最大时间（秒）
        side_width_ratio: 屏幕宽度的多少算做左/右侧（如0.3为左/右各30%）
        callback_left: 左侧回调（先左移再右移）
        callback_right: 右侧回调（先右移再左移）
        """
        self.edge_size = edge_size
        self.min_zigzag_dist = min_zigzag_dist
        self.max_interval = max_interval
        self.callback_left = callback_left
        self.callback_right = callback_right

        # 添加方向追踪
        self.left_direction_tracker = DirectionTracker()
        self.right_direction_tracker = DirectionTracker()
        
        self.last_trigger_time_left = 0
        self.last_trigger_time_right = 0

        screen = pyautogui.size()
        self.screen_width = screen.width
        self.screen_height = screen.height
        self.left_max_x = int(self.screen_width * side_width_ratio)
        self.right_min_x = int(self.screen_width * (1 - side_width_ratio))

    def update(self, state):
        mouse_x = state.get('mouse_x', 0)
        mouse_y = state.get('mouse_y', 0)
        now = time.time()

        # 在屏幕底部边缘
        if mouse_y >= self.screen_height - self.edge_size:
            # 左侧区域 - 检测先左移再右移
            if mouse_x <= self.left_max_x:
                self.left_direction_tracker.add_point(mouse_x, now)
                
                # 检查"先左移再右移"模式
                if self.left_direction_tracker.check_left_then_right(self.min_zigzag_dist, self.max_interval):
                    if now - self.last_trigger_time_left > self.max_interval:
                        self.on_trigger_left()
                        self.last_trigger_time_left = now
                        self.left_direction_tracker.reset()
            else:
                self.left_direction_tracker.reset()

            # 右侧区域 - 检测先右移再左移
            if mouse_x >= self.right_min_x:
                self.right_direction_tracker.add_point(mouse_x, now)
                
                # 检查"先右移再左移"模式
                if self.right_direction_tracker.check_right_then_left(self.min_zigzag_dist, self.max_interval):
                    if now - self.last_trigger_time_right > self.max_interval:
                        self.on_trigger_right()
                        self.last_trigger_time_right = now
                        self.right_direction_tracker.reset()
            else:
                self.right_direction_tracker.reset()
        else:
            self.left_direction_tracker.reset()
            self.right_direction_tracker.reset()

    def on_trigger_left(self):
        if self.callback_left:
            self.callback_left()

    def on_trigger_right(self):
        if self.callback_right:
            self.callback_right()


class DirectionTracker:
    """专门追踪鼠标移动方向的辅助类"""
    def __init__(self):
        self.points = []  # (x, time)
        self.reset()
        
    def reset(self):
        self.points = []
        self.min_x = None
        self.max_x = None
        self.min_time = None
        self.max_time = None
        self.direction_changes = []  # 记录方向变化
        
    def add_point(self, x, time):
        self.points.append((x, time))
        
        # 清理超过2秒的数据
        self.points = [(px, pt) for px, pt in self.points if time - pt <= 2.0]
        
        # 记录极值点
        if self.min_x is None or x < self.min_x:
            self.min_x = x
            self.min_time = time
            
        if self.max_x is None or x > self.max_x:
            self.max_x = x
            self.max_time = time
            
        # 检测方向变化
        if len(self.points) >= 2:
            last_x = self.points[-2][0]
            if x < last_x and (not self.direction_changes or self.direction_changes[-1] != 'left'):
                self.direction_changes.append('left')
            elif x > last_x and (not self.direction_changes or self.direction_changes[-1] != 'right'):
                self.direction_changes.append('right')
                
            # 只保留最近的方向变化
            if len(self.direction_changes) > 3:
                self.direction_changes = self.direction_changes[-3:]
    
    def check_left_then_right(self, min_dist, max_interval):
        """检查先左移再右移的模式"""
        if len(self.points) < 4:  # 至少需要4个点才能形成完整模式
            return False
            
        # 检查移动距离
        if self.max_x is None or self.min_x is None:
            return False
            
        if self.max_x - self.min_x < min_dist:
            return False
            
        # 检查时间窗口
        if self.max_time - self.min_time > max_interval:
            return False
            
        # 检查方向变化模式：必须是先左移，再右移
        if len(self.direction_changes) >= 2:
            # 模式1：['left', 'right'] - 先左后右
            # 模式2：['left', 'right', 'left'] - 先左后右再左（也可以接受）
            if self.direction_changes[0] == 'left' and 'right' in self.direction_changes:
                # 确保有方向反转（从左转到右）
                for i in range(1, len(self.direction_changes)):
                    if self.direction_changes[i] == 'right':
                        return True
                        
        return False
    
    def check_right_then_left(self, min_dist, max_interval):
        """检查先右移再左移的模式"""
        if len(self.points) < 4:  # 至少需要4个点才能形成完整模式
            return False
            
        # 检查移动距离
        if self.max_x is None or self.min_x is None:
            return False
            
        if self.max_x - self.min_x < min_dist:
            return False
            
        # 检查时间窗口
        if self.max_time - self.min_time > max_interval:
            return False
            
        # 检查方向变化模式：必须是先右移，再左移
        if len(self.direction_changes) >= 2:
            # 模式1：['right', 'left'] - 先右后左
            # 模式2：['right', 'left', 'right'] - 先右后左再右（也可以接受）
            if self.direction_changes[0] == 'right' and 'left' in self.direction_changes:
                # 确保有方向反转（从右转到左）
                for i in range(1, len(self.direction_changes)):
                    if self.direction_changes[i] == 'left':
                        return True
                        
        return False