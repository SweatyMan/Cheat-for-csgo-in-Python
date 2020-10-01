import pymem, requests, time
import pymem.process
from threading import Thread

offsets = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
response = requests.get(offsets).json()

dwGlowObjectManager = int(response["signatures"]["dwGlowObjectManager"])
dwEntityList = int(response["signatures"]["dwEntityList"])

m_iTeamNum = int(response["netvars"]["m_iTeamNum"])
m_iGlowIndex = int(response["netvars"]["m_iGlowIndex"])

pr = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pr.process_handle, "client.dll").lpBaseOfDll


def ESP():
    while True:
        glow_manager = pr.read_int(client + dwGlowObjectManager)

        for i in range(1, 32):
            entity = pr.read_int(client + dwEntityList + i * 0x10)

            if entity:
                entity_team_id = pr.read_int(entity + m_iTeamNum)
                entity_glow = pr.read_int(entity + m_iGlowIndex)

                if entity_team_id == 2:  # Terrorist
                    pr.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(1))
                    pr.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(1))
                    pr.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))
                    pr.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))
                    pr.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)

                elif entity_team_id == 3:
                    pr.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(0))
                    pr.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))
                    pr.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))
                    pr.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))
                    pr.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)
        time.sleep(0.025)


Thread(target=ESP).start()
