from colorbeam import ColorBeamLightInstance
import asyncio

light = ColorBeamLightInstance("192.168.8.172","3334",180)
asyncio.run(light.turn_on())
    