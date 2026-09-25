'''
Inspector
    ↓
BrowserPageState
    ↓
Policy
    ↓
continue / retry / pause / fail

CHALLENGE

可以配置成：

WAIT_FOR_USER

而：

NOT_FOUND

可以：

FAIL

而：

SERVER_ERROR

可以：

RETRY
'''

class BrowserPageStatePolicy:
    pass