#SSHA Password Hashing

This directory contains an example of hashing passwords in SSHA format. Some schools may
prefer doing this rather than sending plaintext passwords in the users.CSV file.  

The password is generated following the following process:

1. calculate the sha1 hex digest of the password with the salt and the salt
2. append the salt to the end
3. calculate the base64 string
4. prepend "{SSHA}" 
5. return the result

The result will end up looking like the following (which is the sha version of the
password `password` and the salt `asdf`.

```{SSHA}NjViMjRhYmZjODc2MTA1YzFiYTg4ZDQ4MThiMDNkMmUyN2RlOTQ5M2FzZGY=```

A CSV file with this information would look like the file `users_hashed.csv`.