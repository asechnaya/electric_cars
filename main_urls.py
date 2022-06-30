MAIN_URL = "http://localhost:8099/api/pins"
SIGNALS_URL = "http://localhost:8099/api/signals"

UPDATE_GEAR_1 = "{0}/{1}/update_pin".format(MAIN_URL, 1)
UPDATE_GEAR_2 = "{0}/{1}/update_pin".format(MAIN_URL, 2)
UPDATE_ACC = "{0}/{1}/update_pin".format(MAIN_URL, 3)
UPDATE_BRAKE = "{0}/{1}/update_pin".format(MAIN_URL, 4)
UPDATE_BATTERY = "{0}/{1}/update_pin".format(MAIN_URL, 5)

DEFAULT_DRIVE = {
    UPDATE_GEAR_1: 3.12,
    UPDATE_GEAR_2: 0.67,
    UPDATE_ACC: 1.0,
    UPDATE_BRAKE: 1.0,
    UPDATE_BATTERY: 600
}

DEFAULT_PARK = {
    UPDATE_GEAR_1: 0.67,
    UPDATE_GEAR_2: 3.12,
    UPDATE_ACC: 1.0,
    UPDATE_BRAKE: 1.9,
    UPDATE_BATTERY: 600
}

DEFAULT_NEUTRAL = {
    UPDATE_GEAR_1: 1.48,
    UPDATE_GEAR_2: 3.12,
    UPDATE_ACC: 1.0,
    UPDATE_BRAKE: 1.9,
    UPDATE_BATTERY: 600
}


DEFAULT_REVERSE = {
    UPDATE_GEAR_1: 2.28,
    UPDATE_GEAR_2: 1.48,
    UPDATE_ACC: 1.0,
    UPDATE_BRAKE: 1.9,
    UPDATE_BATTERY: 600
}
