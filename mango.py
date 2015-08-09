#!/usr/bin/python

import csv, sys, argparse

#####
# parse args
#####

parser = argparse.ArgumentParser(description="This software is to help you find the correct contacts.")
parser.add_argument('-input-csv', dest="seed_data_file",
                    help="[ REQUIRED ] Name of CSV file. This file provides the original data.")
parser.add_argument('-state', dest="state",
                    help="[ REQUIRED ] State abbreviation, not full state name.")
parser.add_argument('-company', dest="company",
                    help="[ optional ] Company name.")
parser.add_argument('-type', dest="type",
                    help="[ REQUIRED ] Type, must be either 'Independent' or 'Captive'.")
parser.add_argument('-output-name', dest="output_file",
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

inputs.state = states[inputs.state]

#####
# setup
####

csv_file = csv.reader(open(inputs.seed_data_file))

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

if inputs.type == "Independent":
  campaign_limit = 3
else:
  campaign_limit = 1

qualified_rows = [row for row in csv_rows if is_qualified(inputs, row)]

rows_to_write = qualified_rows[:campaign_limit]
for r in rows_to_write:
  r[indexes['campaign_num']] = 3

# for r in qualified_rows:
#   print "------ qualified row --------"
#   print "name", r[0], r[1]
#   print "state", r[indexes['state']]
#   print "company", r[indexes['company']]
#   print "type", r[indexes['type']]
#   print "email", r[indexes['email']]
#   print "phone", r[indexes['phone']]
#   print "campaign_num", r[indexes['campaign_num']]
#   print "------ end row --------"
#   print ""
with open(inputs.output_file, 'wb') as output_file:
  writer = csv.writer(output_file)
  writer.writerows(csv_rows)
