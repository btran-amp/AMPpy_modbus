from pymodbus.client import ModbusSerialClient as ModbusClientRTU
#from pymodbus.client import ModbusTcpClient as ModbusClientTCP
from ampmotor import AMP_Motor
from AMP_Opcodes import *
from conversions import AMP_Converter
import time 
import keyboard

# Initialize Modbus client
"""
Use either Modbus RTU or Modbus TCP based on the product's supported communication interface.
Uncomment the appropriate line below
"""
modbus_client = ModbusClientRTU(port="COM8", baudrate=9600, timeout=1)
#modbus_client = ModbusClientTCP(host='10.10.10.10', port=502) 

# Create an instance of AMP_Motor
AMP_Axis = AMP_Motor(identifier="MDXT82", slave=1, client=modbus_client) 
print(f"AMP_Axis1 identifier: {AMP_Axis.identifier}")  # Output: MDXT82
print(f"AMP_Axis1 slave address: {AMP_Axis.slave}")  # Output: 1


AMP_Axis_Convert = AMP_Converter(steps_per_rev=10000, gear_multiplier=1)


# Acceleration Set Below
Jog_acceleration_sent = AMP_Axis.set_jog_acceleration(AMP_Axis_Convert.convert_acceleration_to_smunits(100))
print(f"{AMP_Axis.identifier} acceleration set to 100 rps/s: {Jog_acceleration_sent}")

# Deceleration Set Below
Jog_deceleration_sent = AMP_Axis.set_jog_deceleration(AMP_Axis_Convert.convert_acceleration_to_smunits(1000))
print(f"{AMP_Axis.identifier}  deceleration set to 100rps/s: {Jog_deceleration_sent}")

# Jog Speed Set Below
Jog_speed_sent = AMP_Axis.set_jog_speed(AMP_Axis_Convert.convert_speed_to_VEunits(25*60))  # 25 rps
print(f"{AMP_Axis.identifier} jog speed sent?: {Jog_speed_sent}")



# Enable all motors
SCL_cmd_sent = AMP_Axis.SCL_Command(ME)
print(f"SCL command Motor Enable sent: {SCL_cmd_sent}")

Commence_jog_sent = AMP_Axis.SCL_Command(CJ)


print(f"Jog Motion in Progress: {Commence_jog_sent}")


# Logging loop for 30 minute
log_time = 10 #seconds
log_filename = "JL_1000_noRegen_25rps.txt" 
runtime_seconds = log_time
start_time = time.time()

with open(log_filename, "w") as file:
    file.write(f"[time, {AMP_Axis.identifier}]\n")
    print(f"Logging started. Saving to '{log_filename}'...")

    while (time.time() - start_time) < runtime_seconds:
        elapsed_time = round(time.time() - start_time, 2)
        try:
            immediate_current_value = AMP_Axis.get_current()
        except Exception as e:
            immediate_current_value = "ERROR"
            print(f"Error reading current: {e}")
        if keyboard.is_pressed('esc'):  
            print("Esc key pressed. Exiting the loop...")
            break

        file.write(f"[{elapsed_time}, {immediate_current_value}]\n")
        file.flush()
        

        time.sleep(0.030)  # log every second
print("Logging complete.")

# Stop Jogging
motor_stop_sent = AMP_Axis.stop_motor()
print("The motor has stopped moving")

SCL_cmd_sent1 = AMP_Axis.SCL_Command(MD)
print("The motor has been disabled")

modbus_client.close()