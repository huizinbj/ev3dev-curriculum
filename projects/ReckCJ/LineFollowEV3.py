"""This is the file for Improved_LineFollow that sets the robot itself
running and connects it to the mqtt server so that it can recieve messages
containing function calls from the PC and communicate messages of
obstructions back to the PC so that the user can relay further instructions

Author: Cory Reck"""

import ev3dev.ev3 as ev3
import robot_controller as robo

import mqtt_remote_method_calls as com


class ListenerDelegate(object):
    def __init__(self, robot):
        self.robot = robot
        self.mqtt_client = self.robot.mqtt_client

    def drive_inches(self, inches, speed):
        pass

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        pass

    def arm_calibration(self):
        pass

    def arm_up(self):
        pass

    def arm_down(self):
        pass

    def shutdown(self):
        self.robot.shutdown()

    def loop_forever(self):
        pass

    def stop(self):
        self.robot.stop()

    def drive_forward(self, leftspeed, rightspeed):
        pass

    def seek_beacon(self):
        pass

    def calibrate_light(self):
        pass

    def calibrate_dark(self):
        pass

    def wave_hello(self, n):
        pass

    def flex(self, n):
        pass

    def return_start(self):
        pass

    def line_follow(self):
        pass

    def wrong_input(self):
        pass

    def move_obstruction(self):
        pass

    def go_around(self):
        pass

    def drive_to_waypoint(self, x, y, speed):
        pass

    def drive_inches_botwards(self, inches, speed):
        pass

    def drive_inches_bot(self, inches, speed):
        pass

    def reset_xy(self):
        pass

    def return_bot_origin(self):
        pass


def main():
    ev3.Sound.speak("Fancy Line Following")

    robot = robo.Snatch3r()
    stopper_delegate = ListenerDelegate(robot)
    mqtt_client_stop = com.MqttClient(stopper_delegate)
    mqtt_client_stop.connect_to_pc()
    regular_client = com.MqttClient(robot)
    robot.set_mqtt_client(regular_client)
    regular_client.connect_to_pc()
    robot.loop_forever()


main()
