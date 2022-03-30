import os
import hmac
import hashlib
import json

from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse

from .views import verify_hash

# Create your tests here.


class EnvironmentTest(TestCase):
    def test_that_monnify_secret_is_set(self):
        """
        Tests to see that your monnify secret key is set
        """

        self.assertIsNot(os.getenv("MONNIFY_SECRET", None), None)

    def test_that_monnify_ip_is_set(self):
        """
        Tests to see that monnify ip address is set
        """

        self.assertIsNot(os.getenv("MONNIFY_IP", None), None)


def hasher(payload_in_bytes, secret_key_bytes):
    your_hash_in_bytes = hmac.new(
        secret_key_bytes, msg=payload_in_bytes, digestmod=hashlib.sha512
    )
    your_hash_in_hex = your_hash_in_bytes.hexdigest()
    return your_hash_in_hex


class UtilsTest(TestCase):
    def test_hashing_function(self):
        payload_in_bytes = b"Monnify is cool"
        secret_key_bytes = os.environ["MONNIFY_SECRET"].encode(
            "utf-8"
        )  # encodes your secret key as byte
        your_hash_in_bytes = hmac.new(
            secret_key_bytes, msg=payload_in_bytes, digestmod=hashlib.sha512
        )
        your_hash_in_hex = your_hash_in_bytes.hexdigest()
        self.assertIs(
            verify_hash(
                payload_in_bytes,
                "59fec58247858a50bed5d21dfd8831c656525a02d61cbd4eb2820402c4257e8ee7b4ffda6d583c55a385ffe3413ed0d9ca2dcc207e8387dd2f04a921b06c8465",
            ),
            True,
        )

    def test_ip_checker(self):
        os.environ["MONNIFY_IP"] = "127.0.0.1"
        self.assertEqual(os.getenv("MONNIFY_IP"), "127.0.0.1")


class ViewTest(TestCase):

    client = APIClient()
    os.environ["MONNIFY_SECRET"] = "Monnify"
    os.environ["MONNIFY_IP"] = "127.0.0.1"

    def test_func_based_view(self):
        url = reverse("process_webhook")
        hash = hasher(b'{"status": true}', b"Monnify")
        headers = {"HTTP_MONNIFY_SIGNATURE": hash}
        resp = self.client.post(
            url,
            data=json.dumps({"status": True}),
            content_type="application/json",
            **headers
        )
        self.assertEqual(resp.status_code, 200)

    def test_class_based_view(self):
        url = reverse("webhook_processor")
        hash = hasher(b'{"status": true}', b"Monnify")
        headers = {"HTTP_MONNIFY_SIGNATURE": hash}
        resp = self.client.post(
            url,
            data=json.dumps({"status": True}),
            content_type="application/json",
            **headers
        )
        self.assertEqual(resp.status_code, 200)
