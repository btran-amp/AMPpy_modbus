from pymodbus.client import ModbusSerialClient as ModbusClientRTU
#from pymodbus.client import ModbusTcpClient as ModbusClientTCP
from ampmotor import AMP_Motor
from AMP_Opcodes import *
from conversions import AMP_Converter
import time

# Initialize Modbus client
"""
Use either Modbus RTU or Modbus TCP based on the product's supported communication interface.
Uncomment the appropriate line below.
"""
modbus_client = ModbusClientRTU(port="COM8", baudrate=9600, timeout=1)
#modbus_client = ModbusClientTCP(host='10.10.10.10', port=502) 

# Create an instance of AMP_Motor
AMP_Axis1 = AMP_Motor(identifier="MXXR83_Auto", slave=1, client=modbus_client) 
print(f"AMP_Axis1 identifier: {AMP_Axis1.identifier}")  # Output: MDXR_a
print(f"AMP_Axis1 slave address: {AMP_Axis1.slave}")  # Output: 1


AMP_Axis2 = AMP_Motor(identifier="MDXR83_Manual", slave=2, client=modbus_client) 
print(f"AMP_Axis2 identifier: {AMP_Axis2.identifier}")  # Output: MDXR_m
print(f"AMP_Axis2 slave address: {AMP_Axis2.slave}")  # Output: 2

AMP_Axis3 = AMP_Motor(identifier="MDXT62", slave=3, client=modbus_client) 
print(f"AMP_Axis3 identifier: {AMP_Axis3.identifier}")  # Output: MDXT
print(f"AMP_Axis3 slave address: {AMP_Axis3.slave}")  # Output: 3
# Create an instance of AMP_Converter to handle unit conversions

"""
Input parameters directly affect motor behavior and must be configured correctly.
- 'steps_per_rev' is set using Luna Software.
- Set 'gear_multiplier' to 1 if only evaluating the motor’s motion profile.
- If a gearbox or coupling ratio is involved and output-side motion is of interest, 
  set 'gear_multiplier' to reflect the actual mechanical ratio.
"""
AMP_Axis1_Convert = AMP_Converter(steps_per_rev=20000, gear_multiplier=1)
AMP_Axis2_Convert = AMP_Converter(steps_per_rev=20000, gear_multiplier=1)
AMP_Axis3_Convert = AMP_Converter(steps_per_rev=20000, gear_multiplier=1)

# Set acceleration, decleration, and jogging speed of axis1
Jog_acceleration_sent = AMP_Axis1.set_jog_acceleration(AMP_Axis1_Convert.convert_acceleration_to_smunits(100))
print(f"Target position set to 100 rps/s: {Jog_acceleration_sent}")
Jog_deceleration_sent = AMP_Axis1.set_jog_deceleration(AMP_Axis1_Convert.convert_acceleration_to_smunits(100))
print(f"Jog deceleration set to 100rps/s: {Jog_deceleration_sent}")
Jog_speed_sent = AMP_Axis1.set_jog_speed(AMP_Axis1_Convert.convert_speed_to_VEunits(23*60))
print(f"Target position set to: {Jog_speed_sent}")


# Set acceleration, decleration, and jogging speed of axis2
Jog_acceleration_sent = AMP_Axis2.set_jog_acceleration(AMP_Axis2_Convert.convert_acceleration_to_smunits(100))
print(f"Target position set to 100 rps/s: {Jog_acceleration_sent}")
Jog_deceleration_sent = AMP_Axis2.set_jog_deceleration(AMP_Axis2_Convert.convert_acceleration_to_smunits(100))
print(f"Jog deceleration set to 100rps/s: {Jog_deceleration_sent}")
Jog_speed_sent = AMP_Axis2.set_jog_speed(AMP_Axis2_Convert.convert_speed_to_VEunits(23*60))
print(f"Target position set to: {Jog_speed_sent}")


# Set acceleration, decleration, and jogging speed of axis3
Jog_acceleration_sent = AMP_Axis3.set_jog_acceleration(AMP_Axis3_Convert.convert_acceleration_to_smunits(100))
print(f"Target position set to 100 rps/s: {Jog_acceleration_sent}")
Jog_deceleration_sent = AMP_Axis3.set_jog_deceleration(AMP_Axis3_Convert.convert_acceleration_to_smunits(100))
print(f"Jog deceleration set to 100rps/s: {Jog_deceleration_sent}")
Jog_speed_sent = AMP_Axis3.set_jog_speed(AMP_Axis3_Convert.convert_speed_to_VEunits(20*60))
print(f"Target position set to: {Jog_speed_sent}")

# Enable all motors, then commensing jog
SCL_cmd_sent1 = AMP_Axis1.SCL_Command(ME)
SCL_cmd_sent2 = AMP_Axis2.SCL_Command(ME)
SCL_cmd_sent3 = AMP_Axis3.SCL_Command(ME)
print(f"SCL command Motor Enable sent: {SCL_cmd_sent1}")

Commence_jog_sent1 = AMP_Axis1.SCL_Command(CJ)
Commence_jog_sent2 = AMP_Axis2.SCL_Command(CJ)
Commence_jog_sent3 = AMP_Axis3.SCL_Command(CJ)
print(f"Jog Motion in Progress: {Commence_jog_sent1}")

# jogs for 30 minutes
log_time = 30
# log_filename = "current_log.txt"
runtime_seconds = log_time * 60
start_time = time.time()

while (time.time() - start_time) < runtime_seconds:
    elapsed_time = round(time.time() - start_time, 2)
    print(f"Elapsed_time: {elapsed_time}")
    time.sleep(1)

print(f"{log_time} minutes have passed")

# Stop Jogging
motor_stop_sent1 = AMP_Axis1.stop_motor()
motor_stop_sent2 = AMP_Axis2.stop_motor()
motor_stop_sent3 = AMP_Axis3.stop_motor()
print("All motors have stopped moving")

SCL_cmd_sent1 = AMP_Axis1.SCL_Command(MD)
SCL_cmd_sent2 = AMP_Axis2.SCL_Command(MD)
SCL_cmd_sent3 = AMP_Axis3.SCL_Command(MD)
print("All motors have been disabled")

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