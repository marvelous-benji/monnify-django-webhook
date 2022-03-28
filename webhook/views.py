
import os
import hmac

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

import hashlib


your_secret_key = os.environ["MONNIFY_SECRET"] # Your Monnify Secret key
monnify_ip = os.environ["MONNIFY_IP"] # Monnify IP address which is: 35.242.133.146



def verify_hash(payload_in_bytes, monnify_hash):
    '''
    Recieves the monnify payload in bytes and perform a SHA-512 hash
    with your secret key which is also encoded in byte.
    uses hmac.compare_digest rather than "=" sign as the former helps
    to prevent timing attacks.
    '''
    secret_key_bytes = your_secret_key.encode('utf-8') # encodes your secret key as byte
    your_hash_in_bytes = hmac.new(secret_key_bytes, msg=payload_in_bytes, digestmod=hashlib.sha512)
    your_hash_in_hex = your_hash_in_bytes.hexdigest() # Hexlify generated hash
    return hmac.compare_digest(your_hash_in_hex,monnify_hash)


def get_sender_ip(headers):
    '''
    Get senders' IP address, by first checking if your API server
    is behind a proxy by checking for HTTP_X_FORWARDED_FOR
    if not gets sender actual IP address using REMOTE_ADDR
    '''

    x_forwarded_for = headers.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # in some cases this might be in the second index ie [1]
        # depending on your hosting environment
        return x_forwarded_for.split(',')[0]
    else:
        return headers.get("REMOTE_ADDR")


def verify_monnify_webhook(payload_in_bytes, monnify_hash, headers):
    '''
    The interface that does the verification by calling necessary functions.
    Though everything has been tested to work well, but if you have issues
    with this function returning False, you can remove the get_sender_ip
    function to be sure that the verify_hash is working, then you can check
    what header contains the IP address.
    '''

    return  get_sender_ip(headers) == monnify_ip and verify_hash(payload_in_bytes, monnify_hash)




@api_view(['POST'])
def process_webhook(request):
    '''
    A function based view implementing the receipt of the webhook payload.
    The webhook payload should be received as bytes rather than json
    that would be converted to bytes.This is most likely one of the
    cause for failed webhook verification. 
    After the webhook verification, you can get a json format of the byte
    object by simply calling json.loads(payload_in_bytes)
    '''

    payload_in_bytes = request.body
    monnify_hash = request.META['HTTP_MONNIFY_SIGNATURE']
    confirmation = verify_monnify_webhook(payload_in_bytes, monnify_hash, request.META)
    if confirmation is False:
        return Response({'status':'failed','msg':'Webhook does not appear to come from Monnify'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        '''
        if payload verification is successful, you can perform your necessary task,
        but if your planned processing would take time, you should first return a 200 response
        and process your stuff in background.
        '''
        return Response(
                {"status": "success", "msg": 'Webhook received successfully'}, status=status.HTTP_200_OK
            )


class WebhookView(APIView):

    def post(self,request):
        '''
        A class based view implementing the receipt of the webhook payload.
        The webhook payload should be received as bytes rather than json
        that would be converted to bytes.This is most likely one of the
        cause for failed webhook verification. 
        After the webhook verification, you can get a json format of the byte
        object by simply calling json.loads(payload_in_bytes)
        '''

        payload_in_bytes = request.body
        monnify_hash = request.META['HTTP_MONNIFY_SIGNATURE']
        confirmation = verify_monnify_webhook(payload_in_bytes, monnify_hash, request.META)
        if confirmation is False:
            return Response({'status':'failed','msg':'Webhook does not appear to come from Monnify'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            '''
            if payload verification is successful, you can perform your necessary task,
            but if your planned processing would take time, you should first return a 200 response
            and process your stuff in background.
            '''
            return Response(
                    {"status": "success", "msg": 'Webhook received successfully'}, status=status.HTTP_200_OK
                )






