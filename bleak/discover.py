"""
Muselsl is broken because it uses pygatt which is not supported on macos.
Additionally, macos for security reasons does not expose MAC addresses of bluetooth devices.
Instead it uses UUIDs, which change so they need to be rediscovered every time??? (this is strange)
If i could add bleak BLE backend to muselsl that may be possible to use muselsl on macos again.
"""

import asyncio
from bleak import BleakScanner
from pprint import pprint


async def run():
    devices = await BleakScanner.discover()
    for d in devices:
        #pprint(vars(d))
        print(d)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(run())
