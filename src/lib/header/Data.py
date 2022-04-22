from lib.header.Header import Header


class Data_header (Header):
    type = 0x03
    MAX_PAYLOAD_SIZE = 114


    def __init__ (self, length:int=1, index:int=1, size:int=0, crc:int=0):
        if size > Data_header.MAX_PAYLOAD_SIZE:
            raise Header.ExcededSizeLimitException()

        super().__init__(length, index, crc)
        self.size = size


    @classmethod
    def decode (cls, data:bytes, length:int=None, index:int=None, size:int=None):
        super().decode(data)

        header = Data_header(
          length = int.from_bytes(data[3:4], 'big'),
          index = int.from_bytes(data[4:5], 'big'),
          size = int.from_bytes(data[5:6], 'big'),
          crc = int.from_bytes(data[8:10], 'big')
        )

        if (
          length and header.length != length or
          index and header.index != index or
          size and header.size != size
        ):
          raise Data_header.UnexpectedDataException(header)

        return header


    def encode (self) -> bytes:
        data = super().encode()

        data[5:6] = self.size.to_bytes(1, 'big')

        return bytes(data)


    class UnexpectedDataException (Header.UnexpectedHeaderException):
      """The received Data does not have the expected parameters
      """
      pass


Header.register_type(Data_header)
