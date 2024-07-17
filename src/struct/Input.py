from ctypes import wintypes, Structure, Union
from src.struct.MouseInput import *
from src.struct.KeyboardInput import *
from src.struct.HardwareInput import *

class Input(Structure):
    class _Input(Union):
        _fields_ = (
            ("kbd_input",   KeyboardInput),
            ("mouse_input", MouseInput),
            ("hw_input",    HardwareInput)
        )
    _anonymous_ = ("_input",)

    _fields_ = (
        ("type",   wintypes.DWORD),
        ("_input", _Input)
    )

            
