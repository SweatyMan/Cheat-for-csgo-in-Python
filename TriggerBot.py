from win32gui import GetWindowText, GetForegroundWindow
from threading import Thread
import pymem.process
import pymem, requests, time

offsets = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
response = requests.get(offsets).json()

dwLocalPlayer = int(response["signatures"]["dwLocalPlayer"])
dwForceAttack = int(response["signatures"]["dwForceAttack"])
dwEntityList = int(response["signatures"]["dwEntityList"])

m_fFlags = int(response["netvars"]["m_fFlags"])
m_iCrosshairId = int(response["netvars"]["m_iCrosshairId"])
m_iTeamNum = int(response["netvars"]["m_iTeamNum"])

pr = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pr.process_handle, "client.dll").lpBaseOfDll

def TriggerBot():
    while True:
        if not GetWindowText(GetForegroundWindow()) == "Counter-Strike: Global Offensive":
            continue
        player = pr.read_int(client + dwLocalPlayer)
        entity_id = pr.read_int(player + m_iCrosshairId)
        entity = pr.read_int(client + dwEntityList + (entity_id - 1) * 0x10)
        entity_team = pr.read_int(entity + m_iTeamNum)
        player_team = pr.read_int(player + m_iTeamNum)
        if 0 < entity_id <= 64 and player_team != entity_team:
            pr.write_int(client + dwForceAttack, 6)
        time.sleep(0.01)

Thread(target=TriggerBot).start()
