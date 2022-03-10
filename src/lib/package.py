class Package:
    TYPES = {
        'ping': 0x00,
        'pong': 0x01,
        'request': 0x01,
        'response': 0x01,
        'success': 0x03,
        'error': 0x04
    }

    SOP = bytes(bytearray((0xB7, )))
    EOP = bytes(bytearray((0xDB, 0x66, 0x99, 0xDB)))

    # PAYLOAD_SIZE = 114
    PAYLOAD_SIZE = 2


    def __init__ (self, data, _type, **kwargs):
        self.data = data
        self.type = _type


    def encode (self):
        packages = []
        payloads = self.splitData(self.data, self.PAYLOAD_SIZE)

        for index, payload in enumerate(payloads):
            package = []

            package.append(self.SOP)

            packageType_byte = (self.TYPES[self.type]).to_bytes(1, 'big')
            package.append(packageType_byte)

            packageIndex_byte = index.to_bytes(1, 'big')
            package.append(packageIndex_byte)

            streamLen_Byte = len(payloads).to_bytes(1, 'big')
            package.append(streamLen_Byte)

            payloadSize_byte = len(payload).to_bytes(1, 'big')
            package.append(payloadSize_byte)

            empty_bytes = bytes(10 - len(package))
            package.append(empty_bytes)

            package.append(payload.encode())

            package.append(self.EOP)

            packages.append(b''.join(package))

        return packages


    @classmethod
    def validate (self, package, packageIndex, streamSize):
        if not package.startswith(self.SOP):
            return False
        elif not package.endswith(self.EOP):
            return False
        elif package[2] != packageIndex:
            return False
        elif package[3] != streamSize:
            return False
        elif package[4] != len(self.decode(package)):
            return False

        return True


    @classmethod
    def decode (self, package):
        return package[10: -4] #  if self.validate(package) else b''


    @classmethod
    def splitData (self, data, size):
        dataLen = len(data)
        buffer = []

        for i in range(0, dataLen, size):
            buffer.append(data[i:min(i+size, dataLen)])

        return buffer


    @classmethod
    def getBufferSize (self, buffer):
        return sum(map(len, buffer))


test = Package('Hello World!', 'response')
result = test.encode()
data = b''.join(map(Package.decode, result))

print(result)
print(data)

for index, package in enumerate(result):
    print(Package.validate(package, index, len(result)))
