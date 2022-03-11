from lib.thread import Thread
from lib.commands import Commands
from lib.package import Package
from lib.stream import Stream


# SERIAL_NAME = '/dev/ttyACM0'          # Ubuntu
# SERIAL_NAME = '/dev/tty.usbmodem1411' # Mac
SERIAL_NAME = 'COM5'                  # Windows


def main ():
    com1 = Thread(SERIAL_NAME)

    try:
        com1.enable()
        Commands.acceptConnection(com1)

        response = Stream.request(com1)
        print(response.type, response.data)

    except Exception as error:
        print('ops! :-\\\n', error)

    finally:
        com1.disable()


if __name__ == '__main__':
    main()
