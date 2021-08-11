import asyncio
from bleak import BleakClient, BleakScanner
from pprint import pprint
import sys

#address = "00:55:DA:B5:7E:45"
#MODEL_NBR_UUID = "3523EA96-3F17-407F-99CD-9A901CFE834C"

address = "3523EA96-3F17-407F-99CD-9A901CFE834C"
if len(sys.argv) == 2:
    address = sys.argv[1]

async def run(address):
    #device = await BleakScanner.find_device_by_address(address)
    #pprint(vars(device))
    print("--------------------------------------")
    #async with BleakClient(device, timeout=30) as client:
    async with BleakClient(address, timeout=30) as client:
        pprint(vars(client))
        #model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        #print("Model Number: {0}".format("".join(map(chr, model_number))))

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
