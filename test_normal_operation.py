import pytest
import requests

from parametrization import Parametrization

from main_urls import SIGNALS_URL, UPDATE_ACC
from utils import fetch_signals, set_acceleration_voltage, set_battery_voltage, set_brake_released_pressed, \
    set_default_drive_voltage, set_default_neutral_voltage, set_default_parking_voltage, set_default_reverse_voltage


class TestPark:
    @Parametrization.parameters('acc_pedal', 'battery', 'brake')
    @Parametrization.case('left margin', 1.0, 400.1, 2)
    @Parametrization.case('right margin', 1.9, 600, 2.5)
    @Parametrization.case('middle value', 1.6, 800, 2.9)
    def test_positive_doing_parking(self, api_connection, acc_pedal, battery, brake):
        set_default_parking_voltage()
        """ Переключились на парковку проверяем переключение передачи, тормоз нажат """
        set_acceleration_voltage(acc_pedal)
        set_brake_released_pressed(acc_pedal)
        pin = requests.get(SIGNALS_URL).json()
        assert pin[0]['Value'] == 'Park' and pin[1]['Value'] == '0 %'
        assert pin[2]['Value'] == 'Pressed' and pin[3]['Value'] == '0 Nm'
        assert pin[4]['Value'] == 'Ready'
        """ отпускаем тормоз """
        set_brake_released_pressed(brake)
        set_acceleration_voltage(acc_pedal)
        set_battery_voltage(battery)
        pin = requests.get(SIGNALS_URL).json()
        assert pin[0]['Value'] == 'Park' and pin[1]['Value'] == '0 %'
        assert pin[2]['Value'] == 'Released' and pin[3]['Value'] == '0 Nm'
        assert pin[4]['Value'] == 'Ready'


class TestNeutral:
    @Parametrization.parameters('acc_pedal', 'battery', 'brake')
    @Parametrization.case('left margin', 1.0, 400.1, 2)
    @Parametrization.case('right margin', 1.9, 600, 2.5)
    @Parametrization.case('middle value', 1.6, 800, 2.9)
    def test_positive_neutral(self, api_connection, acc_pedal, battery, brake):
        set_default_neutral_voltage()
        """ Переключились на нейтраль, тормоз нажат """
        requests.post(UPDATE_ACC, data={"Voltage": acc_pedal})
        pin = requests.get(SIGNALS_URL).json()
        assert pin[0]['Value'] == 'Neutral' and pin[1]['Value'] == '0 %'
        assert pin[2]['Value'] == 'Pressed' and pin[3]['Value'] == '0 Nm' and pin[4]['Value'] == 'Ready'
        """ отпустили тормоз """
        set_brake_released_pressed(brake)
        set_acceleration_voltage(acc_pedal)
        set_battery_voltage(battery)
        pin = fetch_signals()
        assert pin[0]['Value'] == 'Neutral' and pin[1]['Value'] == '0 %'
        assert pin[2]['Value'] == 'Released' and pin[3]['Value'] == '0 Nm'
        assert pin[4]['Value'] == 'Ready'


