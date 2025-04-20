from remoteControl import remoteControl


def calculateVelocity(club): #add ground later
    """
    Calculates the ball velocity based on acceleration input and selected club.
    
    Args:
        acceleration (float): Acceleration magnitude from remote control
        club (str): Selected club type ('driver', 'iron', 'putter', etc)
        
    Returns:
        float: Calculated velocity in m/s
    """
    acceleration = remoteControl()
    # Base multiplier for acceleration to velocity conversion
    
    # Club-specific velocity multipliers
    clubMultipliers = {
        'driver': 1.2,  # Highest velocity multiplier
        'wood': 1.1,
        'iron': .9,
        'wedge': .5,
        'putter': .2  # Lowest velocity multiplier
    }
    # Initial launch angles for each club
    launchAngles = {
        'driver': 10,  # Degrees
        'wood': 14,
        'iron': 40,
        'wedge': 60,
        'putter': 1
    }
    launchAngle = launchAngles.get(club.lower(), launchAngles['putter'])
    launchAngleRad = launchAngle * (3.14/180)
    clubMultiplier = clubMultipliers.get(club.lower(), clubMultipliers['putter'])
    
    # Calculate velocity using acceleration and club multiplier
    velocity = acceleration * clubMultiplier
    
    # Add minimum and maximum velocity constraints
    minVelocity = 0.5  # Minimum velocity in m/s
    maxVelocity = 50.0 # Maximum velocity in m/s
    print(velocity, launchAngle)
    return max(minVelocity, min(velocity, maxVelocity)), launchAngle
