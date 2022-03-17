from threading import Thread
import time

from lib.interface import Interface


class RX:
    READ_LENGTH = 1024
    READ_PREIOD = 0.01


    def __init__ (self, interface:Interface):
        self.interface = interface
        self.buffer = b''
        self.threadStop = False
        self.threadPaused = True


    def _thread (self):
        while not self.threadStop:
            if not self.threadPaused:
                data, size = self.interface.read(self.READ_LENGTH)

                if size > 0:
                    self.buffer += data

            time.sleep(self.READ_PREIOD)


    def enable (self):
        self.thread = Thread(target=self._thread)

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
        self.buffer = b''


    def getBuffer (self, size:int=-1):
        if size == 0:
            return b'', 0
        elif size > 0:
            buffer = self.buffer[0:size]
            self.buffer = self.buffer[size:]
        else:
            buffer = self.buffer
            self.clear()

        return buffer, len(buffer)


    def receive (self, size:int=-1, timeout:int=-1):
        timer = 0

        while self.isEmpty() or self.getLen() < size:
            if self.threadPaused:
                self.resume()

            time.sleep(self.READ_PREIOD)

            if timeout > 0:
                timer += self.READ_PREIOD

                if timer >= timeout:
                    self.pause()

                    return self.getBuffer(0)

        self.pause()

        return self.getBuffer(size)
