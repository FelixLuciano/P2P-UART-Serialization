from logging import Logger

from lib.header.Response import Response_header
from lib.package import Package
from lib.enlace.Enlace import Enlace


class Response_package (Package):
    def __init__ (self):
        super().__init__()


    def encode (self):
        package = bytearray()
        header = Response_header()

        package.extend(header.encode())
        package.extend(self.END)

        return bytes(package)


    def submit (self, enlace:Enlace, logger:Logger=None):
        package = super().submit(enlace)

        if logger != None:
            logger.info(f'Sent Response ({Response_header.type}) in {len(package)} bytes.')


    @staticmethod
    def request (enlace:Enlace, timeout:int=-1, logger:Logger=None, *args, **kwargs):
        try:
            header = Package.request(Response_header, enlace, timeout, *args, **kwargs)
            response = Response_package()

            if logger != None:
                logger.info(f'Received Response ({Response_header.type}) in {Response_header.SIZE + len(Package.END)} bytes.')

            return response

        except Response_header.TimeoutException as error:
            raise Package.TimeoutException(error.time)


Package.register_type(Response_package)
