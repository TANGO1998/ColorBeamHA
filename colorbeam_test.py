from pycolorbeam import ColorBeamLightInstance,ColorBeamRGBLightInstance
import asyncio
import logging

light = ColorBeamLightInstance("192.168.8.172","3334",180)
asyncio.run(light.turn_on(0))
print(f"light brightness: {light.Getbrightness}\n light brightness: {light.is_on}")
