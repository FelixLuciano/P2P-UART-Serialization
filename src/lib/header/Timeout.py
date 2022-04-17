from lib.header.Header import Header


class Timeout_header (Header):
    type = 0x05


    def __init__ (self):
        super().__init__()


    @classmethod
    def decode (cls, data:bytes):
        super().decode(data)

        return Timeout_header()


    def encode (self):
        return bytes(super().encode())


Header.register_type(Timeout_header)
