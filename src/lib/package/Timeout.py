from logging import Logger

from lib.header.Timeout import Timeout_header
from lib.package.Package import Package
from lib.enlace.Enlace import Enlace


class Timeout_package (Package):
    header = Timeout_header


    def __init__ (self):
        super().__init__()


    def encode (self):
        package = bytearray()
        header = Timeout_package.header()

        package.extend(header.encode())
        package.extend(self.END)

        return bytes(package)


    def submit (self, enlace:Enlace, logger:Logger=None):
        package = super().submit(enlace)

        if logger != None:
            logger.info(f'Sent Timeout ({Timeout_header.type}) in {len(package)}.')


    @staticmethod
    def request (enlace:Enlace, timeout:int=-1, logger:Logger=None, *args, **kwargs):
        try:
            header = Package.request(Timeout_header, enlace, timeout, *args, **kwargs)
            package = Timeout_package()

            if logger != None:
                logger.info(f'Received Response ({Timeout_header.type}) in {Timeout_header.SIZE + len(Package.END)} bytes.')

            return package

        except Timeout_header.TimeoutException as error:
            raise Package.TimeoutException(error.time)


Package.register_type(Timeout_package)
