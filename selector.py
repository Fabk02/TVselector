import pygame
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

def launch_steam():
    os.system(' "C:\Program Files (x86)\Steam\Steam.exe" ')
    root.destroy()

def launch_emulator():
    print("Emulator")

def launch_kodi():
    os.system('start shell:AppsFolder\XBMCFoundation.Kodi_4n2hpmxwrvr6p!Kodi')
    root.destroy()

def launch_desktop():
    root.destroy()

cont = 0

def increase_counter(max_value):
    global cont
    if cont < max_value-1 :
        cont += 1

def decrease_counter(min_value):
    global cont
    if cont > min_value:
        cont -= 1

def increase_focus(event, buttons, max_value):
    global cont
    increase_counter(max_value)
    buttons[cont].focus()

def decrease_focus(event, buttons, min_value):
    global cont
    decrease_counter(min_value)
    buttons[cont].focus()

def printcont():
    global cont
    print(cont)
    root.after(50, lambda: printcont())

def update_focus(buttons):
    global cont
    buttons[cont].focus()
    root.after(50, lambda:update_focus(buttons))

def tk_exec_focus(event, buttons):
    global cont
    buttons[cont].invoke()


#######################################################################################

pygame.init()   
pygame.joystick.init()

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

def initialize_axis():
    pygame.event.pump()
    ax_0 = joystick.get_axis(0)
    return ax_0

def initialize_hat():
    pygame.event.pump()
    hat_0 = joystick.get_hat(0)
    return hat_0

def initialize_buttons():
    pygame.event.pump()
    left = joystick.get_button(4)
    right = joystick.get_button(5)
    return (left, right)

def initialize_ok_button():
    pygame.event.pump()
    ok_button = joystick.get_button(0)
    return ok_button

def update(min_value, max_value):
    global cont
    axis = initialize_axis()
    hat = initialize_hat()
    left_button, right_button = initialize_buttons() 

    if (axis > 0 or hat[0] > 0 or right_button) :
        increase_counter(max_value)
    elif (axis < 0 or hat[0] < 0 or left_button):
        decrease_counter(min_value)

    root.after(125, lambda: update(min_value, max_value))

def exec_focus(buttons):
    global cont
    ok_button = initialize_ok_button()

    if ok_button:
        buttons[cont].invoke()

    root.after(125, lambda: exec_focus(buttons))

#######################################################################################

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

###################################################################
buttons[cont].focus()
root.bind("<Right>", lambda event: increase_focus(event, buttons, n_buttons))
root.bind("<Left>", lambda event: decrease_focus(event, buttons, 0))
root.bind("<Return>", lambda event: tk_exec_focus(event, buttons))

update(0, n_buttons)
update_focus(buttons)
exec_focus(buttons)
root.mainloop()
pygame.quit()

