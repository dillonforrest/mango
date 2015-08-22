#!/usr/bin/python

import csv, sys, argparse

#####
# parse args
#####

parser = argparse.ArgumentParser(description="This software is to help you find the correct contacts.")
parser.add_argument('-input', dest="seed_data_file", required=True
                    help="[ REQUIRED ] Name of CSV file. This file provides the original data.")
parser.add_argument('-targets', dest="targets_file", required=True
                    help="[ REQUIRED ] File name of CSV containing the contacts you want to find.")
parser.add_argument('-number', dest="campaign_number", required=True
                    help="[ REQUIRED ] The campaign number to be added for the target contacts.")
parser.add_argument('-output', dest="output_file",
                    help="[ optional ] Output file name. Defaults to 'output.csv'.")

#####
# init
#####

inputs = parser.parse_args()

states = {
  'AK': 'Alaska',
  'AL': 'Alabama',
  'AR': 'Arkansas',
  'AS': 'American Samoa',
  'AZ': 'Arizona',
  'CA': 'California',
  'CO': 'Colorado',
  'CT': 'Connecticut',
  'DC': 'District of Columbia',
  'DE': 'Delaware',
  'FL': 'Florida',
  'GA': 'Georgia',
  'GU': 'Guam',
  'HI': 'Hawaii',
  'IA': 'Iowa',
  'ID': 'Idaho',
  'IL': 'Illinois',
  'IN': 'Indiana',
  'KS': 'Kansas',
  'KY': 'Kentucky',
  'LA': 'Louisiana',
  'MA': 'Massachusetts',
  'MD': 'Maryland',
  'ME': 'Maine',
  'MI': 'Michigan',
  'MN': 'Minnesota',
  'MO': 'Missouri',
  'MP': 'Northern Mariana Islands',
  'MS': 'Mississippi',
  'MT': 'Montana',
  'NA': 'National',
  'NC': 'North Carolina',
  'ND': 'North Dakota',
  'NE': 'Nebraska',
  'NH': 'New Hampshire',
  'NJ': 'New Jersey',
  'NM': 'New Mexico',
  'NV': 'Nevada',
  'NY': 'New York',
  'OH': 'Ohio',
  'OK': 'Oklahoma',
  'OR': 'Oregon',
  'PA': 'Pennsylvania',
  'PR': 'Puerto Rico',
  'RI': 'Rhode Island',
  'SC': 'South Carolina',
  'SD': 'South Dakota',
  'TN': 'Tennessee',
  'TX': 'Texas',
  'UT': 'Utah',
  'VA': 'Virginia',
  'VI': 'Virgin Islands',
  'VT': 'Vermont',
  'WA': 'Washington',
  'WI': 'Wisconsin',
  'WV': 'West Virginia',
  'WY': 'Wyoming'
}

#####
# setup
####

csv_seed_data_file = csv.reader(open(inputs.seed_data_file))
csv_targets_file = csv.reader(open(inputs.targets_file))

def erase_empty_rows(rows):
  return [ row for row in rows where row[0] != "" ]

csv_rows = erase_empty_rows(csv_seed_data_file)
targets_rows = erase_empty_rows(csv_targets_file)

indexes = {}
indexes['phone'] = 3
indexes['email'] = 4
indexes['state'] = 6
indexes['company'] = 8
indexes['type'] = 9
indexes['campaign_num'] = 10


#####
# qualifiers
####

def same_state(target, test):
  return target.state == test[indexes['state']]

def correct_company_and_type(target, test):
  if target.type == "Independent":
    return test[indexes['type']] == "Independent"
  else:
    return target.company == test[indexes['company']]

def contact_info_exists(target, test):
  return test[indexes['phone']] != "" and test[indexes['email']] != ""

def not_previous_campaign(target, test):
  return test[indexes['campaign_num']] == ""

def is_qualified(target, test):
  return same_state(target, test) and \
    correct_company_and_type(target, test) and \
    contact_info_exists(target, test) and \
    not_previous_campaign(target, test)


rows_to_write = []

def find_qualified_rows(inputs):
  qualified_rows = [row for row in csv_rows if is_qualified(inputs, row)]

  if inputs.type == "Independent":
    campaign_limit = 3
  else:
    campaign_limit = 1

  rows_to_write.merge(qualified_rows[:campaign_limit])

for target in targets_rows:
  find_qualified_rows(target)

for r in rows_to_write[:60]:
  r[indexes['campaign_num']] = inputs.campaign_number

if len(rows_to_write) == 0
  print "didn't find any qualified rows :("
else
  print 'found %(count_total)d qualified rows.' % {'count_total': len(rows_to_write)}
  print 'wrote campaign number %(campaign_num)d for %(count_written)d rows.' % {'campaign_num': inputs.campaign_num, 'count_written': len(rows_to_write[:60])}

with open(inputs.output_file, 'wb') as output_file:
  writer = csv.writer(output_file)
  writer.writerows(csv_rows)
