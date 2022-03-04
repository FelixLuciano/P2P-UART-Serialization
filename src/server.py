from lib.enlace import Enlace


# SERIAL_NAME = '/dev/ttyACM0'          # Ubuntu
# SERIAL_NAME = '/dev/tty.usbmodem1411' # Mac
SERIAL_NAME = 'COM9'                  # Windows


def main ():
    com1 = Enlace(SERIAL_NAME)

    try:
        com1.enable()
        print('Serial port enabled successfully!')

        rxBuffer, size = com1.getData()

        nCommands = len(rxBuffer)

        print(f'Received', nCommands, 'commands through', size, 'B of data from', SERIAL_NAME,'.')

        com1.transmit(nCommands.to_bytes(1, 'big'))

        print('Sending response to client.')

    except Exception as error:
        print('ops! :-\\\n', error)

    finally:
        com1.disable()
        print('Serial port disabled.')


main() if __name__ == '__main__' else None
