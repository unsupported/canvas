Import Outcomes
===============

This folder includes two scripts that reads a CVS file of outcomes into Canvas. The only
difference between the two scripts is that one is built to import outcomes into a single
course whereas the other will import them into the account.

Requirements
------------

- Python >= 2.4
- requests library http://docs.python-requests.org/en/latest/
- list of outcomes in CSV format

Step 1
------
- create CSV file with the following headers


+-------------+---------------------------+----------------------------------+---------------------------+--------------------------+--------------------+-----------------+----------------+----------------+----------------+
| vendor_guid | outcome_group_vendor_guid | parent_outcome_group_vendor_guid | title                     | description              | calculation_method | calculation_int | mastery_points | <mastery_n>... | <mastery_n>... |
+=============+===========================+==================================+===========================+==========================+====================+=================+================+================+================+
| sampleguid  | sample_group_guid         | sample_parent_guid               | This is an outcome title. | This is the description. | highest            | 0               | 5              | 1              | 2              |
+-------------+---------------------------+----------------------------------+---------------------------+--------------------------+--------------------+-----------------+----------------+----------------+----------------+

vendor_guid
outcome_group_vendor_guid
parent_outcome_group_vendor_guid
title
description
calculation_method
calculation_int
mastery_points
<mastery_n>...
<mastery_n>...

The first 8 columns are required and need to be in the order given. 

The remaining headers are the scores to give the outcome rankings in that column. 

.. csv-table::
  :file: tests/act_english_calculatio_method.csv

Usage
-------------

[draft]

Create CSV files, run script.  It will prompt for required parameters.
