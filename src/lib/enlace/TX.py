from threading import Thread
import time

from lib.interface.Interface import Interface


class TX:
    TRANSMIT_PREIOD = 0.01


    def __init__ (self, interface:Interface):
        self.interface = interface
        self.buffer = []
        self.threadStop = False
        self.threadPaused = True


    def _thread (self) -> None:
        while not self.threadStop:
            if not self.threadPaused:
                if not self.isEmpty():
                    self.interface.write(self.buffer[0])
                    self.buffer.pop(0)
                else:
                    self.pause()

            time.sleep(self.TRANSMIT_PREIOD)


    def __len__ (self) -> int:
        return len(self.buffer)


    def enable (self) -> None:
        self.thread = Thread(target=self._thread)
        self.threadStop = False

        self.thread.start()


    def disable (self) -> None:
        self.threadStop = True


    def pause (self) -> None:
        self.threadPaused = True


    def resume (self) -> None:
        self.threadPaused = False


    def isEmpty (self) -> bool:
        return len(self) == 0


    def clear (self) -> None:
        self.buffer *= 0


    def transmit (self, data:bytes) -> None:
        self.buffer.append(data)
        self.resume()

        while not self.isEmpty():
            time.sleep(self.TRANSMIT_PREIOD)
