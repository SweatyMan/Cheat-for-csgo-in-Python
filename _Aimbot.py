# Importing Libraries

import math
import requests
import time
import pymem.process

# Get offsets

offsets = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
response = requests.get(offsets).json()

dwLocalPlayer = int(response["signatures"]["dwLocalPlayer"])
dwEntityList = int(response["signatures"]["dwEntityList"])
dwClientState = int(response["signatures"]["dwClientState"])
dwClientState_ViewAngles = int(response["signatures"]["dwClientState_ViewAngles"])

m_vecOrigin = int(response["netvars"]["m_vecOrigin"])
m_iHealth = int(response["netvars"]["m_iHealth"])
m_iTeamNum = int(response["netvars"]["m_iTeamNum"])
m_dwBoneMatrix = int(response["netvars"]["m_dwBoneMatrix"])

# Aimbot injection

pr = pymem.Pymem("csgo.exe")

client = pymem.process.module_from_name(pr.process_handle, "client.dll").lpBaseOfDll
engine = pymem.process.module_from_name(pr.process_handle, "engine.dll").lpBaseOfDll

player = pr.read_int(client + dwLocalPlayer)
clientState = pr.read_int(engine + dwClientState)


def getBone(Target):
    matrix = pr.read_int(Target + m_dwBoneMatrix)
    return (pr.read_float(matrix + 0x30 * 5 + 0x0C),
            pr.read_float(matrix + 0x30 * 5 + 0x1C),
            pr.read_float(matrix + 0x30 * 5 + 0x2C))


def CalcAngle(pPos, ePos):
    try:
        delta = list(map(lambda x, y: x - y, pPos, ePos))
        hyp = math.sqrt((pos[0] - EP[0]) ** 2 + (pos[1] - EP[1]) ** 2)
        x = math.atan(delta[2] / hyp) * 57.295779513082
        y = math.atan(delta[1] / delta[0]) * 57.295779513082
        if delta[0] >= 0.0:
            y += 180.0
        return x, y

    except ValueError:
        pass


def VectorAim(enemy):
    try:
        # TarPos = [pr.read_float(enemy + m_vecOrigin),
        #           pr.read_float(enemy + m_vecOrigin + 0x4),
        #           pr.read_float(enemy + m_vecOrigin + 0x8)]
        TarBonePos = (getBone(enemy)[0],
                      getBone(enemy)[1],
                      getBone(enemy)[2])
        BonePos = (getBone(player)[0],
                      getBone(player)[1],
                      getBone(player)[2])
        pr.write_float(clientState + dwClientState_ViewAngles,
                       CalcAngle(BonePos, TarBonePos)[0])
        pr.write_float(clientState + dwClientState_ViewAngles + 0x4,
                       CalcAngle(BonePos, TarBonePos)[1])

    except:
        pass

while True:
    time.sleep(0.004)
    if pr.read_float(player + m_iHealth):
        pos = [
            pr.read_float(player + m_vecOrigin),
            pr.read_float(player + m_vecOrigin + 0x4),
            pr.read_float(player + m_vecOrigin + 0x8)
            ]

        entDis = []
        ent = []
        for i in range(1, 32):
            entity = pr.read_int(client + dwEntityList + i * 0x10)

            if entity:
                if pr.read_int(entity + m_iHealth):
                    entity_team = pr.read_int(entity + m_iTeamNum)
                    player_team = pr.read_int(player + m_iTeamNum)
                    if player_team != entity_team:
                        ent.append(entity)
                        EP = [
                            pr.read_float(entity + m_vecOrigin),
                            pr.read_float(entity + m_vecOrigin + 0x4),
                            pr.read_float(entity + m_vecOrigin + 0x8)
                            ]

                        ED = math.sqrt((pos[0] - EP[0]) ** 2 + (pos[1] - EP[1]) ** 2)
                        entDis.append(ED)

        VectorAim(ent[entDis.index(min(entDis))])
