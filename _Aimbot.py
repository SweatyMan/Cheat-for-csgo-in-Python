# Importing Libraries

from math import sqrt, atan, pi
from requests import get
from time import sleep
from pymem import process, Pymem

# Get offsets

offsets = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
response = get(offsets).json()

dwLocalPlayer = int(response["signatures"]["dwLocalPlayer"])
dwEntityList = int(response["signatures"]["dwEntityList"])
dwClientState = int(response["signatures"]["dwClientState"])
dwClientState_ViewAngles = int(response["signatures"]["dwClientState_ViewAngles"])

m_vecOrigin = int(response["netvars"]["m_vecOrigin"])
m_iHealth = int(response["netvars"]["m_iHealth"])
m_iTeamNum = int(response["netvars"]["m_iTeamNum"])
m_dwBoneMatrix = int(response["netvars"]["m_dwBoneMatrix"])

# Aimbot injection

pr = Pymem("csgo.exe")

client = process.module_from_name(pr.process_handle, "client.dll").lpBaseOfDll
engine = process.module_from_name(pr.process_handle, "engine.dll").lpBaseOfDll

player = pr.read_int(client + dwLocalPlayer)
clientState = pr.read_int(engine + dwClientState)


def getBone(Target):
    matrix = pr.read_int(Target + m_dwBoneMatrix)
    return (pr.read_float(matrix + 0x30 * 8 + 0x0C),
            pr.read_float(matrix + 0x30 * 8 + 0x1C),
            pr.read_float(matrix + 0x30 * 8 + 0x2C))


def CalcAngle(pPos, ePos):
    try:
        delta_x = pPos[0] - ePos[0]
        delta_y = pPos[1] - ePos[1]
        delta_z = pPos[2] - ePos[2]
        hyp = sqrt(delta_x * delta_x + delta_y * delta_y + delta_z * delta_z)
        x = atan(delta_z / hyp) * 180 / pi
        y = atan(delta_y / delta_x) * 180 / pi
        if delta_x >= 0.0:
            y += 180.0
        return x, y
    except ValueError:
        pass


def ChangeAim(entity):
    TarPos = [pr.read_float(entity + m_vecOrigin),
              pr.read_float(entity + m_vecOrigin + 0x4),
              pr.read_float(entity + m_vecOrigin + 0x8)]
    TarBonePos = [getBone(entity)[0],
                  getBone(entity)[1],
                  getBone(entity)[2]]

    pr.write_float(clientState + dwClientState_ViewAngles,
                   CalcAngle(pos, TarPos)[0])
    pr.write_float(clientState + dwClientState_ViewAngles + 0x4,
                   CalcAngle(pos, TarBonePos)[1])


while True:
    sleep(0.005)
    if pr.read_float(player + m_iHealth):
        pos = [pr.read_float(player + m_vecOrigin),
               pr.read_float(player + m_vecOrigin + 0x4),
               pr.read_float(player + m_vecOrigin + 0x8)]

        entDis = []
        ent = []
        for i in range(1, 32):
            entity = pr.read_int(client + dwEntityList + i * 0x10)

            if entity and pr.read_int(entity + m_iHealth):
                if pr.read_int(entity + m_iHealth):
                    entity_team = pr.read_int(entity + m_iTeamNum)
                    player_team = pr.read_int(player + m_iTeamNum)
                    if player_team != entity_team:
                        ent.append(entity)
                        EP = [pr.read_float(entity + m_vecOrigin),
                              pr.read_float(entity + m_vecOrigin + 0x4),
                              pr.read_float(entity + m_vecOrigin + 0x8)]

                        ED = sqrt((pos[0] - EP[0]) ** 2 + (pos[1] - EP[1]) ** 2)
                        entDis.append(ED)
        try:
            ChangeAim(ent[entDis.index(min(entDis))])
        except ValueError:
            pass
