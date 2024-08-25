import pygame
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

cont = 0
joystick_counter = 0
joystick = 0

#COUNTER FUNCTIONS

def increase_counter(max_value):
    global cont
    if cont < max_value-1 :
        cont += 1

def decrease_counter(min_value):
    global cont
    if cont > min_value:
        cont -= 1

#PYGAME FUNCTIONS

def check_joystick(frame):
    global joystick
    global joystick_counter

    pygame.joystick.quit()
    pygame.joystick.init()

    joystick_counter = pygame.joystick.get_count()
    if joystick_counter > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

    frame.after(50, lambda: check_joystick(frame))

def joystick_loop(buttons, min_value, max_value):
    global cont
    global joystick
    pygame.event.pump()

    buttons[cont].focus()

    left_axis = joystick.get_axis(0)
    hat = joystick.get_hat(0)
    left_button = joystick.get_button(4)
    right_button = joystick.get_button(5)
    ok_button = joystick.get_button(0)


    if (left_axis > 0 or hat[0] > 0 or right_button) :
        increase_counter(max_value)
    elif (left_axis < 0 or hat[0] < 0 or left_button):
        decrease_counter(min_value)

    if ok_button:
        buttons[cont].invoke()

def loop_if_joystick_connected(frame, buttons, min_value, max_value):
    global joystick_counter
    if (joystick_counter > 0) and (frame.focus_displayof() != None):
        joystick_loop(buttons, min_value, max_value)

    frame.after(125, lambda: loop_if_joystick_connected(frame, buttons, min_value, max_value))

#LAUNCH_FUNCTIONS

def launch_steam():
    os.system(' "C:\Program Files (x86)\Steam\Steam.exe" ')

def launch_emulator():
    print("Emulator")

def launch_kodi():
    os.system('start shell:AppsFolder\XBMCFoundation.Kodi_4n2hpmxwrvr6p!Kodi')

def launch_desktop():
    root.destroy()

#TKINTER_FUNCTIONS

def tk_increase_focus(event, buttons, max_value):
    global cont
    increase_counter(max_value)
    buttons[cont].focus()

def tk_decrease_focus(event, buttons, min_value):
    global cont
    decrease_counter(min_value)
    buttons[cont].focus()

def tk_exec_focus(event, buttons):
    global cont
    buttons[cont].invoke()

#MAIN PROGRAM

pygame.init()   
pygame.joystick.init()

root = tk.Tk()
root.title("Selector")
root.attributes('-fullscreen', True)

screen_width = root.winfo_screenwidth()
padding = 10

frame =  ttk.Frame(root)
frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
frame.pack(expand=True, padx=padding)

n_buttons = 4
buttons = [None] * n_buttons

path = "./icons/"
og_icons = [path+"steam.png", path+"retroarch.png", path+"kodi.png", path+"windows.png"]
icons = []
int_ratio = int(screen_width/n_buttons) - padding*(n_buttons)
for icon in og_icons:
    image = Image.open(icon)
    resize_image = image.resize((int_ratio, int_ratio))
    icons.append(ImageTk.PhotoImage(resize_image))

#STEAM BUTTON
buttons[0] = ttk.Button(frame, text="steam", image= icons[0],command=launch_steam)
buttons[0].grid(row=0, column=0, sticky=(tk.E,tk.W))


#EMULATOR BUTTON
buttons[1] = ttk.Button(frame, text="emulator", image= icons[1], command=launch_emulator)
buttons[1].grid(row=0, column=1, sticky=(tk.E,tk.W))

#KODI BUTTON
buttons[2] = ttk.Button(frame, text="kodi", image= icons[2], command=launch_kodi)
buttons[2].grid(row=0, column=2, sticky=(tk.E,tk.W))

#DESKTOP BUTTON 
buttons[3] = ttk.Button(frame, text="desktop", image= icons[3], command=launch_desktop)
buttons[3].grid(row=0, column=3, sticky=(tk.E,tk.W))

for child in frame.winfo_children():
    child.grid(padx=padding)

check_joystick(root)
loop_if_joystick_connected(root, buttons, 0, n_buttons)

root.bind("<Right>", lambda event: tk_increase_focus(event, buttons, n_buttons))
root.bind("<Left>", lambda event: tk_decrease_focus(event, buttons, 0))
root.bind("<Return>", lambda event: tk_exec_focus(event, buttons))

root.mainloop()
pygame.quit()