

import time
import socket
import ssl
import sys
import http.client
import json
import base64
from urllib.parse import urlencode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

# global variables with static information about nExt API
SERVICE = 'NEXTAPI'
URL = 'api.test.nordnet.se'
API_VERSION = '2'
PUBLIC_KEY_FILENAME = r"""C:\Users\Phili\source\repos\System\System\Nordnet\NEXTAPI_TEST_public.pem"""

class MyPub:
    def __init__(self, host, port, ses_key):
        self.host = host
        self.port = port
        self.key = ses_key
    def connect(self):
        # Establish connection to public feed
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.port == 443:
            self.ssl_socket = ssl.wrap_socket(self.s)
            
        self.ssl_socket.connect((self.host, self.port))
       
        # Login to public feed with our session_key from NNAPI response
        cmd = {'cmd': 'login', 'args': {
            'session_key': self.key, 'service': 'NEXTAPI'}}
        
        self.send_cmd_to_socket(cmd)
        

    def send_cmd_to_socket(self, cmd):
        self.ssl_socket.send(bytes(json.dumps(cmd) + '\n', 'utf-8'))
        print("<< Sending cmd to feed: " + str(cmd)) 

    def subscribe(self, market, instrument):  
        cmd = {'cmd': 'subscribe', 'args': {'t': 'price', 'm': market, 'i': str(instrument)}}
        self.send_cmd_to_socket(cmd)
    def response(self):
        # Consume message (price data or heartbeat) from public feed
        time.sleep(0.01)
        output = self.ssl_socket.recv(1024).decode("utf-8")
        j = json.loads(output)
        return j
    def close(self):
        del self.ssl_socket
        self.s.close()



