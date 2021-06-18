"""
Support for DoHome

Developed by Rave from hogc
"""
import logging
import socket
import json
from datetime import timedelta
from homeassistant.helpers.event import track_time_interval
import homeassistant.util.color as color_util
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_COLOR_TEMP,
    ATTR_EFFECT,
    ATTR_HS_COLOR,
    PLATFORM_SCHEMA,
    SUPPORT_BRIGHTNESS,
    SUPPORT_COLOR,
    LightEntity,
)

from . import (DOHOME_GATEWAY, DoHomeDevice)

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
    light_devices = []
    devices = DOHOME_GATEWAY.devices
    for (device_type, device_info) in devices.items():
        for device in device_info:
            _LOGGER.info(device)
            if(device['type'] == '_STRIPE' or device['type'] == '_DT-WYRGB'):
                light_devices.append(DoHomeLight(hass, device))
    
    if(len(light_devices) > 0):
        add_devices(light_devices)


class DoHomeLight(DoHomeDevice, LightEntity):

    def __init__(self, hass, device):

        self._device = device
        self._state = False
        self._rgb = (255, 255, 255)
        self._brightness = 100
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        DoHomeDevice.__init__(self, device['name'], device)

    @property
    def brightness(self):
        """Return the brightness of this light between 0..255."""
        return self._brightness

    @property
    def hs_color(self):
        """Return the color property."""
        return color_util.color_RGB_to_hs(*self._rgb)

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state

    @property
    def supported_features(self):
        """Return the supported features."""
        return SUPPORT_BRIGHTNESS | SUPPORT_COLOR

    def turn_on(self, **kwargs):
        """Turn the light on."""
        if ATTR_HS_COLOR in kwargs:
            self._rgb = color_util.color_hs_to_RGB(*kwargs[ATTR_HS_COLOR])

        if ATTR_BRIGHTNESS in kwargs:
            self._brightness = int(100 * kwargs[ATTR_BRIGHTNESS] / 255)

        self._state = True
        data = {
                "cmd":6,
                "r":int(50 * self._rgb[0] / 255)*self._brightness,
                "g":int(50 * self._rgb[1] / 255)*self._brightness,
                "b":int(50 * self._rgb[2] / 255)*self._brightness,
                "w":0,
                "m":0}
        op = json.dumps(data)
        self._send_cmd(self._device,'cmd=ctrl&devices={[' + self._device["sid"] + ']}&op=' + op + '}', 6)

    def turn_off(self, **kwargs):
        """Turn the light off."""
        self._state = False
        data = {
                "cmd":6,
                "r":0,
                "g":0,
                "b":0,
                "w":0,
                "m":0}
        op = json.dumps(data)
        self._send_cmd(self._device,'cmd=ctrl&devices={[' + self._device["sid"] + ']}&op=' + op + '}', 6)

    def _send_cmd(self, device, cmd, rtn_cmd):

        try:
            self._socket.settimeout(0.5)
            self._socket.sendto(cmd.encode(), (device["sta_ip"], 6091))
            data, addr = self._socket.recvfrom(1024)
        except socket.timeout:
            return None

        if data is None:
            return None
        _LOGGER.debug("result :%s", data.decode("utf-8"))
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