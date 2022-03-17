# import time

from lib.thread import Thread
from lib.commands import tryServerConnection
from lib.stream import Stream


# SERIAL_NAME = '/dev/ttyACM0'          # Ubuntu
# SERIAL_NAME = '/dev/tty.usbmodem1411' # Mac
SERIAL_NAME = 'COM3'                  # Windows

INPUT_IMAGE  = 'image.webp'


def main ():
    com1 = Thread(SERIAL_NAME)

    try:
        com1.enable()
        tryServerConnection(com1, timeout=5)   

        with open(INPUT_IMAGE, 'rb') as file:
            package = Stream(data=file.read())

        package.submit(com1, timeout=1)
    except KeyboardInterrupt:
        pass
    except Exception as error:
        print('ops! :-\\\n', error)

    finally:
        com1.disable()


if __name__ == '__main__':
    main()
