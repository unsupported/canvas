Import Outcomes
===============

This folder includes two scripts that reads a CVS file of outcomes into Canvas. The only
difference between the two scripts is that one is built to import outcomes into a single
course whereas the other will import them into the account.

Requirements
------------

- Python >= 2.7
- requests library http://docs.python-requests.org/en/latest/
- percache library 
- list of outcomes in CSV format


Step 1
-------
Install all needed python modules.

.. code-block:: bash

   pip install requests percache

Step 2
------
Create an outcomes CSV file with the following headers. Note: not all of the
headers are visible on this page. Scroll horizontally to see them all.


+-------------+---------------------------+----------------------------------+---------------------------+--------------------------+--------------------+-----------------+----------------+----------------+----------------+
| vendor_guid | outcome_group_vendor_guid | parent_outcome_group_vendor_guid | title                     | description              | calculation_method | calculation_int | mastery_points | <mastery_n>... | <mastery_n>... |
+=============+===========================+==================================+===========================+==========================+====================+=================+================+================+================+
| sampleguid  | sample_group_guid         | sample_parent_guid               | This is an outcome title. | This is the description. | highest            | 0               | 5              | 1              | 2              |
+-------------+---------------------------+----------------------------------+---------------------------+--------------------------+--------------------+-----------------+----------------+----------------+----------------+





The first 8 columns are required and need to be in the order given. 


+----------------------------------+------------------------------------------------------------------------------------------------------------+---------+-----------------------------------------------+
| field                            | Description                                                                                                | Type    | Required                                      |
+----------------------------------+------------------------------------------------------------------------------------------------------------+---------+-----------------------------------------------+
| vendor_guid                      | This is the unique id for the outcome.  Leave blank for outcome groups                                     | string  | y                                             |
+----------------------------------+------------------------------------------------------------------------------------------------------------+---------+-----------------------------------------------+
| outcome_group_vendor_guid        | Unique id for the outcome group                                                                            | string  | y                                             |
+----------------------------------+------------------------------------------------------------------------------------------------------------+---------+-----------------------------------------------+
| parent_outcome_group_vendor_guid | If this row is creating an outcome group, this columns can optionally be filled out to make it a sub-group | string  | y                                             |
+----------------------------------+------------------------------------------------------------------------------------------------------------+---------+-----------------------------------------------+
| title                            | This is the name of the outcome. Leave blank for groups                                                    | string  | y                                             |
+----------------------------------+------------------------------------------------------------------------------------------------------------+---------+-----------------------------------------------+
| description                      | This is the description of the outcome. Blank for groups                                                   | string  | y                                             |
+----------------------------------+------------------------------------------------------------------------------------------------------------+---------+-----------------------------------------------+
| calculation_method               | Can be a value from the "calculation_method" on this page                                                  | string  | y                                             |
|                                  | https://canvas.instructure.com/doc/api/outcomes.html#method.outcomes_api.update                            |         |                                               |
|                                  | .  Each is explained in https://community.canvaslms.com/docs/DOC-1886                                      |         |                                               |
+----------------------------------+------------------------------------------------------------------------------------------------------------+---------+-----------------------------------------------+
| calculation_int                  | Only needed if calculation_method is set to decaying_average                                               | integer | y if calculation_method is `decaying_average` |
|                                  | or n_mastery. This value is an integer (so no decimals) and is explained at                                |         |                                               |
|                                  | https://community.canvaslms.com/docs/DOC-1886                                                              |         |                                               |
+----------------------------------+------------------------------------------------------------------------------------------------------------+---------+-----------------------------------------------+
| mastery_points                   | The score at which mastery is demonstrated                                                                 | integer | n                                             |
+----------------------------------+------------------------------------------------------------------------------------------------------------+---------+-----------------------------------------------+
| <mastery_1>...                   | The first rubric score (an integer)                                                                        | integer | y                                             |
+----------------------------------+------------------------------------------------------------------------------------------------------------+---------+-----------------------------------------------+
| <mastery_2>...                   | The second rubric score (an integer)                                                                       | integer | n                                             |
+----------------------------------+------------------------------------------------------------------------------------------------------------+---------+-----------------------------------------------+
| <mastery_n>...                   | The n-th rubric score (there can be any number of rubric scores)                                           | integer | n                                             |
+----------------------------------+------------------------------------------------------------------------------------------------------------+---------+-----------------------------------------------+

* calculation_int: Only needed if calculation_method is set to decaying_average
  or n_mastery. This value is an integer (so no decimals) and is explained at
  https://community.canvaslms.com/docs/DOC-1886


The remaining headers are the rubric scores that will be given when a teacher
clicks on an outcome rankings in that column. There must be at least one rubric
rating. There can be as many rating columns as you want


Sample csv files are located in the tests folder.

Usage
-------------

Create CSV files, run script.  It will prompt for required parameters.

An example of running the script would be

.. code-block:: bash

  python outcomes_importer.py --outcomesfile /path/to/file.csv --domain demo.instructure.com --token "token-goes-here"


Notes
-------

If common core or state standards have already been imported into the canvas
instance, the script an appear to stall. This is due to how it must download
all existing groups and outcomes before it can start creating them.
