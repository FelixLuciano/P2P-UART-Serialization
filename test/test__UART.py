import sys
import os
import time
import base64
import unittest
from threading import Thread

sys.path.append(os.path.join('src'))
from UART import UART


class Test__UART (unittest.TestCase):
    def test__push (self):
        """ To do.
        """
        thread = Thread(target=self._test__pull__server)

        thread.start()
        time.sleep(0.5)

        with UART(log_filename='client1') as com:
            with open(os.path.join('assets', 'image', 'image.webp'), 'rb') as file:
                data = file.read().hex()
        
            com.push_data(data, 1, 1)

        result = bytes.fromhex(self.result)

        with open(os.path.join('assets', 'image', 'image.output.webp'), 'wb') as file:
            file.write(result)

        self.assertEqual(self.result, data)


    def _test__pull__server (self):
        with UART() as com:
            self.result = com.pull_data(1, 1)


    def test__pull (self):
        """ To do.
        """
        thread = Thread(target=self._test__push__client)

        thread.start()

        with UART() as com:
            result = com.pull_data(1, 1)

        self.assertEqual(result['foo'], 'bar')
        self.assertEqual(result['value'], 123)
        self.assertEqual(len(result['items']), 3)
        self.assertTrue(result['test'])


    def _test__push__client (self):
        data = {
            'foo': 'bar',
            'value': 123,
            'items': ['abc', 123, False],
            'test': True
        }

        time.sleep(0.5)

        with UART() as com:
            com.push_data(data, 1, 1)


    def test__push_timeout__exception (self):
        """ To do.
        """
        with UART() as com:
            self.assertRaises(UART.TimeoutException, com.push_data, 'Hey!', 1, 1)


    def test__pull_timeout__exception (self):
        """ To do.
        """
        with UART() as com:
            self.assertRaises(UART.TimeoutException, com.pull_data, 1, 1)


if __name__ == '__main__':
    unittest.main()
