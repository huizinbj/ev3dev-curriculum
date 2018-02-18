"""This is the file for Improved_LineFollow that sets the robot itself
running and connects it to the mqtt server so that it can recieve messages
containing function calls from the PC and communicate messages of
obstructions back to the PC so that the user can relay further instructions

Author: Cory Reck"""

import ev3dev.ev3 as ev3
import robot_controller as robo


def main():
    ev3.Sound.speak("Fancy Line Following")

    robot = robo.Snatch3r()
    robot.loop_forever()


main()
