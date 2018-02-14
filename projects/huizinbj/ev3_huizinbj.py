
import ev3dev.ev3 as ev3
import time

import robot_controller as robo
import mqtt_remote_method_calls as com


def main():

    print("--------------------------------------------")
    print(" Running Tracker Control")
    print(" Press the touch sensor to exit")
    print("--------------------------------------------")
    ev3.Sound.speak("Tracker Control").wait()
    print("Press the touch sensor to exit this program.")

    # Creates Mqtt Client and Snatcher Bot
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_pc()
    robot = robo.Snatch3r()
    btn = ev3.Button()

    while not robot.touch_sensor.is_pressed():
        if btn.up:
            mqtt_client.send_message("print_robot_position", [250,
                                                              250, mqtt_client])

    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()
    mqtt_client.close()

main()