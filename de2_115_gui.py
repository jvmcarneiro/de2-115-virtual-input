"""Virtual input for the Altera DE2-115.
Click the buttons to send corresponding input to the FPGA kit.
"""

import tkinter as tk
from functools import partial


def enable_power():
    """Simple function handle for enabling the power switch."""
    power_sw.configure(state="normal")


def power_toggle():
    """Powers board on and off in a 20 seconds minimum interval."""
    curr_relief = power_sw.cget("relief")
    if curr_relief == "raised":
        power_sw.configure(image=powon_img)
        power_sw.configure(relief="sunken")
        print("POW turned ON")
        # send switch on signal
    else:
        power_sw.configure(image=powoff_img)
        power_sw.configure(relief="raised")
        print("POW turned OFF")
        # send switch off signal
    power_sw.configure(state="disabled")
    root_entry.after(20000, enable_power)


def btn_press(num):
    """Enable current button signal on press."""
    print("KEY["+str(num)+"] pressed")
    # send button 3 press signal


def btn_release(num):
    """Disable current button signal on release."""
    print("KEY["+str(num)+"] released")
    # send button 3 press signal


def sw_toggle(num):
    """Update current switch state and send input to board."""
    curr_relief = sw[num]["relief"]
    if curr_relief == "raised":
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
root.rowconfigure(0, weight=1)
root.rowconfigure(4, weight=1)
root.columnconfigure(0, weight=1, uniform="margin")
root.columnconfigure(2, weight=1, uniform="margin")
root_entry = tk.Entry(root)

display = tk.Label(root, text="DE2-115 VIRTUAL INPUT", fg="black",
                   font=("Courier", 20, "bold"))
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

root.mainloop()
