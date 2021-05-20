# de2-115-virtual-input

Virtual GUI for controlling the Altera DE2-115 board.

The program will generate signals for communication via serial.

Also included in the repository files are implementations of an input signal
multiplexer via Arduino Uno and a Verilog module using the board's 14-pin
connector.

## Prerequisites

- python 3

## Running

```bash
python3 de2_115_gui.py
```

The `python3` command may called `python` on your environment.

## Milestones

- [x] Button and switch GUI
- [x] Basic button press functions
- [x] Power switch with a 30 second press interval
- [x] Press and release bindings for the push buttons
- [x] Event receiver on the FPGA
- [x] Encode signal events on Arduino
- [x] Connect GUI to Arduino
- [x] Timer for turning off and cooling FPGA
- [ ] Add support for USB
- [ ] GUI menu for different communication protocols
