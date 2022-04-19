import sys
import os
import time
import base64
import unittest
from threading import Thread
from random import randint

sys.path.append(os.path.join('src'))
from UART import UART


class Test__UART (unittest.TestCase):
    def test__push (self):
        """ To do.
        """
        thread = Thread(target=self._test__push__server)
        image_index = randint(1, 6)

        thread.start()
        time.sleep(0.5)

        with UART(log_filename='Client1') as com:
            with open(os.path.join('assets', 'image', f'image_{image_index}.webp'), 'rb') as file:
                data = file.read().hex()
        
            com.push_data(data, 1, 1)

        result = bytes.fromhex(self.result)

        with open(os.path.join('assets', 'image', f'image_{image_index}.output.webp'), 'wb') as file:
            file.write(result)

        self.assertEqual(self.result, data)


    def _test__push__server (self):
        with UART() as com:
            self.result = com.pull_data(1, 1)


    def test__pull (self):
        """ To do.
        """
        thread = Thread(target=self._test__pull__client)
        image_index = randint(1, 6)

        with open(os.path.join('assets', 'image', f'image_{image_index}.webp'), 'rb') as file:
            data = file.read()

        self.data = data.hex()

        thread.start()

        with UART(log_filename='Server1') as com:
            result = com.pull_data(1, 1)

        with open(os.path.join('assets', 'image', f'image_{image_index}.output.webp'), 'wb') as file:
            file.write(bytes.fromhex(result))

        self.assertEqual(result, self.data)


    def _test__pull__client (self):
        time.sleep(0.5)

        with UART() as com:
            com.push_data(self.data, 1, 1)


    def test__push_timeout__exception (self):
        """ To do.
        """
        with UART(log_filename='Client3') as com:
            self.assertRaises(UART.TimeoutException, com.push_data, 'Hey!', 1, 20)


    def test__pull_timeout__exception (self):
        """ To do.
        """
        with UART(log_filename='Server3') as com:
            self.assertRaises(UART.TimeoutException, com.pull_data, 1, 20)


if __name__ == '__main__':
    unittest.main()
