import pymem, requests
import pymem.process
from threading import Thread

offsets = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
response = requests.get(offsets).json()

dwLocalPlayer = int(response["signatures"]["dwLocalPlayer"])
dwEntityList = int(response["signatures"]["dwEntityList"])

m_iTeamNum = int(response["netvars"]["m_iTeamNum"])
m_bSpotted = int(response["netvars"]["m_bSpotted"])

pm = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll


def RadarHack():
    while True:
        if pm.read_int(client + dwLocalPlayer):
            localplayer = pm.read_int(client + dwLocalPlayer)
            localplayer_team = pm.read_int(localplayer + m_iTeamNum)
            for i in range(64):
                if pm.read_int(client + dwEntityList + i * 0x10):
                    entity = pm.read_int(client + dwEntityList + i * 0x10)
                    entity_team = pm.read_int(entity + m_iTeamNum)
                    if entity_team != localplayer_team:
                        pm.write_int(entity + m_bSpotted, 1)


Thread(target=RadarHack).start()
