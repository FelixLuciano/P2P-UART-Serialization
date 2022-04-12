from lib.thread import Thread


class Header:
    SIZE = 10
    TYPES = {
        'request': 0x01,
        'response': 0x02,
        'data': 0x03,
        'success': 0x04,
        'timeout': 0x05,
        'error': 0x06,
    }


    def __init__ (self, type_:str='data', length:int=1, index:int=1, size:int=0):
        self.type = type_
        self.type_byte = self.TYPES[self.type]
        self.length = length
        self.index = index
        self.size = size


    @classmethod
    def getType (cls, byte:int):
        typeBytes = list(cls.TYPES.values())

        if byte in typeBytes:
            index = typeBytes.index(byte)

            return list(cls.TYPES.keys())[index]

        return 'data'


    def encode (self):
        header = bytearray()

        # Byte h0 - Package type
        header.extend(self.type_byte.to_bytes(2, 'big'))

        # Byte h1 - NC
        header.extend((0).to_bytes(2, 'big'))

        # Byte h2 - NC
        header.extend((0).to_bytes(2, 'big'))

        # Byte h3 - Stream length
        header.extend(self.length.to_bytes(2, 'big'))

        # Byte h4 - Package index
        header.extend(self.index.to_bytes(2, 'big'))

        # Byte h5 - Request ID / Payload size
        if self.type == 'request':
            header.extend(self.index.to_bytes(2, 'big'))
        elif self.type == 'data':
            header.extend(self.size.to_bytes(2, 'big'))
        else:
            header.extend((0).to_bytes(2, 'big'))

        # Byte h6 - Case error: Expected package index
        if self.type == 'error':
            header.extend(self.index.to_bytes(2, 'big'))
        else:
            header.extend((0).to_bytes(2, 'big'))

        # Byte h7 - Case success: Received package index
        if self.type == 'success':
            header.extend(self.index.to_bytes(2, 'big'))
        else:
            header.extend((0).to_bytes(2, 'big'))

        # Byte h8 - CRC
        header.extend((0).to_bytes(2, 'big'))

        # Byte h9 - CRC
        header.extend((0).to_bytes(2, 'big'))

        return bytes(header)


    @classmethod
    def decode (cls, data:bytes):
        if len(data) == 0:
            return cls(type_='error')

        type_ = cls.getType(int.from_bytes(data[0]), 'big')

        length_byte = int.from_bytes(data[3])

        if type_ == 'data':
            index_byte = int.from_bytes(data[4], 'big')
            size_byte = int.from_bytes(data[5], 'big')
        elif type_ == 'request':
            index_byte = int.from_bytes(data[5], 'big')
        elif type_ == 'error':
            index_byte = int.from_bytes(data[6], 'big')
        elif type_ == 'success':
            index_byte = int.from_bytes(data[7], 'big')

        if type_ != 'data':
            size_byte = None

        return cls(
            type_=type_,
            length=length_byte,
            index=index_byte,
            size=size_byte
        )


    @classmethod
    def request (cls, thread:Thread, type_:str=None, length:int=None, index:int=None, size:int=None, timeout:int=-1):
        data, size = thread.receive(cls.SIZE, timeout=timeout)

        if size == 0:
            return cls(type_='timeout', type_=type_, length=length, index=index, size=size)

        return cls.decode(data)


test = Header(type_='request')
