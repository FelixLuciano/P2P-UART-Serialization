import time

from enlace import Enlace


# SERIAL_NAME = '/dev/ttyACM0'          # Ubuntu
# SERIAL_NAME = '/dev/tty.usbmodem1411' # Mac
SERIAL_NAME = 'COM5'                  # Windows


def main ():
    com1 = Enlace(SERIAL_NAME)

    try:
        com1.enable()
        print('Serial port enabled successfully!')

        begin = time.monotonic()
        rxBuffer, nRx = com1.getData(2)
        finish = time.monotonic()

        print(f'Recieved {len(rxBuffer)} kb of data after {(finish - begin) * 1000:.3g} ms.\n', rxBuffer)

        # Do stuff...

        print('sending', len(rxBuffer), 'kb of data to', SERIAL_NAME, '...')
        com1.transmit(rxBuffer)

    except Exception as error:
        print('ops! :-\\\n', error)

    finally:
        com1.disable()
        print('Serial port disabled.')


main() if __name__ == '__main__' else None
