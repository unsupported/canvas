# Bulk Add User Logins

## Purpose

Logins for multiple user accounts can be created in bulk by running the `bulk_add_user_logins.rb` script.

## Script Preparation

After initiating the script, you'll be prompted for the following (have these values ready)\:

- `ENV` - environment (prod, beta, test)
  - When targeting the production environment, simply press `Enter` without any additional text.
  - Otherwise, type 'beta' or 'test' for the appropriate environment.
- `DOMAIN` - For the example of \<domain\>.instructure.com, `domain`is all that\'s needed.
- `TOKEN` - A valid access token that\'s associated to a user with the required permissions to create user logins.
- `CSV FILE PATH` - Full path to the example.csv file. EX\: `Users/panda/full/file/path/example.csv`

The script has been modified so that the lines involving `authentication_provider_id` and `sis_user_id` are disabled.  Comments have been added to the script, indicating which lines should be enabled for either values.

## CSV Preparation

The example.csv file should include specific headers\:

- `canvas_user_id` (**Required**)
  - This is the numeric value found in the URL for a user's account\. EX\: `<domain>.instructure.com/users/:id`
- `login_id` (**Required**)
- `authentication_provider_id` (Optional)
  - Not needed if the authentication used will be Canvas, LDAP, SAML, or CAS.
  - If using this option, values should be passed as all lowercase.
  - This can also be the numeric ID found in the authentication_providers API endpoint.
- `sis_user_id` (Optional)

## Running the Script

In the Command Line, while in the same directory as your script file, type `ruby bulk_add_user_logins.rb`.  Go through the prompts as the script instructs and the API response will be printed each time a login is created.

## Support

As the name of this repository implies, this script is provided AS-IS, without warranty, and without any additional support beyond this document. Instructure will not be able to help you fix or debug this script. Any further assistance needed should be requested via this repository, or from others in the community.

Keep all of this in mind and use these scripts as templates or as a starting point.

Good luck!
