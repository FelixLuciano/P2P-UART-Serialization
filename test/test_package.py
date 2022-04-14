import sys
import os
import unittest

sys.path.append(os.path.join('src'))
from lib.package import Package, Request, Response, Data, Success, Timeout, Error


class TestPackage (unittest.TestCase):
    def test_Request_encode (self):
        """Tests if Request package targeting 0xAA with 0xBB length can be encoded properly.
        """
        package = Request(target=0xAA, length=0xBB)
        
        self.assertEqual(package.encode(), b'\x01\x00\x00\xBB\x01\xAA\x00\x00\x00\x00\xAA\xBB\xCC\xDD')


    def test_Response_encode (self):
        """Tests if Response package can be encoded properly.
        """
        package = Response()
        
        self.assertEqual(package.encode(), b'\x02\x00\x00\x01\x01\x00\x00\x00\x00\x00\xAA\xBB\xCC\xDD')


    def test_Data_encode (self):
        """Tests if Data package 0xAA of 0xBB with some data can be encoded properly.
        """
        package = Data(length=0xAA, index=0xBB, data=b'\x01\x23\x45\x67\x89\xAB\xCD\xEF')
        
        self.assertEqual(package.encode(), b'\x03\x00\x00\xAA\xBB\x08\x00\x00\x00\x00\x01\x23\x45\x67\x89\xAB\xCD\xEF\xAA\xBB\xCC\xDD')


    def test_Success_encode (self):
        """Tests if Success package for package 0xAA can be encoded properly.
        """
        package = Success(package_id=0xAA)
        
        self.assertEqual(package.encode(), b'\x04\x00\x00\x01\x01\x00\x00\xAA\x00\x00\xAA\xBB\xCC\xDD')


    def test_Timeout_encode (self):
        """Tests if Timeout package can be encoded properly.
        """
        package = Timeout()
        
        self.assertEqual(package.encode(), b'\x05\x00\x00\x01\x01\x00\x00\x00\x00\x00\xAA\xBB\xCC\xDD')


    def test_Error_encode (self):
        """Tests if Error package for package 0xAA can be encoded properly.
        """
        package = Error(package_id=0xAA)
        
        self.assertEqual(package.encode(), b'\x06\x00\x00\x01\x01\x00\xAA\x00\x00\x00\xAA\xBB\xCC\xDD')


if __name__ == '__main__':
    unittest.main()
