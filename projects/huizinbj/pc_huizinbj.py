"""
Code to be ran on a computer for Canvas control. This creates an mqtt_remote
 for the robot along with creating the canvas that sends mqtt messages to the
 robot for it to drive to by the user clicking on its interface.

Author: Brett Huizinga
"""
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


def main():
    # This Creates the Remote
    root = tkinter.Tk()
    root.title("Mqtt Remote")
    tab_control = ttk.Notebook(root)

    # Creates the Canvas
    root2 = tkinter.Toplevel()
    root2.title = "Canvas"

    main_frame = ttk.Frame(root2, padding=5)
    main_frame.grid()

    # Creates the canvas
    canvas = tkinter.Canvas(main_frame, background="lightgray", width=480,
                            height=480)
    canvas.grid(columnspan=2)

    # Creates The Mqtt_client for the ev3
    mqtt_client2 = com.MqttClient()
    mqtt_client2.connect_to_ev3()

    # Creates the left click on the Canvas
    canvas.bind("<Button-1>", lambda event: left_click(event, mqtt_client2,
                                                       canvas))

    # Quit Button on Canvas
    quit_button = ttk.Button(main_frame, text="Quit")
    quit_button.grid(row=3, column=1)
    quit_button["command"] = lambda: quit_program(mqtt_client2)

    origin_button = ttk.Button(main_frame, text="Origin")
    origin_button.grid(row=2, column=1)
    origin_button["command"] = lambda: bot_origin(mqtt_client2, canvas)

    # Clear Button on the Canvas
    clear_button = ttk.Button(main_frame, text="Clear")
    clear_button.grid(row=3, column=0)
    clear_button["command"] = lambda: clear(canvas)

    # Creates Tab One
    tab1 = ttk.Frame(tab_control)  # Create a tab
    tab_control.add(tab1, text='Arm Control')  # Add the tab
    tab_control.pack(expand=1, fill="both")  # Pack to make visible

    # Creates Tab Two
    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab2, text='Program')
    tab_control.pack(expand=2, fill="both")

    # Creates Tab Three
    tab3 = ttk.Frame(tab_control)
    tab_control.add(tab3, text='Remote')
    tab_control.pack(expand=2, fill="both")

    # Left speed box
    left_speed_label = ttk.Label(tab3, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(tab3, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=0)

    # Right speed box
    right_speed_label = ttk.Label(tab3, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(tab3, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=1, column=2)

    # Forward Button on Gui
    forward_button = ttk.Button(tab3, text="Forward")
    forward_button.grid(row=2, column=1)
    forward_button['command'] = lambda: send_forward(mqtt_client2,
                                                     int(left_speed_entry.get()
                                                         ),
                                                     int(right_speed_entry.get(

                                                     )))

    root.bind('<Up>', lambda event: send_forward(mqtt_client2,
                                                 int(left_speed_entry.get()),
                                                 int(right_speed_entry.get())))

    # Left Button on Gui
    left_button = ttk.Button(tab3, text="Left")
    left_button.grid(row=3, column=0)
    left_button['command'] = lambda: send_left(mqtt_client2,
                                               int(left_speed_entry.get()),
                                               int(right_speed_entry.get()))
    root.bind('<Left>', lambda event: send_left(mqtt_client2,
                                                int(left_speed_entry.get()),
                                                int(right_speed_entry.get())))

    # Stop Button On Gui
    stop_button = ttk.Button(tab3, text="Stop")
    stop_button.grid(row=3, column=1)
    stop_button['command'] = lambda: stopbot(mqtt_client2)
    root.bind('<space>', lambda event: stopbot(mqtt_client2))

    # Right Button On Gui
    right_button = ttk.Button(tab3, text="Right")
    right_button.grid(row=3, column=2)
    right_button['command'] = lambda: send_right(mqtt_client2,
                                                 int(left_speed_entry.get()),
                                                 int(right_speed_entry.get()))
    root.bind('<Right>', lambda event: send_right(mqtt_client2,
                                                  int(left_speed_entry.get()),
                                                  int(right_speed_entry.get()
                                                      )))

    # Back Button on Gui
    back_button = ttk.Button(tab3, text="Back")
    back_button.grid(row=4, column=1)
    back_button['command'] = lambda: send_back(mqtt_client2,
                                               int(left_speed_entry.get()),
                                               int(right_speed_entry.get()))
    root.bind('<Down>', lambda event: send_back(mqtt_client2,
                                                int(left_speed_entry.get()),
                                                int(right_speed_entry.get())))

    # Up Button On Gui
    up_button = ttk.Button(tab1, text="Arm Up")
    up_button.grid(row=0, column=0)
    up_button['command'] = lambda: send_up(mqtt_client2)
    root.bind('<u>', lambda event: send_up(mqtt_client2))

    # Down Button On Gui
    down_button = ttk.Button(tab1, text="Arm Down")
    down_button.grid(row=1, column=0)
    down_button['command'] = lambda: send_down(mqtt_client2)
    root.bind('<j>', lambda event: send_down(mqtt_client2))

    # Quit Button on Gui
    quit_button = ttk.Button(tab2, text="Quit")
    quit_button.grid(row=0, column=0)
    quit_button['command'] = (lambda: quit_program(mqtt_client2))

    # Keeps the Gui Running
    root.mainloop()


def left_click(event, mqtt_client2, canvas):
    """Creates a waypoint on the canvas and calls the robot's method
    drive_to_waypoint.
    """
    clear(canvas)
    print(event.x, event.y)
    canvas.create_oval(event.x - 5, event.y - 5, event.x + 5, event.y +
                       5, fill="red", width=1)
    mqtt_client2.send_message("drive_to_waypoint", [event.x, event.y, 300])


def obstacle_in_way(mqtt_client):
    print("This way is Blocked")
    mqtt_client.send_message("drive_to_waypoint", [240, 240, 300])


def clear(canvas):
    """Clears the canvas of all the waypoints and lines"""
    canvas.delete("all")


# Arm command callbacks for mqtt_client
def send_up(mqtt_client):
    """Mqtt message that calls for the robot arm to go up"""
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    """Mqtt message that calls for the robot arm to go down"""
    print("arm_down")
    mqtt_client.send_message("arm_down")


def send_forward(mqtt_client, left_speed, right_speed):
    """Mqtt message that calls for the robot to drive forward"""
    print("drive_forward")
    mqtt_client.send_message("drive_forward", [left_speed, right_speed])


def stopbot(mqtt_client):
    """Mqtt message that calls for the robot to stop"""
    print("stop")
    mqtt_client.send_message("stop")


def send_back(mqtt_client, left_speed, right_speed):
    """Mqtt message that calls for the robot to drive backward"""
    print("drive_back")
    mqtt_client.send_message("drive_forward", [-left_speed, -right_speed])


def send_left(mqtt_client, left_speed, right_speed):
    """Mqtt message that calls for the robot turn left"""
    print("drive_left")
    mqtt_client.send_message("drive_forward", [-left_speed, right_speed])


def send_right(mqtt_client, left_speed, right_speed):
    """Mqtt message that calls for the robot to turn right"""
    print("drive_right")
    mqtt_client.send_message("drive_forward", [left_speed, -right_speed])


def bot_origin(mqtt_client, canvas):
    """Mqtt message that calls for the robots origin to be reset"""
    clear(canvas)
    print(240, 240)
    canvas.create_oval(240 - 5, 240 - 5, 240 + 5, 240 +
                       5, fill="red", width=1)
    mqtt_client.send_message("return_bot_origin")


def quit_program(mqtt_client):
    """Closes the mqtt client that forms the GUI"""
    if mqtt_client:
        mqtt_client.close()
    exit()


main()
