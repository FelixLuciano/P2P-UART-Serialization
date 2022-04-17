import sys
import os
import unittest

sys.path.append(os.path.join('src'))
from lib.header import *


class TestHeader (unittest.TestCase):
    def test_UnregisteredType_exception (self):
        """ To do.
        """
        try:
            Header.decode(b'\xFF\x00\x00\x01\x01\x00\x00\x00\x00\x00')
        except Header.UnregisteredTypeException as error:
            self.assertEqual(error.type, 0xFF)


class TestRequestHeader (unittest.TestCase):
    def test_encode (self):
        """Tests if Request header targeting 0xAA with 0xBB length can be encoded properly.
        """
        header = Request_header(0x1A, 0x2B)
        
        self.assertEqual(header.encode(), b'\x01\x00\x00\x2B\x01\x1A\x00\x00\x00\x00')


    def test_ExcededSizeLimit_exception (self):
        """ To do.
        """
        self.assertRaises(Header.ExcededSizeLimitException, Request_header, 0x100, 0x100)


    def test_decode (self):
        """Tests if Request header targeting 0xAA with 0xBB length can be decoded properly.
        """
        header = Header.decode(b'\x01\x00\x00\x1A\x01\x2B\x00\x00\x00\x00')
        
        self.assertIsInstance(header, Request_header, msg="Incorrect class!")
        self.assertEqual(header.type, 0x01, msg="Incorrect type byte!")
        self.assertEqual(header.length, 0x1A, msg="Incorrect length byte!")
        self.assertEqual(header.index, 0x01, msg="Incorrect index byte!")
        self.assertEqual(header.target, 0x2B, msg="Incorrect target byte!")


    def test_unexpected_exception (self):
        """ To do.
        """
        try:
            Request_header.decode(b'\x01\x00\x00\x1A\x01\x2B\x00\x00\x00\x00', target=0x3C)
        except Request_header.UnexpectedRequestException as error:
            self.assertIsInstance(error.header, Request_header, msg="Incorrect class!")
            self.assertEqual(error.header.type, 0x01, msg="Incorrect type byte!")
            self.assertEqual(error.header.length, 0x1A, msg="Incorrect length byte!")
            self.assertEqual(error.header.index, 0x01, msg="Incorrect index byte!")
            self.assertEqual(error.header.target, 0x2B, msg="Incorrect target byte!")


class TestResponseHeader (unittest.TestCase):
    def test_encode (self):
        """Tests if Response header can be encoded properly.
        """
        header = Response_header()
        
        self.assertEqual(header.encode(), b'\x02\x00\x00\x01\x01\x00\x00\x00\x00\x00')


    def test_decode (self):
        """Tests if Response header can be decoded properly.
        """
        header = Header.decode(b'\x02\x00\x00\x01\x01\x00\x00\x00\x00\x00')
        
        self.assertIsInstance(header, Response_header, msg="Incorrect class!")
        self.assertEqual(header.type, 0x02, msg="Incorrect type byte!")
        self.assertEqual(header.length, 0x01, msg="Incorrect length byte!")
        self.assertEqual(header.index, 0x01, msg="Incorrect index byte!")


class TestDataHeader (unittest.TestCase):
    def test_encode (self):
        """Tests if Data header 0xAA of 0xBB for a payload sized 0xCC can be encoded properly.
        """
        header = Data_header(0x1A, 0x2B, 0x3C)
        
        self.assertEqual(header.encode(), b'\x03\x00\x00\x1A\x2B\x3C\x00\x00\x00\x00')


    def test_ExcededSizeLimit_exception (self):
        """ To do.
        """
        self.assertRaises(Header.ExcededSizeLimitException, Data_header, 0xFF, 0xFF, 115)


    def test_decode (self):
        """Tests if Data header 0xAA of 0xBB for a payload sized 0xCC can be decoded properly.
        """
        header = Header.decode(b'\x03\x00\x00\x1A\x2B\x3C\x00\x00\x00\x00')
        
        self.assertIsInstance(header, Data_header, msg="Incorrect class!")
        self.assertEqual(header.type, 0x03, msg="Incorrect type byte!")
        self.assertEqual(header.length, 0x1A, msg="Incorrect length byte!")
        self.assertEqual(header.index, 0x2B, msg="Incorrect index byte!")
        self.assertEqual(header.size, 0x3C, msg="Incorrect index byte!")


    def test_unexpected_exception (self):
        """ To do.
        """
        try:
            Data_header.decode(b'\x03\x00\x00\x1A\x2B\x3C\x00\x00\x00\x00', length=0x4D, index=0x5E, size=0x6F)
        except Data_header.UnexpectedDataException as error:
            self.assertIsInstance(error.header, Data_header, msg="Incorrect class!")
            self.assertEqual(error.header.type, 0x03, msg="Incorrect type byte!")
            self.assertEqual(error.header.length, 0x1A, msg="Incorrect length byte!")
            self.assertEqual(error.header.index, 0x2B, msg="Incorrect index byte!")
            self.assertEqual(error.header.size, 0x3C, msg="Incorrect index byte!")


