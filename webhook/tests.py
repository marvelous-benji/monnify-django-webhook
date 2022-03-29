import os

from django.test import TestCase, Client
from  django.urls import reverse

# Create your tests here.


class EnvironmentTest(TestCase):

    def test_that_monnify_secret_is_set(self):
        '''
        Tests to see that your monnify secret key is set
        '''

        self.assertIsNot(os.getenv("MONNIFY_SECRET_KEY",None), None)


    def test_that_monnify_ip_is_set(self):
        '''
        Tests to see that monnify ip address is set
        '''
        
        self.assertIsNot(os.getenv("MONNIFY_IP",None), None)



class ViewsTest(TestCase):

    def test_function_based_views(self):
        client = Client()
        url = reverse('process-webhook')