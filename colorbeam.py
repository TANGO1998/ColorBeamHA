import asyncio
import logging

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
    
    async def turn_on(self):
        command = None
    
    async def connect(self):
        self._reader , self._writer = await asyncio.open_connection(host=self._ipAddress,port=self._port,ssl_handshake_timeout=40)
        await asyncio.sleep(1)
        self._connected = True

    async def disconnect(self):
        self._writer.close()
        self._writer.wait_closed()
        self._connected = False

    
    
