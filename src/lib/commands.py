from sqlalchemy import false
from lib.package import Package
import time


def tryServerConnection (thread, timeout:int=-1):
    inicia = False
    while inicia == False:
        print('Trying to connect to the server...')
        Package(type_='request').submit(thread=thread, timeout=timeout, id = 1)
        
        response = Package.request(thread=thread, type_='response', timeout=timeout)

        if response.type == 'response':
            inicia == True

    print('Connected to the server successfully!')


def acceptClientConnection (thread):
    print('Waiting for connection request...')
    ocioso = True
    while ocioso == True:
        request = Package.request(thread=thread, type_='request')
        if request.type == 'request' and request.id == 1:
            ocioso = False
        time.sleep(1)
    Package(type_='response').submit(thread=thread)
    print('Client successfully connected!')
