from __future__ import print_function

import time
from sr.robot import *


a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

R = Robot()
""" instance of the class Robot"""


def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_closest_uncaptured_token(code_list):
    """
    Function to find the closest token that hasn't been captured by the robot before
    Parameters:
    code_list (list): list for already captured tokens

    Returns:
    dist (float): distance of the closest token (-1 if no token is detected)
    rot_y (float): angle between the robot and the token (-1 if no token is detected)
    token_code (int): the code of the detected token (-1 if no token is detected)
    """
    dist = 100
    token_code = -1  # Initialize to -1 when no token is detected
    for token in R.see():
        #if the token is already captured do not consider it
        if token.info.code in code_list:
            continue
        else:
            if token.dist < dist:
                dist = token.dist
                rot_y = token.rot_y
                token_code = token.info.code
    if dist == 100:
        return -1, -1, -1
    else:
        return dist, rot_y, token.info.code

def find_reference(code_list):
    """
    Function to find the closest reference
    Parameters:
    code_list (list): list for already captured tokens

    Returns:
    dist (float): distance of the closest token (-1 if no token is detected)
    rot_y (float): angle between the robot and the token (-1 if no token is detected)
    """
    dist = 100
    for token in R.see():
        # The following condition ensures correct comparison with the reference, considering the different possible lengths of code_list.
        # The reference is consistently the second-to-last element in code_list based on experimentation.
        if code_list and token.info.code == code_list[-2 if len(code_list) > 1 else -1]:
            if token.dist < dist:
                dist = token.dist
                rot_y = token.rot_y
                print("Reference now is:", token.info.code)

    if dist == 100:
        return -1, -1
    else:
        return dist, rot_y

   	    
   	    
def go_to_reference(code_list):
    """
    Function to go to the closest reference
    Parameters:
    code_list (list): list for already captured tokens
    """
    while 1:
    
        dist, rot_y = find_reference(code_list)
        if dist==-1:
            print("No reference in sight!!")
	    turn(+5, 1)
        elif dist < 1.75*d_th: # Check if the robot is close enough to the reference token
            # The condition is met when the distance to the reference is less than 1.75 times the orientation threshold.
            # This value is chosen based on experimentation and tuning for the robot's behavior in the specific environment.
            print("Found the reference!")
            break
        elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
            print("Ah, here we are!... Moving towards the reference.")
            drive(10, 0.5)
        elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
            print("Left a bit... Moving towards the reference.")
            turn(-2, 0.5)
        elif rot_y > a_th:
            print("Right a bit... Moving towards the reference.")
            turn(+2, 0.5)
    return
    
    
# Main loop

# Initialize an empty list to keep track of tokens that have been captured by the robot
CapturedTokenList = []

# The code of the first token chosen as a reference
reference = 41

# Append the reference token to CapturedTokenList, indicating that it's already captured by the robot
CapturedTokenList.append(reference)

# CapturedTokenList now contains the reference token, which is considered as already captured by the robot


while 1:

    dist, rot_y, token_code = find_closest_uncaptured_token(CapturedTokenList)
    if dist==-1: # if no token is detected, we make the robot turn 
	print("I don't see any token!!")
	turn(+10, 1)
    elif dist <d_th: # if we are close to the token, we try grab it.
        print("Found it!")
        if R.grab():
            print("Gotcha!")
            print("Trying to find the reference")
            go_to_reference(CapturedTokenList)
            R.release()
            drive(-20, 1)
            CapturedTokenList.append(token_code) 
            if len(CapturedTokenList) == 6:
                print("All boxes are put together!")
                turn(+10, 1)
                drive(-10, 1)
                exit()
	else:
            print("Aww, I'm not close enough.")
    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
	print("Ah, that'll do.")
        drive(10, 0.5)
    elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
        print("Left a bit...")
        turn(-2, 0.5)
    elif rot_y > a_th:
        print("Right a bit...")
        turn(+2, 0.5)
