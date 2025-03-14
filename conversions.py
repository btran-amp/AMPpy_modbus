import math
from math import floor  # Used to round down values to the nearest integer

class AMP_Converter:
    
    def __init__(self, gear_multiplier, steps_per_rev, **kwargs):
        """
        Initializes the AMPconverter with a gear multiplier and steps per revolution.
        Optionally accepts 'hub_diameter' in millimeters.
        """
        assert isinstance(gear_multiplier, int), "gear_multiplier must be an integer"
        assert isinstance(steps_per_rev, int), "steps_per_rev must be an integer"

        self.gear_multiplier = gear_multiplier  # Gear ratio multiplier
        self.steps_per_rev = steps_per_rev  # Steps per full revolution of the motor
        if kwargs:
            self.hub_diameter = kwargs.get("hub_diameter", 1)  # Default hub diameter is 1 mm

    def convert_pulses_to_degrees(self, steps):
        """
        Converts a given number of motor pulses (steps) to degrees of rotation.
        """
        percentage_of_steps = steps / (self.steps_per_rev * self.gear_multiplier)
        degrees = percentage_of_steps * 360
        return int(floor(degrees))  # Return the floored integer value

    def convert_degrees_to_pulses(self, degrees):
        """
        Converts degrees of rotation to the corresponding number of pulses (steps).
        """
        percentage_of_movement = degrees / 360
        steps = percentage_of_movement * self.steps_per_rev * self.gear_multiplier
        return int(floor(steps))

    def convert_speed_to_VEunits(self, speed):  # speed in RPM
        """
        Converts speed from RPM to VE units.
        VE units appear to be based on 240 pulses per revolution.
        """
        VEunits = (speed / 60) * 240 * self.gear_multiplier
        return int(floor(VEunits))

    def convert_smunits_to_speed(self, VEunits):
        """
        Converts speed from VE units back to RPM.
        """
        rpm = (60 * VEunits) / (240 * self.gear_multiplier)
        return int(floor(rpm))

    def convert_acceleration_to_smunits(self, acceleration):  # acceleration in rev/s²
        """
        Converts acceleration from rev/s² to servo motion units (AC register units).
        """
        ACunits = acceleration * 6 * self.gear_multiplier
        return int(floor(ACunits))

    def convert_smunits_to_acceleration(self, AC_value):
        """
        Converts acceleration from servo motion units (AC register units) back to rev/s².
        """
        rps_per_sec = AC_value / (6 * self.gear_multiplier)
        return int(floor(rps_per_sec))

    def convert_millimeters_to_pulses(self, millimeters):
        """
        Converts a linear distance (millimeters) into the corresponding number of motor pulses.
        Uses hub circumference for calculation.
        """
        hub_circumference = self.hub_diameter * math.pi  # Circumference of the hub in mm
        hub_rotations = millimeters / hub_circumference  # Number of hub rotations to cover the distance
        pulses = hub_rotations * self.steps_per_rev * self.gear_multiplier  # Convert to pulses
        return int(floor(pulses))

    def convert_pulses_to_millimeters(self, pulses):
        """
        Converts a number of motor pulses into a linear distance in millimeters.
        """
        steps_as_multiplier = pulses / (self.steps_per_rev * self.gear_multiplier)
        distance = math.pi * self.hub_diameter * steps_as_multiplier  # Convert back to distance
        return int(floor(distance))