from logging import Logger

from lib.header.Error import Error_header
from lib.package.Package import Package
from lib.enlace.Enlace import Enlace


class Error_package (Package):
    def __init__ (self, package_index:int=None):
        if package_index > 255:
            raise Package.ExcededSizeLimitException()

        super().__init__()
        self.package_index = package_index


    def encode (self) -> bytes:
        package = bytearray()
        header = Error_header(self.package_index)

        package.extend(header.encode())
        package.extend(self.END)

        return bytes(package)


    def submit (self, enlace:Enlace, logger:Logger=None):
        package = super().submit(enlace)

        if logger != None:
            logger.info(f'Sent Error ({Error_header.type}) in {len(package)} bytes for package {self.package_index}.')


    @staticmethod
    def request (enlace:Enlace, timeout:int=-1, logger:Logger=None, *args, **kwargs):
        try:
            header = Package.request(Error_header, enlace, timeout, *args, **kwargs)
            package = Error_package(header.package_index)

            if logger != None:
                logger.info(f'Received Error ({header.type}) in {Error_header.SIZE + len(Package.END)} bytes for package {package.package_index}.')

            return package

        except Error_header.UnexpectedErrorException as error:
            raise Error_package.UnexpectedErrorException(error.header)

        except Enlace.TimeoutException:
            raise Package.TimeoutException()


    class UnexpectedErrorException (Error_header.UnexpectedErrorException):
        pass


Package.register_type(Error_package)
