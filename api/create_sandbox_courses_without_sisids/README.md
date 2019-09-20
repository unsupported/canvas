LAST WORKING AS OF 07/30/2018
<h1>Sandbox Course Creation Script</h1>
==============================

<h2>General Info</h2>
This script can be used to create sandbox courses for teachers. This script will not assign a sis_id for users. The goal is to set the email as the login_id so that if/when an integration happens the sis_id's will be assigned based on login_id.

<h2>CSV Sample</h2>
<table>
    <tr>
        <td>first_name</td>
        <td>last_name</td>
        <td>login_id</td>
    </tr>
      <tr>
        <td>John</td>
        <td>Jacob</td>
        <td>jj@example.com</td>
    </tr>
</table>


<h2>How to run</h2>
1. Run PIP install requests, PIP install csv, and PIP install os (if setting api key to environmental variable)
2. Set variables required to run
3. Enjoy
