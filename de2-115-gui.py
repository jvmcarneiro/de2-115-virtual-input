"""Virtual input for the Altera DE2-115.
Click the buttons to send corresponding input to the FPGA kit.
"""

import tkinter as tk
from functools import partial
import serial                   # type: ignore
import serial.tools.list_ports  # type: ignore


def refresh_devices():
    """Refresh list of available serial devices."""
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
    serial_read = 40   # Beacon from arduino
    serial_write = 41  # Say hi to arduino
    serial_ok = 42     # Ok from arduino

    # Close existing connection
    if ser.is_open:
        old_connection = ser.port
        index = device_menu.index(dev_label)
        device_menu.entryconfigure(index, foreground="black",
                                   activeforeground="black",
                                   font=("Helvetica", 10, "normal"))
        display.configure(text="No connection", fg="black")
        # TODO: send reset signal
        ser.close()

        # Return if disconnected from last connection
        if old_connection == dev_label.split()[0]:
            return

    # Attempt to connect to device
    ser.port = dev_label.split()[0]
    ser.open()
    if ser.is_open:
        connection = "Connecting to " + dev_label + "..."
        display.configure(text=connection, fg="black")
        serial_received = ser.read(10)
        if serial_read in serial_received:
            ser.write(serial_write)
            serial_received = ser.read(10)
            if serial_ok in serial_received:
                connection = "Connected to " + dev_label
                display.configure(text=connection, fg="green")
                index = device_menu.index(dev_label)
                device_menu.entryconfigure(index, foreground="green",
                                           activeforeground="green",
                                           font=("Helvetica", 10, "bold"))
                return
    ser.close()
    connection = "Couldn't connect to " + dev_label
    display.configure(text=connection, fg="black")


def enable_power():
    """Enable the power switch button."""
    power_sw.configure(state="normal")


def power_toggle():
    """Powers board on and off in a 20 seconds minimum interval."""
    curr_relief = power_sw.cget("relief")
    if curr_relief == "raised":
        power_sw.configure(image=powon_img)
        power_sw.configure(relief="sunken")
        print("POW turned ON")
        # TODO: send switch on signal
    else:
        power_sw.configure(image=powoff_img)
        power_sw.configure(relief="raised")
        print("POW turned OFF")
        # TODO: send switch off signal
    power_sw.configure(state="disabled")
    root_entry.after(20000, enable_power)


def btn_press(num):
    """Enable current button signal on press."""
    print("KEY["+str(num)+"] pressed")
    # TODO: send button 3 press signal


def btn_release(num):
    """Disable current button signal on release."""
    print("KEY["+str(num)+"] released")
    # TODO: send button 3 press signal


def sw_toggle(num):
    """Update current switch state and send input to board."""
    curr_relief = sw[num]["relief"]
    if curr_relief == "raised":
        sw[num].configure(image=swon_img)
        sw[num].configure(relief="sunken")
        print("SW["+str(num)+"] turned ON")
        # TODO: send switch on signal
    else:
        sw[num].configure(image=swoff_img)
        sw[num].configure(relief="raised")
        print("SW["+str(num)+"] turned OFF")
        # TODO: send switch off signal


# Variables
ser = serial.Serial(timeout=3)

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
file_menu.add_command(label="Exit", command=root.destroy)

device_menu.add_command(label="No device found", state=tk.DISABLED)
device_menu.add_separator()
device_menu.add_command(label="Refresh", command=refresh_devices)


# Create buttons
powoff_img = tk.PhotoImage(file="img/power_off.png")
powon_img = tk.PhotoImage(file="img/power_on.png")
power_sw = tk.Button(buttons, image=powoff_img, text="POW", compound="top",
                     command=power_toggle)
power_sw.pack(side="left")

btn0_img = tk.PhotoImage(file="img/pbutton0_unpressed.png")
btn0 = tk.Button(buttons, image=btn0_img)
btn0.bind("<ButtonPress>", lambda event: btn_press(0))
btn0.bind("<ButtonRelease>", lambda event: btn_release(0))
btn0.pack(side="right", padx=2)

btn1_img = tk.PhotoImage(file="img/pbutton1_unpressed.png")
btn1 = tk.Button(buttons, image=btn1_img)
btn1.bind("<ButtonPress>", lambda event: btn_press(1))
btn1.bind("<ButtonRelease>", lambda event: btn_release(1))
btn1.pack(side="right", padx=2)

btn2_img = tk.PhotoImage(file="img/pbutton2_unpressed.png")
btn2 = tk.Button(buttons, image=btn2_img)
btn2.bind("<ButtonPress>", lambda event: btn_press(2))
btn2.bind("<ButtonRelease>", lambda event: btn_release(2))
btn2.pack(side="right", padx=2)

btn3_img = tk.PhotoImage(file="img/pbutton3_unpressed.png")
btn3 = tk.Button(buttons, image=btn3_img)
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
        sw[i] = tk.Button(sw_row0, image=swoff_img,
                          text="["+str(i).zfill(2)+"]", compound="top")
    else:
        sw[i] = tk.Button(sw_row1, image=swoff_img,
                          text="["+str(i).zfill(2)+"]", compound="top")
    sw[i].config(command=partial(sw_toggle, i))
    sw[i].pack(side="left", padx=1)

root.configure(menu=menubar)
root.title("DE2-115 Virtual Input")
refresh_devices()
root.mainloop()
