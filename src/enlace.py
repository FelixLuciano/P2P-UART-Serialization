import time

from enlaceRx import RX
from enlaceTx import TX
from interface import Interface


class Enlace(object):
    def __init__ (self, name, prefix=0xE0, sufix=0x0E, separator=0xCD):
        self.prefix = prefix
        self.sufix = sufix
        self.separator = separator
        self.interface = Interface(name)
        self.rx = RX(self.interface, prefix, sufix, separator)
        self.tx = TX(self.interface, prefix, sufix, separator)


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
        buffer, size = self.tx.transmit(data)

        return buffer, size


    def getData (self, *args):
        data, size = self.rx.getData(*args)

        return data, size
