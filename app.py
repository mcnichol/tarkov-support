#!/usr/bin/env python3

import time

from ctypes import c_int, c_bool, WINFUNCTYPE, POINTER, windll, wintypes, WinDLL, byref, sizeof, create_unicode_buffer, get_last_error
from ctypes.wintypes import HWND, LPCWSTR, UINT

from src.struct.KeyboardInput import *
from src.struct.MouseInput import *
from src.struct.HardwareInput import *
from src.struct.Input import *

user32                      = WinDLL('user32', use_last_error=True)
kernel32                    = WinDLL('kernel32', use_last_error=True)

EFT_HANDLE                  = None
INPUT_MOUSE                 = 0
INPUT_KEYBOARD              = 1
INPUT_HARDWARE              = 2

KEYEVENTF_EXTENDEDKEY       = 0x0001
KEYEVENTF_KEYUP             = 0x0002
KEYEVENTF_UNICODE           = 0x0004
KEYEVENTF_SCANCODE          = 0x0008

# msdn.microsoft.com/en-us/library/dd375731
VK_TAB                      = 0x09 
VK_MENU                     = 0x12  # Alt
VK_SNAPSHOT                 = 0x2C  # Print Screen 
VK_1                        = 0x31  

EnumWindows                 = windll.user32.EnumWindows
EnumWindowsProc             = WINFUNCTYPE(c_bool, POINTER(c_int), POINTER(c_int))
SetFocus                    = windll.user32.SetFocus


AttachThreadInput           = user32.AttachThreadInput
GetWindowDC                 = user32.GetWindowDC
GetWindowTextW              = user32.GetWindowTextW
GetWindowTextLengthW        = user32.GetWindowTextLengthW
GetWindowThreadProcessId    = user32.GetWindowThreadProcessId    
IsWindowVisible             = user32.IsWindowVisible
PrintWindow                 = user32.PrintWindow
CreateCompatibleBitmap      = windll.gdi32.CreateCompatibleBitmap
CreateCompatibleDC          = windll.gdi32.CreateCompatibleDC

GetCurrentThreadId          = kernel32.GetCurrentThreadId

def _check_count(result, func, args):
    if result == 0:
        raise WinError(get_last_error())
    return args

def PressKey(hexKeyCode):
    x = Input(type=INPUT_KEYBOARD, kbd_input=KeyboardInput(wVk=hexKeyCode))
    user32.SendInput(1, byref(x), sizeof(x))

def ReleaseKey(hexKeyCode):
    x = Input(type=INPUT_KEYBOARD, kbd_input=KeyboardInput(wVk=hexKeyCode, dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, byref(x), sizeof(x))

def windowWorker(hwnd, lParam):
    global EFT_HANDLE
    winTextLength = bmp = None
    winTextLength = GetWindowTextLengthW(hwnd)
    textBuffer = create_unicode_buffer(winTextLength + 1)
    GetWindowTextW(hwnd, textBuffer, winTextLength + 1)
    if textBuffer.value.startswith("EscapeFromTarkov"):
        EFT_HANDLE = hwnd
        print("Setting Window Handle to ", textBuffer.value)
        currentThread = GetCurrentThreadId()
        print(currentThread)
        remoteThread = GetWindowThreadProcessId(hwnd)
        print(remoteThread)
        AttachThreadInput(currentThread, remoteThread, True)

    return True

user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (
        wintypes.UINT,   # nInputs
        POINTER(Input),  # pInputs
        c_int            # cbSize
    )

def app():
    time.sleep(2)
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

    if EFT_HANDLE is not None:
        SetFocus(EFT_HANDLE)
        PressKey(VK_SNAPSHOT)
        ReleaseKey(VK_SNAPSHOT)
    
        print("Print Screen Executed")


if __name__ == "__main__":
    app()
