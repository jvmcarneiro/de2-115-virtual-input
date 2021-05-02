"""Virtual input for the Altera DE2-115.
Click the buttons to send corresponding input to the FPGA kit.
"""

import tkinter as tk
from functools import partial


def power_toggle():
    """Powers board on and off in a 20 seconds minimum interval."""
    state = power_sw.cget("relief")
    if state == "raised":
        power_sw.configure(image=powon_img)
        power_sw.configure(relief="sunken")
        print("POW turned ON")
        # send switch on signal
    else:
        power_sw.configure(image=powoff_img)
        power_sw.configure(relief="raised")
        print("POW turned OFF")
        # send switch off signal


def btn3_press():
    """Send button 3 input after release."""
    print("KEY[3] pressed")
    # send button 3 press signal


def btn2_press():
    """Send button 2 input after release."""
    print("KEY[2] pressed")
    # send button 2 press signal


def btn1_press():
    """Send button 1 input after release."""
    print("KEY[1] pressed")
    # send button 1 press signal


def btn0_press():
    """Send button 0 input after release."""
    print("KEY[0] pressed")
    # send button 0 press signal


def sw_toggle(num):
    """Update current switch state and send input to board."""
    state = sw[num]["relief"]
    if state == "raised":
        sw[num].configure(image=swon_img)
        sw[num].configure(relief="sunken")
        print("SW["+str(num)+"] turned ON")
        # send switch on signal
    else:
        sw[num].configure(image=swoff_img)
        sw[num].configure(relief="raised")
        print("SW["+str(num)+"] turned OFF")
        # send switch off signal


root = tk.Tk()
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1, uniform="sides")
root.columnconfigure(1, weight=2)
root.columnconfigure(2, weight=1, uniform="sides")
root.minsize(542, 369)


display = tk.Label(root, text="DE2-115 VIRTUAL INPUT", fg="black",
                   font=("Courier", 20, "bold"))
power = tk.Frame(root)
buttons = tk.Frame(root)
switches = tk.Frame(root)


display.grid(row=0, column=0, columnspan=3, pady=10)
power.grid(row=1, column=0, pady=10)
buttons.grid(row=1, column=1)
switches.grid(row=2, column=0, columnspan=3, pady=10)


powoff_img = tk.PhotoImage(file="img/power_off.png")
powon_img = tk.PhotoImage(file="img/power_on.png")
power_sw = tk.Button(power, image=powoff_img, text="POW", compound="top",
                     command=power_toggle)
power_sw.grid()


btn3_img = tk.PhotoImage(file="img/pbutton3_unpressed.png")
btn3 = tk.Button(buttons, image=btn3_img, command=btn3_press)
btn3.grid(row=0, column=0, padx=5)

btn2_img = tk.PhotoImage(file="img/pbutton2_unpressed.png")
btn2 = tk.Button(buttons, image=btn2_img, command=btn2_press)
btn2.grid(row=0, column=1, padx=5)

btn1_img = tk.PhotoImage(file="img/pbutton1_unpressed.png")
btn1 = tk.Button(buttons, image=btn1_img, command=btn1_press)
btn1.grid(row=0, column=2, padx=5)

btn0_img = tk.PhotoImage(file="img/pbutton0_unpressed.png")
btn0 = tk.Button(buttons, image=btn0_img, command=btn0_press)
btn0.grid(row=0, column=3, padx=5)


sw_row0 = tk.Frame(switches)
sw_row1 = tk.Frame(switches)
sw_row0.pack(padx=10)
sw_row1.pack(padx=10, pady=5)

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

root.mainloop()
