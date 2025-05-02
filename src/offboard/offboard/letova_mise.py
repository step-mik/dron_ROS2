#!/usr/bin/env python3

import subprocess
import time

def main():
    # Resetování režimu OFFBOARD na začátku každého spuštění
    print("[1] RESETUJEME REŽIM OFFBOARD...")
    offboard_reset = subprocess.Popen(['ros2', 'run', 'offboard', 'reset_offboard'])
    offboard_reset.wait()  # Čekáme na dokončení resetování režimu
    print("[INFO] Režim OFFBOARD resetován.")

    # Vzlet
    print("[2] VZLET...")
    vzlet = subprocess.Popen(['ros2', 'run', 'offboard', 'vzlet'])
    time.sleep(15)  # Pauza po vzletu
    vzlet.terminate()

    # Let dopředu
    print("[3] LET DOPŘEDU...")
    dopredu = subprocess.Popen(['ros2', 'run', 'offboard', 'dopredu'])

    # Nezablokujeme program, čekáme na proces dopredu
    while dopredu.poll() is None:
        time.sleep(1)  # čekáme na dokončení dopredu
    
    # Možná kontrola úspěchu letu (logování nebo podmínky)
    if dopredu.poll() == 0:
        print("[INFO] Let dopředu byl úspěšně dokončen.")
    else:
        print("[ERROR] Let dopředu selhal.")

if __name__ == '__main__':
    main()

