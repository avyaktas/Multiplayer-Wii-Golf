
import requests
import time

# phyphox configuration
PP_ADDRESS = "http://192.168.2.100:8080"
# Specify one or more acceleration channels; here we use only "accY"
PP_CHANNELS = ["accY"]

def getAccelerationList():
    """
    Requests acceleration values from the phyphox API and returns a list of current values.
    Each value in the returned list corresponds to one channel as defined by PP_CHANNELS.
    """
    url = PP_ADDRESS + "/get?" + ("&".join(PP_CHANNELS))
    data = requests.get(url=url).json()
    acceleration_values = []
    for channel in PP_CHANNELS:
        try:
            # Extract the first value from the buffer for this channel.
            value = data["buffer"][channel]["buffer"][0]
        except (KeyError, IndexError):
            # If there is any error getting the value, return None for that channel.
            value = None
        acceleration_values.append(value)
    return acceleration_values

# Example usage:
def remoteControl():
    # Let's collect 10 samples of acceleration readings.
    all_samples = []
    for _ in range(10):
        sample = getAccelerationList()
        print("Acceleration sample:", sample)
        all_samples.append(sample)
        time.sleep(0.1)  # Adjust the delay as needed

    print("Collected acceleration samples:")
    print(all_samples)
