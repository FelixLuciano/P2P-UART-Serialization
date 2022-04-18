import sys
import os
import unittest
from threading import Thread

sys.path.append(os.path.join('src'))
from UART import UART


class Test__UART (unittest.TestCase):
    def test__push (self):
        """ To do.
        """
        thread = Thread(target=self._test__push__server)
        data = {
            'foo': 'bar',
            'value': 123,
            'items': ['abc', 123, False],
            'test': True
        }

        thread.start()

        with UART() as com:
            com.push_data(data, 1, 10)

        self.assertEqual(self.result['foo'], 'bar')
        self.assertEqual(self.result['value'], 123)
        self.assertEqual(len(self.result['items']), 3)
        self.assertTrue(self.result['test'])


    def _test__push__server (self):
        with UART() as com:
            self.result = com.pull_data(1, 10)


if __name__ == '__main__':
    unittest.main()
