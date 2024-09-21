"""Sensor entity for the JLEnergy integration."""
from __future__ import annotations
import os
import json
import sqlite3
from datetime import datetime

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
    _attr_extra_state_attributes = { "daily_values": [], "daily_timestamps": [] }
    _unrecorded_attributes = frozenset(["daily_values", "daily_timestamps"])

    def __init__(self, path) -> None:
        self.data_path = path
    
    def read_daily_usage_from_db(self, db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if tables:
            first_table = tables[0][0]
            cursor.execute(f"SELECT date, usage FROM {first_table}")
            rows = cursor.fetchall()
            dates = [row[0] for row in rows]
            usages = [row[1] for row in rows]
            conn.close()
            return dates, usages
        conn.close()
        return [], []

    def update(self) -> None:
        self._attr_native_value = 0
        with open(os.path.join(self.data_path, "external_api.config.json"), "r") as f:
            data = json.load(f)
            dates, usages = self.read_daily_usage_from_db(data["sgcc"]["db_path"])
            self._attr_extra_state_attributes["daily_values"] = usages
            self._attr_extra_state_attributes["daily_timestamps"] = [int(datetime.strptime(date, '%Y-%m-%d').timestamp()) for date in dates]
