import time

from lib.enlace.RX import RX
from lib.enlace.TX import TX
from lib.interface.Interface import Interface


class Enlace:
    def __init__ (self, interface:Interface):
        self.interface = interface
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


    def clear (self):
        self.rx.clear()
        self.tx.clear()


    def transmit (self, data:bytes) -> None:
        self.tx.transmit(data)


    def receive (self, size:int=-1, timeout:int=-1) -> bytes:
        return self.rx.receive(size, timeout)


    class TimeoutException (RX.TimeoutException):
        """Couldn't receive the amount requested bytes within the timeout.
        """
        pass
