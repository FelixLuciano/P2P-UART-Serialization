from lib.header.Header import Header


class Success_header (Header):
    type = 0x04


    def __init__ (self, package_index:int=0):
        if package_index > 255:
            raise Header.ExcededSizeLimitException()

        super().__init__()
        self.package_index = package_index


    @classmethod
    def decode (cls, data:bytes, package_index:int=0):
        super().decode(data)

        header = Success_header(
          package_index = int.from_bytes(data[7:8], 'big')
        )

        if package_index and header.package_index != package_index:
            raise Success_header.UnexpectedSuccessException(header)

        return header


    def encode (self):
        data = super().encode()

        data[7:8] = self.package_index.to_bytes(1, 'big')

        return bytes(data)


    class UnexpectedSuccessException (Header.UnexpectedHeaderException):
        """The Success received does not have the expected package index
        """
        pass


Header.register_type(Success_header)
