from abc import ABC, abstractmethod

from lib.enlace.Enlace import Enlace


class Header (ABC):
    SIZE = 10
    type = None
    _types = []


    def __init__ (self, length:int=1, index:int=1, crc:int=0):
        if length > 255 or index > 255:
            raise Header.ExcededSizeLimitException()
        elif crc > 255**2:
            raise Header.ExcededSizeLimitException()

        self.length = length
        self.index = index
        self.crc = crc


    @staticmethod
    def register_type (instance) -> None:
        Header._types.append(instance)


    def encode (self):
        header = bytearray()

        # Byte h0 - Package type
        header.extend(self.type.to_bytes(1, 'big'))

        # Byte h1 - NC
        header.extend((0).to_bytes(1, 'big'))

        # Byte h2 - NC
        header.extend((0).to_bytes(1, 'big'))

        # Byte h3 - Stream length
        header.extend(self.length.to_bytes(1, 'big'))

        # Byte h4 - Package index
        header.extend(self.index.to_bytes(1, 'big'))

        # Bytes h5, h6 & h7 - Reserved to type
        header.extend((0).to_bytes(1, 'big'))
        header.extend((0).to_bytes(1, 'big'))
        header.extend((0).to_bytes(1, 'big'))

        # Bytes h8, h9 - Cyclic Redundancy Check
        header.extend((self.crc).to_bytes(2, 'big'))

        return header


    @classmethod
    @abstractmethod
    def decode (cls, data:bytes, *args, **kwargs):
        type_byte = data[0:1]
        type_value = int.from_bytes(type_byte, 'big')

        if cls.type:
            if type_value != cls.type:
                raise Header.UnexpectedHeaderException(Header.decode(data))

        else:
            for instance in Header._types:
                if type_value == instance.type:
                    return instance.decode(data, *args, **kwargs)

            raise Header.UnregisteredTypeException(type_value)


    @staticmethod
    def request (enlace:Enlace, timeout:int=-1, *args, **kwargs):
        try:
            data = enlace.receive(Header.SIZE, timeout)

            return Header.decode(data, *args, **kwargs)

        except Enlace.TimeoutException as error:
            raise Header.TimeoutException(error.time)

    
    class ExcededSizeLimitException (Exception):
        """configuration parameters exceed the data per byte limit.
        """
        pass


    class UnregisteredTypeException (Exception):
        """Given header type was not found
        """
        def __init__ (self, type_, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.type = type_


    class UnexpectedHeaderException (Exception):
        """The received header was not expected
        """
        def __init__ (self, header, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.header = header


    class TimeoutException (Enlace.TimeoutException):
        """The request header was not received within the timeout
        """
        pass
