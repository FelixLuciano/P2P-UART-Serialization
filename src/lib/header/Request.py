from lib.header.Header import Header


class Request_header (Header):
    type = 0x01


    def __init__ (self, target:int=0, length:int=0):
        if target > 255:
            raise Header.ExcededSizeLimitException()

        super().__init__(length)
        self.target = target


    @classmethod
    def decode (cls, data:bytes, target:int=None):
        super().decode(data)

        header = Request_header(
          length = int.from_bytes(data[3:4], 'big'),
          target = int.from_bytes(data[5:6], 'big')
        )

        if target and header.target != target:
            raise Request_header.UnexpectedRequestException(header)

        return header


    def encode (self):
        data = super().encode()

        data[5:6] = self.target.to_bytes(1, 'big')

        return bytes(data)


    class UnexpectedRequestException (Header.UnexpectedHeaderException):
        """The Request received does not have the expected target
        """
        pass


Header.register_type(Request_header)
