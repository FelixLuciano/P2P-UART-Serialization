import math
from abc import ABC, abstractmethod

from lib.enlace.Enlace import Enlace
from lib.header.Header import *


class Package (ABC):
    END = b'\xAA\xBB\xCC\xDD'
    GENERATOR_POLYNOMIAL = 0b1011010110101101
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

    
    @staticmethod
    def cyclic_redundancy_check (data:bytes, crc:int=0):
        len_bits = lambda number: math.floor(math.log(number) / math.log(2) + 1)
        get_bit = lambda number, index: (number >> index) & 1

        divisor = int.from_bytes(data, 'big')
        divisor_size = len_bits(divisor) - 1
        dividend_size = len_bits(Package.GENERATOR_POLYNOMIAL) - 1

        divisor = (divisor << dividend_size) | crc
        remainder = divisor >> divisor_size

        for i in range(divisor_size):
            b0 = get_bit(remainder, dividend_size)

            if b0 == 1:
                remainder ^= Package.GENERATOR_POLYNOMIAL

            remainder <<= 1
            remainder |= get_bit(divisor, divisor_size - i - 1)

        return remainder


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
