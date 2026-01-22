from triggers import (
    MouseCornerTrigger,
    MouseLeftEdgeHorizontalTrigger,
    # MouseDownUpTrigger,
    BothButtonDownTrigger,
    # MouseDownRightOrLeftTrigger,
    MouseLeftUpDownUpTrigger,
    MouseTopEdgeZigzagTrigger,
    # MouseBottomEdgeZigzagTrigger,
    MouseLeftBottomCornerTrigger,
    MouseBottomRightCornerTrigger,
    MouseDiagonalToTopRightTrigger,
    MouseDownLeftTrigger,
    DoubleClickDownRightTrigger,
    DoubleClickDownLeftTrigger,
    DoubleClickLeftUpRightDownTrigger,
    # DoubleClickLeftMoveLeftTrigger,
    DoubleClickDownUpTrigger,
    MouseTripleClickTrigger,
    MouseEdgeUpDownUpTrigger,
    ClickUpEdgeTrigger,
    ClickUpDownShakeTrigger,
    # 新增导入
    DoubleClickHoldTrigger,
)

from key_sender import (
    send_alt_tab,
    send_ctrl_c,
    send_ctrl_v,
    send_ctrl_t,
    send_ctrl_w,
    send_alt_f4,
    send_ctrl_shift_backtick,
    send_alt_left,
    foo,
    send_f5,
    send_win_key,
    send_win_tab,
    send_toggle_maximize_window,
    send_alt_f4_then_esc,
    send_select_all_and_copy,
    send_home_key,
    send_end_key,
    send_secret_string,
    send_ctrl_c_then_right_click_then_esc
)
from actions import (
    open_chrome,
    # open_temp_folder,
    open_hkt_command_file,
    # open_vscode,
)

# 这些全局参数也可以集中放在一个 config.py 里，这里先简单写死
CORNER_SIZE = 5
EDGE_SIZE = 5


def create_triggers():
    triggers = [
        MouseCornerTrigger(CORNER_SIZE, send_alt_tab),

        MouseLeftEdgeHorizontalTrigger(
            edge_size=EDGE_SIZE, move_threshold=300,
            direction='up', callback=send_ctrl_c
        ),
        MouseLeftEdgeHorizontalTrigger(
            edge_size=EDGE_SIZE, move_threshold=300,
            direction='down', callback=send_ctrl_v
        ),

        # MouseDownUpTrigger(min_move=200, max_time=1.2, callback=open_chrome),
        BothButtonDownTrigger(send_ctrl_t),

        MouseLeftUpDownUpTrigger(
            min_move=30, max_time=1.0, callback=send_ctrl_shift_backtick
        ),

        MouseTopEdgeZigzagTrigger(
            edge_size=2,
            min_move_dist=500,
            max_interval=1.2,
            callback_left=foo,
            callback_right=send_f5
        ),

        MouseLeftBottomCornerTrigger(CORNER_SIZE, send_win_key),

        MouseBottomRightCornerTrigger(CORNER_SIZE, send_win_tab),

        MouseDiagonalToTopRightTrigger(
            corner_size=10,
            min_dist=600,
            max_time=1.5,
            callback=send_toggle_maximize_window,
        ),

        MouseDownLeftTrigger(
            min_down=300,
            min_left=300,
            max_time=1.0,
            callback=send_alt_f4_then_esc
        ),

        DoubleClickDownRightTrigger(
            max_double_click_interval=0.4,
            gesture_timeout=1.2,
            min_move=500,
            callback=send_ctrl_w
        ),

        DoubleClickDownLeftTrigger(
            max_double_click_interval=0.4,
            gesture_timeout=1.2,
            min_move=500,
            callback=send_alt_f4
        ),

        DoubleClickLeftUpRightDownTrigger(
            max_double_click_interval=0.4,
            gesture_timeout=2.0,
            min_move=300,
            callback=send_select_all_and_copy
        ),

        DoubleClickDownUpTrigger(
            max_double_click_interval=0.4,
            gesture_timeout=2.0,
            min_down=500,
            max_horizontal_deviation=150,
            callback=open_hkt_command_file
        ),

        MouseTripleClickTrigger(
            max_interval=0.3,
            callback=send_ctrl_c
        ),

        MouseEdgeUpDownUpTrigger(
            edge_size=5,
            max_time=2.0,
            callback=send_ctrl_shift_backtick
        ),

        ClickUpEdgeTrigger(
            min_up_dist=200,
            max_click_time=0.3,
            max_gesture_time=2.0,
            callback_left=send_home_key,
            callback_right=send_end_key
        ),

        ClickUpDownShakeTrigger(
            min_segment_dist=50,   # 每次上下移动至少50像素
            required_shakes=7,     # 至少变向3次 (如 上-下-上)
            max_gesture_time=2.0,  # 整个过程需在2秒内完成
            callback=send_secret_string
        ),

        # === 新增：双击后静止0.5秒执行 Ctrl+C ===
        DoubleClickHoldTrigger(
            max_double_click_interval=0.4, # 双击间隔判定
            hold_duration=1,             # 静止时长
            move_threshold=5,              # 允许的微小抖动像素
            callback=send_ctrl_c_then_right_click_then_esc
        ),
    ]

    return triggers