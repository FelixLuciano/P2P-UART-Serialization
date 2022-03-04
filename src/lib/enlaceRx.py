import threading
import time


class RX(object):
    def __init__ (self, interface, prefix, sufix, separator):
        self.interface = interface
        self.prefix = prefix
        self.sufix = sufix
        self.separator = separator
        self.buffer = bytes(bytearray())
        self.threadStop = False
        self.threadMutex = True
        self.threadIddle = True
        self.READLEN = 1024


    def _thread (self):
        while not self.threadStop:
            if self.threadMutex:
                rxTemp, nRx = self.interface.read(self.READLEN)

                if nRx > 0:
                    if rxTemp.startswith(self.prefix.to_bytes(1, 'big')):
                        self.threadIddle = False

                    if not self.threadIddle:
                        self.buffer += rxTemp

                    if rxTemp.endswith(self.sufix.to_bytes(1, 'big')):
                        self.threadIddle = True

                time.sleep(0.1)


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
