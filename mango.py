#!/usr/bin/python

import csv, sys

#####
# init
#####

INPUT_FILE = sys.argv[1]
INPUT_STATE_ABBR = sys.argv[2]
INPUT_COMPANY = sys.argv[3]
INPUT_TYPE = sys.argv[4]

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
indexes['campaign_num'] = 11


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

for i, row in enumerate(csv_rows):
  if is_qualified(input1, row):
    campaign_num = "-- no campaign number --" if row[indexes['campaign_num']] == "" else "WHOOPS, campaign num is present!"
    print "-------"
    print "row number", i + 1
    print row[0], row[1], row[indexes['phone']], row[indexes['email']], row[indexes['state']], row[indexes['company']], row[indexes['type']], campaign_num
    print "-------"
    print ""
