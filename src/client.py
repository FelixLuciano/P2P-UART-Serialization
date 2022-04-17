from UART import UART


def main ():
    try:
        with UART() as com:
            com.push_data(b'Hey!', 1, 10)

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
