from PyQt5.QtCore import QIODevice, QObject
from PyQt5.QtWidgets import QApplication
from PyQt5.QtBluetooth import QBluetoothDeviceDiscoveryAgent
import sys
import PIL

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

class DeviceScanner(QObject):
    def __init__(self):
        super().__init__()
        self.agent = QBluetoothDeviceDiscoveryAgent()
        self.agent.deviceDiscovered.connect(self.onDeviceDiscovered)

    def startScan(self):
        self.agent.start()

    def onDeviceDiscovered(self, deviceInfo):
        if "YOUR_SPECIAL_SIGNAL_UUID" in deviceInfo.serviceUuids():
            print("Found device:", deviceInfo.name())

if __name__ == "__main__":
    sys.excepthook = except_hook
    app = QApplication([])
    scanner = DeviceScanner()
    scanner.startScan()
    app.exec_()