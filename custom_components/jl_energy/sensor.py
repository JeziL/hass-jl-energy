"""Sensor entity for the JLEnergy integration."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .ElectricityDevice import *
from .WaterDevice import *
from .const import CONF_DATAPATH


async def async_setup_entry(
    hass: HomeAssistant,
    config: ConfigEntry,
    add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    data_path = config.data.get(CONF_DATAPATH)
    add_entities(
        [
            ElectricityDailyUsageSensor(data_path),
            WaterMonthlyUsageSensor(data_path),
            WaterYearlyUsageSensor(data_path),
            WaterYearlyFeeSensor(data_path),
        ]
    )
