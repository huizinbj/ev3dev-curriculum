import tkinter
from tkinter import ttk
from tkinter import *
import mqtt_remote_method_calls as com


def left_click(event):
    print(event.x, event.y)
    waypoint(event.x, event.y)



def waypoint(x, y):
    print(x, y)


def prints():
    print("Works")


def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    # This Creates the Canvas

    root2 = tkinter.Tk()
    root2.title = "Canvas"

    main_frame = ttk.Frame(root2, padding=5)
    main_frame.grid()

    canvas = tkinter.Canvas(main_frame, background="lightgray", width=500,
                            height=500)
    canvas.grid(columnspan=2)
    canvas.bind("<Button-1>", left_click)

    quit_button = ttk.Button(main_frame, text="Quit")
    quit_button.grid(row=3, column=1)
    quit_button["command"] = lambda: print("Hi")

    quit_button = ttk.Button(main_frame, text="Clear")
    quit_button.grid(row=3, column=0)
    quit_button["command"] = lambda: print("Hi")


    # This Creates the Mqtt Remote GUI and Buttons
    root = Tk()
    root.title("Mqtt Remote")
    tab_control = ttk.Notebook(root)

    # Creates Tab One
    tab1 = ttk.Frame(tab_control)  # Create a tab
    tab_control.add(tab1, text='Remote')  # Add the tab
    tab_control.pack(expand=1, fill="both")  # Pack to make visible

    # Creates Tab Two
    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab2, text='Arm Control')
    tab_control.pack(expand=2, fill="both")

    # Creates Tab Three
    tab3 = ttk.Frame(tab_control)
    tab_control.add(tab3, text='Program')
    tab_control.pack(expand=2, fill="both")

    # Left speed box
    left_speed_label = ttk.Label(tab1, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(tab1, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=0)

    # Right speed box
    right_speed_label = ttk.Label(tab1, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(tab1, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=1, column=2)

    # Forward Button
    forward_button = ttk.Button(tab1, text="Forward")
    forward_button.grid(row=2, column=1)
    forward_button['command'] = lambda: prints()
    root.bind('<Up>', lambda event: prints())

    # Left Button
    left_button = ttk.Button(tab1, text="Left")
    left_button.grid(row=3, column=0)
    left_button['command'] = lambda: prints()
    root.bind('<Left>', lambda event: prints())

    # Stop Button
    stop_button = ttk.Button(tab1, text="Stop")
    stop_button.grid(row=3, column=1)
    stop_button['command'] = lambda: prints()
    root.bind('<space>', lambda event: prints())

    # Right Button
    right_button = ttk.Button(tab1, text="Right")
    right_button.grid(row=3, column=2)
    right_button['command'] = lambda: prints()
    root.bind('<Right>', lambda event: prints())

    # Back Button
    back_button = ttk.Button(tab1, text="Back")
    back_button.grid(row=4, column=1)
    back_button['command'] = lambda: prints()
    root.bind('<Down>', lambda event: prints())

    # Up Button
    up_button = ttk.Button(tab2, text="Arm Up")
    up_button.grid(row=0, column=0)
    up_button['command'] = lambda: prints()
    root.bind('<u>', lambda event: prints())

    # Down Button
    down_button = ttk.Button(tab2, text="Arm Down")
    down_button.grid(row=1, column=0)
    down_button['command'] = lambda: prints()
    root.bind('<j>', lambda event: prints())

    # Quit Button
    quit_button = ttk.Button(tab3, text="Quit")
    quit_button.grid(row=0, column=0)
    quit_button['command'] = (lambda: prints())

    # End Button
    end_button = ttk.Button(tab3, text="Exit")
    end_button.grid(row=1, column=0)
    end_button['command'] = (lambda: prints())

    root.mainloop()
    canvas.mainloop()

main()