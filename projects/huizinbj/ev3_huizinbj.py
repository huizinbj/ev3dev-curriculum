import ev3dev.ev3 as ev3
import robot_controller as robo
import mqtt_remote_method_calls as com
import time

class DataContainer(object):
    """ Helper class that might be useful to communicate between different callbacks."""
    def __init__(self):
        self.running = True

def main():
    print("--------------------------------------------")
    print(" Running Tracker Control")
    print(" Press the touch sensor to exit")
    print("--------------------------------------------")
    ev3.Sound.speak("Tracker Control").wait()
    print("Press the touch sensor to exit this program.")

    # Creates Mqtt Client and Snatcher Bot
    robot = robo.Snatch3r()
    dc = DataContainer()

    mqtt_client2 = com.MqttClient(robot)
    robot.set_mqtt_client(mqtt_client2)
    mqtt_client2.connect_to_pc()

    btn = ev3.Button()
    btn.on_up = handle_up_button()
    while dc.running:
        btn.process()  # This command is VERY important when using button callbacks!
        time.sleep(0.01)


def handle_up_button(button_state):
    if button_state:
        print("Up button is pressed")
        mqtt_client2.connect_to_pc

    else:
        print("Up button was released")
main()
