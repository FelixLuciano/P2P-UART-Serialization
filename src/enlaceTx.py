import threading


class TX(object):
    def __init__ (self, interface):
        self.interface = interface
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


    def transmit (self, data):
        self.buffer = data
        self.transLen = 0

        self.resume()
