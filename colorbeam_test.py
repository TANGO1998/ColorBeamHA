import asyncio
import logging
import json

LOGGER = logging.getLogger(__name__)
host = "192.168.8.172"
port = "3334"
command = {"command":"GetLoadStatus"}

async def send_json_via_telnet(host, port, json_data):

    reader, writer = await asyncio.open_connection(host, port)
    print(f"connected to {host} : {port}")

    data_to_send = json.dumps(json_data).encode('utf-8')
    writer.write(data_to_send + b'\n') 
    data = await reader.read(10000) 

    writer.close()

    if data:
        print(f"Received response from server: {json.dump(data.decode('utf-8'))}")
    else:
        print("No response received from server.")
    
asyncio.run(send_json_via_telnet(host,port,command))