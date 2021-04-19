"""Virtual input for the Altera DE2-115.
Click the buttons to send corresponding input to the FPGA kit.
"""

import tkinter as tk

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
        sw[num]["image"] = swon_img
        sw[num].configure(relief="sunken")
        print("SW["+str(num)+"] turned ON")
        # send switch on signal
    else:
        sw[num].configure(image=swoff_img)
        sw[num].configure(relief="raised")
        print("SW["+str(num)+"] turned OFF")
        # send switch off signal

root = tk.Tk()

display = tk.Label(root, text="DE2-115 VIRTUAL INPUT", fg="black")
display.config(font=("Courier", 20, "bold"))
display.pack(pady=20)


btns = tk.Frame(root)
btns.pack(side="top")

btn3_img = tk.PhotoImage(file="img/pbutton3_unpressed.png")
btn3 = tk.Button(btns, image=btn3_img, command=btn3_press)
btn3.pack(side="left", padx=5)

btn2_img = tk.PhotoImage(file="img/pbutton2_unpressed.png")
btn2 = tk.Button(btns, image=btn2_img, command=btn2_press)
btn2.pack(side="left", padx=5)

btn1_img = tk.PhotoImage(file="img/pbutton1_unpressed.png")
btn1 = tk.Button(btns, image=btn1_img, command=btn1_press)
btn1.pack(side="left", padx=5)

btn0_img = tk.PhotoImage(file="img/pbutton0_unpressed.png")
btn0 = tk.Button(btns, image=btn0_img, command=btn0_press)
btn0.pack(side="left", padx=5)

spacing = tk.Frame(root)
spacing.pack(pady=10)

sw_row0 = tk.Frame(root)
sw_row1 = tk.Frame(root)
sw_row0.pack(padx=10)
sw_row1.pack(padx=10, pady=5)

swon_img = tk.PhotoImage(file="img/switch_on.png")
swoff_img = tk.PhotoImage(file="img/switch_off.png")

sw = [None] * 18
for i in reversed(range(18)):
    if i > 8:
        sw[i] = tk.Button(sw_row0, image=swoff_img, text="["+str(i)+"]", compound="top")
    else:
        sw[i] = tk.Button(sw_row1, image=swoff_img, text="["+str(i)+"]", compound="top")
    sw[i].config(command=lambda arg=i:sw_toggle(arg))
    sw[i].pack(side="left", padx=1)

root.mainloop()
