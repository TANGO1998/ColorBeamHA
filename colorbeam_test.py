from colorbeam import ColorBeamLightInstance
import asyncio
import logging

light = ColorBeamLightInstance("192.168.8.172","3334",180)
asyncio.run(light.turn_off())
print(f"light temp: {light.Temp}\n light brightness: {light.is_on}")
