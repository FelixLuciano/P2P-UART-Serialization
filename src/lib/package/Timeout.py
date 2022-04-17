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


    @staticmethod
    def request (enlace:Enlace, timeout:int=-1, *args, **kwargs):
        try:
            header = Package.request(Timeout_header, enlace, timeout, *args, **kwargs)

            return Timeout_package()
        except Timeout_header.TimeoutException as error:
            raise Package.TimeoutException(error.time)


Package.register_type(Timeout_package)
