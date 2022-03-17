from lib.header import Header
from lib.thread import Thread


class Package:
    EOP = b'\xDB\x66\x99\xDB'


    def __init__ (self, type_:str='data', index:int=0, length:int=1, data:bytes=b''):
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
    def request (cls, thread:Thread, type_:str=None, index:int=None, length:int=None, size:int=None, timeout:int=-1):
        header = Header.request(thread, timeout=timeout/3)
        data, _ = thread.receive(header.size, timeout=timeout/3)
        eop, _ = thread.receive(len(cls.EOP), timeout=timeout/3)

        if (type_ and header.type != type_ or
            index and header.index != index or
            length and header.length != length or
            size and header.size != size or
            eop != cls.EOP
        ):
            return cls(type_='error')

        if header.type != 'success':
            cls(type_='success').submit(thread=thread, timeout=timeout)

        return cls(
            type_ = header.type,
            index = header.index,
            length = header.length,
            data = data
        )



    def submit (self, thread:Thread, timeout:int=-1):
        while True:
            thread.transmit(self.encode())

            if self.type != 'success':
                success, done = self.getSuccessDone(
                    thread=thread,
                    message=f'Failed do submit {self.type} at {self.index + 1} of {self.length}.',
                    timeout=timeout
                )

                if success and done:
                    break
                if not success and done:
                    exit()
            else:
                break


    @classmethod
    def getSuccessDone (cls, thread:Thread, message:str='Attempt failed.', timeout:int=-1):
        response = cls.request(thread, type_='success', timeout=timeout)

        if  response.type == 'error':
            print('[Error]', message, end=' ')

            tryAgain = input('Try again? y/n ')

            if tryAgain.lower() not in ('y', 'yes'):
                return False, True
            else:
                return False, False
        elif response.type == 'success':
            return True, True
        else:
            return False, True
