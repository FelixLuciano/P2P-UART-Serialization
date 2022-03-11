from lib.package import Package


class Commands:
    @staticmethod
    def tryServerConnection (thread):
        while True:
            print('Trying to connect to the server...')
            Package(type_='ping').submit(thread)

            response = Package.request(thread, timeout=5)

            if response.type == 'error':
                tryAgain = input('Server down. Try again? Y/N ')

                if tryAgain.lower() not in ('y', 'yes'):
                    exit()
            elif response.type == 'pong':
                break

        print('Connected to the server successfully!')


    @staticmethod
    def acceptConnection (thread):
        print('Waiting for connection request...')

        while True:
            if Package.request(thread).type == 'ping':
                Package(type_='pong').submit(thread)

                break

        print('Client successfully connected!')
