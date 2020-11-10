# Importing Libraries

import pymem, requests
import pymem.process

# Get offsets

offsets = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
response = requests.get(offsets).json()

dwEntityList = int(response["signatures"]["dwEntityList"])
dwLocalPlayer = int(response["signatures"]["dwLocalPlayer"])

m_clrRender = int(response["netvars"]["m_clrRender"])
m_iTeamNum = int(response["netvars"]["m_iTeamNum"])

# Aimbot injection

pr = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pr.process_handle, "client.dll").lpBaseOfDll

player = pr.read_int(client + dwLocalPlayer)
pteam = pr.read_int(player + m_iTeamNum)

while True:
    try:
        for ent_id in range(1, 32):
            entity = pr.read_int(client + dwEntityList + ent_id * 0x10)

            if entity:
                entity_team_id = pr.read_int(entity + m_iTeamNum)

                if entity_team_id != pteam:
                    ent = pr.read_int(client + dwEntityList + ent_id * 0x10)
                    pr.write_int(ent + m_clrRender, 255)  # Red
                    pr.write_int(ent + m_clrRender + 1, 255)  # Green
                    pr.write_int(ent + m_clrRender + 2, 0)  # Blue
                    pr.write_int(ent + m_clrRender + 3, 10)
    except:
        pass

