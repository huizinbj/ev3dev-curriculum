import tkinter
from tkinter import ttk
from tkinter import *

root = tkinter.Tk()
root.title = "Pixy display"

main_frame = ttk.Frame(root, padding=5)
main_frame.grid()

# The values from the Pixy range from 0 to 319 for the x and 0 to 199 for the y.
canvas = tkinter.Canvas(main_frame, background="lightgray", width=320,
                        height=200)
canvas.grid(columnspan=2)

quit_button = ttk.Button(main_frame, text="Quit")
quit_button.grid(row=3, column=1)
quit_button["command"] = lambda: print("Hi")

mainloop()


