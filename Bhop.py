import traceback

try:
    import keyboard
    import pymem
    from pymem import process
    import time, requests
    from threading import Thread

    offsets = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
    response = requests.get(offsets).json()

    dwLocalPlayer = int(response["signatures"]["dwLocalPlayer"])
    dwForceJump = int(response["signatures"]["dwForceJump"])

    m_fFlags = int(response["netvars"]["m_fFlags"])

    # dwLocalPlayer = 0xD3AC5C
    # dwForceJump = 0x51F8E14
    # m_fFlags = 0x104

    pr = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pr.process_handle, "client.dll").lpBaseOfDll


    def Bhop():
        while True:
            try:
                if keyboard.is_pressed("space"):
                    player = pr.read_int(client + dwLocalPlayer)
                    jump = client + dwForceJump
                    player_state = pr.read_int(player + m_fFlags)

                    if player_state == 257 or player_state == 263:
                        pr.write_int(jump, 5)
                        time.sleep(0.05)
                        pr.write_int(jump, 4)
            except pymem.exception.MemoryReadError:
                pass

    Bhop()
except:
    input(traceback.format_exc())
