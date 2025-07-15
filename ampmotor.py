from pymodbus.client import ModbusSerialClient, ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder
from MDXT_modbus_registers import *

class AMP_Motor(object):

    def __init__(self, identifier, slave, client):
        """
        Initializes a new motor with a unique identifier, modbus slave, and modbus client.
        :param identifier: An identifier to recognize your specific motor.
        :param slave: The modbus slave of your motor, set using the AMP Configurator.
        :param modbus_client: The Pymodbus client designed to communicate with AMP motors over modbus. 
        Parameter should be of ModbusSerialClient or ModbusTCPClient Type
        """
        self.identifier = identifier
        self.slave = slave
        self.modbus_client = client
        assert isinstance(identifier, str) and isinstance(slave, int)
        isinstance(client, (ModbusSerialClient, ModbusTcpClient)),\

    def SCL_Command(self, OP_CODE, Param1=None, Param2=None, Param3=None, Param4=None) ->bool:
        """
        Executes an SCL command. Some operation codes (OP_CODEs) may require additional parameters.

        Parameters:
        - OP_CODE (required): The operation code to be written to register 400125.
        - Param1 to Param4 (optional): Command-specific parameters. Only include them if the selected OP_CODE requires them.

        Returns:
        - bool: True if the command was successfully sent, False otherwise.
        """
        if Param1 is not None:
            param1_response = self.modbus_client.write_register(SCL_Param1-1, Param1, slave=self.slave)
            pass
    
        if Param2 is not None:
            param2_response = self.modbus_client.write_register(SCL_Param2-1, Param2, slave=self.slave)
            pass
    
        if Param3 is not None:
            param3_response = self.modbus_client.write_register(SCL_Param3-1, Param3, slave=self.slave)
            pass
    
        if Param4 is not None:
            param4_response = self.modbus_client.write_register(SCL_Param4-1, Param3, slave=self.slave)
            pass
        opcode_response = self.modbus_client.write_register(CMD_WORD-1, OP_CODE, slave=self.slave)

        return not opcode_response.isError()
        

    def get_position(self) -> int:
        """
        Gets the current position of the motor. This is found in the current position register.
        :return: An integer value for the current position of the motor
        """
        pos_response = self.modbus_client.read_holding_registers(IP-1, count = 2, slave=self.slave)
        if pos_response.isError():
            raise Exception('Unable to retrieve current position. {}'.format(pos_response))
        decoder = BinaryPayloadDecoder.fromRegisters(pos_response.registers, byteorder=Endian.BIG, wordorder=Endian.BIG)
        return decoder.decode_32bit_int()


    def get_drivetemp(self) -> int:
        """
        Gets the current drive temperature of the motor. This is found in the motors drive temperature register.
        :return: An integer value for the current temperature of the motor
        """
        drivetemp_response = self.modbus_client.read_holding_registers(IT-1, count = 1, slave=self.slave)
        if drivetemp_response.isError():
            raise Exception('Unable to retrieve current speed. {}'.format(drivetemp_response))
        return drivetemp_response.registers[0]
    
    def get_dsptemp(self) -> int:
        """
        Gets the current dsp temperature of the motor. This is found in the motors dsp temperature register.
        :return: An integer value for the current temperature of the motor
        """
        dsptemp_response = self.modbus_client.read_holding_registers(IT1-1, count = 1, slave=self.slave)
        if dsptemp_response.isError():
            raise Exception('Unable to retrieve current dsp temperature. {}'.format(dsptemp_response))
        return dsptemp_response.registers[0]
    
    def get_position_error(self) -> int:
        """
        Gets the current encoder position error. This is found in the motors position error.
        :return: An integer value for the immidiate position error of the motor
        BROKENTBD
        """
        pos_error_response = self.modbus_client.read_holding_registers(IX-1, count = 2, slave=self.slave)
        if pos_error_response.isError():
            raise Exception('Unable to retrieve enc position error. {}'.format(pos_error_response))
        return pos_error_response.registers[0]
    
    def get_speed(self) -> int:
        """
        Gets the current speed of the motor. This is found in the motors speed register.
        :return: An integer value for the current speed of the motor
        """
        speed_response = self.modbus_client.read_holding_registers(IV-1, count = 1, slave=self.slave)
        if speed_response.isError():
            raise Exception('Unable to retrieve current speed. {}'.format(speed_response))
        return speed_response.registers[0]
    
    def get_voltage(self) -> int:
        """
        Gets the DC bus voltage of the motor. This is found in the DC bus voltage register.
        :return: An integer value for the current DC Bus Voltage of the motor
        """
        volt_response = self.modbus_client.read_holding_registers(IU-1, count = 1, slave=self.slave)
        if volt_response.isError():
            raise Exception('Unable to retrieve Immidiate DC Bus Voltage. {}'.format(volt_response))
        return volt_response.registers[0]
    
    def get_current(self):
        """
        Gets the immidiate current of the motor. This is found in the motors current register.
        :return: An integer value for the current of the motor
        """
        torque_response = self.modbus_client.read_holding_registers(IQ-1, count = 1, slave=self.slave)
        if torque_response.isError():
            raise Exception('Unable to retrieve current torque. {}'.format(torque_response))
        return torque_response.registers[0]        

    def get_mode(self):
        """
        Gets the current control mode setting of the motor
        :return: An integer describing the various modes of operation for the motor
        """
        mode = self.modbus_client.read_holding_registers(CM-1, count =2, slave=self.slave)
        if mode.isError():
            raise Exception('Unable to retrieve current mode. {}'.format(mode))
        decoder = BinaryPayloadDecoder.fromRegisters(mode.registers, byteorder=Endian.BIG, wordorder=Endian.BIG)
        return decoder.decode_32bit_int()

    def set_max_speed(self, sm_units) -> bool:
        """
        Sets the maximum speed for a motor
        :param sm_units: Units of speed measured in SMunits. Use the converter class to convert from RPM to pulses.
        :return: Boolean indicating if the write was successful
        """
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
        builder.add_32bit_int(sm_units)
        write_response = self.modbus_client.write_registers(VM-1, builder.to_registers(), slave=self.slave)
        return not write_response.isError()

    def set_max_torque(self, torque) -> bool:
        """
        Sets the maximum torque for the motor
        :param torque: Units of torque measured in percentage of rated torque
        :return: Boolean indicating if the write was successful
        """
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
        builder.add_32bit_int(torque)
        write_response = self.modbus_client.write_registers(CC-1, builder.to_registers(), slave=self.slave)
        return not write_response.isError()

    def set_max_acceleration(self, sm_units):
        """
        Sets the maximum acceleration for the motor. Also used for Max Brake deceleration.
        :param sm_units: Units of acceleration measured 1/6 rps. Use the converter class to convert from RPM/s to register units.
        :return: Boolean indicating if the write was successful
        """
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
        builder.add_32bit_int(sm_units)
        write_response = self.modbus_client.write_registers(AM-1, builder.to_registers(), slave=self.slave)
        return not write_response.isError()
    
    def set_jog_acceleration(self, sm_units):
        """
        Sets the jog acceleration for the motor
        :param sm_units: Units of acceleration measured in encoder pulses/s/s. Use the converter class to convert from RPM/s^2 to pulses.
        :return: Boolean indicating if the write was successful"""
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
        builder.add_32bit_int(sm_units)
        write_response = self.modbus_client.write_registers(JA-1, builder.to_registers(), slave=self.slave)
        return not write_response.isError()    
    
    def set_jog_deceleration(self, sm_units):
        """
        Sets the maximum deceleration for the motor
        :param sm_units: Units of acceleration measured in encoder pulses. Use the converter class to convert from RPM to pulses/s.
        :return: Boolean indicating if the write was successful"""
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
        builder.add_32bit_int(sm_units)
        write_response = self.modbus_client.write_registers(JL-1, builder.to_registers(), slave=self.slave)
        return not write_response.isError()    
    
    def set_jog_speed(self, sm_units):
        """
        Sets the jog speed for motor speed control
        :param sm_units: Units of speed measured in 1/240 rps. Use the converter class to convert from RPM/s^2 to required units.
        :return: Boolean indicating if the write was successful"""
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
        builder.add_32bit_int(sm_units)
        write_response = self.modbus_client.write_registers(JS-1, builder.to_registers(), slave=self.slave)
        return not write_response.isError()    

    def set_control_mode(self, control_mode):
        """
        Sets the motor operating mode
        :param control_mode: Integer indicating the intended operating mode. Consult the motor manual for details
        :return: Boolean indicating if the write was successful
        """
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
        builder.add_32bit_int(control_mode)
        write_response = self.modbus_client.write_registers(CM-1, builder.to_registers(), slave=self.slave)
        return not write_response.isError()

    def set_target_position(self, target):
        """
        Sets the target position for the motor
        :param target: Point to point distance in pulses measured in SMunits. Use the converter class to convert from desired units to pulses.
        :return: Boolean indicating if the write was successful
        """
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
        builder.add_32bit_int(target)
        request = self.modbus_client.write_registers(DI-1, builder.to_registers(), slave=self.slave)
        return not request.isError()
    
    def set_p2p_vel(self, sm_units):
        """
        Sets the target point-to-point velocity
        :param sm_units: Point to point move velocity in pulses measured in SMunits. Use the converter class to convert from desired units to pulses.
        :return: Boolean indicating if the write was successful
        """
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
        builder.add_32bit_int(sm_units)
        request = self.modbus_client.write_registers(VE-1, builder.to_registers(), slave=self.slave)
        return not request.isError()
    

    def set_p2p_accel(self, sm_units):
        """
        Sets the target point-to-point acceleration
        :param sm_units: Point to point move acceleration in units of 10RPM/s. Use the converter class to convert from desired units to required units.
        :return: Boolean indicating if the write was successful
        """
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
        builder.add_32bit_int(sm_units)
        request = self.modbus_client.write_registers(AC-1, builder.to_registers(), slave=self.slave)
        return not request.isError()
    
    def set_p2p_decel(self, sm_units):
        """
        Sets the target point-to-point deceleration
        :param sm_units: Point to point move deceleration of 10RPM/s. Use the converter class to convert from desired units to required units.
        :return: Boolean indicating if the write was successful
        """
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
        builder.add_32bit_int(sm_units)
        request = self.modbus_client.write_registers(DE-1, builder.to_registers(), slave=self.slave)
        return not request.isError()

    def stop_motor(self):
        """
        Stops the motor
        :return: Boolean indicating if the write was successful
        """
        return self.SCL_Command(0xE2)

    def go_with_speed(self, speed_units, acc_units):
        """
        Rotates the motor with a target speed, and acceleration
        :param speed_units: Units of speed measured in SMUnits. Use the converter class to convert from RPM.
        :param acc_units: Units of acceleration measured in SMUnits. Use the converter class to convert from RPM/s
        :return:
        """
        # Check if speed mode, else set to speed and reset target
        read_mode = self.get_mode()
        if read_mode != 10:
            self.set_mode(10)
        self.set_jog_acceleration(acc_units)
        return self.set_jog_speed(speed_units)

    def go_to_position(self, pulses, speed_units, acc_units):
        """
        Rotates the motor with a target position, at a set speed, and acceleration.
        :param pulses: Units of position measured in pulses. Use the converter class to convert from desired units to pulses.
        :param speed_units: Units of speed measured in 1/240rps. Use the converter class to convert from RPM.
        :param acc_units: Units of acceleration measured in 10RPM/s. Use the converter class to convert from RPM/s
        :return:
        """
        # Check if position mode, else set to position and reset target
        read_mode = self.get_mode()
        if read_mode != 21:
            self.set_mode(21)
        self.set_p2p_vel(speed_units)
        self.set_p2p_accel(acc_units)
        return self.set_target_position(pulses)