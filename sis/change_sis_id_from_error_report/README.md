LAST WORKING AS OF 07/31/2018


<h1>Change_sis_id.csv Generator</h1>
<p>This script will read an error report for users that already have sis_id's in Canvas and generate a change_sis_id.csv that can be used to fix the errors.</p>

<h3>To run this script</h3>

1. Move error report into working directory
2. In terminal, run - python fix_csv.py

<h3>Sample of Error CSV</h3>
<table>
  <tr>
    <th>sis_import_id</th>
    <th>file</th>
    <th>message</th>
    <th>row</th>
  </tr>
  <tr>
    <td>39</td>
    <td>users.csv</td>
    <td>An existing Canvas user with the SIS ID XXXXXX has already claimed YYYYYYY's user_id requested login information, skipping</td>
  </tr>
</table>

<h1>Important Disclaimers</h1>

1. This script is unsupported. Please validate functionality.
2. This script assumes that you do not have spaces in your SIS_ID's.
3. This script is assuming that you do not have integration id's
