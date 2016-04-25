#!/usr/bin/env python
# NOTE: You may need to adjust the python path on your system
import json, sys

key_to_pull = sys.argv[1]
r_input=sys.stdin.read()
try:
  json_obj = json.loads(r_input)
  print json_obj.get(key_to_pull,key_to_pull+' missing, there might be errors')
except Exception,e:
  print e,r_input
