import sys
import os
import unittest

sys.path.append(os.path.join('src'))
from lib.header import Header, Request, Response, Data, Success, Timeout, Error


class TestHeader (unittest.TestCase):
    def test_Request_encode (self):
        """Tests if Request header targeting 0xAA with 0xBB length can be encoded properly.
        """
        header = Request(target=0xAA, length=0xBB)
        
        self.assertEqual(header.encode(), b'\x01\x00\x00\xBB\x01\xAA\x00\x00\x00\x00')


    def test_Request_decode (self):
        """Tests if Request header targeting 0xAA with 0xBB length can be decoded properly.
        """
        header = Header.decode(b'\x01\x00\x00\xBB\x01\xAA\x00\x00\x00\x00')
        
        self.assertEqual(header.type_byte, 0x01, msg="Incorrect type byte!")
        self.assertEqual(header.length, 0xBB, msg="Incorrect length byte!")
        self.assertEqual(header.index, 0x01, msg="Incorrect index byte!")
        self.assertEqual(header.target, 0xAA, msg="Incorrect target byte!")


    def test_Response_encode (self):
        """Tests if Response header can be encoded properly.
        """
        header = Response()
        
        self.assertEqual(header.encode(), b'\x02\x00\x00\x01\x01\x00\x00\x00\x00\x00')


    def test_Response_decode (self):
        """Tests if Response header can be decoded properly.
        """
        header = Header.decode(b'\x02\x00\x00\x01\x01\x00\x00\x00\x00\x00')
        
        self.assertEqual(header.type_byte, 0x02, msg="Incorrect type byte!")
        self.assertEqual(header.length, 0x01, msg="Incorrect length byte!")
        self.assertEqual(header.index, 0x01, msg="Incorrect index byte!")


    def test_Data_encode (self):
        """Tests if Data header 0xAA of 0xBB for a payload sized 0xCC can be encoded properly.
        """
        header = Data(length=0xAA, index=0xBB, size=0xCC)
        
        self.assertEqual(header.encode(), b'\x03\x00\x00\xAA\xBB\xCC\x00\x00\x00\x00')


    def test_Data_decode (self):
        """Tests if Data header 0xAA of 0xBB for a payload sized 0xCC can be decoded properly.
        """
        header = Header.decode(b'\x03\x00\x00\xBB\xAA\xCC\x00\x00\x00\x00')
        
        self.assertEqual(header.type_byte, 0x03, msg="Incorrect type byte!")
        self.assertEqual(header.length, 0xBB, msg="Incorrect length byte!")
        self.assertEqual(header.index, 0xAA, msg="Incorrect index byte!")
        self.assertEqual(header.size, 0xCC, msg="Incorrect index byte!")


    def test_Success_encode (self):
        """Tests if Success header for package 0xAA can be encoded properly.
        """
        header = Success(package_id=0xAA)
        
        self.assertEqual(header.encode(), b'\x04\x00\x00\x01\x01\x00\x00\xAA\x00\x00')


    def test_Success_decode (self):
        """Tests if Success header for package 0xAA can be decoded properly.
        """
        header = Header.decode(b'\x04\x00\x00\x01\x01\x00\x00\xAA\x00\x00')
        
        self.assertEqual(header.type_byte, 0x04, msg="Incorrect type byte!")
        self.assertEqual(header.length, 0x01, msg="Incorrect length byte!")
        self.assertEqual(header.index, 0x01, msg="Incorrect index byte!")
        self.assertEqual(header.package_id, 0xAA, msg="Incorrect package ID byte!")


    def test_Timeout_encode (self):
        """Tests if Timeout header can be encoded properly.
        """
        header = Timeout()
        
        self.assertEqual(header.encode(), b'\x05\x00\x00\x01\x01\x00\x00\x00\x00\x00')


    def test_Timeout_decode (self):
        """Tests if Timeout header can be decoded properly.
        """
        header = Header.decode(b'\x05\x00\x00\x01\x01\x00\x00\x00\x00\x00')
        
        self.assertEqual(header.type_byte, 0x05, msg="Incorrect type byte!")
        self.assertEqual(header.length, 0x01, msg="Incorrect length byte!")
        self.assertEqual(header.index, 0x01, msg="Incorrect index byte!")


    def test_Error_encode (self):
        """Tests if Error header for package 0xAA can be encoded properly.
        """
        header = Error(package_id=0xAA)
        
        self.assertEqual(header.encode(), b'\x06\x00\x00\x01\x01\x00\xAA\x00\x00\x00')


    def test_Error_decode (self):
        """Tests if Error header for package 0xAA can be decoded properly.
        """
        header = Header.decode(b'\x06\x00\x00\x01\x01\x00\xAA\x00\x00\x00')
        
        self.assertEqual(header.type_byte, 0x06, msg="Incorrect type byte!")
        self.assertEqual(header.length, 0x01, msg="Incorrect length byte!")
        self.assertEqual(header.index, 0x01, msg="Incorrect index byte!")
        self.assertEqual(header.package_id, 0xAA, msg="Incorrect package ID byte!")


    def test_untyped_decode (self):
        """Tests if untyped (unregistered type byte) header can be decoded properly into an error header.
        """
        header = Header.decode(b'\xAA\x00\x00\x01\x01\x00\x00\x00\x00\x00')
        
        self.assertEqual(header.type_byte, Error.type_byte, msg="Incorrect type byte!")
        self.assertEqual(header.length, 0x01, msg="Incorrect length byte!")
        self.assertEqual(header.index, 0x01, msg="Incorrect index byte!")
        self.assertEqual(header.package_id, 0x00, msg="Incorrect package ID byte!")


if __name__ == '__main__':
    unittest.main()
