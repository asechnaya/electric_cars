import requests

from main_urls import DEFAULT_PARK, DEFAULT_DRIVE, DEFAULT_NEUTRAL, DEFAULT_REVERSE, MAIN_URL, SIGNALS_URL, UPDATE_ACC, \
    UPDATE_BATTERY, \
    UPDATE_BRAKE, UPDATE_GEAR_1, UPDATE_GEAR_2


def set_default_parking_voltage():
    for key, value in DEFAULT_PARK.items():
        payload = {"Voltage": value}
        requests.post(key, data=payload)


def set_default_drive_voltage():
    for key, value in DEFAULT_DRIVE.items():
        payload = {"Voltage": value}
        response = requests.post(key, data=payload)


def set_default_neutral_voltage():
    for key, value in DEFAULT_NEUTRAL.items():
        payload = {"Voltage": value}
        requests.post(key, data=payload)


def set_default_reverse_voltage():
    for key, value in DEFAULT_REVERSE.items():
        payload = {"Voltage": value}
        requests.post(key, data=payload)


def set_brake_released_pressed(brake_voltage=2):
    requests.post(UPDATE_BRAKE, data={"Voltage": brake_voltage})


def set_battery_voltage(battery):
    requests.post(UPDATE_BATTERY, data={"Voltage": battery})


def set_acceleration_voltage(acc_pedal):
    requests.post(UPDATE_ACC, data={"Voltage": acc_pedal})


def set_gear1_voltage(voltage):
    requests.post(UPDATE_GEAR_1, data={"Voltage": voltage})


def set_gear2_voltage(voltage):
    requests.post(UPDATE_GEAR_2, data={"Voltage": voltage})


def fetch_signals():
    return requests.get(SIGNALS_URL).json()


def fetch_pins():
    return requests.get(MAIN_URL).json()
