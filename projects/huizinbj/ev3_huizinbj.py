import time
import ev3dev.ev3 as ev3
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
    robot = robo.Snatch3r()

    mqtt_client2 = com.MqttClient(robot)
    robot.set_mqtt_client(mqtt_client2)
    mqtt_client2.connect_to_pc()

    while not robot.touch_sensor.is_pressed:
        if robot.ir_sensor.proximity < 10:
            ev3.Sound.beep()
            mqtt_client2.send_message("obstacle_in_way", robot.last_x,
                                      robot.last_y, robot.current_x,
                                      robot.current_y)
            ev3.Sound.speak("There is a Obstacle, Returning to origin").wait()
            time.sleep(1.5)
        time.sleep(0.1)

    robot.loop_forever()

    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()
    robot.stop()
    mqtt_client2.close()


main()
