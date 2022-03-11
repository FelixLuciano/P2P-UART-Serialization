import sys
import os
import unittest

sys.path.append(os.path.join('src'))

from lib.package import Package


class TestPackage (unittest.TestCase):
    def test_encode (self):
        """Tests if Package can encode 'Hello World!' properly.
        """
        package = Package('Hello World!', 'response')
        result = package.encode()
        expected = [b'\xb7\x01\x00\x01\x0c\x00\x00\x00\x00\x00Hello World!\xdbf\x99\xdb']
        
        self.assertEqual(result, expected, msg="Hello World!")

    def test_decode (self):
        """Tests if Package can decode a package properly.
        """
        package = [b'\xb7\x01\x00\x01\x0c\x00\x00\x00\x00\x00Hello World!\xdbf\x99\xdb']
        result = b''.join(map(Package.decode, package))
        expected = b'Hello World!'
        
        self.assertEqual(result, expected, msg="Hello World!")


if __name__ == '__main__':
    unittest.main()
