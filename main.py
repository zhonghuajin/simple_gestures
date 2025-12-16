import pyautogui
import time
import ctypes
import win32api
import win32con
import win32gui
import webbrowser
import os

# 导入拆分后的触发器类
from triggers import (
    MouseCornerTrigger,
    MouseLeftEdgeHorizontalTrigger,
    MouseDownUpTrigger,
    BothButtonDownTrigger,
    MouseDownRightOrLeftTrigger,
    MouseLeftUpDownUpTrigger,
    MouseTopEdgeZigzagTrigger,
    MouseBottomEdgeZigzagTrigger,
    MouseLeftBottomCornerTrigger,
    MouseDiagonalToTopRightTrigger,
    MouseDownLeftTrigger,
    DoubleClickDownUpLeftTrigger,
    DoubleClickDownRightTrigger
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
VK_LWIN = 0x5B


def send_win_key():
    press_key(VK_LWIN)
    time.sleep(0.08)
    release_key(VK_LWIN)
    print(">>> 已执行 Win 键")


def press_key(hexKeyCode):
    user32.keybd_event(hexKeyCode, 0, 0, 0)


def release_key(hexKeyCode):
    user32.keybd_event(hexKeyCode, 0, KEYEVENTF_KEYUP, 0)

# === 打开文件  ===


def open_chrome():
    webbrowser.open('C:\Program Files\Google\Chrome\Application\chrome.exe')
    print(">>> 已打开 Chrome 浏览器")

# === 新增：打开 VS Code ===


def open_vscode():
    vscode_path = r'C:\Users\admin\AppData\Local\Programs\Microsoft VS Code\Code.exe'
    try:
        if os.path.exists(vscode_path):
            os.startfile(vscode_path)
            print(">>> 已打开 Visual Studio Code")
        else:
            # 如果默认路径不存在，尝试其他常见路径
            alternative_paths = [
                r'C:\Program Files\Microsoft VS Code\Code.exe',
                r'C:\Program Files (x86)\Microsoft VS Code\Code.exe',
            ]

            found = False
            for path in alternative_paths:
                if os.path.exists(path):
                    os.startfile(path)
                    print(f">>> 已打开 Visual Studio Code (从 {path})")
                    found = True
                    break

            if not found:
                print(f">>> 错误：未找到 VS Code，请检查路径: {vscode_path}")
    except Exception as e:
        print(f">>> 打开 VS Code 时出错: {e}")

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


def send_ctrl_t():
    press_key(VK_CONTROL)
    time.sleep(0.03)
    press_key(0x54)  # T
    time.sleep(0.05)
    release_key(0x54)
    release_key(VK_CONTROL)
    print(">>> 已执行 Ctrl + T")

    # 再模拟按一次 Esc 键
    time.sleep(0.1)
    press_key(0x1B)  # Esc
    time.sleep(0.03)
    release_key(0x1B)
    print(">>> 已执行 Esc")


def send_ctrl_c():
    press_key(VK_CONTROL)
    time.sleep(0.03)
    press_key(0x43)  # C
    time.sleep(0.05)
    release_key(0x43)
    release_key(VK_CONTROL)
    print(">>> 已执行 Ctrl + C")


def send_ctrl_v():
    press_key(VK_CONTROL)
    time.sleep(0.03)
    press_key(0x56)  # V
    time.sleep(0.05)
    release_key(0x56)
    release_key(VK_CONTROL)
    print(">>> 已执行 Ctrl + V")


def send_alt_left():
    press_key(VK_MENU)
    time.sleep(0.03)
    press_key(0x25)  # 左方向键
    time.sleep(0.05)
    release_key(0x25)
    release_key(VK_MENU)
    print(">>> 已执行 Alt + ←（返回上一层）")


def send_toggle_maximize_window():
    hwnd = win32gui.GetForegroundWindow()
    if hwnd != 0:
        placement = win32gui.GetWindowPlacement(hwnd)
        showCmd = placement[1]
        if showCmd == win32con.SW_SHOWMAXIMIZED:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            print(">>> 已执行 窗口还原")
        else:
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            print(">>> 已执行 窗口最大化")


def send_alt_f4_then_esc():
    send_alt_f4()
    time.sleep(0.1)
    press_key(0x1B)  # Esc
    time.sleep(0.03)
    release_key(0x1B)
    print(">>> 已执行 Esc (延迟 0.1 秒)")

# === 输入状态收集 ===


def is_left_button_down():
    return win32api.GetAsyncKeyState(win32con.VK_LBUTTON) < 0


def is_right_button_down():
    return win32api.GetAsyncKeyState(win32con.VK_RBUTTON) < 0


def get_mouse_position():
    return pyautogui.position()


def open_temp_folder():
    os.startfile(r'c:\\temp')
    print(">>> 已打开 c:\\temp 文件夹")


def open_hkt_command_file():
    os.startfile(
        r'C:\\Users\\admin\\Documents\\BaiduSyncdisk\\思维\\HKT\\常用命令.txt')
    print(">>> 已打开 HKT 常用命令.txt")

# === 主程序 ===


def main():
    print("=== 脚本已启动 (模块化版本) ===")

    triggers = [
        MouseCornerTrigger(CORNER_SIZE, send_alt_tab),
        MouseLeftEdgeHorizontalTrigger(
            edge_size=5, move_threshold=300, direction='up', callback=send_ctrl_c),
        MouseLeftEdgeHorizontalTrigger(
            edge_size=5, move_threshold=300, direction='down', callback=send_ctrl_v),
        MouseDownUpTrigger(min_move=200, max_time=1.2, callback=open_chrome),
        BothButtonDownTrigger(send_ctrl_t),
        MouseDownRightOrLeftTrigger(
            min_down=200,
            min_side=200,
            callback_right=send_ctrl_w,
            callback_left=send_alt_f4,
        ),
        MouseLeftUpDownUpTrigger(
            min_move=30, max_time=1.0, callback=send_ctrl_shift_backtick
        ),
        MouseTopEdgeZigzagTrigger(
            edge_size=2,
            min_move_dist=500,
            max_interval=1.2,
            callback_left=send_alt_left,
            callback_right=send_f5
        ),
        MouseBottomEdgeZigzagTrigger(
            edge_size=5,
            min_zigzag_dist=200,
            max_interval=1.2,
            side_width_ratio=0.3,  # 左右各30%为判定区域
            callback_left=open_hkt_command_file,
            callback_right=open_temp_folder
        ),
        MouseLeftBottomCornerTrigger(CORNER_SIZE, send_win_key),
        MouseDiagonalToTopRightTrigger(
            corner_size=10,         # 右上角判定区域
            min_dist=600,           # 移动距离阈值（可根据分辨率调整）
            max_time=1.5,           # 必须在多长时间内完成
            callback=send_toggle_maximize_window,
        ),
        MouseDownLeftTrigger(
            min_down=300,       # 向下移动至少100像素
            min_left=300,       # 向左移动至少100像素
            max_time=1.0,       # 1秒内完成
            callback=send_alt_f4_then_esc
        ),
        DoubleClickDownUpLeftTrigger(
            max_double_click_interval=0.4,  # 两次点击最大间隔
            gesture_timeout=1.2,            # 手势最大时长
            min_move=500,                    # 每段最小像素
            callback=open_vscode
        ),
        DoubleClickDownRightTrigger(
            max_double_click_interval=0.4,  # 双击最大间隔，秒
            gesture_timeout=1.2,            # 手势完成最大允许时长，秒
            min_move=500,                    # 每段最小趋势位移像素
            callback=send_ctrl_w            # 触发回调
        ),
    ]

    try:
        while True:
            x, y = get_mouse_position()
            input_state = {
                'mouse_x': x,
                'mouse_y': y,
                'right_button': is_right_button_down(),
                'left_button': is_left_button_down(),
            }
            for trigger in triggers:
                trigger.update(input_state)
            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\n程序已停止。")


if __name__ == "__main__":
    main()
