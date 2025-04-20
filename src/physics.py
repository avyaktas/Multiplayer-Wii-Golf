from remoteControl import remoteControl
import math
import random 

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
        'driver': 1,  # Highest velocity multiplier
        'wood': .8,
        'iron': .55,
        'wedge': .3,
        'putter': .1  # Lowest velocity multiplier
    }
    # Initial launch angles for each club
    launchAngles = {
        'driver': 17,  # Degrees
        'wood': 25,
        'iron': 40,
        'wedge': 50,
        'putter': 1
    }
    launchAngle = launchAngles.get(club.lower(), launchAngles['putter'])
    launchAngleRad = math.radians(launchAngle)
    clubMultiplier = clubMultipliers.get(club.lower(), clubMultipliers['putter'])
    
    # Calculate velocity using acceleration and club multiplier
    velocity = acceleration * clubMultiplier 

    deviation = 0 
    if velocity > 100:
        deviation = random.randint(-1, 1)
    if velocity > 170:
        deviation = random.randint(-3, 3)
    if velocity > 210:
        deviation = random.randint(-15, 15)

    # if club == 'driver':
    #     maxVelocity = 180
    # if club == 'wood':
    #     maxVelocity = 110
    # if club == 'iron':
    #     maxVelocity = 80
    # if club == 'wedge':
    #     maxVelocity = 60
    # else:
    #     maxVelocity = 10
    

    
    
    
    print(velocity, launchAngleRad)
    return velocity, launchAngleRad, math.radians(deviation)
