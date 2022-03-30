import os
import hmac
import hashlib

from django.test import TestCase, Client
from  django.urls import reverse

from .views import verify_hash

# Create your tests here.


class EnvironmentTest(TestCase):

    def test_that_monnify_secret_is_set(self):
        '''
        Tests to see that your monnify secret key is set
        '''

        self.assertIsNot(os.getenv("MONNIFY_SECRET",None), None)


    def test_that_monnify_ip_is_set(self):
        '''
        Tests to see that monnify ip address is set
        '''
        
        self.assertIsNot(os.getenv("MONNIFY_IP",None), None)



class HashTest(TestCase):

    def test_hashing_function(self):
        payload_in_bytes = b"Monnify is cool"
        secret_key_bytes = os.environ["MONNIFY_SECRET"].encode(
            "utf-8"
        )  # encodes your secret key as byte
        your_hash_in_bytes = hmac.new(
            secret_key_bytes, msg=payload_in_bytes, digestmod=hashlib.sha512
        )
        your_hash_in_hex = your_hash_in_bytes.hexdigest()
        self.assertIs(verify_hash(payload_in_bytes,"59fec58247858a50bed5d21dfd8831c656525a02d61cbd4eb2820402c4257e8ee7b4ffda6d583c55a385ffe3413ed0d9ca2dcc207e8387dd2f04a921b06c8465"), True)