@pytest.mark.xfail
class TestDrive:
    @Parametrization.parameters('acc_pedal', 'battery')
    @Parametrization.case('left margin', 1.0, 400.1)
    @Parametrization.case('right margin', 1.9, 600)
    @Parametrization.case('middle value', 1.6, 800)
    def test_neutral_to_drive(self, api_connection, acc_pedal, battery):
        """ Из припаркованного положения переключаемся на нейтраль"""
        set_default_parking_voltage()
        """ Из нейтрального положения переключаемся на drive"""
        set_default_drive_voltage()
        set_brake_released_pressed()
        set_battery_voltage(battery)
        set_acceleration_voltage(acc_pedal)
        response = fetch_signals()
        assert response[0]['Value'] == 'Drive'
        assert response[1]['Value'] == '0 %'
        assert response[2]['Value'] == 'Released'
        assert response[3]['Value'] == '0 Nm'
        assert response[4]['Value'] == 'Ready'

    """ Поехали после переключения передач """

    @Parametrization.parameters('acc_pedal', 'acceleration', 'torque')
    @Parametrization.case('0% left margin', 1.0, "0 %", '0 Nm')
    @Parametrization.case('0% right margin', 1.9, "0 %", '0 Nm')
    @Parametrization.case('0% middle value', 1.6, "0 %", '0 Nm')
    @Parametrization.case('30% left margin', 2.0, "30 %", '3000 Nm')
    @Parametrization.case('30% right margin', 2.49, "30 %", '3000 Nm')
    @Parametrization.case('30% middle value', 2.2, "30 %", '3000 Nm')
    @Parametrization.case('50% left margin', 2.5, "50 %", '5000 Nm')
    @Parametrization.case('50% right margin', 2.99, "50 %", '5000 Nm')
    @Parametrization.case('50% middle value', 2.7, "50 %", '5000 Nm')
    @Parametrization.case('100% left margin', 3.0, "100 %", '10000 Nm')
    @Parametrization.case('100% right margin', 3.49, "100 %", '10000 Nm')
    @Parametrization.case('100% middle value', 3.2, "100 %", '10000 Nm')
    def test_positive_acc_pedal_during_drive(self, api_connection, acc_pedal, acceleration, torque):
        set_default_drive_voltage()
        """ отпускаем тормоз """
        set_brake_released_pressed()
        """Поехали"""
        set_acceleration_voltage(acc_pedal)
        pin = fetch_signals()
        assert pin[0]['Value'] == 'Drive' and pin[1]['Value'] == acceleration
        assert pin[2]['Value'] == 'Released' and pin[3]['Value'] == torque
        assert pin[4]['Value'] == 'Ready'
        """ Возникают проблемы при 100% ускорении """


@pytest.mark.xfail
class TestReverse:
    @Parametrization.parameters('acc_pedal', 'battery')
    @Parametrization.case('left margin', 1.0, 400.1)
    @Parametrization.case('right margin', 1.9, 600)
    @Parametrization.case('middle value', 1.6, 800)
    def test_going_reverse(self, api_connection, acc_pedal, battery):
        """ Из положения park переключаемся на нейтраль"""
        set_default_parking_voltage()
        set_default_neutral_voltage()
        """ Из neutral положения переключаемся на reverse"""
        set_default_reverse_voltage()
        set_brake_released_pressed()
        set_battery_voltage(battery)
        set_acceleration_voltage(acc_pedal)
        pin = fetch_signals()
        assert pin[0]['Value'] == 'Reverse' and pin[1]['Value'] == '0 %'
        assert pin[2]['Value'] == 'Released' and pin[3]['Value'] == '0 Nm'
        assert pin[4]['Value'] == 'Ready'

    """ Поехали после переключения передач """

    @Parametrization.parameters('acc_pedal', 'acceleration', 'torque')
    @Parametrization.case('0% left margin', 1.0, "0 %", '0 Nm')
    @Parametrization.case('0% right margin', 1.9, "0 %", '0 Nm')
    @Parametrization.case('0% middle value', 1.6, "0 %", '0 Nm')
    @Parametrization.case('30% left margin', 2.0, "30 %", '3000 Nm')
    @Parametrization.case('30% right margin', 2.4, "30 %", '3000 Nm')
    @Parametrization.case('30% middle value', 2.2, "30 %", '3000 Nm')
    @Parametrization.case('50% left margin', 2.5, "50 %", '5000 Nm')
    @Parametrization.case('50% right margin', 2.99, "50 %", '5000 Nm')
    @Parametrization.case('50% middle value', 2.7, "50 %", '5000 Nm')
    @Parametrization.case('100% left margin', 3.0, "100 %", '10000 Nm')
    @Parametrization.case('100% right margin', 3.4, "100 %", '10000 Nm')
    @Parametrization.case('100% middle value', 3.2, "100 %", '10000 Nm')
    def test_positive_acc_pedal_during_drive(self, api_connection, acc_pedal, acceleration, torque):
        set_default_reverse_voltage()
        """ отпускаем тормоз """
        set_brake_released_pressed()
        """Поехали"""
        set_acceleration_voltage(acc_pedal)
        """ Возникают проблемы при 100% ускорении """
        pin = fetch_signals()
        assert pin[0]['Value'] == 'Reverse' and pin[1]['Value'] == acceleration
        assert pin[2]['Value'] == 'Released' and pin[3]['Value'] == torque
        assert pin[4]['Value'] == 'Ready'