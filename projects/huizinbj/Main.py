import tkinter
from tkinter import ttk


def main():

    # Creates The G.U.I.
    root = tkinter.Tk() # Create instance
    root.title("Mqtt Remote")  # Add a title
    tab_control = ttk.Notebook(root)  # Create Tab Control

    # Creates Tab One
    tab1 = ttk.Frame(tab_control)  # Create a tab
    tab_control.add(tab1, text='Remote')  # Add the tab
    tab_control.pack(expand=1, fill="both")  # Pack to make visible

    # Creates Tab Two
    tab2 = ttk.Frame(tab_control)  # Create a tab
    tab_control.add(tab2, text='Arm Control')  # Add the tab
    tab_control.pack(expand=2, fill="both")  # Pack to make visible

    # Creates Tab Three
    tab3 = ttk.Frame(tab_control)  # Create a tab
    tab_control.add(tab3, text='Program')  # Add the tab
    tab_control.pack(expand=2, fill="both")  # Pack to make visible

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

def prints():
    print("Hi")

main()