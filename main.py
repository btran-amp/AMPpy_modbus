from pymodbus.client import ModbusSerialClient as ModbusClient
from ampmotor import AMP_Motor
from AMP_Opcodes import *
from conversions import AMP_Converter
import time

# Initialize Modbus client
modbus_client = ModbusClient(port="COM4", baudrate=9600, timeout=1)


# Create an instance of AMP_Motor
AMP_Axis1 = AMP_Motor(identifier="MDXR4", slave=32, modbus_client=modbus_client)
print(f"AMP_Axis1 identifier: {AMP_Axis1.identifier}")  # Output: MDXR4
print(f"AMP_Axis1 slave address: {AMP_Axis1.slave}")  # Output: 32

# Create an instance of AMP_Converter to handle unit conversions
AMP_Axis1_Convert = AMP_Converter(steps_per_rev=10000, gear_multiplier=1)

# Example 1: Set Output 2 to Low using a specific command
SCL_cmd_sent = AMP_Axis1.SCL_Command(SO, ord('2'), ord('L'))
print(f"SCL command sent: {SCL_cmd_sent}")

# Example 2: Set the target position (absolute position in pulses)
Target_position_sent = AMP_Axis1.set_target_position(20000)
print(f"Target position set to: {Target_position_sent}")

# Example 3: Initiate movement by pointing to the target position
Feed_to_position_sent = AMP_Axis1.SCL_Command(FP)
print(f"Point-to-point movement in progress: {Feed_to_position_sent}")

# Wait for a short period to simulate movement
time.sleep(2)

# Example 4: Stop the AMP_Axis1 after movement
motor_stop_sent = AMP_Axis1.stop_motor()
print(f"AMP_Axis1 stopping: {motor_stop_sent}")

# Example 4: Verify position
Current_absolute_position = AMP_Axis1.get_position()
print(f"Current Actual Position is: {Current_absolute_position}")

# Close the Modbus client connection

modbus_client.close()


""" 
    Testing Code
    client = ModbusClient(
    port="COM4",  # Adjust to your port
    baudrate=9600,
    timeout=1,
    parity="N",
    stopbits=1,
    bytesize=8
)

if client.connect():
    response = client.read_holding_registers(address=344, count=2, slave=32)  # STATUS register
    if not response.isError():
        high_word = response.registers[0]
        low_word = response.registers[1]
        value_32bit = (high_word << 16) | low_word
        acceleration = AMP_Axis1_Convert.convert_smunits_to_acceleration(value_32bit)
        print("32-bit Value at address 40345:", value_32bit)
        print("Use AMP_Converter to convert to real units:", acceleration)
        #print("32-bit Value at address 40038:", high_word)
    else:
        print("Error reading STATUS:", response)
    client.close() """