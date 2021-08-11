# TODO
# 1. Discover Muse EEG headset.
# 2. Discover services and characteristics of the device.
# 3. Connect to a device.
# 4. Get data from a device.
# 5. Disconnect from a device.


import CoreBluetooth
from Foundation import NSObject
import objc
from pprint import pprint
import asyncio
from libdispatch import dispatch_queue_create, DISPATCH_QUEUE_SERIAL
import threading
import time


class CentralManagerDelegate(NSObject):

    def init(self):
        objc.super(CentralManagerDelegate, self).init()
        if self is None: return None
        self._did_update_state_event = threading.Event()
        self.central_manager = CoreBluetooth.CBCentralManager.alloc().initWithDelegate_queue_(
            self,
            dispatch_queue_create(b"bleak.corebluetooth", DISPATCH_QUEUE_SERIAL),
        )
        self._did_update_state_event.wait(1)
        self.discovered = dict()
        return self

    def centralManager_didDiscoverPeripheral_advertisementData_RSSI_(
            self,
            central,
            peripheral,
            advertismentData,
            RSSI
        ):
        if peripheral.identifier() not in self.discovered.keys() or \
           peripheral.name() != self.discovered[peripheral.identifier()]:

            print(f"{peripheral.name()} {peripheral.identifier()}")
            self.discovered[peripheral.identifier()] = peripheral.name()

    def centralManager_didDisconnectPeripheral_error_(
            self,
            central,
            peripheral,
            error
        ):
        print(f"Error while attempting discovery...")
        print(error)

    def centralManagerDidUpdateState_(self, centralManager):
        print("centralManagerDidUpdateState_")
        if centralManager.state() == CoreBluetooth.CBManagerStateUnknown:
            print("Cannot detect bluetooth device")
        elif centralManager.state() == CoreBluetooth.CBManagerStateResetting:
            print("Bluetooth is resetting")
        elif centralManager.state() == CoreBluetooth.CBManagerStateUnsupported:
            print("Bluetooth is unsupported")
        elif centralManager.state() == CoreBluetooth.CBManagerStateUnauthorized:
            print("Bluetooth is unauthorized")
        elif centralManager.state() == CoreBluetooth.CBManagerStatePoweredOff:
            print("Bluetooth powered off")
        elif centralManager.state() == CoreBluetooth.CBManagerStatePoweredOn:
            print("Bluetooth powered on")
        self._did_update_state_event.wait(1)


async def main():
    cmd = CentralManagerDelegate.alloc().init()
    cmd.central_manager.scanForPeripheralsWithServices_options_(None, None)
    while True:
        print(f"Discovered {len(cmd.discovered)} devices nearby.")
        await asyncio.sleep(1.0)
        

asyncio.run(main())

