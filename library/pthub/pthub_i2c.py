from ptcommon.logger import PTLogger
from ptcommon.counter import Counter
from smbus import SMBus
from threading import Thread
from time import sleep
from numpy import int16
import traceback

_battery_state_handler = None
_main_thread = None
_run_main_thread = False

# Time to pause between command sends
_cycle_sleep_time = 1


class BatteryRegisters():
    charging_state = 0x0a
    capacity = 0x0d
    charge_time = 0x13
    discharge_time = 0x12


class BatteryDataType():
    charging_state = 'charging_state'
    capacity = 'capacity'
    time = 'time'


class BatteryStateHandler:

    def __init__(self, state_instance):
        self._state = state_instance
        self._bus_no = 1
        self._chip_address = 0x0b

        self._i2c_ctr = Counter(20)

        self._connected = self._setup_i2c()

    def set_charging_state(self, state):
        self._state.set_battery_charging_state(state)

    def set_capacity(self, capacity):
        self._state.set_battery_capacity(capacity)

    def set_time(self, time):
        self._state.set_battery_time(time)

    def is_connected(self):
        return self._connected

    def _setup_i2c(self):
        try:
            PTLogger.debug("Setting up i2c connection to battery")
            self._bus = SMBus(self._bus_no)

            PTLogger.debug("Testing comms with battery")
            return self._refresh_state()
        except:
            PTLogger.warning("Unable to find pi-topHUB battery")

        return False

    def _refresh_state(self):

        PTLogger.debug("Refreshing battery state...")

        if not self._get_battery_data(BatteryDataType.charging_state):
            PTLogger.debug("Unable to get battery charging state")
            return False

        if not self._get_battery_data(BatteryDataType.capacity):
            PTLogger.debug("Unable to get battery capacity")
            return False

        if not self._get_battery_data(BatteryDataType.time):
            PTLogger.debug("Unable to get battery time")
            return False

        return True

    def _get_battery_register_to_read(self, data_to_get):
        if data_to_get == BatteryDataType.charging_state:
            register = BatteryRegisters.charging_state
        elif data_to_get == BatteryDataType.capacity:
            register = BatteryRegisters.capacity
        elif data_to_get == BatteryDataType.time:
            # requires charging state to be correct...
            if self._state._battery_charging_state == 1:
                register = BatteryRegisters.charge_time
            else:
                register = BatteryRegisters.discharge_time
        else:
            raise ValueError("Unknown data type to read from battery")

        return register

    def _parse_response(self, resp, register, data_to_get):
        # Successful read, check that value is valid
        resp_bin = bin(resp)
        resp_dec = int16(resp)

        if register == BatteryRegisters.charging_state:
            return self._process_charging_state_i2c_resp(resp_dec, data_to_get)
        elif register == BatteryRegisters.capacity:
            return self._process_capacity_i2c_resp(resp_dec)
        elif register == BatteryRegisters.discharge_time:
            return self._process_discharging_time_i2c_resp(resp_dec)
        elif register == BatteryRegisters.charge_time:
            return self._process_charging_time_i2c_resp(resp_dec)
        else:
            # Unknown register
            return False

    def _process_charging_state_i2c_resp(self, resp_dec, data_to_get):
        if resp_dec == 0xffff:
            PTLogger.debug("\tCurrent reading out of range")
            return False

        # Get signed decimal output of response
        # Check for valid read
        # Out of range or FFFF

        if resp_dec < -4000 or resp_dec > 4000:
            # Not valid
            PTLogger.debug("Value received not valid - not accepted")
            return False

        if resp_dec <= -10:
            self.set_charging_state(0)
        else:
            charging_state = 2 if (self._state._battery_time == 0) else 1  # charging state
            self.set_charging_state(charging_state)

        if data_to_get == BatteryDataType.time:
            # Determined state, now get correct time value
            self._i2c_ctr.reset()
        else:
            return True

    def _process_capacity_i2c_resp(self, resp_dec):
        # 100 for capacity

        if resp_dec <= 100 and resp_dec >= 0:
            # valid
            self.set_capacity(resp_dec)

            return True
        else:
            PTLogger.debug("Invalid, not less than or equal to 100")
            return False

    def _process_discharging_time_i2c_resp(self, resp_dec):
        #   1800 for remaining time

        if resp_dec <= 1800:
            # valid
            self.set_time(resp_dec)
            return True
        else:
            PTLogger.debug("Invalid, not less than or equal to 1800")

    def _process_charging_time_i2c_resp(self, resp_dec):
        #   2400 for charging time

        if resp_dec <= 2400:
            # valid
            self.set_time(resp_dec)
            return True
        else:
            PTLogger.debug("Invalid, not less than or equal to 2400")
            return False

    def _attempt_read(self, data_to_get):
        successful_read = False
        resp = ""
        register = None
        try:
            register = self._get_battery_register_to_read(data_to_get)
            resp = self._bus.read_word_data(self._chip_address, register)
            successful_read = True
        except:
            pass

        return successful_read, resp, register

    def _get_battery_data(self, data_to_get):
        reattempt_sleep_s = float(_cycle_sleep_time / self._i2c_ctr._max)

        self._i2c_ctr.reset()
        while not self._i2c_ctr.maxed():
            self._i2c_ctr.increment()
            successful_read, resp, register = self._attempt_read(data_to_get)
            if successful_read:
                return self._parse_response(resp, register, data_to_get)
            # else:
                PTLogger.debug("Unsuccessful read...")
            sleep(reattempt_sleep_s)

        # Value was not fetched
        PTLogger.debug("Unable to read I2C after multiple attempts")
        return False


def start():
    global _main_thread
    global _run_main_thread

    if is_initialised():
        if _main_thread is None:
            _main_thread = Thread(target=_main_thread_loop)

        _run_main_thread = True
        _main_thread.start()
    else:
        PTLogger.error("Unable to start pi-topHUB SPI communication - run initialise() first!")


def stop():
    global _run_main_thread

    _run_main_thread = False
    _main_thread.join()


def is_initialised():
    return (_battery_state_handler is not None) and (_battery_state_handler.is_connected() is True)


def initialise(state):
    global _battery_state_handler

    try:
        _battery_state_handler = BatteryStateHandler(state)
        return True
    except Exception as e:
        PTLogger.error("Error initialising I2C. " + str(e))
        PTLogger.info(traceback.format_exc())
        _battery_state_handler = None
        return False


def communicate():
    if not is_initialised():
        PTLogger.error("I2C has not been initialised - call initialise() first")
        return False

    try:
        _battery_state_handler._refresh_state()
        return True
    except Exception as e:
        PTLogger.error("Error refreshing the state of the battery handler. " + str(e))
        PTLogger.info(traceback.format_exc())
        return False


def _main_thread_loop():
    '''
        ///////////////////////////
        // MAIN CODE STARTS HERE //
        ///////////////////////////
    '''

    while _run_main_thread:
        communicate()
        sleep(_cycle_sleep_time)


def set_speed(no_of_polls_per_second=4):
    global _cycle_sleep_time

    _cycle_sleep_time = float(1 / no_of_polls_per_second)
