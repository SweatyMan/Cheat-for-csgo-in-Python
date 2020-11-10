# Importing Libraries

import requests, time
import pymem.process

# Get offsets

offsets = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
response = requests.get(offsets).json()

dwEntityList = int(response["signatures"]["dwEntityList"])
dwLocalPlayer = int(response["signatures"]["dwLocalPlayer"])

m_iFOV = int(response["netvars"]["m_iFOV"])
m_bIsScoped = int(response["netvars"]["m_bIsScoped"])

# Aimbot injection

pr = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pr.process_handle, "client.dll").lpBaseOfDll

player = pr.read_int(client + dwLocalPlayer)

while True:
    time.sleep(0.01)
    if not pr.read_int(player + m_bIsScoped):
        pr.write_int(player + m_iFOV, 125)
