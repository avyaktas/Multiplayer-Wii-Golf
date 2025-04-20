from cmu_graphics import *
import requests
import json
import time

# phyphox configuration
def getPhyphoxAddress():
    defaultPort = "80"
    ip = input("Enter the PhyPhox IP address (e.g., 192.168.2.100): ")
    port = input(f"Enter the port number (press Enter for default {defaultPort}): ") or defaultPort
    return f"http://{ip}:{port}"

PP_ADDRESS = getPhyphoxAddress()
# Update channels to include all directions
PP_CHANNELS = ["acc"]

def getURL():
    if not hasattr(getURL, "url"): 
        getURL.url = PP_ADDRESS + "/get?" + ("&".join(PP_CHANNELS))
    return getURL.url


def getAcceleration():
    """
    Requests acceleration values from the phyphox API and returns the magnitude of acceleration.
    """
    url = getURL()
    response = requests.get(url).text
    data = json.loads(response)
    for item in PP_CHANNELS:
        acc_data = data['buffer'][item]['buffer'][0]
        # print(f"{item}: {acc_data}", end='\t')
    
    # Get values for all directions
    magnitude = data["buffer"]["acc"]["buffer"][0]
    return magnitude

# Example usage:
def remoteControl():
    # Let's collect samples and track maximum acceleration
    maxAcceleration = 0
    samples = []
    
    # Collect for 10 samples (you can adjust this number)
    for i in range(500):
        magnitude = getAcceleration()
        if magnitude != None and magnitude > 15:
            samples.append(magnitude)
            maxAcceleration = max(maxAcceleration, magnitude)
            # print(samples)
            print(maxAcceleration)
        time.sleep(0.01)  # Adjust thedelay as needed
    return maxAcceleration
remoteControl()