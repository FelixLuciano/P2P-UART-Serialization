import time

from enlaceRx import RX
from enlaceTx import TX
from interface import Interface


class Enlace(object):
    def __init__ (self, name):
        self.interface = Interface(name)
        self.rx = RX(self.interface)
        self.tx = TX(self.interface)


    def enable (self):
        self.interface.open()
        time.sleep(0.1)
        self.rx.enable()
        self.tx.enable()


    def disable (self):
        self.rx.disable()
        self.tx.disable()
        time.sleep(0.1)
        self.interface.close()


    def transmit (self, data):
        self.tx.transmit(data)


    def getData (self, *args):
        data = self.rx.getData(*args)

        return data, len(data)
