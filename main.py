import time
import pyautogui
import win32api
import win32con

from triggers_config import create_triggers

CHECK_INTERVAL = 0.03

def is_left_button_down():
    return win32api.GetAsyncKeyState(win32con.VK_LBUTTON) < 0

def is_right_button_down():
    return win32api.GetAsyncKeyState(win32con.VK_RBUTTON) < 0

def get_mouse_position():
    return pyautogui.position()

def main():
    print("=== 脚本已启动 (模块化版本) ===")

    triggers = create_triggers()

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