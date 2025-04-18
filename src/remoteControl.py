import requests
import time


# phyphox configuration
def getPhyphoxAddress():
    default_port = "8080"
    ip = input("Enter the PhyPhox IP address (e.g., 192.168.2.100): ")
    port = input(f"Enter the port number (press Enter for default {default_port}): ") or default_port
    return f"http://{ip}:{port}"

PP_ADDRESS = getPhyphoxAddress()
# Update channels to include all directions
PP_CHANNELS = ["accX", "accY", "accZ"]

def getAccelerationList():
    """
    Requests acceleration values from the phyphox API and returns the magnitude of acceleration.
    """
    url = PP_ADDRESS + "/get?" + ("&".join(PP_CHANNELS))
    data = requests.get(url=url).json()
    accelerationValues = []
    
    while True:
        # Get values for all directions
        x = data["buffer"]["accX"]["buffer"][0]
        y = data["buffer"]["accY"]["buffer"][0]
        z = data["buffer"]["accZ"]["buffer"][0]
        
        # Calculate magnitude using Pythagorean theorem
        magnitude = (x**2 + y**2 + z**2)**0.5
        return magnitude

# Example usage:
def remoteControl():
    # Let's collect samples and track maximum acceleration
    max_acceleration = 0
    samples = []
    
    # Collect for 10 samples (you can adjust this number)
    for _ in range(10):
        magnitude = getAccelerationList()
        if magnitude is not None:
            samples.append(magnitude)
            maxAcceleration = max(maxAcceleration, magnitude)
        time.sleep(0.1)  # Adjust the delay as needed
    
    print(f"Maximum acceleration magnitude: {max_acceleration} m/s²")
    print("All samples:", samples)

remoteControl()