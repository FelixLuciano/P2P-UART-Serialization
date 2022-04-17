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


    @staticmethod
    def request (enlace:Enlace, timeout:int=-1, *args, **kwargs):
        try:
            header = Package.request(Response_header, enlace, timeout, *args, **kwargs)

            return Response_package()

        except Response_header.TimeoutException as error:
            raise Package.TimeoutException(error.time)


Package.register_type(Response_package)