class TestSuccessHeader (unittest.TestCase):
    def test_encode (self):
        """Tests if Success header for package 0xAA can be encoded properly.
        """
        header = Success_header(0x1A)
        
        self.assertEqual(header.encode(), b'\x04\x00\x00\x01\x01\x00\x00\x1A\x00\x00')


    def test_ExcededSizeLimit_exception (self):
        """ To do.
        """
        self.assertRaises(Header.ExcededSizeLimitException, Success_header, 0x100)


    def test_decode (self):
        """Tests if Success header for package 0xAA can be decoded properly.
        """
        header = Header.decode(b'\x04\x00\x00\x01\x01\x00\x00\x1A\x00\x00')
        
        self.assertIsInstance(header, Success_header, msg="Incorrect class!")
        self.assertEqual(header.type, 0x04, msg="Incorrect type byte!")
        self.assertEqual(header.length, 0x01, msg="Incorrect length byte!")
        self.assertEqual(header.index, 0x01, msg="Incorrect index byte!")
        self.assertEqual(header.package_index, 0x1A, msg="Incorrect package ID byte!")


    def test_unexpected_exception (self):
        """ To do.
        """
        try:
            Success_header.decode(b'\x04\x00\x00\x01\x01\x00\x00\x1A\x00\x00', package_index=0x2B)
        except Success_header.UnexpectedSuccessException as error:
            self.assertIsInstance(error.header, Success_header, msg="Incorrect class!")
            self.assertEqual(error.header.type, 0x04, msg="Incorrect type byte!")
            self.assertEqual(error.header.length, 0x01, msg="Incorrect length byte!")
            self.assertEqual(error.header.index, 0x01, msg="Incorrect index byte!")
            self.assertEqual(error.header.package_index, 0x1A, msg="Incorrect package ID byte!")


class TestTimeoutHeader (unittest.TestCase):
    def test_encode (self):
        """Tests if Timeout header can be encoded properly.
        """
        header = Timeout_header()
        
        self.assertEqual(header.encode(), b'\x05\x00\x00\x01\x01\x00\x00\x00\x00\x00')


    def test_decode (self):
        """Tests if Timeout header can be decoded properly.
        """
        header = Header.decode(b'\x05\x00\x00\x01\x01\x00\x00\x00\x00\x00')
        
        self.assertIsInstance(header, Timeout_header, msg="Incorrect class!")
        self.assertEqual(header.type, 0x05, msg="Incorrect type byte!")
        self.assertEqual(header.length, 0x01, msg="Incorrect length byte!")
        self.assertEqual(header.index, 0x01, msg="Incorrect index byte!")


class TestErrorHeader (unittest.TestCase):
    def test_encode (self):
        """Tests if Error header for package 0xAA can be encoded properly.
        """
        header = Error_header(0x1A)
        
        self.assertEqual(header.encode(), b'\x06\x00\x00\x01\x01\x00\x1A\x00\x00\x00')


    def test_ExcededSizeLimit_exception (self):
        """ To do.
        """
        self.assertRaises(Header.ExcededSizeLimitException, Error_header, 0x100)


    def test_decode (self):
        """Tests if Error header for package 0xAA can be decoded properly.
        """
        header = Header.decode(b'\x06\x00\x00\x01\x01\x00\x1A\x00\x00\x00')
        
        self.assertIsInstance(header, Error_header, msg="Incorrect class!")
        self.assertEqual(header.type, 0x06, msg="Incorrect type byte!")
        self.assertEqual(header.length, 0x01, msg="Incorrect length byte!")
        self.assertEqual(header.index, 0x01, msg="Incorrect index byte!")
        self.assertEqual(header.package_index, 0x1A, msg="Incorrect package ID byte!")


    def test_unexpected_exception (self):
        """ To do.
        """
        try:
            Error_header.decode(b'\x06\x00\x00\x01\x01\x00\x1A\x00\x00\x00', package_index=0x2B)
        except Error_header.UnexpectedErrorException as error:
            self.assertIsInstance(error.header, Error_header, msg="Incorrect class!")
            self.assertEqual(error.header.type, 0x06, msg="Incorrect type byte!")
            self.assertEqual(error.header.length, 0x01, msg="Incorrect length byte!")
            self.assertEqual(error.header.index, 0x01, msg="Incorrect index byte!")
            self.assertEqual(error.header.package_index, 0x1A, msg="Incorrect package ID byte!")


if __name__ == '__main__':
    unittest.main()
