from lib.header import Header
from lib.thread import Thread


class Package:
    EOP = b'\xDB\x66\x99\xDB'


    def __init__ (self, type_:str, index:int=0, length:int=1, data:bytes=b''):
        self.type = type_
        self.index = index
        self.length = length
        self.data = data


    def encode (self):
        package = []
        header = Header(
            type_ = self.type,
            index = self.index,
            length = self.length,
            size = len(self.data)
        )

        package.append(header.encode())
        package.append(self.data)
        package.append(self.EOP)

        return b''.join(package)


    @classmethod
    def request (cls, thread:Thread, type_:str=None, index:int=0, timeout:int=-1):
        header = Header.request(thread, timeout=timeout)
        data, _ = thread.request(header.size, timeout=timeout)
        eop, _ = thread.request(len(cls.EOP), timeout=timeout)

        if (index != header.index or
            type_ and header.type != type or
            eop != cls.EOP
        ):
            return cls(type_='error')

        return cls(
            type_ = header.type,
            index = header.index,
            length = header.length,
            data = data
        )


    def submit (self, thread:Thread):
        thread.submit(self.encode())
