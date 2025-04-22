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
        'driver': .8,  # Highest velocity multiplier
        'wood': .7,
        'iron': .55,
        'wedge': .3,
        'putter': .25  # Lowest velocity multiplier
    }
    # Initial launch angles for each club
    launchAngles = {
        'driver': 17,  # Degrees
        'wood': 25,
        'iron': 40,
        'wedge': 50,
        'putter': 0  # Putter has no launch angle
    }
    launchAngle = launchAngles.get(club.lower(), launchAngles['putter'])
    clubMultiplier = clubMultipliers.get(club.lower(), clubMultipliers['putter'])
    
    # Calculate velocity using acceleration and club multiplier
    velocity = acceleration * clubMultiplier 

    deviation = 0 
    if acceleration > 100:
        deviation = random.randint(-1, 1)
    if acceleration > 170:
        deviation = random.randint(-3, 3)
    if acceleration > 210:
        deviation = random.randint(-15, 15)

    if club == 'driver':
        maxVelocity = 140
    elif club == 'wood':
        maxVelocity = 110
    elif club == 'iron':
        maxVelocity = 80
    elif club == 'wedge':
        maxVelocity = 60
    elif club == 'putter':
        maxVelocity = 20
    
    if velocity > maxVelocity:
       if club != 'wedge' and club != 'putter':
            randNumber = random.randint(0, 1)
            if randNumber == 0:
                randAngle = random.randint(-2, 0)
            else:
                randAngle = random.randint(0, 8)
            launchAngle += randAngle

    launchAngleRad = math.radians(launchAngle)
    
    print(velocity, launchAngleRad)
    return min(maxVelocity, velocity), launchAngleRad, math.radians(deviation)
