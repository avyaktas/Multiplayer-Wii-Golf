#from graphicsTogether import app 
import requests
import json
import time
# the get logic for using channel and getting data is inspired from phyPhox api 
# phyphox configuration

def getAcceleration(ip):
    """
    Fetch the latest acceleration magnitude from PhyPhox.
    """
    url = f"http://{ip}:80" + "/get?" + "&" + "acc"
    resp = requests.get(url, timeout=1)
    resp.raise_for_status()
    data = resp.json()
    return data["buffer"]["acc"]["buffer"][0]


def remoteControl(ip):
    """
    Runs for 10 seconds, sampling acceleration,
    and returns the maximum value seen.
    """
    maxAcc = 0.0
    startTime = time.time()
    endTime = startTime + 7.0

    while time.time() < endTime:
        magnitude = getAcceleration(ip)
        if isinstance(magnitude, float):
            maxAcc = max(maxAcc, magnitude)
        time.sleep(0.05)

    print("Final maxAcc:", maxAcc)
    return maxAcc


