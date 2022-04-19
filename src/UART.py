import os
import json
from lib.interface import Interface
from lib.enlace import Enlace
from lib.stream import Data_stream
import logging


class UART ():
    logger = None


    def __init__ (self, port:str=None, log_filename:str=None):
        com = Interface.get_available_interface() if port == None else Interface(port)

        self.enlace = Enlace(com)
        
        if log_filename != None:
            self.logger = logging.getLogger(log_filename)

            logging.basicConfig(
                filename=os.path.join('logs', f'{log_filename}.log'),
                filemode='w',
                format='%(asctime)s.%(msecs)03d %(message) s',
                datefmt='%d/%m/%Y %H:%M:%S',
                level=logging.INFO
            )


    def __enter__ (self):
        self.enlace.enable()

        return self


    def __exit__ (self, type, value, traceback):
        self.enlace.disable()


    def push_data (self, data:any, to:int, timeout:int=-1):
        try:
            if type(data) != bytes:
                data = json.dumps(data).encode()

            Data_stream(data).submit(self.enlace, to, timeout, self.logger)

        except Data_stream.ExcededSizeLimitException:
            raise UART.ExcededSizeLimitException()

        except Data_stream.TimeoutException as error:
            raise UART.TimeoutException(error.time)


    def pull_data (self, from_:int, type_=any, timeout:int=-1) -> any:
        try:
            response = Data_stream.request(self.enlace, from_, timeout, self.logger)

            if type_ != bytes:
                response.data = json.loads(response.data)

            return response.data

        except Data_stream.TimeoutException as error:
            raise UART.TimeoutException(error.time)


    class ExcededSizeLimitException (Data_stream.ExcededSizeLimitException):
        """Data size exceed limit.
        """
        pass
        

    class TimeoutException (Data_stream.TimeoutException):
        """Couldn't receive data within the timeout.
        """
        pass
