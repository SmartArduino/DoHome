"""
Support for DoHome

Developed by Rave from hogc
"""
import logging
import json
import socket
from datetime import timedelta
from homeassistant.helpers.event import track_time_interval

from homeassistant.const import TEMP_CELSIUS

from . import (DOHOME_GATEWAY, DoHomeDevice)

_LOGGER = logging.getLogger(__name__)



TEMPERATURE_KEY = "temp"
HUMIDITY_KEY = "humi"
ILLUMINATION_KEY = "illu"

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Perform the setup for DoHome devices."""
    sensor_devices = []
    devices = DOHOME_GATEWAY.devices
    for (device_type, device_info) in devices.items():
        for device in device_info:
            _LOGGER.info(device)
            if(device['type'] == '_THIMR'):
                sensor_devices.append(DoHomeSensor(hass, 'Temperature_' + device['sid'], TEMPERATURE_KEY, device))
                sensor_devices.append(DoHomeSensor(hass, 'Humidity_' + device['sid'], HUMIDITY_KEY, device))
            if(device['type'] == '_THIMR'):
                sensor_devices.append(DoHomeSensor(hass, 'illumination_' + device['sid'], ILLUMINATION_KEY, device))
    
    if(len(sensor_devices) > 0):
        add_devices(sensor_devices)


class DoHomeSensor(DoHomeDevice):
    """Representation of a XiaomiSensor."""

    def __init__(self, hass, name, data_key, device):
        self._device = device
        self.current_value = None
        self._data_key = data_key
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        DoHomeDevice.__init__(self, name ,device)

        track_time_interval(hass, self.updateStatus, timedelta(seconds=1))

    @property
    def _is_humidity(self):
        return self._data_key == HUMIDITY_KEY

    @property
    def _is_temperature(self):
        return self._data_key == TEMPERATURE_KEY

    @property
    def _is_illumination(self):
        return self._data_key == ILLUMINATION_KEY


    @property
    def available(self):
        """Return True if entity is available."""
        if self._is_temperature and self.current_value != 100:
            return True
        elif self._is_humidity and self.current_value != 0:
            return True
        elif self._is_illumination and self.current_value != -1:
            return True
        return False

    @property
    def state(self):
        """Return the name of the sensor."""
        return self.current_value

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        if self._is_temperature and self.current_value != 100:
            return TEMP_CELSIUS
        elif self._is_humidity and self.current_value != 0:
            return '%'
        elif self._is_illumination and self.current_value != -1:
            return ''

    def updateStatus(self, now):
        resp = self._send_cmd(self._device, 'cmd=ctrl&devices={[' + self._device["sid"] + ']}&op={"cmd":25}', 25)
        if resp is not None and self._data_key in resp:
    
            self.current_value = int(resp[self._data_key])
            # _LOGGER.info("%s :%s", self._data_key, self.current_value)
            self.schedule_update_ha_state()

    def _send_cmd(self, device, cmd, rtn_cmd):

        try:
            self._socket.settimeout(0.5)
            self._socket.sendto(cmd.encode(), (device["sta_ip"], 6091))
            data, addr = self._socket.recvfrom(1024)
        except socket.timeout:
            return None

        if data is None:
            return None
        dic = {i.split("=")[0]:i.split("=")[1] for i in data.decode("utf-8").split("&")}
        resp = []
        if(dic["dev"][8:12] == device["sid"]):
            resp = json.loads(dic["op"])
            if resp['cmd'] != rtn_cmd:
                _LOGGER.debug("Non matching response. Expecting %s, but got %s", rtn_cmd, resp['cmd'])
                return None
            return resp
        else:
            _LOGGER.debug("Non matching response. device %s, but got %s", device["sid"], dic["dev"][8:12])
            return None
