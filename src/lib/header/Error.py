from lib.header.Header import Header


class Error_header (Header):
    type = 0x06


    def __init__ (self, package_index:int=0):
        if package_index > 255:
            raise Header.ExcededSizeLimitException()

        super().__init__()
        self.package_index = package_index


    @classmethod
    def decode (cls, data:bytes, package_index:int=None):
        super().decode(data)

        header = Error_header(
          package_index = int.from_bytes(data[6:7], 'big')
        )

        if package_index and header.package_index != package_index:
          raise Error_header.UnexpectedErrorException(header)

        return header


    def encode (self) -> bytes:
        data = super().encode()

        data[6:7] = self.package_index.to_bytes(1, 'big')

        return bytes(data)


    class UnexpectedErrorException (Header.UnexpectedHeaderException):
        """The Error received does not have the expected package index
        """
        pass


Header.register_type(Error_header)
