import sys
import os
import unittest
from threading import Thread

from dotenv import dotenv_values

sys.path.append(os.path.join('src'))
from lib.interface import Interface
from lib.enlace import Enlace
from lib.stream import Data_stream
from lib.package.Data import Data_package

config = dotenv_values()


class Test__Data_stream (unittest.TestCase):
    def test__encode (self):
        """ To do.
        """
        stream = Data_stream(b'Stet erat consequat et erat et consetetur dignissim sit. At lorem est erat possim praesent at velit nulla sed te amet diam erat lorem labore.')
        result = b''.join([package.encode() for package in stream.encode()])

        self.assertEqual(result, b'\x03\x00\x00\x02\x01\x72\x00\x00\x00\x00Stet erat consequat et erat et consetetur dignissim sit. At lorem est erat possim praesent at velit nulla sed te a\xAA\xBB\xCC\xDD\x03\x00\x00\x02\x02\x1B\x00\x00\x00\x00met diam erat lorem labore.\xAA\xBB\xCC\xDD')
        self.assertEqual(len(stream), 2)


    def test__decode (self):
        """ To do.
        """
        data = [
            Data_package(2, 1, b'Stet erat consequat et erat et consetetur dignissim sit. At lorem est erat possim praesent at velit nulla sed te a'),
            Data_package(2, 2, b'met diam erat lorem labore.')
        ]
        result = Data_stream.decode(data)

        self.assertEqual(result.data, b'Stet erat consequat et erat et consetetur dignissim sit. At lorem est erat possim praesent at velit nulla sed te amet diam erat lorem labore.')
        self.assertEqual(len(result), 2)


    def test__submit (self):
        """ To do.
        """
        com = Interface.get_available_interface()
        enlace = Enlace(com)
        thread = Thread(target=self._test__submit__server)

        try:
            enlace.enable()
            thread.start()

            Data_stream(b'Hello World!').submit(enlace, 1, 1)
            
            self.assertEqual(self.response.data, b'Hello World!', msg='Timeout! No success response.')

        finally:
            enlace.disable()


    def _test__submit__server (self):
        com = Interface.get_available_interface()
        enlace = Enlace(com)

        try:
            enlace.enable()

            self.response = Data_stream.request(enlace, 1, 1)

        finally:
            enlace.disable()


if __name__ == '__main__':
    unittest.main()
