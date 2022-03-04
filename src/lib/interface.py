import binascii

import serial


class Interface(object):
    def __init__ (self, name):
        self.name = name
        self.port = None
        # self.baudrate = 115200
        self.baudrate = 9600
        self.bytesize = serial.EIGHTBITS
        self.parity = serial.PARITY_NONE
        self.stop = serial.STOPBITS_ONE
        self.timeout = 0.1
        self.rxRemain = b''


    def open (self):
        self.port = serial.Serial(
            self.name,
            self.baudrate,
            self.bytesize,
            self.parity,
            self.stop,
            self.timeout
        )


    def close (self):
        self.port.close()


    def flush (self):
        self.port.flushInput()
        self.port.flushOutput()


    def encode (self, data):
        return binascii.hexlify(data)


    def decode (self, data):
        return binascii.unhexlify(data)


    def write (self, txBuffer):
        """ Write data to serial port

        This command takes a buffer and format
        it before transmit. This is necessary
        because the pyserial and arduino uses
        Software flow control between both
        sides of communication.
        """
        nTx = self.port.write(self.encode(txBuffer))

        self.flush()

        return nTx / 2


    def read (self, nBytes):
        """ Read nBytes from the UART com port

        Not all reading returns a multiple of 2
        we must check this to prevent the self.
        decode function from being called with
        odd numbers.
        """
        rxBuffer = self.port.read(nBytes)
        rxBufferConcat = self.rxRemain + rxBuffer
        nValid = (len(rxBufferConcat) // 2) * 2
        rxBufferValid = rxBufferConcat[0:nValid]

        self.rxRemain = rxBufferConcat[nValid:]

        try:
            """ Sometimes there are errors in decoding
            outside the linux environment, this tries
            to partially correct these errors. Improve
            in the future. often a flush at the
            beginning solves!
            """
            # self.flush()

            rxBufferDecoded = self.decode(rxBufferValid)
            nRx = len(rxBuffer)

            return rxBufferDecoded, nRx

        except:
            print('[ERROR] Physical interface, read, decode. buffer:\n', rxBufferValid)

            return b'', 0
