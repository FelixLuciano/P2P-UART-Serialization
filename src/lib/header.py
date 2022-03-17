from lib.thread import Thread


class Header:
    SIZE = 10
    TYPES = {
        'ping': 0x00,
        'pong': 0x01,
        'data': 0x02,
        'success': 0x03,
        'error': 0x04
    }


    def __init__ (self, type_:str='data', index:int=0, length:int=0, size:int=0):
        self.index = index
        self.length = length
        self.size = size

        if type(type_) != str:
            try:
                index = list(self.TYPES.values()).index(type_)
                self.type = list(self.TYPES.keys())[index]
            except:
                self.type = 'data'

            self.type_byte = self.type
        else:
            self.type = type_
            self.type_byte = self.TYPES[self.type]


    def encode (self):
        header = bytearray()

        header.extend(self.type_byte.to_bytes(1, 'big'))
        header.extend(self.index.to_bytes(2, 'big'))
        header.extend(self.length.to_bytes(2, 'big'))
        header.extend(self.size.to_bytes(1, 'big'))
        header.extend(bytes(self.SIZE - len(header)))

        return bytes(header)


    @classmethod
    def decode (cls, data:bytes):
        if len(data) == 0:
            return cls(type_='error')

        return cls(
            type_= int.from_bytes(data[0:1], 'big'),
            index= int.from_bytes(data[1:3], 'big'),
            length= int.from_bytes(data[3:5], 'big'),
            size= int.from_bytes(data[5:6], 'big')
        )


    @classmethod
    def request (cls, thread:Thread, timeout:int=-1):
        data, size = thread.receive(cls.SIZE, timeout=timeout)

        return cls.decode(data)
