# de2-115-virtual-input

Virtual GUI for controlling the Altera DE2-115 board.

![Interface exemplo](screenshots/on.jpg?raw=true "Interface exemplo.")

The program will generate signals for serial communication.

Also included in the repository files are implementations of an input signal
multiplexer via Arduino Uno and a Verilog sample module using the board's
14-pin connector.

## Prerequisites

- python 3

## Running

```bash
python3 de2_115_gui.py
```

Note: the `python3` command may be named just `python` in your environment.


## Setting default serial port and camera
To list only one specific device, change the constant `DEFAULT_DEVICE` to the name of the port in `"/dev/ttyXXXX"` format. Determine `XXXX` by running `dmesg | grep tty`.

To determine a default camera device modify the `launch_camera()` function to launch `guvcview -d /dev/videoX`. Determine `X` by running `v4ls-ctl --list-devices`. 


## Compiling
```bash
python3 -m PyInstaller --onefile --add-data "img/:img/" de2-115-gui.py
```


## Milestones

- [x] Button and switch GUI
- [x] Basic button press functions
- [x] Power switch with a 30 second press interval
- [x] Press and release bindings for the push buttons
- [x] Event receiver on the FPGA
- [x] Encode signal events on Arduino
- [x] Connect GUI to Arduino
- [x] Timer for turning off and cooling FPGA
