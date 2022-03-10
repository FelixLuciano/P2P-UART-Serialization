import threading
import time

from package import Package


class RX(object):
    READLEN = 1024


    def __init__ (self, interface):
        self.interface = interface
        self.buffer = []
        self.threadStop = False
        self.threadPaused = True
        self.threadIddle = True


    def _thread (self):
        while not self.threadStop:
            if self.threadPaused:
                rxTemp, nRx = self.interface.read(self.READLEN)

                if nRx > 0 and Package.valid(rxTemp):
                    self.buffer.append(Package.decode(rxTemp))

                time.sleep(0.1)


    def enable (self):
        self.thread = threading.Thread(target=self._thread, args=())

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


    def decode (self, buffer):
        data = []

        prefix_byte = buffer.index(self.prefix)
        sufix_byte = buffer.index(self.sufix)

        if -1 < prefix_byte < sufix_byte:
            data = buffer[prefix_byte+1:sufix_byte].split(self.separator.to_bytes(1, 'big'))

        return data


    def getData (self, size=-1):
        timeout = 0

        while (size > 0 and self.getLen() < size) or (size < 0 and self.isEmpty()) or not self.threadIddle:
            time.sleep(0.1)

            timeout += 0.1

            if timeout >= 10:
                return [], 0

        self.pause()

        buffer = self.buffer[0:size] if size > 0 else self.buffer
        self.buffer = self.buffer[size:] if size > 0 else self.clear()

        self.resume()

        return self.decode(buffer), len(buffer)
