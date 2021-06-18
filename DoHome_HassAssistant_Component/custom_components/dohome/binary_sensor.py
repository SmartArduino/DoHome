"""
Support for DoHome

Developed by Rave from hogc
"""
import logging
import json
import socket
from datetime import timedelta
from homeassistant.helpers.event import track_time_interval

from homeassistant.components.binary_sensor import BinarySensorEntity

from . import (DOHOME_GATEWAY, DoHomeDevice)

NO_CLOSE = 'no_close'
ATTR_OPEN_SINCE = 'Open since'

MOTION = 'motion'
NO_MOTION = 'no_motion'
ATTR_NO_MOTION_SINCE = 'No motion since'


_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Perform the setup for DoHome devices."""
    sensor_devices = []
    devices = DOHOME_GATEWAY.devices
    for (device_type, device_info) in devices.items():
        for device in device_info:
            _LOGGER.info(device)
            if(device['type'] == '_MOTION' or device['type'] == '_THIMR'):
                sensor_devices.append(MotionSensor(hass, device))
    
    if(len(sensor_devices) > 0):
        add_devices(sensor_devices)


class MotionSensor(DoHomeDevice, BinarySensorEntity):

    def __init__(self, hass, device):
        self._device = device
        self._state = False
        self._data_key = 'motion'
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        DoHomeDevice.__init__(self, 'Motion_' + device['sid'], device)

        track_time_interval(hass, self.updateStatus, timedelta(seconds=1))

    @property
    def device_class(self):
        """Return the class of binary sensor."""
        return 'motion'

    @property
    def is_on(self):
        """Return true if sensor is on."""
        return self._state


    def updateStatus(self, now):
        resp = self._send_cmd(self._device, 'cmd=ctrl&devices={[' + self._device["sid"] + ']}&op={"cmd":25}', 25)
        if resp is not None and self._data_key in resp:
            if resp[self._data_key] == True:
                self._state = True
            else:
                self._state = False
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
