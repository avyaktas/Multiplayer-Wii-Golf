

def calculateVelocity(acceleration, club):
    """
    Calculates the ball velocity based on acceleration input and selected club.
    
    Args:
        acceleration (float): Acceleration magnitude from remote control
        club (str): Selected club type ('driver', 'iron', 'putter', etc)
        
    Returns:
        float: Calculated velocity in m/s
    """
    # Base multiplier for acceleration to velocity conversion
    baseMultiplier = 2.0
    
    # Club-specific velocity multipliers
    clubMultipliers = {
        'driver': 5.0,  # Highest velocity multiplier
        'wood': 4.0,
        'iron': 3.0,
        'wedge': 2.0,
        'putter': 1.0   # Lowest velocity multiplier
    }
    # Initial launch angles for each club
    launchAngles = {
        'driver': 10,  # Degrees
        'wood': 12,
        'iron': 15,
        'wedge': 20,
        'putter': 30
    }
    launchAngle = launchAngles.get(club.lower(), launchAngles['putter'])
    clubMultiplier = clubMultipliers.get(club.lower(), clubMultipliers['putter'])
    
    # Calculate velocity using acceleration and club multiplier
    velocity = acceleration * baseMultiplier * clubMultiplier
    
    # Add minimum and maximum velocity constraints
    minVelocity = 0.5  # Minimum velocity in m/s
    maxVelocity = 50.0 # Maximum velocity in m/s
    
    return max(minVelocity, min(velocity, maxVelocity)), launchAngle 
