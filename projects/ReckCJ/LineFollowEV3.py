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

    def send_light(self):
        pass

    def send_dark(self):
        pass

    def send_wave(self):
        pass

    def send_flex(self):
        pass

    def send_stop(self):
        """Secondary MQTTClient receives message through follow loop to
        stop the robot"""
        print("Stopping the Bot")
        self.robot.stop()

    def send_uturn(self):
        pass

    def send_shutdown(self):
        """Secondary MQTTClient receives message through follow loop to
        shutdown the robot"""
        print("Shutting Down")
        self.robot.shutdown()

    def send_follow(self):
        pass

    def send_move_comand(self):
        pass

    def send_obstacle_command(self):
        pass


def main():
    ev3.Sound.speak("Fancy Line Following")

    robot = robo.Snatch3r()
    stopper_delegate = ListenerDelegate(robot)
    mqtt_cleint_stop = com.MqttClient(stopper_delegate)
    mqtt_cleint_stop.connect_to_pc()
    robot.loop_forever()


main()
