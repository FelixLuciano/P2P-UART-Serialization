import sys
import os
import unittest

sys.path.append(os.path.join('src'))
from lib.package import *


class Test__Request_package (unittest.TestCase):
    def test__encode (self):
        """Tests if Request package targeting 0xAA with 0xBB length can be encoded properly.
        """
        package = Request_package(0x1A, 0x2B)
        
        self.assertEqual(package.encode(), b'\x01\x00\x00\x2B\x01\x1A\x00\x00\x00\x00\xAA\xBB\xCC\xDD')


    def test__ExcededSizeLimit_exception (self):
        """ To do.
        """
        self.assertRaises(Package.ExcededSizeLimitException, Request_package, 0x100, 0x100)


class Test__Response_package (unittest.TestCase):
    def test__encode (self):
        """Tests if Response package can be encoded properly.
        """
        package = Response_package()
        
        self.assertEqual(package.encode(), b'\x02\x00\x00\x01\x01\x00\x00\x00\x00\x00\xAA\xBB\xCC\xDD')


class Test__Data_package (unittest.TestCase):
    def test__encode (self):
        """Tests if Data package 0xAA of 0xBB with some data can be encoded properly.
        """
        package = Data_package(0x1A, 0x2B, b'\x01\x23\x45\x67\x89\xAB\xCD\xEF')
        
        self.assertEqual(package.encode(), b'\x03\x00\x00\x1A\x2B\x08\x00\x00\x00\x00\x01\x23\x45\x67\x89\xAB\xCD\xEF\xAA\xBB\xCC\xDD')


    def test__ExcededSizeLimit_exception (self):
        """ To do.
        """
        self.assertRaises(Package.ExcededSizeLimitException, Data_package, 0xFF, 0xFF, 'c'*(Data_package.MAX_PAYLOAD_SIZE + 1))


class Test__Success_package (unittest.TestCase):
    def test__encode (self):
        """Tests if Success package for package 0xAA can be encoded properly.
        """
        package = Success_package(0x1A)
        
        self.assertEqual(package.encode(), b'\x04\x00\x00\x01\x01\x00\x00\x1A\x00\x00\xAA\xBB\xCC\xDD')


    def test__ExcededSizeLimit_exception (self):
        """ To do.
        """
        self.assertRaises(Package.ExcededSizeLimitException, Success_package, 0x100)


class Test__Timeout_package (unittest.TestCase):
    def test__encode (self):
        """Tests if Timeout package can be encoded properly.
        """
        package = Timeout_package()
        
        self.assertEqual(package.encode(), b'\x05\x00\x00\x01\x01\x00\x00\x00\x00\x00\xAA\xBB\xCC\xDD')


class Test__Error_package (unittest.TestCase):
    def test__encode (self):
        """Tests if Error package for package 0xAA can be encoded properly.
        """
        package = Error_package(0x1A)
        
        self.assertEqual(package.encode(), b'\x06\x00\x00\x01\x01\x00\x1A\x00\x00\x00\xAA\xBB\xCC\xDD')


    def test__ExcededSizeLimit_exception (self):
        """ To do.
        """
        self.assertRaises(Package.ExcededSizeLimitException, Error_package, 0x100)


if __name__ == '__main__':
    unittest.main()
