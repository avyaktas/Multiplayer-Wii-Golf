print('hello')
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

def getAcceleration():
    """
    Requests acceleration values from the phyphox API and returns the magnitude of acceleration.
    """
    url = PP_ADDRESS + "/get?" + ("&".join(PP_CHANNELS))
    response = requests.get(url).text
    data = json.loads(response)
    for item in PP_CHANNELS:
        acc_data = data['buffer'][item]['buffer'][0]
        print(f"{item}: {acc_data}", end='\t')
    
    # Get values for all directions
    magnitude = data["buffer"]["acc"]["buffer"][0]
    return magnitude

# Example usage:
def remoteControl():
    # Let's collect samples and track maximum acceleration
    maxAcceleration = 0
    samples = []
    
    # Collect for 10 samples (you can adjust this number)
    for i in range(50):
        magnitude = getAcceleration()
        if magnitude is not None:
            samples.append(magnitude)
            maxAcceleration = max(maxAcceleration, magnitude)
        time.sleep(0.2)  # Adjust the delay as needed
    
    print(f"Maximum acceleration magnitude: {maxAcceleration} m/s²")
    print("All samples:", samples)

remoteControl()