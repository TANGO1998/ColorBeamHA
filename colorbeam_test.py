import asyncio
import logging
import json

LOGGER = logging.getLogger(__name__)
host = "192.168.8.172"
port = "3334"
command = """{"command":"GetLoads"}"""
json.encoder.encode_basestring_ascii(command)

async def main(host,port,command):
    try:
        connection = await asyncio.open_connection(host= host,port= port)
        print( "connected to ({host}:{port})")
        connection.write("{command}\n".encode())
        data = await connection.read(10000)
        formated = json.dumps(data,ident=4)
        print(formated)
    except Exception as e :
        raise Exception("ERROR:%s", e)
    

asyncio.run(main(host,port,command))