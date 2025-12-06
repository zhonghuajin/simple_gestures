# main.py
import pyautogui
import time
import ctypes
import win32api
import win32con

# 导入拆分后的触发器类
from triggers import (
    RightButtonDownUpDownTrigger,
    MouseCornerTrigger,
    RightButtonDownRightTrigger,
    RightButtonDownDownLeftTrigger,
    RightButtonDownLeftUpLeftTrigger,
    RightButtonDownLeftUpRightTrigger
)

# === 全局参数 ===
CHECK_INTERVAL = 0.03
CORNER_SIZE = 5
MOVE_MIN_DIST = 30

# === Windows 按键码 ===
user32 = ctypes.WinDLL('user32', use_last_error=True)
VK_CONTROL = 0x11
VK_SHIFT = 0x10
VK_OEM_3 = 0xC0
VK_MENU = 0x12
VK_TAB = 0x09
VK_F4 = 0x73
VK_W = 0x57
VK_N = 0x4E
VK_F5 = 0x74
KEYEVENTF_KEYUP = 0x0002

def press_key(hexKeyCode):
    user32.keybd_event(hexKeyCode, 0, 0, 0)

def release_key(hexKeyCode):
    user32.keybd_event(hexKeyCode, 0, KEYEVENTF_KEYUP, 0)

# === 组合键封装 ===
def send_ctrl_shift_backtick():
    press_key(VK_CONTROL)
    time.sleep(0.03)
    press_key(VK_SHIFT)
    time.sleep(0.03)
    press_key(VK_OEM_3)
    time.sleep(0.05)
    release_key(VK_OEM_3)
    release_key(VK_SHIFT)
    release_key(VK_CONTROL)
    print(">>> 已执行 Ctrl + Shift + `")

def send_alt_tab():
    press_key(VK_MENU)
    time.sleep(0.03)
    press_key(VK_TAB)
    time.sleep(0.05)
    release_key(VK_TAB)
    release_key(VK_MENU)
    print(">>> 已执行 Alt + Tab")

def send_alt_f4():
    press_key(VK_MENU)
    time.sleep(0.03)
    press_key(VK_F4)
    time.sleep(0.05)
    release_key(VK_F4)
    release_key(VK_MENU)
    print(">>> 已执行 Alt + F4")

def send_ctrl_w():
    press_key(VK_CONTROL)
    time.sleep(0.03)
    press_key(VK_W)
    time.sleep(0.05)
    release_key(VK_W)
    release_key(VK_CONTROL)
    print(">>> 已执行 Ctrl + W")

def send_ctrl_shift_n():
    press_key(VK_CONTROL)
    time.sleep(0.03)
    press_key(VK_SHIFT)
    time.sleep(0.03)
    press_key(VK_N)
    time.sleep(0.05)
    release_key(VK_N)
    release_key(VK_SHIFT)
    release_key(VK_CONTROL)
    print(">>> 已执行 Ctrl + Shift + N")

def send_f5():
    press_key(VK_F5)
    time.sleep(0.05)
    release_key(VK_F5)
    print(">>> 已执行 F5")

# === 输入状态收集 ===
def is_right_button_down():
    return win32api.GetAsyncKeyState(win32con.VK_RBUTTON) < 0

def get_mouse_position():
    return pyautogui.position()

# === 主程序 ===
def main():
    print("=== 脚本已启动 (模块化版本) ===")

    triggers = [
        RightButtonDownUpDownTrigger(MOVE_MIN_DIST, send_ctrl_shift_backtick),
        MouseCornerTrigger(CORNER_SIZE, send_alt_tab),
        RightButtonDownRightTrigger(MOVE_MIN_DIST, send_alt_f4),  # 下→右 Alt+F4
        RightButtonDownDownLeftTrigger(MOVE_MIN_DIST, send_ctrl_w),  # 下→左 Ctrl+W
        RightButtonDownLeftUpLeftTrigger(MOVE_MIN_DIST, send_ctrl_shift_n),  # 左→上→左 Ctrl+Shift+N
        RightButtonDownLeftUpRightTrigger(MOVE_MIN_DIST, send_f5),  # 左→上→右 F5
    ]

    try:
        while True:
            x, y = get_mouse_position()
            input_state = {
                'mouse_x': x,
                'mouse_y': y,
                'right_button': is_right_button_down(),
                # 可继续扩展更多输入状态
            }
            for trigger in triggers:
                trigger.update(input_state)
            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\n程序已停止。")

if __name__ == "__main__":
    main()