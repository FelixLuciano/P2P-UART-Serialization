from threading import Thread
import time

from lib.interface import Interface


class TX:
    TRANSMIT_PREIOD = 0.01


    def __init__ (self, interface:Interface):
        self.interface = interface
        self.buffer = []
        self.threadStop = False
        self.threadPaused = True


    def _thread (self):
        while not self.threadStop:
            if not self.threadPaused:
                if not self.isEmpty():
                    data = self.buffer[0]

                    self.interface.write(data)
                    self.buffer.pop(0)
                else:
                    self.pause()

            time.sleep(self.TRANSMIT_PREIOD)


    def enable (self):
        self.thread = Thread(target=self._thread)
        self.threadStop = False

        self.thread.start()


    def disable (self):
        self.threadStop = True


    def pause (self):
        self.threadPaused = True


    def resume (self):
        self.threadPaused = False


    def getLen (self):
        return len(self.buffer)


    def isEmpty (self):
        return self.getLen() == 0


    def clear (self):
        self.buffer *= 0


    def transmit (self, data:bytes):
        self.buffer.append(data)
        self.resume()

        while not self.isEmpty():
            time.sleep(self.TRANSMIT_PREIOD)
