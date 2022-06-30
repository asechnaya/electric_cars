import pytest
from parametrization import Parametrization

from main_urls import DEFAULT_NEUTRAL
from utils import fetch_pins, fetch_signals, set_acceleration_voltage, set_battery_voltage, set_brake_released_pressed, \
    set_default_drive_voltage, set_default_neutral_voltage, set_default_parking_voltage, set_gear1_voltage


@pytest.mark.xfail
@Parametrization.parameters('acc_pedal', 'battery', 'brake', 'acc_pos')
@Parametrization.case('error left margin 1', 1.9, 0.1, 2.9, '0 %')
@Parametrization.case('error middle margin 2', 2.4, 200, 2.9, '30 %')
@Parametrization.case('error right margin 3', 2.9, 400, 2.9, '50 %')
class TestMotor:
    """Нетипичные режимы работы мотора - NotReady и Error"""

    GearPosition = 'Neutral'
    AccPedalPos = 'Error'
    BrakePedalState = 'Error'
    ReqTorque = '0 Nm'
    BatteryState = 'Error'
    Gear_1 = 0
    Gear_2 = 0
    AccPedal = 0
    BrakePedal = 0

    def test_battery_error(self, api_connection, acc_pedal, battery, brake, acc_pos):
        """ Переключились на нейтраль, тормоз нажат """
        set_default_drive_voltage()
        set_acceleration_voltage(acc_pedal)
        set_battery_voltage(battery)
        signals = fetch_signals()
        assert signals[0]['Value'] == self.GearPosition and signals[1]['Value'] == self.AccPedalPos
        assert signals[2]['Value'] == self.BrakePedalState and signals[3]['Value'] == self.ReqTorque
        assert signals[4]['Value'] == self.BatteryState
        pin = fetch_pins()
        assert pin[0]['Voltage'] == self.Gear_1 and pin[1]['Voltage'] == self.Gear_2
        assert pin[2]['Voltage'] == self.AccPedal and pin[3]['Voltage'] == self.BrakePedal
        """ переключение передач не возможно т.е. напряжение не поменяется """
        set_brake_released_pressed(brake)
        set_gear1_voltage(1)
        pin = fetch_signals()
        assert pin[0]['Voltage'] == self.Gear_1 and pin[1]['Voltage'] == self.Gear_2
        assert pin[2]['Voltage'] == self.AccPedal and pin[3]['Voltage'] == self.BrakePedal

    def test_battery_not_ready(self, api_connection, acc_pedal, battery, brake, acc_pos):
        """ Переключились на нейтраль, тормоз нажат """
        set_default_neutral_voltage()
        set_acceleration_voltage(acc_pedal)
        set_battery_voltage(battery)
        signals = fetch_signals()
        assert signals[0]['Value'] == self.GearPosition and signals[1]['Value'] == acc_pos
        assert signals[2]['Value'] == 'Pressed' and signals[3]['Value'] == self.ReqTorque
        assert signals[4]['Value'] == 'NotReady'
        """ отпустили тормоз """
        set_gear1_voltage(3.12)
        signals = fetch_signals()
        assert signals[0]['Value'] == self.GearPosition and signals[1]['Value'] == acc_pos
        assert signals[2]['Value'] == 'Pressed' and signals[3]['Value'] == self.ReqTorque
        assert signals[4]['Value'] == 'NotReady'
        pin = fetch_signals()
        assert pin[0]['Voltage'] == DEFAULT_NEUTRAL['UPDATE_GEAR_1']


@pytest.mark.xfail
class TestIdling:
    """ Увеличие газа при холостом ходу (когда машина на нейтриали или на паркинге """

    @Parametrization.parameters('acc_pedal', 'acceleration', 'torque')
    @Parametrization.case('0% left margin', 1.0, "0 %", '0 Nm')
    @Parametrization.case('0% right margin', 1.9, "0 %", '0 Nm')
    @Parametrization.case('0% middle value', 1.6, "0 %", '0 Nm')
    @Parametrization.case('30% left margin', 2.0, "30 %", '0 Nm')
    @Parametrization.case('30% right margin', 2.4, "30 %", '0 Nm')
    @Parametrization.case('30% middle value', 2.2, "30 %", '0 Nm')
    @Parametrization.case('50% left margin', 2.5, "50 %", '0 Nm')
    @Parametrization.case('50% right margin', 2.99, "50 %", '0 Nm')
    @Parametrization.case('50% middle value', 2.7, "50 %", '0 Nm')
    @Parametrization.case('100% left margin', 3.0, "100 %", '0 Nm')
    @Parametrization.case('100% right margin', 3.4, "100 %", '0 Nm')
    @Parametrization.case('100% middle value', 3.2, "100 %", '0 Nm')
    def test_idling(self, api_connection, acc_pedal, acceleration, torque):
        # Паркинг
        set_default_parking_voltage()
        set_acceleration_voltage(acc_pedal)
        signal = fetch_signals()
        assert signal[0]['Value'] == 'Park' and signal[1]['Value'] == acceleration
        assert signal[2]['Value'] == 'Pressed' and signal[3]['Value'] == torque
        assert signal[4]['Value'] == 'Ready'

        # Нейтралка
        set_default_neutral_voltage()
        set_acceleration_voltage(acc_pedal)
        signal = fetch_signals()
        assert signal[0]['Value'] == 'Neutral' and signal[1]['Value'] == acceleration
        assert signal[2]['Value'] == 'Pressed' and signal[3]['Value'] == torque
        assert signal[4]['Value'] == 'Ready'
