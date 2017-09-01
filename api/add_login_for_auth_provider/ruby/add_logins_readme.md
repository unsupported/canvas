Bulk Add User Logins Read.Me

Requires Ruby and the Typhoeus gem

To use this script, generate a CSV that contains the following headers:
- canvas_user_id (Numeric ID that appears in a Canvas user page URL; not the SIS ID)
- login_id (The desired username)
- authentication_provider_id (The ID you'll find via API for a configured Authentication Provider)
- sis_user_id (the SIS ID (if desired) for the login you're adding to a user)

After preparing your CSV, modify the User Area in the script (surrounded by #'s) with your desired parameters, leveraging the code notes for guidance.

Last, run the script.
