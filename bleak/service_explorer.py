import asyncio
from bleak import BleakClient


async def run(address):

    async with BleakClient(address, timeout=30) as client:
        print(f"Connected: {client.is_connected}")
        return

        for service in client.services:
            print(f"[Service] {service}")

            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        value = bytes(await client.read_gatt_char(char.uuid))
                        print(f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}")
                    except Exception as e:
                        print(f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {e}")
                else:
                    value = None
                    print(f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}")

                for descriptor in char.descriptors:
                    try:
                        value = bytes(await client.read_gatt_descriptor(descriptor.handle))
                        print(f"\t\t[Descriptor] {descriptor}) | Value: {value}")
                    except Exception as e:
                        print(f"\t\t[Descriptor] {descriptor}) | Value: {e}")


if __name__ == "__main__":
    ADDRESS = "3523EA96-3F17-407F-99CD-9A901CFE834C"

    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(run(ADDRESS))
