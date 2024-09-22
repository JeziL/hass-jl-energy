"""Sensor entity for the JLEnergy integration."""
from __future__ import annotations

import os
import json

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass
)
from homeassistant.components.binary_sensor import (BinarySensorEntity, BinarySensorDeviceClass)
from homeassistant.const import (UnitOfVolume, UnitOfElectricPotential)
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN


DEVICE = DeviceInfo(
    identifiers={(DOMAIN, "e2324487-d53b-4e34-8d60-8092d83cbbac")},
    name="Gas Meter",
    manufacturer="LiLi Industry",
    model="G001",
    sw_version="0.9",
)


class GasAccountBalanceSensor(SensorEntity):
    _attr_name = "Gas account balance"
    _attr_native_unit_of_measurement = "CNY"
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.TOTAL
    _attr_unique_id = "38678eac-04cf-4b0b-8a09-a180a4fe51ff"
    _attr_device_info = DEVICE

    def __init__(self, path) -> None:
        self.data_path = path

    def update(self) -> None:
        with open(os.path.join(self.data_path, "bjgas.data.json"), "r") as f:
            data = json.load(f)
            self._attr_native_value = data["balance"]


class GasYearlyUsageSensor(SensorEntity):
    _attr_name = "Gas yearly usage"
    _attr_native_unit_of_measurement = UnitOfVolume.CUBIC_METERS
    _attr_device_class = SensorDeviceClass.GAS
    _attr_state_class = SensorStateClass.TOTAL
    _attr_unique_id = "64836f09-da12-427d-8e92-1eeec939d3f5"
    _attr_device_info = DEVICE

    def __init__(self, path) -> None:
        self.data_path = path

    def update(self) -> None:
        with open(os.path.join(self.data_path, "bjgas.data.json"), "r") as f:
            data = json.load(f)
            self._attr_native_value = data["yearlyTotal"]


class GasLevel1RemainSensor(SensorEntity):
    _attr_name = "Gas level 1 remain"
    _attr_native_unit_of_measurement = UnitOfVolume.CUBIC_METERS
    _attr_device_class = SensorDeviceClass.GAS
    _attr_state_class = SensorStateClass.TOTAL
    _attr_unique_id = "069a1a0f-2209-4b5a-bb76-281bb5e26d31"
    _attr_device_info = DEVICE

    def __init__(self, path) -> None:
        self.data_path = path

    def update(self) -> None:
        with open(os.path.join(self.data_path, "bjgas.data.json"), "r") as f:
            data = json.load(f)
            self._attr_native_value = data["level1Remain"]


class GasLevel2RemainSensor(SensorEntity):
    _attr_name = "Gas level 2 remain"
    _attr_native_unit_of_measurement = UnitOfVolume.CUBIC_METERS
    _attr_device_class = SensorDeviceClass.GAS
    _attr_state_class = SensorStateClass.TOTAL
    _attr_unique_id = "3ab4c54a-9885-46b8-8c20-f69edee6c62c"
    _attr_device_info = DEVICE

    def __init__(self, path) -> None:
        self.data_path = path

    def update(self) -> None:
        with open(os.path.join(self.data_path, "bjgas.data.json"), "r") as f:
            data = json.load(f)
            self._attr_native_value = data["level2Remain"]


class GasValveBinarySensor(BinarySensorEntity):
    _attr_name = "Gas valve status"
    _attr_device_class = BinarySensorDeviceClass.OPENING
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_unique_id = "43c31b95-0f25-4320-a460-657a3a7f64c8"
    _attr_device_info = DEVICE

    def __init__(self, path) -> None:
        self.data_path = path

    def update(self) -> None:
        with open(os.path.join(self.data_path, "bjgas.data.json"), "r") as f:
            data = json.load(f)
            self._attr_is_on = data["valveSwitch"]


class GasValveBatterySensor(SensorEntity):
    _attr_name = "Gas valve battery"
    _attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_unique_id = "766abc13-c1c6-46e6-ad62-d48058e07c26"
    _attr_device_info = DEVICE

    def __init__(self, path) -> None:
        self.data_path = path

    def update(self) -> None:
        with open(os.path.join(self.data_path, "bjgas.data.json"), "r") as f:
            data = json.load(f)
            self._attr_native_value = data["valveBattery"]


class GasDailyUsageSensor(SensorEntity):
    _attr_name = "Gas daily usage"
    _attr_native_unit_of_measurement = UnitOfVolume.CUBIC_METERS
    _attr_device_class = SensorDeviceClass.GAS
    _attr_state_class = SensorStateClass.TOTAL
    _attr_unique_id = "198b6bcd-8cc0-408d-8ef6-86e51f3ea94c"
    _attr_device_info = DEVICE
    _attr_extra_state_attributes = { "daily_values": [], "daily_timestamps": [] }
    _unrecorded_attributes = frozenset(["daily_values", "daily_timestamps"])

    def __init__(self, path) -> None:
        self.data_path = path

    def update(self) -> None:
        with open(os.path.join(self.data_path, "bjgas.data.json"), "r") as f:
            data = json.load(f)
            self._attr_native_value = data["weekAmounts"][-1]
            self._attr_extra_state_attributes["daily_values"] = data["weekAmounts"]
            self._attr_extra_state_attributes["daily_timestamps"] = data["weekTimes"]
