from lib.header.Header import Header


class Response_header (Header):
    type = 0x02


    def __init__ (self):
        super().__init__()


    @classmethod
    def decode (cls, data:bytes):
        super().decode(data)

        return Response_header()


    def encode (self):
        return bytes(super().encode())


Header.register_type(Response_header)
