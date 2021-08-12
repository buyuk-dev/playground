# Notes:
#
# The timeouts on connectPeripheral() calls have been resolved after i deleted the
# /Library/Preferences/com.apple.Bluetooth.plist file and installed 
# https://download.developer.apple.com/OS_X/OS_X_Logs/Bluetooth_Logging_Instructions.pdf
# debug log profile and rebooted.
#

# TODO:
# 2. Discover services and characteristics of the device.
# 3. Connect to a device.
# 4. Get data from a device.
# 5. Disconnect from a device.

import pdb

import objc
from Foundation import (
    NSObject,
)
import CoreBluetooth
from libdispatch import (
    dispatch_queue_create,
    DISPATCH_QUEUE_SERIAL,
)

import asyncio
import threading
import time
from pprint import pprint


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
        self.discovered = None
        self.connected = None
        return self

    def centralManager_didDiscoverPeripheral_advertisementData_RSSI_(
            self,
            central,
            peripheral,
            advertismentData,
            RSSI
        ):
        if peripheral.name() == "Muse-7E45":
            self.discovered = peripheral
            print(f"{peripheral.name()} {peripheral.identifier()}")

    def centralManager_didDisconnectPeripheral_error_(
            self,
            central,
            peripheral,
            error
        ):
        print(f"Error while attempting discovery: {error}")

    def centralManager_didConnectPeripheral_(
            self,
            central,
            peripheral
        ):
        print(f"Peripheral {peripheral.name()} connected.")
        peripheral.delegate = self
        self.connected = peripheral

    def centralManager_didFailToConnect_error_(self, central, peripheral, error):
        print(f"Failed to connect to {peripheral.name()}.")
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
    while cmd.discovered is None:
        await asyncio.sleep(1.0)

    muse = cmd.discovered
    cmd.central_manager.stopScan()

    await asyncio.sleep(1.0)

    print("Attempting connection to:")
    print((muse.name(), muse.identifier()))

    #pdb.set_trace()
    cmd.central_manager.connectPeripheral_options_(muse, None)

    while cmd.connected is None:
        await asyncio.sleep(1.0)

    muse = cmd.connected
    print(f"Connected to {muse.name()}.")


asyncio.run(main())

