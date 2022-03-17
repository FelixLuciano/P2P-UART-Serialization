import os

from lib.thread import Thread
from lib.commands import acceptClientConnection
from lib.stream import Stream


# SERIAL_NAME = '/dev/ttyACM0'          # Ubuntu
# SERIAL_NAME = '/dev/tty.usbmodem1411' # Mac
SERIAL_NAME = 'COM5'                  # Windows

OUTPUT_IMAGE = 'output.webp'


def main ():
    com1 = Thread(SERIAL_NAME)

    if os.path.isfile(OUTPUT_IMAGE):
        os.remove(OUTPUT_IMAGE)

    try:
        com1.enable()
        acceptClientConnection(com1)

        response = Stream.request(com1, timeout=5)

        with open(OUTPUT_IMAGE, 'wb') as file:
            file.write(response.data)
    except KeyboardInterrupt:
        pass
    except Exception as error:
        print('ops! :-\\\n', error)

    finally:
        com1.disable()


if __name__ == '__main__':
    main()
