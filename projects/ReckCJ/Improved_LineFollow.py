"""This project's purpose is to have the robot follow a line which may (or
may not) change colors at any point and recalibrate the color sensor as
necessary. Additionally, the robot will sense obstacles in its path and
either move them or simply circumvent them, and wil be able to return to its
original position on command, and have a couple "personality" movement commands

Entry Box Commands: "Return to start"
                    "About Face"

                    "Go around"
                    "Move object"

Authors: Cory Reck, utilizing robot_controller library as written by Brett
Huizinga and Cory Reck"""

import ev3dev.ev3 as ev3
import time
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
    move_entry_submit = ttk.Button(tab_1, text="Submit Move Commands")
    move_entry_submit.grid(row=2, column=0)
    movement_entry_box['command'] = lambda: send_move_comand(mqtt_client,
                                                            movement_entry_box)

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
    obstacle_submit = ttk.Button(tab_2, text="Obstacle Submit")
    obstacle_submit.grid(row=2, column=0)
    obstacle_submit['command'] = lambda: send_move_comand(mqtt_client,
                                                          obstacle_entry_box)

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

    while True:
        if robot.light_calibrated and robot.dark_calibrated:
            break
        time.sleep(0.01)
    if robot.color_sensor.reflected_light_intensity < robot.dark_level+10:
        robot.drive_forward(300, 300)
        time.sleep(0.1)
    elif robot.color_sensor.reflected_light_intensity > robot.light_level-10:
        robot.turn_degrees(5, 200)
        time.sleep(0.1)
    else:
        robot.dark_calibrated = False
        robot.light_calibrated = False
        while True:
            time.sleep(0.1)
            if robot.light_calibrated and robot.dark_calibrated:
                break

    if robot.ir_sensor.proximity < 10:
        robot.obstructed = True
        robot.stop()
        ev3.Sound.speak("Obstacle")

    while robot.obstructed:
        time.sleep(0.01)
        if robot.obstructed == False:
            break

    root.mainloop()


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
    mqtt_client.send_message("wave_hello", [5])


def send_flex(mqtt_client):
    print("Flexing that claw")
    ev3.Sound.speak("Flex")
    mqtt_client.send_message("flex", [2])


def send_stop(mqtt_client):
    print("Stopping the Bot")
    ev3.Sound.speak("Stopping")
    mqtt_client.send_message("stop")


def send_uturn(mqtt_client):
    print("U-Turn")
    ev3.Sound.speak("Turning Around")
    mqtt_client.send_message("turn_degrees", [180, 300])


def send_move_comand(mqtt_client, entry_box):
    if entry_box.get() == "Return to start":
        ev3.Sound.speak("Going Home")
        mqtt_client.send_message("return_start")
    elif entry_box.get() == "About Face":
        ev3.Sound.speak("Ten Hut")
        mqtt_client.send_message("turn_degrees", [90, 300])
        time.sleep(3)
    else:
        ev3.Sound.speak("What")