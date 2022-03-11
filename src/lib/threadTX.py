from threading import Thread
import time

from lib.interface import Interface


class TX:
    def __init__ (self, interface:Interface):
        self.interface = interface
        self.buffer = []
        self.threadStop = False


    def _thread (self):
        while not self.threadStop:
            if len(self.buffer) > 0:
                self.interface.write(self.buffer[0])
                self.buffer.pop(0)


    def enable (self):
        self.thread = Thread(target=self._thread, args=())
        self.threadStop = False

        self.thread.start()


    def disable (self):
        self.threadStop = True


    def transmit (self, data:bytes):
        self.buffer.append(data)
        time.sleep(.05)
