"""Sensor entity for the JLEnergy integration."""
from __future__ import annotations

import os
import json
from collections import OrderedDict

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfVolume
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN


DEVICE = DeviceInfo(
    identifiers={(DOMAIN, "294b5a2e-363d-49d3-a10e-9ba03c532e84")},
    name="Water Meter",
    manufacturer="LiLi Industry",
    model="W001",
    sw_version="0.9",
)


class WaterYearlyUsageSensor(SensorEntity):
    _attr_name = "Water yearly usage"
    _attr_native_unit_of_measurement = UnitOfVolume.CUBIC_METERS
    _attr_device_class = SensorDeviceClass.WATER
    _attr_state_class = SensorStateClass.TOTAL
    _attr_unique_id = "6a3017f7-0acb-41af-8f52-6541861353ed"
    _attr_device_info = DEVICE

    def __init__(self, path) -> None:
        self.data_path = path

    def update(self) -> None:
        with open(os.path.join(self.data_path, "bjwater.data.json"), "r") as f:
            data = json.load(f)
            self._attr_native_value = sum(data["analysis"]["thisYear"])


class WaterYearlyFeeSensor(SensorEntity):
    _attr_name = "Water yearly fee"
    _attr_native_unit_of_measurement = "CNY"
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.TOTAL
    _attr_unique_id = "38ade376-6b57-4841-b52d-4869293b84bc"
    _attr_device_info = DEVICE

    def __init__(self, path) -> None:
        self.data_path = path

    def update(self) -> None:
        with open(os.path.join(self.data_path, "bjwater.data.json"), "r") as f:
            data = json.load(f, object_pairs_hook=OrderedDict)
            self._attr_native_value = list(data["yearly"].values())[-1]["amountTotal"]


class WaterMonthlyUsageSensor(SensorEntity):
    _attr_name = "Water monthly usage"
    _attr_native_unit_of_measurement = UnitOfVolume.CUBIC_METERS
    _attr_device_class = SensorDeviceClass.WATER
    _attr_state_class = SensorStateClass.TOTAL
    _attr_unique_id = "2bbb6483-5c4a-4a76-8bf6-3cc6dd062847"
    _attr_device_info = DEVICE

    def __init__(self, path) -> None:
        self.data_path = path

    def update(self) -> None:
        with open(os.path.join(self.data_path, "bjwater.data.json"), "r") as f:
            data = json.load(f, object_pairs_hook=OrderedDict)
            self._attr_native_value = list(data["monthly"].values())[0]["total"]


class WaterMonthlyFeeSensor(SensorEntity):
    _attr_name = "Water monthly fee"
    _attr_native_unit_of_measurement = "CNY"
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.TOTAL
    _attr_unique_id = "08a90855-9b9f-48ad-bfc1-c2cf2f72836b"
    _attr_device_info = DEVICE

    def __init__(self, path) -> None:
        self.data_path = path

    def update(self) -> None:
        with open(os.path.join(self.data_path, "bjwater.data.json"), "r") as f:
            data = json.load(f, object_pairs_hook=OrderedDict)
            self._attr_native_value = list(data["monthly"].values())[0]["amount"]
