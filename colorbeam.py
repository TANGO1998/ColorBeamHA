import asyncio
import logging
import json

LOGGER = logging.getLogger(__name__)

class ColorBeamLightInstance:
    def __init__(self,ipAddress:str,port:str,id=int) -> None:
        self._ipAddress = ipAddress
        self._port = port
        self._id = id
        self._connected = None
        self._reader = None
        self._writer = None
        self._brightness = None
        self._temp = None
        self._isRGBW = None
        self._RGBValue = dict()
        self._isOn = None 
    
    async def _send(self,command:str):
        if (not self._connected):
            await self.connect()

        self._writer.write(json.dumps(command).encode('utf-8')+b'\n')
        await self._writer.drain()
        LOGGER.debug('command Sent:%s'.format(command))
        # await self.disconnect()
    
    @property
    def is_on(self):
        return self._brightness
    
    @property
    def ipAddress(self):
        return self._ipAddress
    
    @property
    def port(self):
        return self._port
    
    @property
    def id(self):
        return self._id
    
    @property
    def Getbrightness(self):
        return self._brightness
    
    @property
    def Temp(self):
        return self._temp
    
    async def turn_on(self):
        command ={"command":"SetLoads","params":[{"id":self._id,"d":750,"l":255}]}
        await self._send(command)
        LOGGER.debug('command sent:%s'.format(command))
        await self.update()
        self._isOn = True

    async def turn_off(self):
        command = {"command":"SetLoads","params":[{"id":self._id,"d":750,"l":0}]}
        await self._send(command)
        LOGGER.debug('command sent:%s'.format(command))
        await self.update()
        self._isOn = False

    async def setBrightness(self,brightness):
        command = {"command":"SetLoads","params":[{"id":self._id,"d":750,"l":brightness}]}
        await self._send(command)
        LOGGER.debug('command sent:%s'.format(command))
        await self.update()
        self._brightness = brightness
        self._isOn = True
    
    async def setTemp(self,temp):
        command = {"command":"SetLoads","params":[{"id":self.id,"d":750,"k":temp}]}
        await self._send(command)
        LOGGER.debug('command sent:%s'.format(command))
        await self.update()
        self._temp = temp
    
    async def update(self):
        command = {"command":"GetLoadStatus","params":[self.id]}
        await self._send(command)
        LOGGER.debug('command Sent:%s'.format(command))
        data = await self._reader.readuntil(b"}}\n")
        LOGGER.debug('data Received:%s'.format(data))
        data = data.decode('utf-8')
        print(data)
        # if data["l"] > 0 :
        #     self._isOn = True
        # else:
        #     self._ison = False
        # self._brightness = data["l"]
        # self._temp = data["k"]
        LOGGER.debug('instance updated')
    
    async def connect(self):
        connect = asyncio.open_connection(host=self._ipAddress,port=self._port)
        try:
            self._reader , self._writer = await asyncio.wait_for(connect,timeout=10)
            await asyncio.sleep(1)
            self._connected = True
        except asyncio.TimeoutError:
            pass
            self._connected = False
            LOGGER.warning("WARNING: Connection Timeout")

    async def disconnect(self):
        self._writer.close()
        await self._writer.wait_closed()
        self._connected = False