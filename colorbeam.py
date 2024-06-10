import asyncio
import logging
import json

_LOGGER = logging.getLogger(__name__)

class ColorBeamLightInstance:
    def __init__(self,ipAddress:str,port:str,id=str) -> None:
        self._ipAddress = ipAddress
        self._port = port
        self._id = id
        self._connected = None
        self._reader = None
        self._writer = None
        self._brightness = None
        self._temp = None
        self._isRGBW = None
        self._RGBValue = []
        self._data = None
        self._isOn = None 
    
    async def _send(self,command:str):
        try:
            if (not self._connected):
                await self.connect()

            self._writer.write(json.dumps(command).encode('utf-8')+b'\n')
            await self._writer.drain()
            _LOGGER.debug('command Sent:%s'.format(command))
            #await self.disconnect()
        except Exception as e:
            pass
            _LOGGER.warning("WARNING: Connection Timeout")
        
    
    @property
    def is_on(self)->bool:
        return self._isOn
    
    @property
    def ipAddress(self)->str:
        return self._ipAddress
    
    @property
    def port(self)->str:
        return self._port
    
    @property
    def id(self)->str:
        return self._id
    
    @property
    def Getbrightness(self)->int:
        return self._brightness
    
    @property
    def Temp(self)-> int:
        return self._temp
    
    async def turn_on(self,brightness):
        command ={"command":"SetLoads","params":[{"id":self._id,"d":750,"l":brightness}]}
        await self._send(command)
        _LOGGER.debug('command sent:%s'.format(command))
        await asyncio.sleep(2)
        await self.update()
        self._brightness = brightness
        self._isOn = True

    async def turn_off(self):
        command = {"command":"SetLoads","params":[{"id":self._id,"d":750,"l":0}]}
        await self._send(command)
        _LOGGER.debug('command sent:%s'.format(command))
        await asyncio.sleep(2)
        await self.update()
        self._isOn = False

    async def setBrightness(self,brightness):
        command = {"command":"SetLoads","params":[{"id":self.id,"d":750,"l":brightness}]}
        await self._send(command)
        _LOGGER.debug('command sent:%s'.format(command))
        #await self.update()
        self._brightness = brightness
        self._isOn = True
    
    async def setTemp(self,temp):
        command = {"command":"SetLoads","params":[{"id":self.id,"d":750,"k":temp}]}
        await self._send(command)
        _LOGGER.debug('command sent:%s'.format(command))
        #await self.update()
        self._temp = temp
    
    async def update(self):
        command = {"command":"GetLoadStatus","params":[self.id]}
        await self._send(command)
        _LOGGER.debug('command Sent:%s'.format(command))
        data = await self._reader.readuntil(b"}]}}")
        _LOGGER.debug('data Received:%s'.format(data))
        data = data.decode('utf-8')
        for x in data.split("\n"):
            response = json.loads(x)
            try:
                if "load_status" in response["data"]:
                    if response["data"]["load_status"][0]["l"] > 0 :
                        self._isOn = True
                    if response["data"]["load_status"][0]["l"] == 0 :
                        self._isOn = False
                    self._brightness = response["data"]["load_status"][0]["l"]
                    self._temp = response["data"]["load_status"][0]["k"]
                    _LOGGER.debug('instance updated')
            except Exception as e:
                pass
    
    async def connect(self):
        connect = asyncio.open_connection(host=self._ipAddress,port=self._port)
        try:
            self._reader , self._writer = await asyncio.wait_for(connect,timeout=10)
            await asyncio.sleep(1)
            self._connected = True
        except Exception as e:
            pass
            self._connected = False
            _LOGGER.warning("WARNING: Connection Timeout")

    async def disconnect(self):
        self._writer.close()
        await self._writer.wait_closed()
        self._connected = False