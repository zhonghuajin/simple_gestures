from triggers import (
    MouseCornerTrigger,
    MouseLeftEdgeHorizontalTrigger,
    MouseDownUpTrigger,
    BothButtonDownTrigger,
    MouseDownRightOrLeftTrigger,
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
    send_f5,
    send_win_key,
    send_win_tab, 
    send_toggle_maximize_window,
    send_alt_f4_then_esc,
    send_select_all_and_copy,
)
from actions import (
    open_chrome,
    # open_temp_folder,
    open_hkt_command_file,
    # open_vscode,  # 如需启用相关双击手势，可在这里导入
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
            callback_left=send_ctrl_c,
            callback_right=send_f5
        ),

        # MouseBottomEdgeZigzagTrigger(
        #     edge_size=5,
        #     min_zigzag_dist=200,
        #     max_interval=1.2,
        #     side_width_ratio=0.3,
        #     callback_left=open_hkt_command_file,
        #     callback_right=open_temp_folder
        # ),

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

        # DoubleClickLeftMoveLeftTrigger(
        #     max_double_click_interval=0.45,   # 可根据需求调整
        #     gesture_timeout=1.2,              # 可根据需求调整
        #     min_left_move=1000,                # 向左最小移动距离
        #     callback=open_temp_folder         # 触发后调用 open_temp_folder
        # ),
        
        MouseTripleClickTrigger(
            max_interval=0.3,
            callback=send_ctrl_c
        ),

        MouseEdgeUpDownUpTrigger(
            edge_size=5,
            max_time=2.0,
            callback=send_ctrl_shift_backtick
        ),
    ]

    return triggers
