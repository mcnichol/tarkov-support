#!/usr/bin/env python3

import platform
from ctypes.util import find_library
from ctypes import *
import time


def app():
    
    operatingSystem = platform.uname()[0]

    if operatingSystem == "Windows":
        name = "win.dll"
    elif operatingSystem == "Linux":
        name = find_library("c")
    else:
        name = "osx.dylib"
        
    lib = cdll.LoadLibrary(value)

def windows():
    user32 = ctypes.WinDLL('user32', use_last_error=True)

    INPUT_MOUSE    = 0
    INPUT_KEYBOARD = 1
    INPUT_HARDWARE = 2

    KEYEVENTF_EXTENDEDKEY = 0x0001
    KEYEVENTF_KEYUP       = 0x0002
    KEYEVENTF_UNICODE     = 0x0004
    KEYEVENTF_SCANCODE    = 0x0008

    MAPVK_VK_TO_VSC = 0

    # msdn.microsoft.com/en-us/library/dd375731
    VK_TAB      = 0x09 
    VK_MENU     = 0x12  # Alt
    VK_SNAPSHOT = 0x2C  # Print Screen 

    ctypes.wintypes.ULONG_PTR = ctypes.wintypes.WPARAM

    class MOUSEINPUT(ctypes.Structure):
        _fields_ = (
            ("dx",          ctypes.wintypes.LONG),
            ("dy",          ctypes.wintypes.LONG),
            ("mouseData",   ctypes.wintypes.DWORD),
            ("dwFlags",     ctypes.wintypes.DWORD),
            ("time",        ctypes.wintypes.DWORD),
            ("dwExtraInfo", ctypes.wintypes.ULONG_PTR)
        )

    class KEYBDINPUT(ctypes.Structure):
        _fields_ = (
            ("wVk",         ctypes.wintypes.WORD),
            ("wScan",       ctypes.wintypes.WORD),
            ("dwFlags",     ctypes.wintypes.DWORD),
            ("time",        ctypes.wintypes.DWORD),
            ("dwExtraInfo", ctypes.wintypes.ULONG_PTR)
        )

        def __init__(self, *args, **kwds):
            super(KEYBDINPUT, self).__init__(*args, **kwds)

            # some programs use the scan code even if KEYEVENTF_SCANCODE
            # isn't set in dwFflags, so attempt to map the correct code.
            if not self.dwFlags & KEYEVENTF_UNICODE:
                self.wScan = user32.MapVirtualKeyExW(self.wVk, MAPVK_VK_TO_VSC, 0)

    class HARDWAREINPUT(ctypes.Structure):
        _fields_ = (
            ("uMsg",    ctypes.wintypes.DWORD),
            ("wParamL", ctypes.wintypes.WORD),
            ("wParamH", ctypes.wintypes.WORD)
        )

    class INPUT(ctypes.Structure):
        _anonymous_ = ("_input",)
        _fields_ = (
            ("type",   ctypes.wintypes.DWORD),
            ("_input", _INPUT)
        )

        class _INPUT(ctypes.Union):
            _fields_ = (
                ("kbd_input",   KEYBDINPUT),
                ("mouse_input", MOUSEINPUT),
                ("hw_input",    HARDWAREINPUT)
            )
                
    LPINPUT = ctypes.POINTER(INPUT)

    def _check_count(result, func, args):
        if result == 0:
            raise ctypes.WinError(ctypes.get_last_error())
        return args

    user32.SendInput.errcheck = _check_count
    user32.SendInput.argtypes = (
            ctypes.wintypes.UINT,   # nInputs
            LPINPUT,                # pInputs
            ctypes.c_int            # cbSize
        )

    def PressKey(hexKeyCode):
        x = INPUT(type=INPUT_KEYBOARD, kbd_input=KEYBDINPUT(wVk=hexKeyCode))
        user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

    def ReleaseKey(hexKeyCode):
        x = INPUT(type=INPUT_KEYBOARD, kbd_input=KEYBDINPUT(wVk=hexKeyCode, dwFlags=KEYEVENTF_KEYUP))
        user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

    def run():
        PressKey(VK_SNAPSHOT)   
        ReleaseKey(VK_SNAPSHOT)  
        print("Print Screen Executed")

if __name__ == "__main__":
    app()
