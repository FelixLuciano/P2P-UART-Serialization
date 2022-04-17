from lib.header.Request import Request_header
from lib.package.Package import Package
from lib.enlace.Enlace import Enlace


class Request_package (Package):
    def __init__ (self, target:int=None, length:int=1):
        if target > 255:
            raise Package.ExcededSizeLimitException()

        super().__init__(length)
        self.target = target


    def encode (self) -> bytes:
        package = bytearray()
        header = Request_header(self.target, self.length)

        package.extend(header.encode())
        package.extend(Package.END)

        return bytes(package)


    @staticmethod
    def request (enlace:Enlace, timeout:int=-1, *args, **kwargs):
        try:
            header = Package.request(Request_header, enlace, timeout,*args, **kwargs)

            return Request_package(header.target, header.length)

        except Request_header.UnexpectedHeaderException as error:
            raise Request_package.UnexpectedRequestException(error.header)

        except Request_header.TimeoutException as error:
            raise Package.TimeoutException(error.time)


    class UnexpectedRequestException (Request_header.UnexpectedRequestException):
        """The Request received does not have the expected target
        """
        pass


Package.register_type(Request_package)
