import requests
import time
import pymem.process
from win32api import GetAsyncKeyState
from win32gui import GetWindowText, GetForegroundWindow


def Check():
    if GetWindowText(GetForegroundWindow()) == "Counter-Strike: Global Offensive":
        for i in range(1, 256):
            if GetAsyncKeyState(1):
                if i == 0x01:
                    return True
        return False

offsets = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
response = requests.get(offsets).json()

dwLocalPlayer = int(response["signatures"]["dwLocalPlayer"])
dwForceAttack = int(response["signatures"]["dwForceAttack"])

pr = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pr.process_handle, "client.dll").lpBaseOfDll


while True:
    time.sleep(0.03)
    if Check():
        pr.write_int(client + dwForceAttack, 6)
