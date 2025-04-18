# AMPpy_modbus
AMPpy_modbus is a module based atop Pymodbus, to allow for direct control to Applied Motion Drives and Integrated motors using the Modbus RTU protocol. (TCP support to be added)

## Installation of pymodbus
To get started, first install pymodbus using the pip installer with command `pip install pymodbus` 

## Using AMPpy_modbus
Simply clone this repository after installing pymodbus into your project, and import the required modules.

# About Applied Motion Modbus Register
MODBUS Registers Xlsx provided for reference. A quick way to check which registers are supported by your model is through Luna Software.

## Examples
**`amp_rtu_tcp_example.py`**  
This example demonstrates how to communicate with Applied Motion Products drives (MDX+, M5, MBDV series) using either Modbus RTU or Modbus TCP.

The script is based on a real testing scenario where a motor was exposed to -32°C. During the test, current readings were collected every second for 30 minutes and stored in a `.txt` file.
