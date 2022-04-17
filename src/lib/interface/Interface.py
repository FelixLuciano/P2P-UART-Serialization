import sys
import glob
import binascii

import serial


class Interface:
    BAUDRATE = 115200
    # BAUDRATE = 57600
    # BAUDRATE = 38400
    # BAUDRATE = 31250
    # BAUDRATE = 28800
    # BAUDRATE = 19200
    # BAUDRATE = 14400
    # BAUDRATE = 9600
    # BAUDRATE = 4800
    # BAUDRATE = 2400
    # BAUDRATE = 1200
    # BAUDRATE = 600
    # BAUDRATE = 300
    BYTESIZE = serial.EIGHTBITS
    PARITY = serial.PARITY_NONE
    STOPBITS = serial.STOPBITS_ONE
    TIMEOUT = 0.1
    port = None


    def __init__ (self, port:str):
        self.name = port
        self.rxRemain = b''


    @staticmethod
    def list_ports () -> list[str]:
        """ From: https://stackoverflow.com/a/70514001/13587869
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % i for i in range(1, 256)]

        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')

        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')

        else:
            raise EnvironmentError('Unsupported platform')

        result = []

        for index, port in enumerate(ports):
            try:
                serial.Serial(port).close()
                result.append(port)

            except (OSError, serial.SerialException):
                pass

        return result

    
    @staticmethod
    def get_available_interface ():
        ports = Interface.list_ports()

        if len(ports) > 0:
            return Interface(ports[0])


    def open (self) -> None:
        self.port = serial.Serial(
            port = self.name,
            baudrate = self.BAUDRATE,
            bytesize = self.BYTESIZE,
            parity = self.PARITY,
            stopbits = self.STOPBITS,
            timeout = self.TIMEOUT
        )


    def close (self) -> None:
        self.port.close()


    def flush (self) -> None:
        self.port.flushInput()
        self.port.flushOutput()


    @staticmethod
    def encode (data:bytes) -> bytes:
        return binascii.hexlify(data)


    @staticmethod
    def decode (data:bytes) -> bytes:
        return binascii.unhexlify(data)


    def write (self, txBuffer:bytes) -> int:
        """ Write data to serial port

        This command takes a buffer and format
        it before transmit. This is necessary
        because the pyserial and arduino uses
        Software flow control between both
        sides of communication.
        """
        nTx = self.port.write(self.encode(txBuffer))

        self.flush()

        return nTx // 2


    def read (self, nBytes:int) -> tuple[bytes, int]:
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
            return b'', 0
