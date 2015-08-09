#!/usr/bin/python

import csv, sys

#####
# init
#####

INPUT_FILE = sys.argv[1]
INPUT_STATE_ABBR = sys.argv[2]
INPUT_COMPANY = sys.argv[3]
INPUT_TYPE = sys.argv[4]
INPUT_DESIRED_OUTPUT_FILENAME = sys.argv[5]

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

INPUT_STATE = states[INPUT_STATE_ABBR]

#####
# setup
####

csv_file = csv.reader(open(INPUT_FILE))

csv_rows = []
for row in csv_file:
  if row[0] != "":
    csv_rows.append(row)

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
  return target['state'] == test[indexes['state']]

def correct_company_and_type(target, test):
  if target['type'] == "Independent":
    return test[indexes['type']] == "Independent"
  else:
    return target['company'] == test[indexes['company']]

def contact_info_exists(target, test):
  return test[indexes['phone']] != "" and test[indexes['email']] != ""

def not_previous_campaign(target, test):
  return test[indexes['campaign_num']] == ""

def is_qualified(target, test):
  return same_state(target, test) and \
    correct_company_and_type(target, test) and \
    contact_info_exists(target, test) and \
    not_previous_campaign(target, test)

input = {
  'state': INPUT_STATE,
  'company': INPUT_COMPANY,
  'type': INPUT_TYPE
}

if INPUT_TYPE == "Independent":
  campaign_limit = 3
else:
  campaign_limit = 1

qualified_rows = [row for row in csv_rows if is_qualified(input, row)]

rows_to_write = qualified_rows[:campaign_limit]
for r in rows_to_write:
  r[indexes['campaign_num']] = 3

with open(INPUT_DESIRED_OUTPUT_FILENAME, 'wb') as output_file:
  writer = csv.writer(output_file)
  writer.writerows(csv_rows)
