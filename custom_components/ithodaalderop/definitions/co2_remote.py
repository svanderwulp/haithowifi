"""Definitions for Itho Remote sensors added to MQTT."""

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import PERCENTAGE, UnitOfRatio, UnitOfTemperature

from .base_definitions import IthoSensorEntityDescription

REMOTE_SENSOR_TEMPLATES = (
    IthoSensorEntityDescription(
        key="remote_co2",
        value_field="co2",
        device_class=SensorDeviceClass.CO2,
        native_unit_of_measurement=UnitOfRatio.PARTS_PER_MILLION,
        state_class=SensorStateClass.MEASUREMENT,
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        key="remote_temperature",
        value_field="temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        key="remote_humidity",
        value_field="hum",
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        key="remote_dew_point",
        value_field="dewpoint",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        key="remote_battery",
        value_field="battery",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        is_selected_entity=True,
    ),
)
