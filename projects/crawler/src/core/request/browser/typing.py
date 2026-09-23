from enum import Enum


class BrowserActionType(str, Enum):

    # Input / form
    FILL = "fill"
    TYPE = "type"
    CLEAR = "clear"
    PRESS = "press"

    # Mouse / element interaction
    CLICK = "click"
    DOUBLE_CLICK = "double_click"
    HOVER = "hover"
    FOCUS = "focus"
    BLUR = "blur"

    # Select / checkbox
    SELECT = "select"
    CHECK = "check"
    UNCHECK = "uncheck"

    # Keyboard
    KEYBOARD_PRESS = "keyboard_press"
    KEYBOARD_TYPE = "keyboard_type"

    # Page navigation
    GOTO = "goto"
    GO_BACK = "go_back"
    GO_FORWARD = "go_forward"
    RELOAD = "reload"

    # Waiting
    WAIT = "wait"
    WAIT_FOR_SELECTOR = "wait_for_selector"
    WAIT_FOR_URL = "wait_for_url"
    WAIT_FOR_LOAD_STATE = "wait_for_load_state"

    # JavaScript / DOM
    EVALUATE = "evaluate"

    # File
    SET_INPUT_FILES = "set_input_files"

    # Screenshot / debugging
    SCREENSHOT = "screenshot"