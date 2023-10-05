"""Sensor entity for the JLEnergy integration."""
from __future__ import annotations

import os
import json

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfEnergy
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN


DEVICE = DeviceInfo(
    identifiers={(DOMAIN, "a22fb4ad-e6c3-4c50-9fa5-72b1f66d0d06")},
    name="Electricity Meter",
    manufacturer="LiLi Industry",
    model="E001",
    sw_version="0.9",
)


class ElectricityDailyUsageSensor(SensorEntity):
    _attr_name = "Electricity daily usage"
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL
    _attr_unique_id = "9b391d76-57cd-4498-94c8-ad195489de95"
    _attr_device_info = DEVICE

    def __init__(self, path) -> None:
        self.data_path = path

    def update(self) -> None:
        with open(os.path.join(self.data_path, "sgcc.data.json"), "r") as f:
            data = json.load(f)
            self._attr_native_value = data["daily"][-1]["PAP_R"]


class ElectricityMonthlyUsageSensor(SensorEntity):
    _attr_name = "Electricity monthly usage"
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL
    _attr_unique_id = "026cf2f9-9f78-4868-9a76-1250e1aa8e21"
    _attr_device_info = DEVICE

    def __init__(self, path) -> None:
        self.data_path = path

    def update(self) -> None:
        with open(os.path.join(self.data_path, "sgcc.data.json"), "r") as f:
            data = json.load(f)
            self._attr_native_value = data["overview"]["billDetails"][0]["SETTLE_APQ"]


class ElectricityMonthlyFeeSensor(SensorEntity):
    _attr_name = "Electricity monthly fee"
    _attr_native_unit_of_measurement = "CNY"
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.TOTAL
    _attr_unique_id = "43047ec5-ad76-467e-9751-c833181354a6"
    _attr_device_info = DEVICE

    def __init__(self, path) -> None:
        self.data_path = path

    def update(self) -> None:
        with open(os.path.join(self.data_path, "sgcc.data.json"), "r") as f:
            data = json.load(f)
            self._attr_native_value = data["overview"]["billDetails"][0]["T_AMT"]


class ElectricityBalanceSensor(SensorEntity):
    _attr_name = "Electricity account balance"
    _attr_native_unit_of_measurement = "CNY"
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.TOTAL
    _attr_unique_id = "5da7442a-5993-454e-be4d-7c473a9b467b"
    _attr_device_info = DEVICE

    def __init__(self, path) -> None:
        self.data_path = path

    def update(self) -> None:
        with open(os.path.join(self.data_path, "sgcc.data.json"), "r") as f:
            data = json.load(f)
            self._attr_native_value = float(data["overview"]["balanceSheet"])
