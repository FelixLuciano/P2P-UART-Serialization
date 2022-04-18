from logging import Logger

from lib.header.Data import Data_header
from lib.package.Package import Package
from lib.package.Success import Success_package
from lib.package.Error import Error_package
from lib.enlace.Enlace import Enlace


class Data_package (Package):
    MAX_PAYLOAD_SIZE = Data_header.MAX_PAYLOAD_SIZE


    def __init__ (self, length:int=1, index:int=1, data:bytes=b''):
        if len(data) > Data_package.MAX_PAYLOAD_SIZE:
            raise Package.ExcededSizeLimitException()

        super().__init__(length, index)
        self.data = data


    def __len__ (self) -> int:
        return len(self.data)


    def encode (self) -> bytes:
        package = bytearray()
        header = Data_header(self.length, self.index, len(self))

        package.extend(header.encode())
        package.extend(self.data)
        package.extend(Package.END)

        return bytes(package)


    def submit (self, enlace:Enlace, timeout:int=-1, logger:Logger=None):
        while True:
            package = super().submit(enlace)

            if logger != None:
                logger.info(f'Sent Data ({Data_header.type}) {self.index} of {self.length} in {len(package)} bytes.')

            try:
                return Success_package.request(enlace, timeout, logger, package_index=self.index)

            except Success_package.UnexpectedSuccessException as error:
                response = error.header

                if (
                    type(response) == Success_package and response.package_index != self.index or
                    type(response) == Error_package and response.package_index == self.index
                ):
                    pass
                else:
                    raise error


    @staticmethod
    def request (enlace:Enlace, timeout:int=-1, logger:Logger=None, *args, **kwargs):
        while True:
            try:
                header = Data_header.request(enlace, timeout, *args, **kwargs)
                payload = enlace.receive(header.size, timeout)
                end = enlace.receive(len(Package.END), timeout)

                if logger != None:
                    logger.info(f'Received Data ({header.type}) {header.index} of {header.length} in {Data_header.SIZE + len(payload) + len(Package.END)} bytes.')

                if end != Package.END:
                    enlace.clear()

                    raise Package.InvalidEndException()

                Success_package(header.index).submit(enlace, logger)

                return Data_package(header.length, header.index, payload)
            except Data_header.UnnexpectedDataException as error:
                enlace.clear()
                Error_package(error.header.index).submit(enlace, logger)
                pass

            except Enlace.TimeoutException as error:
                raise Package.TimeoutException(error.time)

            except Package.InvalidEndException:
                print('ERR EOP RX')
                enlace.clear()
                Error_package(header.index).submit(enlace, logger)
                pass


Package.register_type(Data_package)
