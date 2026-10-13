import time
import subprocess

def killWifi(wifiShutdownTime: int):

    shutdownWifiCommand = ['netsh', 'interface', 'set', 'interface', 'Wi-Fi', 'disable']

    turnOnWifiCommand = ['netsh', 'interface', 'set', 'interface', 'Wi-Fi', 'enable']
    

    subprocess.run(['netsh', 'interface', 'set', 'interface', 'Wi-Fi', 'disable'], check=True, capture_output=True, text=True)
    time.sleep(wifiShutdownTime)
    subprocess.run(turnOnWifiCommand, check=True, capture_output=True, text=True)