from pymodbus.client import ModbusSerialClient as ModbusClientRTU
#from pymodbus.client import ModbusTcpClient as ModbusClientTCP
from ampmotor import AMP_Motor
from AMP_Opcodes import *
from conversions import AMP_Converter
import time 
import keyboard
import threading
import csv



def log_values(axis, filename, duration):
    start_time = time.time()
    with open(filename, "w") as file:
        file.write(f"time, current, drtemp, dsptemp, DCVolt, speed, pos\n")
        print(f"Logging started. Saving to '{filename}'...")

        while (time.time() - start_time) < duration:
            elapsed_time = round(time.time() - start_time, 2)
            try:
                current = axis.get_current()
                temp = axis.get_drivetemp() 
                dsp_temp = axis.get_dsptemp()
                DCvolts = axis.get_voltage()
                speed = axis.get_speed()
                pos= axis.get_position()

            except Exception as e:
                current = "ERROR"
                temp = "ERROR"
                dsp_temp = "ERROR"
                DCvolts = "ERROR"
                speed = "ERROR"
                pos = "ERROR"
                print(f"Error reading something: {e}")

            if keyboard.is_pressed('esc'):
                print("Esc key pressed. Exiting logging...")
                break

            file.write(f"{elapsed_time}, {current}, {temp}, {dsp_temp}, {DCvolts}, {speed}, {pos}\n")
            file.flush()

    print("Logging complete.")

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
Jog_acceleration_sent = AMP_Axis.set_jog_acceleration(AMP_Axis_Convert.convert_acceleration_to_smunits(300))
print(f"{AMP_Axis.identifier} acceleration set to 100 rps/s: {Jog_acceleration_sent}")

# Deceleration Set Below
Jog_deceleration_sent = AMP_Axis.set_jog_deceleration(AMP_Axis_Convert.convert_acceleration_to_smunits(3500))
print(f"{AMP_Axis.identifier}  deceleration set to 100rps/s: {Jog_deceleration_sent}")


# Jog Speed Set Below
Jog_speed_sent = AMP_Axis.set_jog_speed(AMP_Axis_Convert.convert_speed_to_VEunits(30*60))  # 25 rps
print(f"{AMP_Axis.identifier} jog speed sent?: {Jog_speed_sent}")


# Start logging in a separate thread
log_thread = threading.Thread(target=log_values, args=(AMP_Axis, "JL_3500_noRegen_30rps4.txt", 10))
log_thread.start()
time.sleep(1.5)

# Enable all motors
SCL_cmd_sent = AMP_Axis.SCL_Command(ME)
print(f"SCL command Motor Enable sent: {SCL_cmd_sent}")

Commence_jog_sent = AMP_Axis.SCL_Command(CJ)
print(f"Jog Motion in Progress: {Commence_jog_sent}")

time.sleep(4)

# Stop Jogging
motor_stop_sent = AMP_Axis.stop_motor()
print("The motor has stopped moving")

SCL_cmd_sent = AMP_Axis.SCL_Command(MD)
print("The motor has been disabled")

log_thread.join()

modbus_client.close()
