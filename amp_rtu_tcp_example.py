from pymodbus.client import ModbusSerialClient as ModbusClientRTU
from pymodbus.client import ModbusTcpClient as ModbusClientTCP
from ampmotor import AMP_Motor
from AMP_Opcodes import *
from conversions import AMP_Converter
import time

# Initialize Modbus client
"""
Use either Modbus RTU or Modbus TCP based on the product's supported communication interface.
Uncomment the appropriate line below.
"""
#modbus_client = ModbusClientRTU(port="COM2", baudrate=9600, timeout=1)
modbus_client = ModbusClientTCP(host='10.10.10.10', port=502) 

# Create an instance of AMP_Motor
AMP_Axis1 = AMP_Motor(identifier="MDXT", slave=32, client=modbus_client) 
print(f"AMP_Axis1 identifier: {AMP_Axis1.identifier}")  # Output: MDXT
print(f"AMP_Axis1 slave address: {AMP_Axis1.slave}")  # Output: 32

# Create an instance of AMP_Converter to handle unit conversions
"""
Input parameters directly affect motor behavior and must be configured correctly.
- 'steps_per_rev' is set using Luna Software.
- Set 'gear_multiplier' to 1 if only evaluating the motor’s motion profile.
- If a gearbox or coupling ratio is involved and output-side motion is of interest, 
  set 'gear_multiplier' to reflect the actual mechanical ratio.
"""
AMP_Axis1_Convert = AMP_Converter(steps_per_rev=20000, gear_multiplier=1)

# Example 1: motor enable
SCL_cmd_sent = AMP_Axis1.SCL_Command(ME)
print(f"SCL command Motor Enable sent: {SCL_cmd_sent}")

# Example 2: Set target deceleration rate
"""
Sets the acceleration to 100 rps/s, it uses the AMP_Converter instance to convert to servo motor units.
"""
Jog_acceleration_sent = AMP_Axis1.set_jog_acceleration(AMP_Axis1_Convert.convert_acceleration_to_smunits(100))
print(f"Target position set to 100 rps/s: {Jog_acceleration_sent}")

# Example 3: Set target deceleration rate
"""
Sets the deceleration to 100 rps/s, it uses the AMP_Converter instance to convert to servo motor units.
"""
Jog_deceleration_sent = AMP_Axis1.set_jog_deceleration(AMP_Axis1_Convert.convert_acceleration_to_smunits(100))
print(f"Jog deceleration set to 100rps/s: {Jog_deceleration_sent}")

# Example 4: Set target jog speed rate (convert from rpm to sm VE units)
Jog_speed_sent = AMP_Axis1.set_jog_speed(AMP_Axis1_Convert.convert_speed_to_VEunits(240))
print(f"Target position set to: {Jog_speed_sent}")

# Example 5: Commence Jog 
Commence_jog_sent = AMP_Axis1.SCL_Command(CJ)
print(f"Jog Motion in Progress: {Commence_jog_sent}")


# Logging loop for 30 minute
log_time = 30
log_filename = "current_log.txt" 
runtime_seconds = log_time * 60
start_time = time.time()

with open(log_filename, "w") as file:
    file.write("[time, Immediate_Current_Value]\n")
    print(f"Logging started. Saving to '{log_filename}'...")

    while (time.time() - start_time) < runtime_seconds:
        elapsed_time = round(time.time() - start_time, 2)
        try:
            immediate_current_value = AMP_Axis1.get_current()
        except Exception as e:
            immediate_current_value = "ERROR"
            print(f"Error reading current: {e}")

        file.write(f"[{elapsed_time}, {immediate_current_value}]\n")
        file.flush()

        time.sleep(1)  # log every second

print("Logging complete.")


# Example 7: Stop the AMP_Axis1 after movement
motor_stop_sent = AMP_Axis1.stop_motor()
print(f"AMP_Axis1 stopping: {motor_stop_sent}")

SCL_cmd_sent = AMP_Axis1.SCL_Command(MD)
print(f"SCL command Motor Disable sent: {SCL_cmd_sent}")

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