from lib.package import Package


def tryServerConnection (thread, timeout:int=-1):
    while True:
        print('Trying to connect to the server...')
        Package(type_='ping').submit(thread=thread, timeout=timeout)

        response = Package.request(thread=thread, type_='pong', timeout=timeout)

        if response.type == 'pong':
            break

    print('Connected to the server successfully!')


def acceptClientConnection (thread):
    print('Waiting for connection request...')

    while True:
        if Package.request(thread=thread, type_='ping').type == 'ping':
            Package(type_='pong').submit(thread=thread)

            break

    print('Client successfully connected!')
