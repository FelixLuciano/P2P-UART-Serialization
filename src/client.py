import time
import random

import numpy as np

from enlace import Enlace
from commands import Commands


# SERIAL_NAME = '/dev/ttyACM0'          # Ubuntu
# SERIAL_NAME = '/dev/tty.usbmodem1411' # Mac
SERIAL_NAME = 'COM5'                  # Windows

Commands.add(0x00, 0xFF, 0x00, 0xFF)
Commands.add(0x00, 0xFF, 0xFF, 00)
Commands.add(0xFF)
Commands.add(0x00)
Commands.add(0xFF, 0x00)
Commands.add(0x00, 0xFF)


def main ():
    com1 = Enlace(SERIAL_NAME)

    try:
        com1.enable()
        print('Serial port enabled successfully!')

        txBuffer = Commands.getSequence(random.randint(10, 30))
        txLen = len(txBuffer)
        begin = time.monotonic()

        buffer, size = com1.transmit(txBuffer)
        print('sending', txLen, 'commands through', size, 'B of data to', SERIAL_NAME, '...')

        print('Waiting for server response...')

        rxBuffer, size = com1.getData()
        finish = time.monotonic()
        response = rxBuffer[0][0]

        print(f'Received response through', size, 'B of data after', f'{(finish - begin) * 1000:.3g}', 'ms.\nResponse:', response)

        if response == txLen:
            print('Success!')
        else:
            print('Fail!')

    except Exception as error:
        print('ops! :-\\\n', error)

    finally:
        com1.disable()
        print('Serial port disabled.')


main() if __name__ == '__main__' else None
