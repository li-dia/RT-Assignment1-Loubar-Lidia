# Box Assembling Robot 
## Description:
This repository contains the code for controlling a robot to autonomously put boxes together by detecting and capturing individual components represented by tokens.

The code is designed for a robot to navigate its environment, identify uncaptured tokens, capture them, and then align itself with a reference token to assemble boxes. Tokens are visual markers representing boxes. The robot uses a set of predefined functions for driving, turning, and interacting with the environment.

## Pseudo Code:

```python
# Define constants
a_th = 2.0  # Threshold for the control of the linear distance
d_th = 0.4  # Threshold for the control of the orientation

# Initialize the robot
R = Robot()

# Define functions for driving and turning
function drive(speed, seconds):
    Set linear velocity of the robot wheels
    Wait for 'seconds'
    Set linear velocity of the robot wheels to 0

function turn(speed, seconds):
    Set angular velocity of the robot wheels
    Wait for 'seconds'
    Set angular velocity of the robot wheels to 0

function find_closest_uncaptured_token(code_list):
    Initialize dist to 100
    Initialize token_code to -1
    For each token in R.see():
        If token.info.code is in code_list:
            Continue to the next token
        Else:
            If token.dist < dist:
                Update dist, rot_y, and token_code
    If dist is still 100:
        Return -1, -1, -1
    Else:
        Return dist, rot_y, token_code

function find_reference(code_list):
    Initialize dist to 100
    For each token in R.see():
        If token.info.code is the second-to-last element in code_list:
            Update dist and rot_y
            Print the reference code
    If dist is still 100:
        Return -1, -1
    Else:
        Return dist, rot_y

function go_to_reference(code_list):
    Loop indefinitely:
        Get dist, rot_y from find_reference(code_list)
        If dist is -1:
            Print "No reference in sight!!"
            Turn the robot to the right
        Else if dist < 1.75 * d_th:
            Print "Found the reference!"
            Break out of the loop
        Else if -a_th <= rot_y <= a_th:
            Print "Ah, here we are!... Moving towards the reference."
            Drive forward
        Else if rot_y < -a_th:
            Print "Left a bit... Moving towards the reference."
            Turn the robot to the left
        Else if rot_y > a_th:
            Print "Right a bit... Moving towards the reference."
            Turn the robot to the right

# Main loop
Initialize CapturedTokenList to an empty list
Set reference to 41
Append reference to CapturedTokenList

Loop indefinitely:
    Get dist, rot_y, and token_code from find_closest_uncaptured_token(CapturedTokenList)
    If dist is -1:
        Print "I don't see any token!!"
        Turn the robot to the right
    Else if dist < d_th:
        Print "Found it!"
        If R.grab():
            Print "Gotcha!"
            Print "Trying to find the reference"
            Call go_to_reference(CapturedTokenList)
            Release the grabbed object
            Drive backward
            Append token_code to CapturedTokenList
            If the length of CapturedTokenList is 6:
                Print "All boxes are put together!"
                Turn the robot to the right
                Drive backward
                Exit the program
        Else:
            Print "Aww, I'm not close enough."
    Else if -a_th <= rot_y <= a_th:
        Print "Ah, that'll do."
        Drive forward
    Else if rot_y < -a_th:
        Print "Left a bit..."
        Turn the robot to the left
    Else if rot_y > a_th:
        Print "Right a bit..."
        Turn the robot to the right
```
## Flowchart:
The flowchart visually represents the sequential steps the robot takes to assemble the boxes. It illustrates the decision-making process, token detection, and the loop that guides the robot through capturing and assembling components.

![image](https://github.com/li-dia/RT-Assignment1-Loubar-Lidia/assets/118188149/eedee2f9-cb9b-46bf-b715-287139185099)

## Getting Started:

1. Clone the repository using:
```bash
git clone https://github.com/li-dia/RT-Assignment1-Loubar-Lidia.git
```
2. When done, go to `robot-sim` folder, you can run the program with:

```bash
$ python run.py assignment.py
```

## Possible Improvements:

1. **Optimization:**
Optimize the code for better performance.
2. **Error Handling:**
Implement robust error handling for unexpected scenarios.
3. **Enhance Token Detection:**
Explore ways to improve token detection accuracy.
