"""
Code to be ran on the ev3 for Canvas control. The robot is receiving waypoint
selected on the computers canvas and converts them in a 4ft by 4 ft area.

Author: Brett Huizinga
"""
import ev3dev.ev3 as ev3
import robot_controller as robo
import mqtt_remote_method_calls as com
import time


def main():
    print("--------------------------------------------")
    print(" Running Canvas Control")
    print(" Press the touch sensor to exit")
    print("--------------------------------------------")
    ev3.Sound.speak("Canvas Control").wait()
    print("Press the touch sensor to exit this program.")

    # Creates Mqtt Client and Snatcher Bot
    robot = robo.Snatch3r()
    mqtt_client2 = com.MqttClient(robot)
    robot.set_mqtt_client(mqtt_client2)
    mqtt_client2.connect_to_pc()

    while robot.running:
        time.sleep(0.01)
        if robot.ir_sensor.proximity < 10:
            robot.stop()
        if robot.touch_sensor.is_pressed:
            print("I have the object")
            time.sleep(0.01)
            robot.arm_down()



main()
