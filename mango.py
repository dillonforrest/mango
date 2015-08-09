import csv

#####
# setup
####

csv_file = csv.reader(open('auto-insurance.csv'))

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
# TODO: allow inputs
####

input1 = {}
input1['state'] = 'Massachusetts'
input1['company'] = 'Any'
input1['type'] = 'Independent'

input2 = {}
input2['state'] = 'Massachusetts'
input2['company'] = 'MetLife'
input2['type'] = 'Captive'

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

for i, row in enumerate(csv_rows):
  if is_qualified(input1, row):
    campaign_num = "-- no campaign number --" if row[indexes['campaign_num']] == "" else "WHOOPS, campaign num is present!"
    print "-------"
    print "row number", i + 1
    print row[0], row[1], row[indexes['phone']], row[indexes['email']], row[indexes['state']], row[indexes['company']], row[indexes['type']], campaign_num
    print "-------"
    print ""
