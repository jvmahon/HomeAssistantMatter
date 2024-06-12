"""Matter ModeSelect."""

from __future__ import annotations

from typing import Any

from chip.clusters import Objects as clusters
from matter_server.client.models import device_types

from homeassistant.components.select import (
    SelectEntity,
    SelectEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import MatterEntity
from .helpers import get_matter
from .models import MatterDiscoverySchema


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Matter ModeSelect from Config Entry."""
    matter = get_matter(hass)
    matter.register_platform_handler(Platform.SELECT, async_add_entities)


class MatterModeSelect(MatterEntity, SelectEntity):
    """Representation of a Matter select."""

    async def async_select_option(self, option: str) -> None:
        """Change the device mode"""
        
    @callback
    def _update_from_device(self) -> None:
        """Update from device."""
        '''This is from switch and is a placeholder that needs to be updated'''
        self._attr_is_on = self.get_matter_attribute_value(
            self._entity_info.primary_attribute
        )
        
    @property
    def options(self)->list[str]:
        return ["one", "two", "three"]

    @property
    def current_option(self) -> str:
        return "two"


# Discovery schema(s) to map Matter Attributes to HA entities
DISCOVERY_SCHEMAS = [
    MatterDiscoverySchema(
        platform=Platform.SELECT,
        entity_description=SelectEntityDescription(
            key="MatterModeSelect", name=None
        ),
        entity_class=MatterModeSelect,
        required_attributes=(
            clusters.ModeSelect.Attributes.Description,
            clusters.ModeSelect.Attributes.StandardNamespace,
            clusters.ModeSelect.Attributes.SupportedModes,
            clusters.ModeSelect.Attributes.CurrentMode,
        ),
    ),
]
