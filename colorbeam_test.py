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
        reader,writer = await asyncio.open_connection(host= host,port= port)
        print( "connected to ({host}:{port})")
        writer.write("{command}\n".encode())
        data = await reader.read(10000)
        formated = json.dumps(data,ident=4)
        print(formated)
        writer.close()
        await writer.wait_closed()
    except Exception as e :
        raise Exception("ERROR:%s", e)
    
asyncio.run(main(host,port,command))