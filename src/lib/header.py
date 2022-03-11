from lib.thread import Thread


class Header:
    SIZE = 10
    TYPES = {
        'ping': 0x00,
        'pong': 0x01,
        'request': 0x02,
        'response': 0x03,
        'success': 0x04,
        'error': 0x05
    }


    def __init__ (self, type_:str, index:int=0, length:int=0, size:int=0):
        self.type = [k for k, v in self.TYPES.items() if type_ == v][0] if type(type_) != str else type_
        self.type_byte = self.TYPES[type_] if type(type_) == str else type_
        self.index = index
        self.length = length
        self.size = size


    def encode (self):
        header = []

        header.append(self.type_byte.to_bytes(1, 'big'))
        header.append(self.index.to_bytes(1, 'big'))
        header.append(self.length.to_bytes(1, 'big'))
        header.append(self.size.to_bytes(1, 'big'))
        header.append(bytes(self.SIZE - len(header)))

        return b''.join(header)


    @classmethod
    def decode (cls, data:bytes):
        if len(data) == 0:
            return cls(type_='error')

        return cls(
            type_= data[0],
            index= data[1],
            length= data[2],
            size= data[3]
        )


    @classmethod
    def request (cls, thread:Thread, timeout:int=-1):
        data, size = thread.request(cls.SIZE, timeout=timeout)

        return cls.decode(data)
