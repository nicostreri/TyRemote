import json
import os
import subprocess
import iwlist
import platform


def __get_first_interface_linux():
    """
    Return the first wireless interface in the system.
    :pre: Only invoke in Linux system. Requires iw and awk commands.
    :return: the first interface, otherwise "wlan0"
    :rtype: str
    """
    output = subprocess.check_output("iw dev | awk '$1==\"Interface\"{print $2}'", shell=True)
    for row in output.decode('utf-8').split('\n'):
        return row
    return 'wlan0'


def __get_wifi_networks_linux():
    networks = []
    scanned_networks = iwlist.parse(iwlist.scan(interface=__get_first_interface_linux()))
    for c_net in scanned_networks:
        networks.append({
            "mac": c_net["mac"],
            "powrx": int(c_net["signal_level_dBm"]),
            "name": c_net["essid"]
        })
    return networks


def __read_networks_from_file_windows():
    scanned_networks = []
    f = None
    try:
        f = open('tempWifi.json', 'r', encoding="utf-16")
        scanned_networks = json.loads(f.read())
    finally:
        if f is not None:
            f.close()
            os.remove('tempWifi.json')
    return scanned_networks


def __get_wifi_networks_windows():
    execution_result = os.system('WifiInfoView.exe /sjson tempWifi.json')
    if execution_result != 0:
        return []
    scanned_networks = __read_networks_from_file_windows()
    networks = []
    for c_net in scanned_networks:
        networks.append({
            "mac": c_net["MAC Address"],
            "powrx": int(c_net["RSSI"]),
            "name": c_net["SSID"]
        })
    return networks


def get_wifi_networks():
    """
    For each wifi network in range gets SSID, MAC and Signal
    :return: List of wifi networks
    """
    os = platform.system()
    if os == 'Linux':
        return __get_wifi_networks_linux()
    elif os == 'Windows':
        return __get_wifi_networks_windows()
    else:
        return []
