import threading
import time

from package import Package


class TX(object):
    def __init__ (self, interface):
        self.interface = interface
        self.buffer = []
        self.threadStop = False
        self.threadPaused = False


    def _thread (self):
        while not self.threadStop:
            if self.threadPaused:
                if len(self.buffer) > 0:
                    self.interface.write(self.buffer[0])
                    self.buffer.pop(0)
                else:
                    self.pause()


    def enable (self):
        self.thread = threading.Thread(target=self._thread, args=())
        self.threadStop = False

        self.thread.start()


    def disable (self):
        self.threadStop = True


    def pause (self):
        self.threadPaused = False


    def resume (self):
        self.threadPaused = True


    def isPaused (self):
        return self.threadPaused


    def transmit (self, package):
        buffer = package.encode()
        size = Package.getSize(buffer)

        self.pause()
        self.buffer.extend(buffer)
        self.resume()
        time.sleep(.05)

        return buffer, size
