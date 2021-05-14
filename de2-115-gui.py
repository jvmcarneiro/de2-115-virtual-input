"""Virtual input for the Altera DE2-115.
Click the buttons to send corresponding input to the FPGA kit.
"""

import tkinter as tk
from tkinter import messagebox
from functools import partial
import signal
import serial                   # type: ignore
import serial.tools.list_ports  # type: ignore
from threading import Timer


def not_idle():
    if timer_idle.isAlive():
        timer_idle.cancel()
        timer_idle.start()

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
        dev_label = port.device + " - " + port.description
        device_menu.insert_command(last_index - 1, label=dev_label,
                                   command=lambda: toggle_connect(dev_label))

    # Let user know that device menu is empty
    if device_menu.type(0) == tk.SEPARATOR:
        device_menu.insert_command(0, label="No device found",
                                   state=tk.DISABLED)


def toggle_connect(dev_label):
    """Attempt to connect to (or disconnect from) device in sub-menu."""
    serial_read = 40   # Beacon from device
    serial_write = 41  # Say hi to device
    serial_ok = 42     # Ok from device
    serial_close = 88  # End connection

    # Close existing connection
    if ser.is_open:
        old_connection = ser.port
        index = device_menu.index(dev_label)
        device_menu.entryconfigure(index, foreground="black",
                                   activeforeground="black",
                                   font=("Helvetica", 10, "normal"))
        display.configure(text="No connection", fg="black")
        ser.write(chr(serial_close).encode())
        ser.close()
        if power_sw.cget("relief") == "sunken":
            power_toggle()
        power_sw.configure(state="disabled")

        # Return if disconnected from last connection
        if old_connection == dev_label.split()[0]:
            return

    # Attempt to connect to device
    ser.port = dev_label.split()[0]
    try:
        ser.open()
        connection = "Connecting to " + dev_label + "..."
        display.configure(text=connection, fg="black")
        serial_received = ser.read(5).decode("ascii","ignore")
        if chr(serial_read) in serial_received:
            ser.write(chr(serial_write).encode())
            serial_received = ser.read(2).decode("ascii","ignore")
            if chr(serial_ok) in serial_received:
                connection = "Connected to " + dev_label
                display.configure(text=connection, fg="green")
                index = device_menu.index(dev_label)
                device_menu.entryconfigure(index, foreground="green",
                                           activeforeground="green",
                                           font=("Helvetica", 10, "bold"))
                power_sw.configure(state="normal")
                return 1
            else:
                raise Exception("Did not receive acknowledgement from device.")
        else:
            raise Exception("Device doesn't seem available.")
    except Exception as error:
        print(error)
        ser.close()
        connection = "Couldn't connect to " + dev_label
        display.configure(text=connection, fg="red")
        if power_sw.cget("relief") == "sunken":
            power_toggle()
        power_sw.configure(state="disabled")


def on_closing(*args):
    """Close connections on program termination."""
    serial_close = 88  # End connection

    if ser.is_open:
        if messagebox.askokcancel("Confirmation", "Exiting will close all connections and turn the FPGA off. Do you still want to quit?"):
            display.configure(text="No connection", fg="black")
            ser.write(chr(serial_close).encode())
            ser.close()
            root.destroy()
        else:
            return
    else:
        root.destroy()


def enable_power():
    """Enable the power switch button."""
    power_sw.configure(state="normal")


def power_toggle():
    """Start timers for powering off auto"""
    if not timer_idle.isAlive():
        timer_idle.start()
    else:
        timer_idle.cancel()
    if not timer_max_on.isAlive():
        timer_max_on.start()
    else:
        timer_idle.cancel()

    """Power board on and off at a minimum interval of 1 minute."""
    serial_write = 90  # Power trigger message
    serial_ok = 91     # Power toggle ok
    serial_fail = 92   # Power toggle failed

    ser.reset_input_buffer()
    ser.write(chr(serial_write).encode())
    serial_received = ser.read(5).decode("ascii","ignore")
    if chr(serial_ok) in serial_received:
        curr_relief = power_sw.cget("relief")
        if curr_relief == "raised":
            power_sw.configure(image=powon_img)
            power_sw.configure(relief="sunken")
            connection = "POW turned ON"
            display.configure(text=connection, fg="black")
            btn0.configure(state="normal")
            btn1.configure(state="normal")
            btn2.configure(state="normal")
            btn3.configure(state="normal")
            for i in range(18):
                sw[i].configure(state="normal")
        else:
            power_sw.configure(image=powoff_img)
            power_sw.configure(relief="raised")
            connection = "POW turned OFF"
            display.configure(text=connection, fg="black")
            btn0.configure(state="disabled")
            btn1.configure(state="disabled")
            btn2.configure(state="disabled")
            btn3.configure(state="disabled")
            for i in range(18):
                sw[i].configure(image=swoff_img)
                sw[i].configure(relief="raised")
                sw[i].configure(state="disabled")
        power_sw.configure(state="disabled")
        root_entry.after(60000, enable_power)
    elif chr(serial_fail) in serial_received:
        connection = "POW not available right now (board cools down for 1 minute)"
        display.configure(text=connection, fg="red")
    else:
        connection = "Input not acknowledged (try reconnecting)"
        display.configure(text=connection, fg="red")


