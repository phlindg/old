


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
import requests

# global variables with static information about nExt API
SERVICE = 'NEXTAPI'
URL = 'api.test.nordnet.se'
FULL_URL = "http://api.test.nordnet.se/next/2"
API_VERSION = '2'
PUBLIC_KEY_FILENAME = r"""C:\Users\Phili\source\repos\System\System\Nordnet\NEXTAPI_TEST_public.pem"""




def get_hash(username, password):
    timestamp = int(round(time.time() * 1000))
    timestamp = str(timestamp).encode('ascii')

    username_b64 = base64.b64encode(username.encode('ascii'))
    password_b64 = base64.b64encode(password.encode('ascii'))
    timestamp_b64 = base64.b64encode(timestamp)

    auth_val = username_b64 + b':' + password_b64 + b':' + timestamp_b64
    # Need local copy of public key for NNAPI in PEM format

    try:
        public_key_file_handler = open(PUBLIC_KEY_FILENAME).read()
    except IOError:
        print("Could not find the following file: ",
              "\"", PUBLIC_KEY_FILENAME, "\"", sep="")
        sys.exit()
    rsa_key = RSA.importKey(public_key_file_handler)
    cipher_rsa = PKCS1_v1_5.new(rsa_key)
    encrypted_hash = cipher_rsa.encrypt(auth_val)
    encoded_hash = base64.b64encode(encrypted_hash)

    return encoded_hash

class MyPriv:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    def login(self):
        USERNAME = self.username
        PASSWORD = self.password
        auth_hash = get_hash(USERNAME, PASSWORD)
       
        headers = {"Accept": "application/json"}
        self.conn = http.client.HTTPSConnection(URL)

        # Check NNAPI status
        j = self.send_http_request('GET', '/next/' + API_VERSION + '/', '', headers)


        # POST login to NNAPI
        params = urlencode({'service': 'NEXTAPI', 'auth': auth_hash})
        j = self.send_http_request('POST', '/next/' + API_VERSION + '/login', params, headers)
        self.j = j

        
    def login_response(self):
        # Store NNAPI login response data
        public_hostname = self.j["public_feed"]["hostname"]
        public_port = self.j["public_feed"]["port"]
        our_session_key = self.j["session_key"]
        self.ses_key = our_session_key
        return public_hostname, public_port, our_session_key
    def acc(self):
        headers = {"Accept": "application/json",'Accept-Language':'sv'}
        headers['Authorization'] = 'Basic ' + self.ses_hash()
        j = self.send_http_request("GET", "/next/" + API_VERSION + "/accounts","", headers)
        
        self.accno = j[0]["accno"]
    def ses_hash(self):
        b64_auth = base64.b64encode(bytes(self.ses_key + ":" + self.ses_key, encoding='utf-8')).decode("utf-8")
        return b64_auth

    def send_http_request(self, method, uri, params, headers):
        self.conn.request(method, uri, params, headers)
        r = self.conn.getresponse()
        #print("<< HTTP Request "+method+ " " + uri)
        response = r.read().decode("utf-8")
        j = json.loads(response)
        #print(json.dumps(j, indent=4, sort_keys=True))
        return j
    def send_get(self,ext, params, headers):
        r = requests.get(FULL_URL + ext, params = params, headers = headers)
        print(r)
        r = r.json()
        return r
    def close_socket():
        pass

    def order(self,market, instrument,price, currency, volume, side, order_type):
        headers = {"Accept": "application/json"}
        headers['Authorization'] = 'Basic ' + self.ses_hash()
        r = requests.post("https://"+URL +"/next/"+API_VERSION+ "/accounts/" + str(self.accno) + "/orders",
                          data = {"identifier":instrument,
                              "market_id":market,
                              "price":price,
                              "currency":currency,
                              "volume": volume,
                              "side":side,
                              "order_type":order_type,
                              "Accept-Language": "sv",
                              "auth":{self.ses_key}}, headers = headers).text
        print(r)
        print(json.loads(r))

    def get_positions(self):
        headers = {"Accept": "application/json"}
        headers['Authorization'] = 'Basic ' + self.ses_hash()
        j = self.send_get("/accounts/" + str(self.accno) + "/positions","", headers)
        return j
    def get_account(self):
        headers = {"Accept": "application/json"}
        headers['Authorization'] = 'Basic ' + self.ses_hash()
        j = self.send_get("/accounts/"+str(self.accno), "", headers)
        return j
    def get_list(self, list_id):
        headers = {"Accept": "application/json"}
        headers['Authorization'] = 'Basic ' + self.ses_hash()
        j = self.send_get("/lists/"+list_id,"", headers)
        return j



