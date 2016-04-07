#Functional as of Apr 07, 2016

#!/usr/bin/env python
import base64
import hashlib

"""
This method generates a SSHA password. This generated password can be included
in a Canvas users.csv file. If you do this, you would use a column called
ssha_password rather than simply password
"""
def gen_ssha_password(password,salt):
  final_hashed_pw = "{SSHA}%s" % base64.b64encode(gen_digested_password(password,salt)+salt)
  # '{SSHA}NjJmOTIzY2RlODEwOWI2MWEzMjRmMDY3N2Q3YzBjYWZkYjllNjQ4MDEyMzU='
  print 'final_hashed_pw',final_hashed_pw
  return final_hashed_pw

"""
This method generates the sha1 hex of the password+salt.
"""
def gen_digested_password(pw,salt):
  return hashlib.sha1('%s%s'%(pw,salt)).hexdigest()

"""
This method decodes a ssha-encoded password string, returning the
digest and salt
"""
def decode_ssha_password(ssha_password):
  decoded = base64.b64decode(ssha_password.replace("{SSHA}",""))
  digest = decoded[0:40]
  salt = decoded[40:]
  return digest,salt

"""
This method simply compares a given password to a ssha-encoded string.
"""
def compare_passwords(plaintext_password,ssha_password):

  if not plaintext_password or not ssha_password:
    return False 

  decoded = base64.b64decode(ssha_password.replace("{SSHA}",""))
  digest = decoded[0:40]
  salt = decoded[40:]
  if not all((digest,salt)):
    return False

  digested_password = gen_digested_password(plaintext_password,salt)
  print digest,digested_password
  return digest == digested_password

if __name__ == '__main__':
  ps = gen_ssha_password('password','asdf')
  #decode_ssha_password(ps)

  print compare_passwords('password',ps)
