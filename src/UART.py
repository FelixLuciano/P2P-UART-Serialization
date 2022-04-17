from lib.interface import Interface
from lib.enlace import Enlace
from lib.stream import Data_stream


class UART ():
    def __init__ (self, port:str=None):
        com = Interface.get_available_interface() if port == None else Interface(port)

        self.enlace = Enlace(com)


    def __enter__ (self):
        self.enlace.enable()

        return self


    def __exit__ (self, type, value, traceback):
        self.enlace.disable()


    def push_data (self, data:bytes, target:int, timeout:int=-1):
        try:
            Data_stream(data).submit(self.enlace, target, timeout)

        except Data_stream.TimeoutException as error:
            raise UART.TimeoutException(error.time)


    def pull_data (self, target:int, timeout:int=-1):
        try:
            response = Data_stream.request(self.enlace, target, timeout)

            return response.data

        except Data_stream.TimeoutException as error:
            raise UART.TimeoutException(error.time)
        

    class TimeoutException (Data_stream.TimeoutException):
        """Couldn't receive data within the timeout.
        """
        pass
