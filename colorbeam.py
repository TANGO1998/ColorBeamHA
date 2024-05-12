import asyncio
import logging
import json

LOGGER = logging.getLogger(__name__)

class ColorBeamLightInstance:
    def __init__(self,ipAddress:str,port:str,id=str) -> None:
        self._ipAddress = ipAddress
        self._port = port
        self._id = id
        self._connected = None
        self._reader = None
        self._writer = None
        self._brightness = None
        self._isRGBW = None
        self._isOn = None 
    
    async def _send(self,command:str):
        if (not self._connected):
            await self.connect()

        await self._connected
        self._writer.write(command.encode())
        
    
    @property
    def is_on(self):
        return self._brightness
    
    @property
    def ipAddress(self):
        return self._ipAddress
    
    @property
    def port(self):
        return self.port
    
    @property
    def id(self):
        return self._id
    
    async def turn_on(self):
        command = """{"command":"SetLoads","params":[{"id":%s,"d":750,l":255}]}""".format(self._id)
        await self._send(json.encoder.encode_basestring_ascii(command))
        self._isOn = True
    async def turn_off(self):
        command = """{"command":"SetLoads","params":[{"id":%s,"d":750,"l":0}]}""".format(self._id)
        await self._send(json.encoder.encode_basestring_ascii(command))
        self._isOn = False

    async def setBrightness(self,brightness):
        command = """{"command":"SetLoads","params":[{"id":%s,"d":750,"l":%d}]}""".format(self._id,brightness)
        await self._send(json.encoder.encode_basestring_ascii(command))
    
    async def connect(self):
        self._reader , self._writer = await asyncio.open_connection(host=self._ipAddress,port=self._port,ssl_handshake_timeout=40)
        await asyncio.sleep(1)
        self._connected = True

    async def disconnect(self):
        self._writer.close()
        self._writer.wait_closed()
        self._connected = False