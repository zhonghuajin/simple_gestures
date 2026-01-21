import time
import ctypes
import win32api
import win32con
import win32gui
import pyautogui

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
VK_A = 0x41
VK_HOME = 0x24
VK_END = 0x23  # 新增 End 键码

def press_key(hexKeyCode):
    user32.keybd_event(hexKeyCode, 0, 0, 0)

def release_key(hexKeyCode):
    user32.keybd_event(hexKeyCode, 0, KEYEVENTF_KEYUP, 0)

def send_win_key():
    press_key(VK_LWIN)
    time.sleep(0.08)
    release_key(VK_LWIN)
    print(">>> 已执行 Win 键")

def send_home_key():
    press_key(VK_HOME)
    time.sleep(0.05)
    release_key(VK_HOME)
    print(">>> 已执行 Home 键")

def send_end_key():
    press_key(VK_END)
    time.sleep(0.05)
    release_key(VK_END)
    print(">>> 已执行 End 键")

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

def send_ctrl_a():
    press_key(VK_CONTROL)
    time.sleep(0.03)
    press_key(VK_A)
    time.sleep(0.05)
    release_key(VK_A)
    release_key(VK_CONTROL)
    print(">>> 已执行 Ctrl + A")

def send_select_all_and_copy():
    send_ctrl_a()
    time.sleep(0.1)
    send_ctrl_c()
    print(">>> 已执行 全选并复制")

def send_alt_left():
    press_key(VK_MENU)
    time.sleep(0.03)
    press_key(0x25)  # 左方向键
    time.sleep(0.05)
    release_key(0x25)
    release_key(VK_MENU)
    print(">>> 已执行 Alt + ←（返回上一层）")
    
def foo():
    pass

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

def send_ctrl_z():
    press_key(VK_CONTROL)
    time.sleep(0.03)
    press_key(0x5A)  # Z
    time.sleep(0.05)
    release_key(0x5A)
    release_key(VK_CONTROL)
    print(">>> 已执行 Ctrl + Z")

def send_delete_key():
    press_key(0x2E)  # Delete
    time.sleep(0.03)
    release_key(0x2E)
    print(">>> 已执行 Delete 键")
    
def send_win_tab():
    press_key(VK_LWIN)
    time.sleep(0.05)
    press_key(VK_TAB)
    time.sleep(0.05)
    release_key(VK_TAB)
    release_key(VK_LWIN)
    print(">>> 已执行 Win + Tab")
    
    
def send_secret_string():
    # 使用 pyautogui.write 可以自动处理大小写和特殊字符
    pyautogui.write('zjhZHNzhj@1979')
    print(">>> 已输入密码字符串: zjhZHNzhj@1979")    