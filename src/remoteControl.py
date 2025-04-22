from cmu_graphics import *
import requests
import json
import time
# the get logic for using channel and getting data is inspired from phyPhox 
# phyphox configuration
def getPhyphoxAddress():
    defaultPort = "80"
    ip = input("Enter the PhyPhox IP address (e.g., 192.168.2.100): ")
    port = input(f"Enter the port number (press Enter for default {defaultPort}): ") or defaultPort
    return f"http://{ip}:{port}"

PP_ADDRESS = "http://170.20.10.1:80"
PP_CHANNELS = ["acc"]

def getURL():
    if not hasattr(getURL, "url"):
        # builds "http://172.20.10.1:80/get?acc"
        getURL.url = PP_ADDRESS + "/get?" + "&".join(PP_CHANNELS)
    return getURL.url


def getAcceleration():
    """
    Fetch the latest acceleration magnitude from PhyPhox.
    """
    url = getURL()   # ← use getURL(), not PP_ADDRESS
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data["buffer"]["acc"]["buffer"][0]


def remoteControl():
    """
    Runs for 10 seconds, sampling acceleration,
    and returns the maximum value seen.
    """
    maxAcc = 0.0
    startTime = time.time()
    endTime = startTime + 7.0

    while time.time() < endTime:
        magnitude = getAcceleration()
        if isinstance(magnitude, float):
            maxAcc = max(maxAcc, magnitude)
        time.sleep(0.05)

    print("Final maxAcc:", maxAcc)
    return maxAcc


