import threading
import time


class RX(object):
    def __init__ (self, interface):
        self.interface = interface
        self.buffer = bytes(bytearray())
        self.threadStop = False
        self.threadMutex = True
        self.READLEN = 1024


    def _thread (self):
        while not self.threadStop:
            if self.threadMutex:
                rxTemp, nRx = self.interface.read(self.READLEN)

                if nRx > 0:
                    self.buffer += rxTemp

                time.sleep(0.01)


    def enable (self):
        self.thread = threading.Thread(target=self._thread, args=())

        self.thread.start()


    def disable (self):
        self.threadStop = True


    def pause (self):
        self.threadMutex = False


    def resume (self):
        self.threadMutex = True


    def getLen (self):
        return len(self.buffer)


    def isEmpty (self):
        return self.getLen() == 0


    def clear (self):
        self.buffer = b''


    def getData (self, size=0):
        while size > 0 and self.getLen() < size or size == 0 and self.isEmpty():
            time.sleep(0.05)

        self.pause()

        buffer = self.buffer[0:size]
        self.buffer = self.buffer[size:]

        self.resume()

        return buffer
