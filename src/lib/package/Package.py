from abc import ABC, abstractmethod

from lib.enlace.Enlace import Enlace
from lib.header.Header import *


class Package (ABC):
    END = b'\xAA\xBB\xCC\xDD'
    _types = []


    def __init__ (self, length:int=1, index:int=1):
        if length > 255 or index > 255:
            raise Package.ExcededSizeLimitException()

        self.length = length
        self.index = index


    @staticmethod
    def register_type ( instance):
        Package._types.append(instance)


    @staticmethod
    @abstractmethod
    def encode() -> bytes:
        return bytes()


    def submit (self, enlace:Enlace):
        package = self.encode()

        enlace.transmit( package)

        return package


    @staticmethod
    def request (header_instance:Header, enlace:Enlace, timeout:int=-1, *args, **kwargs):
        header = header_instance.request(enlace, timeout, *args, **kwargs)
        end = enlace.receive(len(Package.END), timeout)

        if end != Package.END:
            enlace.clear()

            raise Package.InvalidEndException()

        return header


    class ExcededSizeLimitException (Header.ExcededSizeLimitException):
        """configuration parameters exceed the data per byte limit.
        """
        pass


    class TimeoutException (Enlace.TimeoutException):
        """The requested Package was not received within the timeout
        """
        pass


    class InvalidPackageException (Exception):
        """The received Package is not valid
        """
        pass


    class InvalidEndException (InvalidPackageException):
        """The requested Package received an invalid End of Package
        """
        pass
