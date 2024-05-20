import asyncio
import logging
import json

LOGGER = logging.getLogger(__name__)
host = "192.168.8.172"
port = "3334"
command = {"command":"SetLoads","params":[{"id":180,"d":750,"k":3200,"l":204}]}

async def send_json_via_telnet(host, port, json_data):
    fut =  asyncio.open_connection(host, port)
    try:
        reader,writer = await asyncio.wait_for(fut,timeout=5)
        print(f"connected to {host} : {port}")

        data_to_send = json.dumps(json_data).encode('utf-8')
        writer.write(data_to_send + b'\n') 
        data = await reader.read(10000) 
        data = json.loads(data.decode('utf-8'))
        writer.close()

        if data:
            print(f"Received response from server: {json.dumps(data,indent=4)}")
        else:
            print("No response received from server.")
        # for x in data["data"]["load_status"]:
        #     if x['l']:
        #         print(f"for id :{x['id']} : l value {x['l']}")
    except asyncio.TimeoutError:
        LOGGER.warning("WARNING: connection timeout")
    
asyncio.run(send_json_via_telnet(host,port,command))