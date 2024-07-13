from ctypes import Structure, wintypes

class MouseInput(Structure):
    _fields_ = (
        ("dx",          wintypes.LONG),
        ("dy",          wintypes.LONG),
        ("mouseData",   wintypes.DWORD),
        ("dwFlags",     wintypes.DWORD),
        ("time",        wintypes.DWORD),
        ("dwExtraInfo", wintypes.WPARAM) #Depending on the arch, ULONG_PTR is uLong or uLongLong. wintypes.WPARAM checks for this
    )
