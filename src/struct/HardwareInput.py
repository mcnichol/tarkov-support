from ctypes import wintypes, Structure

class HardwareInput(Structure):
    _fields_ = (
        ("uMsg",    wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD)
    )

