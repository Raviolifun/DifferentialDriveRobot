""" this is a PID controller"""

import time


class PIDController:

    def __init__(self, sensor, sensor_property, proportional, integral, derivative, frequency):
        # setting up access to sensor data
        self._sensor = sensor
        self._sensor_property = sensor_property
        # setting properties to avoid crazy initial conditions
        self._proportional = proportional
        self._integral = integral
        self._derivative = derivative
        self._past_value = getattr(sensor, sensor_property)
        self._past_error = 0
        self._past_time = time.time()
        self._error_integral = 0
        self._set_point = getattr(sensor, sensor_property)
        self._frequency = frequency
        # Controller outputs are limited to -1 and 1 by default.
        self._output_min = -1
        self._output_max = 1
        # Integral clamping by default
        self._integral_clamp = True

    # I need to learn threading before I do this, could end up with some real problems!
    # def start_up(self):
    #    while True:
    #
    #
    #        time.sleep(1/self._frequency)

    def set_goal(self, set_point):
        self._set_point = set_point

    def set_limits(self, minimum, maximum):
        self._output_min = minimum
        self._output_max = maximum

    def get_controller_output(self):

        new_input = getattr(self._sensor, self._sensor_property)

        print("Sensor Reading: ", new_input)

        error = new_input - self._past_value
        current_time = time.time()

        dt = current_time - self._past_time
        error_derivative = (error - self._past_error) / dt

        proportional_term = self._proportional * error
        integral_term = self._integral * self._error_integral
        derivative_term = self._derivative * error_derivative

        output = proportional_term + integral_term + derivative_term

        clamp = False

        if output > self._output_max:
            output = self._output_max
            clamp = True

        if output < self._output_min:
            output = self._output_min
            clamp = True

        if clamp and self._integral_clamp:
            # only add to integral term if output at limits and clamping enabled
            self._error_integral = self._error_integral + error * dt

        self._past_time = current_time
        self._past_value = new_input

        return output



