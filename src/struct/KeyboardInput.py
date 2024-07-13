from ctypes import windll, wintypes, Structure

class KeyboardInput(Structure):
    _fields_ = (
        ("wKeyCode",    wintypes.WORD),
        ("wScan",       wintypes.WORD),
        ("dwFlags",     wintypes.DWORD),
        ("time",        wintypes.DWORD),
        ("dwExtraInfo", wintypes.WPARAM)
    )

    def __init__(self, *args, **kwds):
        super(KeyboardInput, self).__init__(*args, **kwds)

        KEYEVENTF_UNICODE   = 0x0004

        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            MAPVK_VK_TO_VSC = 0

            user32 = ctypes.WinDLL('user32', use_last_error=True)

            self.wScan = user32.MapVirtualKeyExW(self.wVk, MAPVK_VK_TO_VSC, 0)
