"""Virtual input for the Altera DE2-115.
Click the buttons to send corresponding input via serial to the FPGA kit.

Message translation table **
Read:
  40 - "Is there a GUI out there?"
  42 - "Ok GUI, got you."
  50 - "I'm already paired."
  91 - "Power toggle succeeded."
  92 - "Power toggle failed."
Write:
  41 - "Hi Device, GUI here."
  88 - "End connection."
  90 - "Power the board on and off."
  00 - "Button 3 changed state."
  01 - "Button 2 changed state."
  02 - "Button 1 changed state."
  03 - "Button 0 changed state."
  04 - "Switch 17 changed state."
  05 - "Switch 16 changed state."
  06 - "Switch 15 changed state."
  07 - "Switch 14 changed state."
  08 - "Switch 13 changed state."
  09 - "Switch 12 changed state."
  10 - "Switch 11 changed state."
  11 - "Switch 10 changed state."
  12 - "Switch 09 changed state."
  13 - "Switch 08 changed state."
  14 - "Switch 07 changed state."
  15 - "Switch 06 changed state."
  16 - "Switch 05 changed state."
  17 - "Switch 04 changed state."
  18 - "Switch 03 changed state."
  19 - "Switch 02 changed state."
  20 - "Switch 01 changed state."
  21 - "Switch 00 changed state."
"""

import tkinter as tk
from tkinter import messagebox
from threading import Timer
from functools import partial
import serial                   # type: ignore
import serial.tools.list_ports  # type: ignore
import threading
import signal
import subprocess
import sys
import os


