from UART import UART


def main ():
    try:
        with UART() as com:
            data = com.pull_data(2, 10)

            print(data)

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
