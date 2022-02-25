import time
import random

import numpy as np

from enlace import Enlace
from commands import Commands


# SERIAL_NAME = '/dev/ttyACM0'          # Ubuntu
# SERIAL_NAME = '/dev/tty.usbmodem1411' # Mac
SERIAL_NAME = 'COM3'                  # Windows

INPUT_IMAGE  = 'image.webp'
OUTPUT_IMAGE = 'output.webp'

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

        sequence = Commands.getSequence(random.randint(10, 30))
        txBuffer = Commands.getStream(sequence)
        txLen = len(txBuffer)
        begin = time.monotonic()

        print('sending', len(sequence), 'commands through', txLen, 'kb of data to', SERIAL_NAME, '...\n', txBuffer)
        com1.transmit(txBuffer)

        print('Waiting for server response...')

        rxBuffer, nRx = com1.getData()
        finish = time.monotonic()

        print(f'Recieved {len(rxBuffer)} kb of data after {(finish - begin) * 1000:.3g} ms.\n', rxBuffer)

    except Exception as error:
        print('ops! :-\\\n', error)

    finally:
        com1.disable()
        print('Serial port disabled.')


main() if __name__ == '__main__' else None
