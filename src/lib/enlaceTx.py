import threading
import time


class TX(object):
    def __init__ (self, interface, prefix, sufix, separator):
        self.interface = interface
        self.prefix = prefix
        self.sufix = sufix
        self.separator = separator
        self.buffer = bytes(bytearray())
        self.transLen = 0
        self.threadMutex = False
        self.threadStop = False


    def _thread (self):
        while not self.threadStop:
            if self.threadMutex:
                self.transLen = self.interface.write(self.buffer)

                self.pause()


    def enable (self):
        self.thread = threading.Thread(target=self._thread, args=())

        self.thread.start()


    def disable (self):
        self.threadStop = True


    def pause (self):
        self.threadMutex = False


    def resume (self):
        self.threadMutex = True


    def isBussy (self):
        return self.threadMutex


    def getLen (self):
        return len(self.buffer)


    def getStatus (self):
        return self.transLen


    def encode (self, *data):
        if len(data) == 1 and type(data[0]) == list and len(data[0]) > 1:
            data = data[0]

        buffer = bytearray([self.separator]).join(data)

        buffer.insert(0, self.prefix)
        buffer.append(self.sufix)

        return buffer


    def transmit (self, data):
        buffer = self.encode(data)

        self.buffer = buffer
        self.transLen = 0

        self.resume()
        time.sleep(.05)

        return buffer, len(buffer)
