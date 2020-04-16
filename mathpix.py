
'''
@#!/usr/bin/env: Python3.7.6
@# -*- encoding: utf-8-*-
@Description: 
@Author: Allen
@Date: 2020-04-12 16:12:26
@LastEditTime: 2020-04-12 16:14:49
@LastEditors: Allen
'''
#!/usr/bin/env python3

import os
import base64
import requests
import json

#
# Common module for calling Mathpix OCR service from Python.
#
# N.B.: Set your credentials in environment variables APP_ID and APP_KEY,
# either once via setenv or on the command line as in
# APP_ID=my-id APP_KEY=my-key python3 simple.py
#

env = os.environ

app_id='xiaopanlyu_outlook_com_bbe977'
app_key='2b6992473e5844c35283'
group_id='xiaopanlyu_outlook_com_bbe977'

default_headers = {
    'app_id': env.get('APP_ID', 'trial'),
    'app_key': env.get('APP_KEY', '34f1a4cea0eaca8540c95908b4dc84ab'),
    'Content-type': 'application/json'
}

service = 'https://api.mathpix.com/v3/latex'


#
# Return the base64 encoding of an image with the given filename.
#
def image_uri(filename):
    image_data = open(filename, "rb").read()
    return "data:image/jpg;base64," + base64.b64encode(image_data).decode()


#
# Call the Mathpix service with the given arguments, headers, and timeout.
#
def latex(args, headers=default_headers, timeout=30):
    r = requests.post(service,
                      data=json.dumps(args),
                      headers=headers,
                      timeout=timeout)
    return json.loads(r.text)