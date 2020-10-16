import logging
import socket
import json
from datetime import timedelta
from homeassistant.helpers.event import track_time_interval

from homeassistant.components.switch import SwitchEntity
try:
    from homeassistant.components.dohome import (DOHOME_GATEWAY, DoHomeDevice)
except ImportError:
    from custom_components.dohome import (DOHOME_GATEWAY, DoHomeDevice)

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
    switch_devices = []
    devices = DOHOME_GATEWAY.devices
    for (device_type, device_info) in devices.items():
        for device in device_info:
            _LOGGER.info(device)
            if(device['type'] == '_DT-PLUG'):
                switch_devices.append(DoHomeSwitch(hass, device["name"], "soft_poweroff", device))
            if(device['type'] == '_THIMR'):
                switch_devices.append(DoHomeSwitch(hass, device["name"], "relay", device))
            if(device['type'] == '_REALY2'):    
                switch_devices.append(DoHomeSwitch(hass, "Relay_" + device["sid"] + '_1', "relay1", device))
                switch_devices.append(DoHomeSwitch(hass, "Relay_" + device["sid"] + '_2', "relay2", device))
            if(device['type'] == '_REALY4'):    
                switch_devices.append(DoHomeSwitch(hass, "Relay_" + device["sid"] + '_1', "relay1", device))
                switch_devices.append(DoHomeSwitch(hass, "Relay_" + device["sid"] + '_2', "relay2", device))
                switch_devices.append(DoHomeSwitch(hass, "Relay_" + device["sid"] + '_3', "relay3", device))
                switch_devices.append(DoHomeSwitch(hass, "Relay_" + device["sid"] + '_4', "relay4", device))
    
    if(len(switch_devices) > 0):
        add_devices(switch_devices)


class DoHomeSwitch(DoHomeDevice, SwitchEntity):

    def __init__(self, hass, name, data_key, device):
        self._device = device
        self._state = False
        self._data_key = data_key
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        DoHomeDevice.__init__(self, name, device)

        track_time_interval(hass, self.updateStatus, timedelta(seconds=1))


    @property
    def is_on(self):
        """Return true if plug is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self._state = True
        if(self._device['type'] == '_DT-PLUG' or self._device['type'] == '_THIMR'):
            self._send_cmd(self._device,'cmd=ctrl&devices={[' + self._device["sid"] + ']}&op={"cmd":5,"op":1 }', 5)
        if(self._device['type'] == '_REALY2' or self._device['type'] == '_REALY4'):
            self._send_cmd(self._device, 'cmd=ctrl&devices={[' + self._device["sid"] + ']}&op={"cmd":5,"'+ self._data_key +'":1 }', 5)

    def turn_off(self):
        """Turn the switch off."""
        self._state = False
        if(self._device['type'] == '_DT-PLUG' or self._device['type'] == '_THIMR'):
            self._send_cmd(self._device, 'cmd=ctrl&devices={[' + self._device["sid"] + ']}&op={"cmd":5,"op":0 }', 5)
        if(self._device['type'] == '_REALY2' or self._device['type'] == '_REALY4'): 
            self._send_cmd(self._device, 'cmd=ctrl&devices={[' + self._device["sid"] + ']}&op={"cmd":5,"'+ self._data_key +'":0 }', 5)

    def updateStatus(self, now):
        resp = self._send_cmd(self._device, 'cmd=ctrl&devices={[' + self._device["sid"] + ']}&op={"cmd":25}', 25)
        if resp is not None and self._data_key in resp:
            if(self._device['type'] == '_DT-PLUG'):
                if(resp[self._data_key]):
                    if(self._state != False):
                        self._state = False
                        self.schedule_update_ha_state()
                else:
                    if(self._state != True):
                        self._state = True
                        self.schedule_update_ha_state()
            else:
                if(resp[self._data_key]):
                    if(self._state != True):
                        self._state = True
                        self.schedule_update_ha_state()
                else:
                    if(self._state != False):
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