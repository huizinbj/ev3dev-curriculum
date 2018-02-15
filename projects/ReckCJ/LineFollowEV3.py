"""This is the file for Improved_LineFollow that sets the robot itself
running and connects it to the mqtt server so that it can recieve messages
containing function calls from the PC and communicate messages of
obstructions back to the PC so that the user can relay further instructions

Author: Cory Reck"""

import mqtt_remote_method_calls as com
import robot_controller as robo


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    robot.loop_forever()
