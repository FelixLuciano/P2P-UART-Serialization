from lib.header.Success import Success_header
from lib.package.Package import Package
from lib.enlace.Enlace import Enlace


class Success_package (Package):
    header = Success_header


    def __init__ (self, package_index:int=None):
        if package_index > 255:
            raise Package.ExcededSizeLimitException()

        super().__init__()
        self.package_index = package_index


    def encode (self):
        package = bytearray()
        header = Success_package.header(self.package_index)

        package.extend(header.encode())
        package.extend(self.END)

        return bytes(package)


    @staticmethod
    def request (enlace:Enlace, timeout:int=-1, *args, **kwargs):
        try:
            header = Package.request(Success_header, enlace, timeout, *args, **kwargs)

            return Success_package(header.package_index)

        except Success_header.UnexpectedSuccessException as error:
            raise Success_package.UnexpectedSuccessException(error.header)

        except Enlace.TimeoutException as error:
            raise Package.TimeoutException(error.time)


    class UnexpectedSuccessException (Success_header.UnexpectedSuccessException):
        pass


Package.register_type(Success_package)
