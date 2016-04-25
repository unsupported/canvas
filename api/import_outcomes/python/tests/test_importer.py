from unittest import TestCase
import os
import uuid

import outcomes_importer
from outcomes_importer import checkFileReturnCSVReader
from outcomes_importer import isValidRow
from outcomes_importer import createOutcome
from outcomes_importer import getOrCreateOutcome
from outcomes_importer import updateOutcome
from outcomes_importer import createOutcomeGroup
from outcomes_importer import getOrCreateOutcomeGroup
from outcomes_importer import deleteOutcomeGroup
from outcomes_importer import paginated_outcome_subgroups
from outcomes_importer import getRootOutcomeGroup
from outcomes_importer import findOutcomeGroup

#from outcomes_importer.outcomes_importercsv_onefile import checkFileReturnCSVReader

class OutcomeImporterTests(TestCase):
  def setUp(self):
    outcomes_importer.domain = os.environ['CANVAS_DOMAIN']
    outcomes_importer.token = os.environ['CANVAS_ACCESS_TOKEN']
    self.path_to_valid_file = "./tests/act_english_calculatio_method.csv"
    self.outcome_group = None
    self.outcome_vendor_guid = uuid.uuid4().hex
    self.outcome_group_vendor_guid = uuid.uuid4().hex

  def tearDown(self):
    print 'hello from tearDown'
    # TODO Delete outcome and outcome groups if they are created
    if self.outcome_group:
      # TODO delete it
      print deleteOutcomeGroup(self.outcome_group['id'])

  def test_check_file_exists(self):
    '''
    vendor_guid	outcome_group_vendor_guid	parent_outcome_group_vendor_guid	title	description	calculation_method	calculation_int	mastery_points	1	2	3	4
    '''
    self.assertTrue(os.path.exists(self.path_to_valid_file))
    outcomes_file = checkFileReturnCSVReader(self.path_to_valid_file)
    self.assertTrue(outcomes_file)
    
  def test_check_validates_first_row(self):
    outcomes_file = checkFileReturnCSVReader(self.path_to_valid_file)
    first_row = outcomes_file.next()
    fields = ('vendor_guid','outcome_group_vendor_guid','parent_outcome_group_vendor_guid','title','description','calculation_method','calculation_int','mastery_points','1','2','3','4')
    for idx,f in enumerate(fields):
      self.assertEqual(first_row[idx],f)

    second_row = outcomes_file.next()
    self.assertTrue(isValidRow(second_row))

  def test_findOutcomeGroup(self):
    # Create outcome group
    # Delete the vendor cache
    # outcome group should exist

    self.assertTrue(False)

  def test_create_outcome(self):
    outcome = {
      'title':'test outcome',
      'description':'test description',
      'short_description':'test description',
      'vendor_guid':'test_guid_{}'.format(self.outcome_vendor_guid),
      'outcome_group_vendor_guid':'test_group_guid_{}'.format(self.outcome_group_vendor_guid),
      'mastery_points':5,
      #'ratings':
      'calculation_method':'decaying_average',
      'calculation_int':'75'
      }

    self.outcome_group = getOrCreateOutcomeGroup(outcome['outcome_group_vendor_guid'],outcome['outcome_group_vendor_guid'],outcome['outcome_group_vendor_guid'])
    self.assertTrue(self.outcome_group.has_key('id'))

    outcome['group_id'] = self.outcome_group['id']
    o = createOutcome(outcome)
    self.assertTrue(o.has_key('outcome'),msg=o)
    self.assertTrue(o['outcome'].has_key('id'),msg=o)

  def test_getRootOutcomeGroup(self):
    self.assertIsInstance(getRootOutcomeGroup(),dict)
    self.assertTrue(getRootOutcomeGroup().has_key('id'))
    self.assertEqual(3755,getRootOutcomeGroup()['id'])

  def test_paginatedOutcomeSubgroups(self):
    root_group = getRootOutcomeGroup()
    self.assertEqual(3755,root_group['id'])
    og = createOutcomeGroup(self.outcome_group_vendor_guid,'test group','test description',root_group['id'])

    pog = paginated_outcome_subgroups(root_group['id'])
    #self.assertIsInstance(pog,iterator)
    for og in pog:
      self.assertIsInstance(og,dict)

  def test_findOutcomeGroup(self):
    outcome = {
      'title':'test outcome',
      'description':'test description',
      'vendor_guid':'test_guid_{}'.format(self.outcome_vendor_guid),
      'outcome_group_vendor_guid':'test_group_guid_{}'.format(self.outcome_group_vendor_guid),
      'mastery_points':5,
      #'ratings':
      'calculation_method':'decaying_average',
      'calculation_int':'75'
      }

    self.outcome_group = getOrCreateOutcomeGroup(outcome['outcome_group_vendor_guid'],outcome['outcome_group_vendor_guid'],outcome['outcome_group_vendor_guid'])
    og = findOutcomeGroup(outcome['outcome_group_vendor_guid'])
    self.assertTrue(og)
    self.assertTrue(og.has_key('id'))

  def test_update_outcome(self):
    outcome = {
      'title':'test outcome',
      'description':'test description',
      'vendor_guid':'test_guid_{}'.format(self.outcome_vendor_guid),
      'outcome_group_vendor_guid':'test_group_guid_{}'.format(self.outcome_group_vendor_guid),
      'mastery_points':5,
      #'ratings':
      'calculation_method':'decaying_average',
      'calculation_int':'75'
     }
    self.outcome_group = getOrCreateOutcomeGroup(outcome['outcome_group_vendor_guid'],outcome['outcome_group_vendor_guid'],outcome['outcome_group_vendor_guid'])
    outcome['group_id'] = self.outcome_group['id']
    o = getOrCreateOutcome(outcome)
    self.assertTrue(o.has_key('outcome'))
    self.assertTrue(o['outcome'].has_key('id'))
    
    o['title'] = 'updated title'
    o = updateOutcome(o)
    
    updated_outcome = getOrCreateOutcome(outcome)
    self.assertEqual(updated_outcome['outcome']['title'],'updated title')