def resource_path(relative_path):
    """Import data files from internal package data."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def ser_exchange(ser, message, *args):
    """Exchange serial information with device."""
    ser.reset_input_buffer()
    if message != 999:  # flag for just read
        ser.write(chr(message).encode())

    if message == 999:  # look for device beacon
        reply = ser.read(5).decode("ascii","ignore")
        try:
            if chr(40) in reply:  # device available
                thread_connect = threading.Thread(target=ser_exchange, args=(ser, 41, args[0]), daemon=True)
                thread_connect.start()
            else:
                raise Exception("Device doesn't seem available.")
        except Exception as error:
            if timer_idle.is_alive():
                timer_idle.cancel()
            print(error)
            ser.close()
            connection = "Couldn't connect to " + args[0]
            display.configure(text=connection, fg="red")
            if power_sw.cget("relief") == "sunken":
                power_toggle()
            power_sw.configure(state="disabled")

    elif message == 41:   # send connection request 
        reply = ser.read(3).decode("ascii","ignore")
        try:
            if chr(42) in reply:  # if connection is confirmed
                create_timer_idle()
                timer_idle.start()
                connection = "Connected to " + args[0]
                display.configure(text=connection, fg="green")
                index = device_menu.index(args[0])
                device_menu.entryconfigure(index, foreground="green",
                                           activeforeground="green",
                                           font=("Helvetica", 10, "bold"))
                power_sw.configure(state="normal")
            else:
                raise Exception("Did not receive acknowledgement from device.")
        except Exception as error:
            if timer_idle.is_alive():
                timer_idle.cancel()
            print(error)
            ser.close()
            connection = "Couldn't connect to " + args[0]
            display.configure(text=connection, fg="red")
            if power_sw.cget("relief") == "sunken":
                power_toggle()
            power_sw.configure(state="disabled")

    elif message == 90:   # toggle power state
        reply = ser.read(3).decode("ascii","ignore")
        if chr(91) in reply:  # success
            curr_relief = power_sw.cget("relief")
            if curr_relief == "raised":
                power_sw.configure(image=powon_img)
                power_sw.configure(relief="sunken")
                connection = "POW turned ON"
                display.configure(text=connection, fg="black")
                reset_sw.configure(state="normal")
                btn0.configure(state="normal")
                btn1.configure(state="normal")
                btn2.configure(state="normal")
                btn3.configure(state="normal")
                for i in range(18):
                    sw[i].configure(state="normal")
                restart_jtagd()
            else:
                power_sw.configure(image=powoff_img)
                power_sw.configure(relief="raised")
                connection = "POW turned OFF"
                display.configure(text=connection, fg="black")
                reset_sw.configure(image=resetoff_img)
                reset_sw.configure(relief="raised")
                reset_sw.configure(state="disabled")
                btn0.configure(state="disabled")
                btn1.configure(state="disabled")
                btn2.configure(state="disabled")
                btn3.configure(state="disabled")
                for i in range(18):
                    sw[i].configure(image=swoff_img)
                    sw[i].configure(relief="raised")
                    sw[i].configure(state="disabled")
            power_sw.configure(state="disabled")
            root_entry.after(20000, enable_power)
        elif chr(92) in reply:  # fail
            connection = "POW not available right now, try again in a minute"
            display.configure(text=connection, fg="red")
        else:
            connection = "Input not acknowledged, try reconnecting"
            display.configure(text=connection, fg="red")

    sys.exit()


def restart_jtagd():
    """Restart the JTAG service."""
    subprocess.run(["killall", "jtagd"])
    subprocess.Popen(["/opt/intelFPGA/20.1/quartus/bin/jtagd"], shell=True)


def launch_quartus():
    """Open a Quartus instance."""
    subprocess.Popen(["/opt/intelFPGA/20.1/quartus/bin/quartus"])


def launch_camera():
    """Open a Cheese instance."""
    subprocess.Popen(["/usr/bin/cheese"])


def create_timer_idle():
    """Reset idle timer."""
    global timer_idle
    timer_idle = Timer(590, timer_timeout)
    timer_idle.daemon = True


def create_timer_max_on():
    """Reset idle timer."""
    global timer_max_on
    timer_max_on = Timer(595, timer_timeout)
    timer_max_on.daemon = True


def refresh_devices():
    """Refresh list of available serial devices."""
    display.configure(text="No connection", fg="black")
    ports = list(serial.tools.list_ports.comports())
    last_index = device_menu.index(tk.END) - 1
    dev_to_pop = []
    port_to_pop = []

    # Check if devices in menu are also in ports list
    for index in range(0, last_index):
        dev_label = device_menu.entrycget(index, 'label')
        for port in ports:
            dev_split = dev_label.split()
            if port.device == dev_split[0]:
                if port.description == dev_split[2]:
                    port_to_pop.append(port)
            else:
                dev_to_pop.append(dev_label)

    # Remove not found devices from menu
    for dev in dev_to_pop:
        index = device_menu.index(dev)
        device_menu.delete(index)

    # Remove repeat devices from ports list
    for port in port_to_pop:
        index = ports.index(port)
        ports.pop(index)

    # Add new ports to device menu
    for port in ports:
        dev_label = port.device + " - " + str(port.description)
        device_menu.insert_command(last_index - 1, label=dev_label,
                                   command=lambda: toggle_connect(dev_label))

    # Let user know that device menu is empty
    if device_menu.type(0) == tk.SEPARATOR:
        device_menu.insert_command(0, label="No device found",
                                   state=tk.DISABLED)


def toggle_connect(dev_label):
    """Attempt to connect to (or disconnect from) device in sub-menu."""
    # Close existing connection
    if ser.is_open:
        if timer_max_on.is_alive():
            timer_max_on.cancel()
        timer_idle.cancel()
        power_sw.configure(image=powoff_img)
        power_sw.configure(relief="raised")
        power_sw.configure(state="disabled")
        connection = "POW turned OFF"
        display.configure(text=connection, fg="black")
        reset_sw.configure(image=resetoff_img)
        reset_sw.configure(relief="raised")
        reset_sw.configure(state="disabled")
        btn0.configure(state="disabled")
        btn1.configure(state="disabled")
        btn2.configure(state="disabled")
        btn3.configure(state="disabled")
        for i in range(18):
            sw[i].configure(image=swoff_img)
            sw[i].configure(relief="raised")
            sw[i].configure(state="disabled")
        old_connection = ser.port
        index = device_menu.index(tk.END) - 2
        while index >= 0:
            if dev_label in device_menu.entrycget(index, 'label'):
                break
            else:
                index -= 1
        device_menu.entryconfigure(index, foreground="black",
                                   activeforeground="black",
                                   font=("Helvetica", 10, "normal"))
        display.configure(text="No connection", fg="black")
        ser.write(chr(88).encode())
        ser.close()
        # Return if disconnected from last connection
        if old_connection == dev_label.split()[0]:
            return

    # Attempt to connect to device
    ser.port = dev_label.split()[0]
    try:
        ser.open()
        thread_beacon = threading.Thread(target=ser_exchange, args=(ser, 999, dev_label), daemon=True)
        thread_beacon.start()
        connection = "Connecting to " + dev_label + "..."
        display.configure(text=connection, fg="black")
    except Exception as error:
        if timer_idle.is_alive():
            timer_idle.cancel()
        print(error)
        ser.close()
        connection = "Couldn't connect to " + dev_label
        display.configure(text=connection, fg="red")
        if power_sw.cget("relief") == "sunken":
            power_toggle()
        power_sw.configure(state="disabled")


def on_close(*args):
    """Close connections on program termination."""
    if ser.is_open:
        if messagebox.askokcancel("Confirmation", "Exiting will close all connections and turn the FPGA off. Do you still want to quit?"):
            display.configure(text="No connection", fg="black")
            ser.write(chr(88).encode())
            ser.close()
            root.destroy()
        else:
            return
    else:
        root.destroy()


def timer_timeout():
    """Disconnect board after timer time out."""
    if timer_idle.is_alive():
        timer_idle.cancel()
    if timer_max_on.is_alive():
        timer_max_on.cancel()
    toggle_connect(ser.name)
    connection = "Session timed out"
    display.configure(text=connection, fg="red")


def enable_power():
    """Enable the power switch button."""
    if ser.is_open:
        power_sw.configure(state="normal")


def power_toggle():
    """Power board on and off at a minimum interval of 1 minute."""
    if power_sw.cget("state") == "disabled":
        return
    if not timer_max_on.is_alive():
        connection = "Powering on..."
        display.configure(text=connection, fg="black")
        create_timer_max_on()
        timer_max_on.start()
    else:
        connection = "Powering off..."
        display.configure(text=connection, fg="black")
        timer_max_on.cancel()
    if timer_idle.is_alive():
        timer_idle.cancel()
        create_timer_idle()
        timer_idle.start()
    thread_power = threading.Thread(target=ser_exchange, args=(ser, 90), daemon=True)
    thread_power.start()

def reset_toggle():
    """Reset button trigger for the fpga board state."""
    if reset_sw.cget("state") == "disabled":
        return
    serial_message = 127  # Reset trigger message
    if timer_idle.is_alive():
        timer_idle.cancel()
        create_timer_idle()
        timer_idle.start()
    curr_relief = reset_sw["relief"]
    if curr_relief == "raised":
        thread_sw = threading.Thread(target=ser_exchange, args=(ser, serial_message), daemon=True)
        thread_sw.start()
        reset_sw.configure(image=reseton_img)
        reset_sw.configure(relief="sunken")
        for i in range(18):
            sw[i].configure(image=swoff_img)
            sw[i].configure(relief="raised")
        connection = "RESET turned ON"
        display.configure(text=connection, fg="black")
    else:
        reset_sw.configure(image=resetoff_img)
        reset_sw.configure(relief="raised")
        connection = "RESET turned OFF"
        display.configure(text=connection, fg="black")

def btn_press(num):
    """Enable current button signal on press."""
    if btn0.cget("state") == "disabled":
        return
    serial_message = 3 - num  # Button trigger message
    if timer_idle.is_alive():
        timer_idle.cancel()
        create_timer_idle()
        timer_idle.start()
    thread_btn_press = threading.Thread(target=ser_exchange, args=(ser, serial_message), daemon=True)
    thread_btn_press.start()
    connection = "KEY["+str(num)+"] pressed"
    display.configure(text=connection, fg="black")


def btn_release(num):
    """Disable current button signal on release."""
    if btn0.cget("state") == "disabled":
        return
    serial_message = 3 - num  # Button trigger message
    if timer_idle.is_alive():
        timer_idle.cancel()
        create_timer_idle()
        timer_idle.start()
    thread_btn_release = threading.Thread(target=ser_exchange, args=(ser, serial_message), daemon=True)
    thread_btn_release.start()
    connection = "KEY["+str(num)+"] released"
    display.configure(text=connection, fg="black")


def sw_toggle(num):
    """Update current switch state and send input to board."""
    if sw[num].cget("state") == "disabled":
        return
    serial_message = 21 - num  # Switch trigger message
    if timer_idle.is_alive():
        timer_idle.cancel()
        create_timer_idle()
        timer_idle.start()
    thread_sw = threading.Thread(target=ser_exchange, args=(ser, serial_message), daemon=True)
    thread_sw.start()
    curr_relief = sw[num]["relief"]
    if curr_relief == "raised":
        sw[num].configure(image=swon_img)
        sw[num].configure(relief="sunken")
        connection = "SW["+str(num)+"] turned ON"
        display.configure(text=connection, fg="black")
    else:
        sw[num].configure(image=swoff_img)
        sw[num].configure(relief="raised")
        connection = "SW["+str(num)+"] turned OFF"
        display.configure(text=connection, fg="black")


# Initial config
ser = serial.Serial(timeout=3)
create_timer_idle()
create_timer_max_on()
timer_idle.cancel()
timer_max_on.cancel()


# Set up grid with resizeable margins and maintain buttons' position
root = tk.Tk()
root.rowconfigure(0, weight=1)
root.rowconfigure(4, weight=1)
root.columnconfigure(0, weight=1, uniform="margin")
root.columnconfigure(2, weight=1, uniform="margin")
root_entry = tk.Entry(root)

display = tk.Label(root, text="Not connected", fg="black",
                   font=("Helvetica", 12, "bold"))
buttons = tk.Frame(root)
switches = tk.Frame(root)
top_margin = tk.Frame(root)
bottom_margin = tk.Frame(root)
left_margin = tk.Frame(root)
right_margin = tk.Frame(root)

display.grid(row=1, column=1, sticky="ew")
buttons.grid(row=2, column=1, pady=20, sticky="ew")
switches.grid(row=3, column=1, sticky="ew")
top_margin.grid(row=0, column=0, columnspan=3, ipady=10, sticky="nsew")
bottom_margin.grid(row=4, column=0, columnspan=3, ipady=10, sticky="nsew")
left_margin.grid(row=0, column=0, rowspan=5, ipadx=10, sticky="nsew")
right_margin.grid(row=0, column=2, rowspan=5, ipadx=10, sticky="nsew")


# Create menus
menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=0)
device_menu = tk.Menu(file_menu, tearoff=0)

menubar.add_cascade(label="File", menu=file_menu)
menubar.add_cascade(label="Devices", menu=device_menu)

file_menu.add_command(label="Open Quartus", command=launch_quartus)
file_menu.add_command(label="Open Camera", command=launch_camera)
file_menu.add_command(label="Restart JTAG", command=restart_jtagd)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=on_close)

device_menu.add_command(label="No device found", state=tk.DISABLED)
device_menu.add_separator()
device_menu.add_command(label="Refresh", command=refresh_devices)


# Create buttons
powoff_img = tk.PhotoImage(file=resource_path("img/power_off.png"))
powon_img = tk.PhotoImage(file=resource_path("img/power_on.png"))
power_sw = tk.Button(buttons, image=powoff_img, text="POW", compound="top",
                     state="disabled", command=power_toggle)
power_sw.pack(side="left")

resetoff_img = tk.PhotoImage(file=resource_path("img/switch_off.png"))
reseton_img = tk.PhotoImage(file=resource_path("img/switch_on.png"))
reset_sw = tk.Button(buttons, image=resetoff_img, text="RESET", compound="top",
                     state="disabled", command=reset_toggle)
reset_sw.pack(side="left", padx=10)

btn0_img = tk.PhotoImage(file=resource_path("img/pbutton0_unpressed.png"))
btn0 = tk.Button(buttons, image=btn0_img, state="disabled")
btn0.bind("<ButtonPress>", lambda event: btn_press(0))
btn0.bind("<ButtonRelease>", lambda event: btn_release(0))
btn0.pack(side="right", padx=2)

btn1_img = tk.PhotoImage(file=resource_path("img/pbutton1_unpressed.png"))
btn1 = tk.Button(buttons, image=btn1_img, state="disabled")
btn1.bind("<ButtonPress>", lambda event: btn_press(1))
btn1.bind("<ButtonRelease>", lambda event: btn_release(1))
btn1.pack(side="right", padx=2)

btn2_img = tk.PhotoImage(file=resource_path("img/pbutton2_unpressed.png"))
btn2 = tk.Button(buttons, image=btn2_img, state="disabled")
btn2.bind("<ButtonPress>", lambda event: btn_press(2))
btn2.bind("<ButtonRelease>", lambda event: btn_release(2))
btn2.pack(side="right", padx=2)

btn3_img = tk.PhotoImage(file=resource_path("img/pbutton3_unpressed.png"))
btn3 = tk.Button(buttons, image=btn3_img, state="disabled")
btn3.bind("<ButtonPress>", lambda event: btn_press(3))
btn3.bind("<ButtonRelease>", lambda event: btn_release(3))
btn3.pack(side="right", padx=2)

sw_row0 = tk.Frame(switches)
sw_row1 = tk.Frame(switches)
sw_row0.pack()
sw_row1.pack(pady=(5, 0))

swon_img = tk.PhotoImage(file=resource_path("img/switch_on.png"))
swoff_img = tk.PhotoImage(file=resource_path("img/switch_off.png"))

sw = [tk.Button()] * 18
for i in reversed(range(18)):
    if i > 8:
        sw[i] = tk.Button(sw_row0, image=swoff_img, state="disabled",
                          text="["+str(i).zfill(2)+"]", compound="top")
    else:
        sw[i] = tk.Button(sw_row1, image=swoff_img, state="disabled",
                          text="["+str(i).zfill(2)+"]", compound="top")
    sw[i].config(command=partial(sw_toggle, i))
    sw[i].pack(side="left", padx=1)

root.configure(menu=menubar)
root.title("DE2-115 Virtual Input")
refresh_devices()

signal.signal(signal.SIGINT, on_close)
signal.signal(signal.SIGTERM, on_close)
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
