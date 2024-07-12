#!/usr/bin/env python3

import ctypes
import time
import os

from ctypes import c_int, WINFUNCTYPE, windll, wintypes
from ctypes.wintypes import HWND, LPCWSTR, UINT


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

EnumWindows = windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))

GetWindowDC = windll.user32.GetWindowDC
GetWindowTextW = windll.user32.GetWindowTextW
GetWindowTextLengthW = windll.user32.GetWindowTextLengthW
CreateCompatibleDC = windll.gdi32.CreateCompatibleDC
CreateCompatibleBitmap = windll.gdi32.CreateCompatibleBitmap
PrintWindow = windll.user32.PrintWindow

IsWindowVisible = windll.user32.IsWindowVisible



class MOUSEINPUT(ctypes.Structure):
    _fields_ = (
        ("dx",          wintypes.LONG),
        ("dy",          wintypes.LONG),
        ("mouseData",   wintypes.DWORD),
        ("dwFlags",     wintypes.DWORD),
        ("time",        wintypes.DWORD),
        ("dwExtraInfo", wintypes.ULONG_PTR)
    )

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (
        ("wKeyCode",    wintypes.WORD),
        ("wScan",       wintypes.WORD),
        ("dwFlags",     wintypes.DWORD),
        ("time",        wintypes.DWORD),
        ("dwExtraInfo", wintypes.ULONG_PTR)
    )

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)

        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk, MAPVK_VK_TO_VSC, 0)

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (
        ("uMsg",    wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD)
    )

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (
            ("kbd_input",   KEYBDINPUT),
            ("mouse_input", MOUSEINPUT),
            ("hw_input",    HARDWAREINPUT)
        )
    _anonymous_ = ("_input",)

    _fields_ = (
        ("type",   wintypes.DWORD),
        ("_input", _INPUT)
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

def windowWorker(hwnd, lParam):
    winTextLength = bmp = None
    winTextLength = GetWindowTextLengthW(hwnd)
    textBuffer = ctypes.create_unicode_buffer(winTextLength + 1)
    GetWindowTextW(hwnd, textBuffer, winTextLength + 1)
    if textBuffer.value.startswith("EscapeFromTarkov"):
        print(textBuffer.value)

    return True

def app():
    #time.sleep(10)
    #PressKey(VK_SNAPSHOT)   
    #ReleaseKey(VK_SNAPSHOT)  
    #print("Print Screen Executed")

    # #                    SS Date | Server Time? | X-Axis? | Z-Axis? | Y-Axis? | ??? | ??? | ??? | ??? | ???
    # # Screenshot Format: YYYY-MM-DD[HH-MM]_-XXX.X, #.#, -YYY.Y_#.#, #.#, #.#, #.#_##.##
    # # C:\Users\desktop_6950xt\Documents\Escape from Tarkov\Screenshots\2024-06-13[20-31]_-340.8, 1.2, -116.0_0.0, 1.0, 0.0, 0.2_13.62

    #files = os.listdir("C://Users//desktop_6950xt//Documents//Escape from Tarkov//Screenshots")
    #files.sort(reverse=True)
    #currentLocation = files[0].split("_")[1].split(",")
    #x = currentLocation[0]
    #y = currentLocation[2]
    #z = currentLocation[1]
    #print(x, y, z)
    ## Delete files
    ## Draw location on canvas

    EnumWindows(EnumWindowsProc(windowWorker),0)


if __name__ == "__main__":
    app()
