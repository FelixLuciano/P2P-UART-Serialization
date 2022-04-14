import sys
import os
import unittest
from threading import Thread

from dotenv import dotenv_values

sys.path.append(os.path.join('src'))
from lib.thread import Thread as Thread_
from lib.stream import Data_stream

config = dotenv_values()


class TestStream (unittest.TestCase):
    def test_Stream_encode (self):
        """Tests if Data Stream with some data can be encoded properly.
        """
        stream = Data_stream(data=b'Stet erat consequat et erat et consetetur dignissim sit. At lorem est erat possim praesent at velit nulla sed te amet diam erat lorem labore.')
        print(stream.encode())
        data = b''.join([package.encode() for package in stream.encode()])
        
        self.assertEqual(data, b'\x03\x00\x00\x02\x01\x72\x00\x00\x00\x00Stet erat consequat et erat et consetetur dignissim sit. At lorem est erat possim praesent at velit nulla sed te a\xAA\xBB\xCC\xDD\x03\x00\x00\x02\x02\x1B\x00\x00\x00\x00met diam erat lorem labore.\xAA\xBB\xCC\xDD')


    def test_Stream_submit (self):
        com = Thread_(config.get('CLIENT_PORT'))
        thread = Thread(target=self._test_Stream_submit_server)
        stream = Data_stream(b'Hello World!')

        try:
            com.enable()
            thread.start()

            success = stream.submit(thread=com, target=1, timeout=1)
            
            self.assertEqual(success, True, msg='Timeout! No success response.')
        finally:
            com.disable()

    def _test_Stream_submit_server (self):
        com = Thread_(config.get('SERVER_PORT'))

        try:
            com.enable()
            response = Data_stream.request(thread=com, target=1, timeout=1)

            self.assertIsNotNone(response, msg='Timeout! No data received.')
            self.assertEqual(response.data, b'Hello World', msg='Incorrect data!')
        finally:
            com.disable()


if __name__ == '__main__':
    unittest.main()
