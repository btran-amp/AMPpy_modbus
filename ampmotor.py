from pymodbus.client import ModbusSerialClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder

from MDXT_modbus_registers import *


class AMP_Motor(object):

    def __init__(self, identifier, slave, modbus_client):
        """
        Initializes a new motor with a unique identifier, modbus slave, and modbus client.
        :param identifier: An identifier to recognize your specific motor.
        :param slave: The modbus slave slave of your motor, set using the SimplexMotion tool.
        :param modbus_client: The Pymodbus client designed to communicate with SimplexMotion motors over modbus.
        """
        self.identifier = identifier
        self.slave = slave
        self.modbus_client = modbus_client
        assert isinstance(identifier, str) and isinstance(slave, int) and isinstance(modbus_client, ModbusSerialClient)
    
    def SCL_Command(self, OP_CODE, Param1=None, Param2=None, Param3=None, Param4=None) ->bool:
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

    def get_speed(self) -> int:
        """
        Gets the current speed of the motor. This is found in the motors speed register.
        :return: An integer value for the current speed of the motor
        """
        speed_response = self.modbus_client.read_holding_registers(IV-1, count = 2, slave=self.slave)
        if speed_response.isError():
            raise Exception('Unable to retrieve current speed. {}'.format(speed_response))
        return speed_response.registers[0]

    def get_torque(self):
        """
        Gets the current torque of the motor. This is found in the motors torque register.
        :return: An integer value for the current torque of the motor
        """
        torque_response = self.modbus_client.read_holding_registers(IC-1, count = 1, slave=self.slave)
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


    def go_with_speed(self, speed_units, acc_units):
        """
        Rotates the motor with a target speed, and acceleration
        :param speed_units: Units of speed measured in SMUnits. Please use the converter class to convert from RPM.
        :param acc_units: Units of acceleration measured in SMUnits. Please use the converter class to convert from RPM/s
        :return:
        """
        # Check if speed mode, else set to speed and reset target
        read_mode = self.get_mode()
        if read_mode != 33:
            reset = self.reset_motor()
            if not reset:
                raise Exception('Unable to reset motor. {}'.format(reset))
            self.set_mode(33)
        self.set_max_acceleration(acc_units)
        return self.set_target(speed_units)

    def go_to_position(self, steps, speed_units, acc_units):
        """
        Rotates the motor with a target position, at a set speed, and acceleration
        :param steps: Units of position measured in steps. Please use the converter class to convert from steps to meters.
        :param speed_units: Units of speed measured in SMUnits. Please use the converter class to convert from RPM.
        :param acc_units: Units of acceleration measured in SMUnits. Please use the converter class to convert from RPM/s
        :return:
        """
        # Check if position mode, else set to position and reset target
        read_mode = self.get_mode()
        if read_mode != 21:
            reset = self.reset_motor()
            if not reset:
                raise Exception('Unable to reset motor. {}'.format(reset))
            self.set_mode(21)
        self.set_max_speed(speed_units)
        self.set_max_acceleration(acc_units)
        return self.set_target(steps)

    def set_max_speed(self, sm_units) -> bool:
        """
        Sets the maximum speed for a motor
        :param sm_units: Units of speed measured in SMunits. Please use the converter class to convert from RPM to steps.
        :return: Boolean indicating if the write was successful
        """
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
        builder.add_32bit_int(sm_units)
        write_response = self.modbus_client.write_registers(VM-1, builder.to_registers(), slave=self.slave)
        return not write_response.isError()

    def set_max_torque(self, torque) -> bool:
        """
        Sets the maximum torque for the motor
        :param torque: Units of torque measured in mNm
        :return: Boolean indicating if the write was successful
        """
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
        builder.add_32bit_int(torque)
        write_response = self.modbus_client.write_registers(CC-1, builder.to_registers(), slave=self.slave)
        return not write_response.isError()

    def set_max_acceleration(self, steps):
        """
        Sets the maximum acceleration for the motor
        :param steps: Units of acceleration measured in SMunits. Please use the converter class to convert from RPM/s to steps.
        :return: Boolean indicating if the write was successful
        """
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
        builder.add_32bit_int(steps)
        write_response = self.modbus_client.write_registers(AM-1, builder.to_registers(), slave=self.slave)
        return not write_response.isError()

    def set_max_deceleration(self, steps):
        """
        Sets the maximum deceleration for the motor
        :param steps: Units of acceleration measured in encoder pulses. Please use the converter class to convert from RPM/s to steps.
        :return: Boolean indicating if the write was successful"""
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
        builder.add_32bit_int(steps)
        write_response = self.modbus_client.write_registers(AM-1, steps, slave=self.slave)
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
        :param target: Point to point distance in pulses measured in SMunits. Please use the converter class to convert from desired units to steps.
        :return: Boolean indicating if the write was successful
        """
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
        builder.add_32bit_int(target)
        request = self.modbus_client.write_registers(DI-1, builder.to_registers(), slave=self.slave)
        return not request.isError()

    def stop_motor(self):
        """
        Stops the motor
        :return: Boolean indicating if the write was successful
        """
        return self.SCL_Command(0xE2)

