import win32api, win32con
def mouseMove(x,y):
    win32api.SetCursorPos((x,y))

def mouseClick(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def detectOS():
    print(platform.system())