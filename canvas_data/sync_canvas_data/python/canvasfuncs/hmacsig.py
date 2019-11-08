#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import hashlib
import hmac
from datetime import datetime, timezone
from urllib import parse

def HMACopts(call_url, method, params, cdata_secret):

  ###############################################################################
  ###################### HMAC Signature Building Section ########################
  ###############################################################################

  # generate UTC timestamp for HMAC-256 signature
  dt_now = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')

  # break the call into components to build HMAC-256 signature
  call_info = list(parse.urlparse(call_url))

  # set components for HMAC-256 signature
  reqOpts = {
    'method' : method.upper(),
    'host' : call_info[1],
    # intentionally blank
    'content_type' : '',
    # intentionally blank
    'content_md5' : '',
    'path' : call_info[2],
    'parameters' : params,
    'req_timestamp' : dt_now,
    'api_secret' : cdata_secret
    }
  return reqOpts

def HMACsig(reqOpts, api_key):

  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
  ############### DO NOT CHANGE ANYTHING IN THIS SUBSECTION #####################
  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#

  # build a bytes message by joining the signature components
  message = bytes('\n'.join(str(x) for x in reqOpts.values()), 'utf-8')
  # change the Canvas Data API secret to bytes
  api_secb = bytes(reqOpts['api_secret'], 'utf-8')

  # create an SHA-256 hashed HMAC object, then base 64 encode it
  signed_msg = base64.b64encode(hmac.new(api_secb, message,
                       digestmod=hashlib.sha256).digest())
  # must be 'decoded'to utf-8 to get rid of byte marks (^,.,^)
  signature = signed_msg.decode('utf-8')

  # build auth headers from Canvas Data API key, HMAC-256 sig, and timestamp
  auth_headers = { 'Authorization' : 'HMACAuth {}:{}'.format(api_key, signature),
                   'Date' : '{}'.format(reqOpts['req_timestamp']) }

  return auth_headers

