from threading import Thread
import time

from lib.interface import Interface


class RX:
    READ_LENGTH = 1024
    READ_PREIOD = 0.1


    def __init__ (self, interface:Interface):
        self.interface = interface
        self.buffer = b''
        self.threadStop = False
        self.threadPaused = True


    def _thread (self):
        while not self.threadStop:
            if self.threadPaused:
                data, size = self.interface.read(self.READ_LENGTH)

                if size > 0:
                    self.buffer += data

                time.sleep(self.READ_PREIOD)


    def enable (self):
        self.thread = Thread(target=self._thread, args=())

        self.thread.start()


    def disable (self):
        self.threadStop = True


    def pause (self):
        self.threadPaused = False


    def resume (self):
        self.threadPaused = True


    def getLen (self):
        return len(self.buffer)


    def isEmpty (self):
        return self.getLen() == 0


    def clear (self):
        self.buffer = b''

    
    def getBuffer (self, size:int=-1):
        if size == 0:
            return b'', 0

        self.pause()

        buffer = self.buffer[0:size] if size > 0 else self.buffer
        self.buffer = self.buffer[size:] if size > 0 else b''

        self.resume()

        return buffer, len(buffer)


    def getData (self, size:int=-1, timeout:int=-1):
        timer = 0

        while self.isEmpty() or self.getLen() < size:
            time.sleep(self.READ_PREIOD)

            if timeout > 0:
                timer += self.READ_PREIOD

                if timer >= timeout:
                    return b'', 0

        return self.getBuffer(size)
