from UART import UART


def main ():
    try:
        data = {
            'foo': 'bar',
            'value': 123,
            'test': True
        }

        with UART() as com:
            com.push_data(data, 1, 10)

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
