# run in Python 3
''' 
This file audits the fields phone, postcode and street. 
These individual audits are all called in the audit() function.
''' 

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint



OSMFILE = 'small-sample.osm'



''' Audit phone numbers '''
phone_re = re.compile(r'^\+49\s\d{3}\s\d{6,8}$')


def audit_phone(phone_types, number):
	good_format = phone_re.search(number)
	if not good_format:
		phone_types.add(number)


def is_phone_number(elem):
	return (elem.attrib['k'] == 'phone')



''' Audit postcode '''
postcode_re = re.compile(r'^\d{5}$')


# https://www.suche-postleitzahl.org/koeln-plz-50667-51467.4c37
expected = ['50667', '50668', '50670', '50672', '50674', '50676', 
'50677', '50678', '50679', '50733', '50735', '50737', '50739', '50765', '50767', 
'50769', '50823', '50825', '50827', '50829', '50858', '50859', '50931', '50933', '50935', 
'50937', '50939', '50968', '50969', '50996', '50997', '50999', '51061', '51063', '51065', 
'51067', '51069', '51103', '51105', '51107', '51109', '51143', '51145', '51147', '51149']


def audit_postcode(bad_postcodes, postcode):
	m = postcode_re.search(postcode)
	if m:
		postcode = m.group()
		if postcode not in expected:
			bad_postcodes[postcode] +=1
	else:
		bad_postcodes[postcode] +=1


def is_postcode(elem):
	return (elem.attrib['k'] == 'addr:postcode')


''' Audit street types '''
pattern = r'''
^(Am\b|Auf\sdem\b|Auf\sder\b|Im\b|In\sder\b|An\b|Zum\b|Zur\b)| # match beginnings of street names
(straße|\bStraße|-Straße|\bWeg|weg|-Weg|platz|-Platz|\bPlatz| # match end of street names
gasse|\bRing|ring|\bHof|hof|
\bAllee|-Allee|allee|wall|\bWall|markt|gürtel)$'''



street_type_re = re.compile(pattern, re.VERBOSE)


# I- count occurences for each street type
def count_street_type(street_type_count, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        street_type_count[street_type] +=1
    else:
        street_type_count[street_name] +=1


# II- group streets by type
def group_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        street_types[street_type].add(street_name)
    else:
    	street_types[street_name].add(street_name)

# sorts the count of street types in descending order
def sort_values(street_type_count):
	sorted_counts = []
	d_view = [(v,k) for k,v in street_type_count.items()]
	d_view.sort(reverse=True) # natively sort tuples by first element
	for v,k in d_view:
		sorted_counts.append("%s: %d" % (k,v))
	return sorted_counts


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")





# perform all of the above audits on the file
def audit(osmfile):
    osm_file = open(osmfile, "r")

    phone_types = set()
    bad_postcodes = defaultdict(int)
    street_type_count = defaultdict(int)
    street_types = defaultdict(set)
    
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                	count_street_type(street_type_count, tag.attrib['v'])
                	group_street_type(street_types, tag.attrib['v'])
                if is_phone_number(tag):
                	audit_phone(phone_types,tag.attrib['v'])
                if is_postcode(tag):
                	audit_postcode(bad_postcodes, tag.attrib['v'])
    osm_file.close()

    street_type_count = sort_values(street_type_count)

    return phone_types, street_type_count, street_types, bad_postcodes


pprint.pprint(audit(OSMFILE))





