"""Sensor class for handling Remote sensors."""

import copy
import json
from json import JSONDecodeError
from typing import Any

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from ..const import _LOGGER, MQTT_DEFAULT_QOS_SUBSCRIBE
from ..definitions.co2_remote import REMOTE_SENSOR_TEMPLATES
from ..utils import get_mqtt_remote_topic
from .base_sensors import IthoBaseSensor


def get_co2_remote_sensors(config_entry: ConfigEntry) -> list[IthoBaseSensor]:
    """Create sensors for monitoring different remotes."""

    sensors: list[IthoBaseSensor] = []
    topic = get_mqtt_remote_topic(config_entry.data)

    for remote_number in range(1, 6):
        remote_name = config_entry.data.get(f"remote{remote_number}", "")

        if remote_name in ("", "Remote_" + str(remote_number)):
            continue

        for template in REMOTE_SENSOR_TEMPLATES:
            description = copy.deepcopy(template)
            description.topic = topic
            description.json_field = remote_name
            description.translation_placeholders = {"remote_name": remote_name}
            if description.value_field == "co2":
                description.unique_id = remote_name
                description.name = f"Remote - {remote_name} CO2"
            else:
                description.unique_id = f"{remote_name}_{description.value_field}"
            sensors.append(IthoSensorRemote(description, config_entry))

    return sensors


class IthoSensorRemote(IthoBaseSensor):
    """Representation of Itho add-on sensor for a Remote that is updated via MQTT."""

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""

        await mqtt.async_subscribe(
            self.hass,
            self.entity_description.topic,
            self.message_received,
            MQTT_DEFAULT_QOS_SUBSCRIBE,
        )

    @callback
    def message_received(self, message: mqtt.ReceiveMessage) -> None:
        """Handle a new MQTT message."""

        try:
            payload: dict[str, Any] = json.loads(message.payload)
        except (JSONDecodeError, TypeError):
            _LOGGER.warning(
                "Unable to decode remote MQTT message on topic %s", message.topic
            )
            return

        remote_name = self.entity_description.json_field
        value_field = self.entity_description.value_field

        remote_data = payload.get(remote_name)

        if not isinstance(remote_data, dict):
            value = None
        else:
            value = remote_data.get(value_field)

        self._attr_native_value = value
        self.async_write_ha_state()
