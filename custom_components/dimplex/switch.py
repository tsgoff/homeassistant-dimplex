"""Switch platform for Dimplex integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, VarID
from .coordinator import DimplexCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Dimplex switch entities."""
    coordinator: DimplexCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        DimplexBypassSwitch(coordinator),
    ])


class DimplexBypassSwitch(CoordinatorEntity[DimplexCoordinator], SwitchEntity):
    """Representation of the Dimplex ventilation bypass switch."""

    _attr_has_entity_name = True
    _attr_translation_key = "ventilation_bypass"
    _attr_device_class = SwitchDeviceClass.SWITCH
    _attr_icon = "mdi:valve"

    def __init__(self, coordinator: DimplexCoordinator) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.client.device_id}_bypass_switch"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.client.device_id)},
            "name": "Dimplex Heat Pump",
            "manufacturer": "Dimplex",
            "model": "Heat Pump",
        }

    @property
    def is_on(self) -> bool | None:
        """Return True if bypass is enabled."""
        value = self.coordinator.get_value(VarID.VENTILATION_BYPASS_SWITCH)
        if value is None:
            return None
        return str(value) == "1"

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the bypass."""
        _LOGGER.debug("Turning on ventilation bypass")
        await self.coordinator.client.set_ventilation_bypass(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the bypass."""
        _LOGGER.debug("Turning off ventilation bypass")
        await self.coordinator.client.set_ventilation_bypass(False)
        await self.coordinator.async_request_refresh()
