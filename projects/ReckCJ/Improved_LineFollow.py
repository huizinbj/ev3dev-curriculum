"""This project's purpose is to have the robot follow a line which may (or
may not) change colors at any point and recalibrate the color sensor as
necessary. Additionally, the robot will sense obstacles in its path and
either move them or simply circumvent them, and have a couple "personality"
movement commands

Entry Box Commands: "About Face"

                    "Go around"
                    "Move object"

Authors: Cory Reck, utilizing robot_controller library as written by Brett
Huizinga and Cory Reck"""

import time
import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


class MyDelegate(object):
    """Simple delegate object class created for the purpose of receiving a
    message that the robot has encountered an obstruction to allow
    obstruction messages to be handled properly."""
    def __init__(self):
        self.robot_obstructed = False

    def obstructed(self):
        self.robot_obstructed = True


def main():
    print("--------------------------------------------")
    print("Advanced Line Following with user commands")
    print("--------------------------------------------")

    delegate = MyDelegate()
    mqtt_client = com.MqttClient(delegate)
    mqtt_client.connect_to_ev3()

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
    move_entry_submit['command'] = lambda: send_move_comand(mqtt_client,
                                                            movement_entry_box)

    stop_button = ttk.Button(tab_1, text="Stop Following")
    stop_button.grid(row=0, column=1)
    # stop_button['command'] = lambda: send_stop(mqtt_client)
    # TODO: Implement secondary MQTTClient to handle loop interruptions

    uturn_button = ttk.Button(tab_1, text="U-turn")
    uturn_button.grid(row=1, column=1)
    uturn_button['command'] = lambda: send_uturn(mqtt_client)

    follow_button = ttk.Button(tab_1, text="Follow Line")
    follow_button.grid(row=0, column=2)
    follow_button['command'] = lambda: send_follow(mqtt_client)

    shutdown_button = ttk.Button(tab_1, text="Shutdown")
    shutdown_button.grid(row=1, column=2)
    shutdown_button['command'] = lambda: send_shutdown(mqtt_client)

    obstacle_entry_label = ttk.Label(tab_2, text="Obstacle Handling")
    obstacle_entry_label.grid(row=0, column=0)
    obstacle_entry_box = ttk.Entry(tab_2, width=10)
    obstacle_entry_box.grid(row=1, column=0)
    obstacle_submit = ttk.Button(tab_2, text="Obstacle Submit")
    obstacle_submit.grid(row=2, column=0)
    obstacle_submit['command'] = lambda: send_obstacle_command(mqtt_client,
                                                          obstacle_entry_box,
                                                          delegate)

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

    root.mainloop()


def send_light(mqtt_client):
    """Sends a message to the robot to calibrate the 'light' value"""
    print("Calibrate Light")
    mqtt_client.send_message("calibrate_light")


def send_dark(mqtt_client):
    """Sends a message to the robot to calibrate the 'dark' value"""
    print("Calibrate Dark")
    mqtt_client.send_message("calibrate_dark")


def send_wave(mqtt_client):
    """Personality command, sends the robot a message to wave using the arm
    motor"""
    print("Waving Hello!")
    mqtt_client.send_message("wave_hello", [5])


def send_flex(mqtt_client):
    """Personality command, sends the robot a message to flex the claw"""
    print("Flexing that claw")
    mqtt_client.send_message("flex", [2])


def send_stop(mqtt_client):
    """Sends a message to the robot to stop moving"""
    print("Stopping the Bot")
    mqtt_client.send_message("stop")


def send_uturn(mqtt_client):
    """Sends a message to the robot to turn around completely"""
    print("U-Turn")
    mqtt_client.send_message("turn_degrees", [180, 300])


def send_shutdown(mqtt_client):
    """Sends a message to the robot to break the loop_forever and cease the
    robot program"""
    print("Shutting Down")
    mqtt_client.send_message("shutdown")


def send_follow(mqtt_client):
    """Sends a message to begin following the line"""
    print("Following the Line")
    mqtt_client.send_message("line_follow")


def send_move_comand(mqtt_client, entry_box):
    """Sends a message to the robot for certain movement commands based upon
    what is in the entry box. In the case that a command is not recognized,
    sends a message that causes an audible indicator of error"""
    if entry_box.get() == "Return to start":
        print("Returning to starting point")
        # mqtt_client.send_message("return_start")
    elif entry_box.get() == "About Face":
        print("Standing at attention for 3 seconds")
        mqtt_client.send_message("turn_degrees", [90, 300])
        time.sleep(3)
    else:
        print("Incorrect Command")
        mqtt_client.send_message("wrong_input")


def send_obstacle_command(mqtt_client, entry_box, delegate):
    """If there is an obstruction in the way of the robot, sends messages to
    the robot regarding how to handle said obstruction. If not, prints a
    statement that there is no obstruction in the console."""
    if delegate.robot_obstructed:
        if entry_box.get() == "Go around":
            mqtt_client.send_message("go_around")
        elif entry_box.get() == "Move Object":
            mqtt_client.send_message("move_obstruction")
            time.sleep(3)
        else:
            print("Incorrect Command")
            mqtt_client.send_message("wrong_input")
    else:
        print("No obstruction")


main()
