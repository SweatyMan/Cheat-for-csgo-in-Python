import pymem, time, requests
import pymem.process
from threading import Thread

offsets = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
response = requests.get(offsets).json()

dwLocalPlayer = int(response["signatures"]["dwLocalPlayer"])
m_flFlashMaxAlpha = int(response["netvars"]["m_flFlashMaxAlpha"])

pr = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pr.process_handle, "client.dll").lpBaseOfDll


def NoFlash():
    while True:
        player = pr.read_int(client + dwLocalPlayer)
        if player:
            flash_value = player + m_flFlashMaxAlpha
            if flash_value:
                pr.write_float(flash_value, float(0))
        time.sleep(1)


Thread(target=NoFlash).start()
