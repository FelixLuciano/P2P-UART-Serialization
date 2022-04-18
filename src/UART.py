import json
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


    def push_data (self, data:any, target:int, timeout:int):
        try:
            adata = json.dumps(data)

            Data_stream(adata.encode()).submit(self.enlace, target, timeout)

        except Data_stream.TimeoutException as error:
            raise UART.TimeoutException(error.time)


    def pull_data (self, target:int, timeout:int) -> any:
        try:
            response = Data_stream.request(self.enlace, target, timeout)

            return json.loads(response.data)

        except Data_stream.TimeoutException as error:
            raise UART.TimeoutException(error.time)
        

    class TimeoutException (Data_stream.TimeoutException):
        """Couldn't receive data within the timeout.
        """
        pass
