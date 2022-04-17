from threading import Thread
import time

from lib.interface.Interface import Interface


class RX:
    READ_LENGTH = 1024
    READ_PREIOD = 0.01


    def __init__ (self, interface:Interface):
        self.interface = interface
        self.buffer = b''
        self.threadStop = False
        self.threadPaused = True

    
    def __len__ (self) -> int:
        return len(self.buffer)


    def _thread (self) -> None:
        while not self.threadStop:
            if not self.threadPaused:
                data, size = self.interface.read(self.READ_LENGTH)

                if size > 0:
                    self.buffer += data

            time.sleep(self.READ_PREIOD)


    def enable (self) -> None:
        self.thread = Thread(target=self._thread)

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
        self.buffer = b''


    def getBuffer (self, size:int=-1) -> bytes:
        if size == 0:
            return b''

        elif size > 0:
            buffer = self.buffer[0:size]
            self.buffer = self.buffer[size:]

        else:
            buffer = self.buffer
            self.clear()

        return buffer


    def receive (self, size:int=-1, timeout:int=-1) -> bytes:
        timer = 0

        while 0 == len(self) < size:
            if self.threadPaused:
                self.resume()

            time.sleep(self.READ_PREIOD)

            if timeout > 0:
                timer += self.READ_PREIOD

                if timer >= timeout:
                    self.pause()

                    raise self.TimeoutException(timer)

        self.pause()

        return self.getBuffer(size)


    class TimeoutException (Exception):
        """Couldn't receive the amount requested bytes within the timeout.
        """
        def __init__ (self, time, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.time = time