def btn_press(num):
    """Not idle flag"""
    not_idle()
    """Enable current button signal on press."""
    serial_write = 3 - num  # Button trigger message

    ser.reset_input_buffer()
    ser.write(chr(serial_write).encode())
    connection = "KEY["+str(num)+"] pressed"
    display.configure(text=connection, fg="black")


def btn_release(num):
    """Not idle flag"""
    not_idle()
    """Disable current button signal on release."""
    serial_write = 3 - num  # Button trigger message

    ser.reset_input_buffer()
    ser.write(chr(serial_write).encode())
    connection = "KEY["+str(num)+"] released"
    display.configure(text=connection, fg="black")


def sw_toggle(num):
    """Not idle flag"""
    not_idle()
    """Update current switch state and send input to board."""
    serial_write = 21 - num  # Switch trigger message

    ser.reset_input_buffer()
    ser.write(chr(serial_write).encode())
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
timer_idle = Timer(300, power_toggle)
timer_max_on = Timer(600, power_toggle)


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

file_menu.add_separator()
file_menu.add_command(label="Exit", command=on_closing)

device_menu.add_command(label="No device found", state=tk.DISABLED)
device_menu.add_separator()
device_menu.add_command(label="Refresh", command=refresh_devices)


# Create buttons
powoff_img = tk.PhotoImage(file="img/power_off.png")
powon_img = tk.PhotoImage(file="img/power_on.png")
power_sw = tk.Button(buttons, image=powoff_img, text="POW", compound="top",
                     state="disabled", command=power_toggle)
power_sw.pack(side="left")

btn0_img = tk.PhotoImage(file="img/pbutton0_unpressed.png")
btn0 = tk.Button(buttons, image=btn0_img, state="disabled")
btn0.bind("<ButtonPress>", lambda event: btn_press(0))
btn0.bind("<ButtonRelease>", lambda event: btn_release(0))
btn0.pack(side="right", padx=2)

btn1_img = tk.PhotoImage(file="img/pbutton1_unpressed.png")
btn1 = tk.Button(buttons, image=btn1_img, state="disabled")
btn1.bind("<ButtonPress>", lambda event: btn_press(1))
btn1.bind("<ButtonRelease>", lambda event: btn_release(1))
btn1.pack(side="right", padx=2)

btn2_img = tk.PhotoImage(file="img/pbutton2_unpressed.png")
btn2 = tk.Button(buttons, image=btn2_img, state="disabled")
btn2.bind("<ButtonPress>", lambda event: btn_press(2))
btn2.bind("<ButtonRelease>", lambda event: btn_release(2))
btn2.pack(side="right", padx=2)

btn3_img = tk.PhotoImage(file="img/pbutton3_unpressed.png")
btn3 = tk.Button(buttons, image=btn3_img, state="disabled")
btn3.bind("<ButtonPress>", lambda event: btn_press(3))
btn3.bind("<ButtonRelease>", lambda event: btn_release(3))
btn3.pack(side="right", padx=2)

sw_row0 = tk.Frame(switches)
sw_row1 = tk.Frame(switches)
sw_row0.pack()
sw_row1.pack(pady=(5, 0))

swon_img = tk.PhotoImage(file="img/switch_on.png")
swoff_img = tk.PhotoImage(file="img/switch_off.png")

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

signal.signal(signal.SIGINT, on_closing)
signal.signal(signal.SIGTERM, on_closing)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
