CMD_WORD = 125 # Command word register
SCL_Param1 = 126 
SCL_Param2 = 127
SCL_Param3 = 128
SCL_Param4 = 129


EP = 11  # Encoder Position 32Bit
IP = 7 # Immediate Absolute Position 32Bit
IV = 17 # Immediate Actual Velocity 
IQ = 32 # Immedidiate Actual Current

DI = 351  # Point-to-Point Distance 32Bit

CC = 275 # 1st Torque Limit 32Bit
VM = 337 # Max Velocity 32Bit
AC = 345 # Point to Point Acceleration 32Bit
DE = 347 # Point to Point Deceleration 32Bit
VE = 349 # Point to Point Velocity 32Bit 
AM = 353 # Max Brake Deceleration 32 Bit
JA = 339 # Jog Acceleration 32 Bit
JL = 341 # Jog Deceleration 32 Bit
JS = 343 # Jog Speed 32 Bit
CM = 263 # Control Mode 32Bit
IU = 22  # Immediate DC Bus Voltage
IT = 19  # Immediate Drive Temperature
IT1 = 20 # Immediate Encoder Temperature
IX = 23  # Immidiate Position Error


GC = 273 # Torque Command for Torque Control 32 Bit

#old PRODUCT
"""
IC = 19 # Immediate Current Command 
JA = 47 # Jog acceleration
JL = 48 # Jog Decceleration
JS = 49
 """