"""Matter Number Inputs."""

from __future__ import annotations

from dataclasses import dataclass

from chip.clusters import Objects as clusters
from chip.clusters.Types import Nullable, NullValue
from matter_server.common.helpers.util import create_attribute_path_from_attribute

from homeassistant.components.time import (
    TimeEntity,
    TimeEntityDescription,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    Platform, 
    EntityCategory
)

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import MatterEntity, MatterEntityDescription
from .helpers import get_matter
from .models import MatterDiscoverySchema



async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Matter Number Input from Config Entry."""
    matter = get_matter(hass)
    matter.register_platform_handler(Platform.TIME, async_add_entities)

@dataclass(frozen=True)
class MatterTimeEntityDescription(TimeEntityDescription, MatterEntityDescription):
    """Describe Matter Number Input entities."""


class MatterTime(MatterEntity, TimeEntity):
    """Representation of a Matter Number INput."""
    """Representation of a Matter select."""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the entity."""
        super().__init__(*args, **kwargs)
        # fill the event types based on the features the switch supports
        self._attr_name =   self.entity_description.name + " EP " + str(self._endpoint.endpoint_id)

        
    # entity_description: MatterTimeEntityDescription
    
    async def async_set_native_value(self, value: float) -> None:
        """Update the current value"""
        matter_attribute = ( self._entity_info.primary_attribute )


    @callback
    def _update_from_device(self) -> None:
        """Update from device."""
        value = self.get_matter_attribute_value(self._entity_info.primary_attribute)
        if value in (None, NullValue):
            value = None
        elif value_convert := self.entity_description.measurement_to_ha:
            value = value_convert(value)
        self._attr_native_value = value
        
        

# Discovery schema(s) to map Matter Attributes to HA entities
DISCOVERY_SCHEMAS = [
    MatterDiscoverySchema(
        platform=Platform.TIME,
        entity_description=MatterTimeEntityDescription(
            key="OffTransitionTime",
            entity_category=EntityCategory.CONFIG,
            name="OffTransitionTime",
        ),
        entity_class=MatterTime,
        required_attributes=(
            clusters.LevelControl.Attributes.OffTransitionTime,
        ),
    ),
]
