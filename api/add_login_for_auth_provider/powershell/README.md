#Add additional login for a specific authentication provider

This script can be used to add an additional login to a Canvas user for a specific authentication provider. The authentication provider must already be configured in Canvas BEFORE running this script. Please see [Configuring Authentication Providers](https://community.canvaslms.com/docs/DOC-4284). More information on the API used to add authentication provider specific logins is available at [Create User Login](https://canvas.instructure.com/doc/api/logins.html#method.pseudonyms.create).

The input CSV has 2 required columns and one optional column. An example is provided below:
```
    user_id,new_login_id,new_sis_id
    student_1234,sample_username,new_sis_id
```

* `user_id:` The Canvas or SIS ID for the user on which you would like to add the new login_id
* `new_login_id:` The new login_id for the user. This can be the same as an existing login_id for the user as long as the authentication provider is different.
* `new_sis_id:` (optional field) This column contains the value that will be used as the SIS ID for the new login on the user. The SIS ID must NOT already be in use on any active or deleted login in your Canvas instance. If this column is not included or the value is blank an SIS ID will be auto generated based on the authentication provider ID and the provided user_id.
