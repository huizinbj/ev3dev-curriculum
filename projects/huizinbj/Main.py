import tkinter
from  tkinter import ttk


def main():
    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=1, column=2)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    forward_button['command'] = lambda: prints()
    root.bind('<Up>', lambda event: prints())

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    left_button['command'] = lambda: prints()
    root.bind('<Left>', lambda event: prints())

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    stop_button['command'] = lambda: prints()
    root.bind('<space>', lambda event: prints())

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    right_button['command'] = lambda: prints()
    root.bind('<Right>', lambda event: prints())

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    back_button['command'] = lambda: prints()
    root.bind('<Down>', lambda event: prints())

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=6, column=0)
    up_button['command'] = lambda: prints()
    root.bind('<u>', lambda event: prints())

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=7, column=0)
    down_button['command'] = lambda: prints()
    root.bind('<j>', lambda event: prints())

    quit_button = ttk.Button(main_frame, text="Quit")
    quit_button.grid(row=6, column=2)
    quit_button['command'] = (lambda: prints())

    end_button = ttk.Button(main_frame, text="Exit")
    end_button.grid(row=7, column=2)
    end_button['command'] = (lambda: prints())


    root.mainloop()



main()

def prints():
    print("Hi")