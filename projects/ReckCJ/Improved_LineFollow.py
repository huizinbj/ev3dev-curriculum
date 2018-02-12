"""This project's purpose is to have the robot follow a line which may (or
may not) change colors at any point and recalibrate the color sensor as
necessary. Additionally, the robot will sense obstacles in its path and
either move them or simply circumvent them, and wil be able to return to its
original position on command.

Entry Box Commands: "Return to start"

                    "Go around"
                    "Move object"

Authors: Cory Reck, utilizing robot_controller library as written by Brett
Huizinga and Cory Reck"""

import ev3dev.ev3 as ev3
import time
import math
import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com
import robot_controller as robo


def main():
    print("--------------------------------------------")
    print("Advanced Line Following with user commands")
    print("--------------------------------------------")
    ev3.Sound.speak("Follow Fancy Line").wait()

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()
    robot = robo.Snatch3r()

    root = tkinter.Tk()
    root.title("Advanced Line Follow controls")
    tab_control = ttk.Notebook(root)

    tab_1 = ttk.Frame(tab_control)
    tab_control.add(tab_1, text="Movement")
    tab_control.pack(expand=1, fill="both")

    tab_2 = ttk.Frame(tab_control)
    tab_control.add(tab_2, text="Obstacle Handling")
    tab_control.pack(expand=2, fill="both")

    movement_entry_label = ttk.Label(tab_1, text="Movement Command Entry")
    movement_entry_label.grid(row=0, column=0)
    movement_entry_box = ttk.Entry(tab_1, width=10)
    movement_entry_box.grid(row=1, column=0)

    stop_button = ttk.Button(tab_1, text="Stop")
    stop_button.grid(row=0, column=1)
    stop_button['command'] = lambda: send_stop(mqtt_client)

    uturn_button = ttk.Button(tab_1, text="U-turn")
    uturn_button.grid(row=1, column=1)
    uturn_button['command'] = lambda: send_uturn(mqtt_client)

    obstacle_entry_label = ttk.Label(tab_2, text="Obstacle Handling")
    obstacle_entry_label.grid(row=0, column=0)
    obstacle_entry_box = ttk.Entry(tab_2, width=10)
    obstacle_entry_box.grid(row=1, column=0)

    light_button = ttk.Button(tab_2, text="Calibrate Light")
    light_button.grid(row=0, column=2)
    light_button['command'] = lambda: send_light(mqtt_client)

    dark_button = ttk.Button(tab_2, text="Calibrate Dark")
    dark_button.grid(row=2, column=2)
    dark_button['command'] = lambda: send_dark(mqtt_client)

    wave_button = ttk.Button(tab_2, text="Wave Hello!")
    wave_button.grid(row=1, column=1)
    wave_button['command'] = lambda: send_wave(mqtt_client)

    flex_button = ttk.Button(tab_2, text="Flex Claw")
    flex_button.grid(row=1, column=3)
    flex_button['command'] = lambda: send_flex(mqtt_client)

    if robot.color_sensor.reflected_light_intensity < robot.dark_level+10:
        robot.drive_forward(300, 300)
    else:
        robot.turn_degrees(1, 200)






def send_light(mqtt_client):
    print("Calibrate Light")
    ev3.Sound.speak("Calibrating Light")
    mqtt_client.send_message("calibrate_light")


def send_dark(mqtt_client):
    print("Calibrate Dark")
    ev3.Sound.speak("Calibrating Dark")
    mqtt_client.send_message("calibrate_dark")


def send_wave(mqtt_client):
    print("Waving Hello!")
    ev3.Sound.speak("Hello")
    mqtt_client.send_message("wave_hello", 5)


def send_flex(mqtt_client):
    print("Flexing that claw")
    ev3.Sound.speak("Flex")
    mqtt_client.send_message("flex", 2)


def send_stop(mqtt_client):
    print("Stopping the Bot")
    ev3.Sound.speak("Stopping")
    mqtt_client.send_message("stop")


def send_uturn(mqtt_client):
    print("U-Turn")
    ev3.Sound.speak("Turning Around")
    mqtt_client.send_message("uturn")