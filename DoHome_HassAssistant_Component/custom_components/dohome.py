import socket
import json
import logging
import struct
import platform
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from threading import Thread
from collections import defaultdict
from homeassistant.helpers import discovery
from homeassistant.helpers.entity import Entity

DOMAIN = 'dohome'
CONF_GATEWAYS = 'discovery_ip'
CONF_DISCOVERY_RETRY = 'discovery_retry'

DISCOVERY_IP = ''
DEFAULT_DISCOVERY_IP = '192.168.1.255'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_GATEWAYS, default=DEFAULT_DISCOVERY_IP): cv.string,
        vol.Optional(CONF_DISCOVERY_RETRY, default=2): cv.positive_int
    })
}, extra=vol.ALLOW_EXTRA)

DOHOME_COMPONENTS = [('switch', 'dohomeswitch'), ('light','dohomelight' ), ('sensor','dohomesensor' ), ('binary_sensor','dohomebinarysensor' )]
DOHOME_GATEWAY = None

_LOGGER = logging.getLogger(__name__)

def setup(hass, config):

    global DISCOVERY_IP
    DISCOVERY_IP = config[DOMAIN][CONF_GATEWAYS]
    discovery_retry = config[DOMAIN][CONF_DISCOVERY_RETRY]

    if(DISCOVERY_IP == DEFAULT_DISCOVERY_IP):
        hostname = socket.getfqdn(socket.gethostname())
        hosts = socket.gethostbyname_ex(hostname)
        for add in hosts[2]:
            if(add[0:8] == '192.168.'):
                addlist = add.split(".")
                DISCOVERY_IP = addlist[0] + '.' + addlist[1] + '.' + addlist[2] + '.255'
    _LOGGER.info("DoHome discovery_ip:%s",DISCOVERY_IP)
    
    global DOHOME_GATEWAY
    DOHOME_GATEWAY = DoHomeGateway()

    for _ in range(discovery_retry):
        DOHOME_GATEWAY._discover_devices()

    for component, component_dir in DOHOME_COMPONENTS:
        discovery.load_platform(hass, component, component_dir, {}, config)

    return True

class DoHomeGateway:
    GATEWAY_DISCOVERY_PORT = 6091
    SOCKET_BUFSIZE = 1024

    devices = defaultdict(list)

    def _discover_devices(self):

        _socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _socket.bind(('', self.GATEWAY_DISCOVERY_PORT))

        try:
            _socket.sendto('cmd=ping\r\n'.encode(),(DISCOVERY_IP, self.GATEWAY_DISCOVERY_PORT))
            _socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            _socket.settimeout(1.0)

            while True:
                data, addr = _socket.recvfrom(self.SOCKET_BUFSIZE)

                if len(data) < 70:
                    continue

                _LOGGER.debug('DoHome devices %s ', data.decode("utf-8"))
                resp = {i.split("=")[0]:i.split("=")[1] for i in data.decode("utf-8").split("&")}
                if resp["cmd"] != 'pong':
                    continue

                device_type = resp["device_type"]

                dohome_device = {
                    "sid":resp["device_name"][-4:],
                    "name":resp["device_name"],
                    "sta_ip":resp["sta_ip"],
                    "type":device_type}

                if(dohome_device not in self.devices[device_type]):
                    self.devices[device_type].append(dohome_device)

        except socket.timeout:
            _LOGGER.info("Gateway finding finished in 5 seconds")
            _socket.close()

class DoHomeDevice(Entity):

    def __init__(self, name, device):
        self._sid = device['sid']
        self._name = name
        self._sta_ip = device['sta_ip']
        self._device_state_attributes = {}

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._device_state_attributes
