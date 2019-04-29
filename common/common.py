import hashlib
import re

# function to create a dictionary that will be used to 
# store data and then that dictionary is being used to write out output
def dictGenerator():
    entity = {}
    entity['reserved_1'] = ''
    entity['app_trans_id'] = ''
    entity['cust_ref_text_1'] = ''
    entity['cust_ref_text_2'] = ''
    entity['reserved_2'] = ''
    entity['reserved_3'] = ''
    entity['reserved_4'] = ''
    entity['reserved_5'] = ''
    entity['DUNS'] = ''
    entity['bus_name'] = ''
    entity['reserved_6'] = ''
    entity['address_line_1'] = ''
    entity['address_line_2'] = ''
    entity['city'] = ''
    entity['territory'] = ''
    entity['postal_code'] = ''
    entity['reserved_7'] = ''
    entity['countryISOAlpha'] = ''
    entity['reserved_8'] = ''
    entity['phone'] = ''
    entity['nat_id_code'] = ''
    entity['nat_id_value'] = ''

    return entity

# function to take the dictionary provided above and generate csv into comma seperated
# it takes each value and puts it into double quotes if there is a comma in the row
def csvGenerator(entity):
    result = ''

    for k, v in entity.items():
        if ',' in str(entity[k]):
            result += "\"" + str(entity[k]) + "\"" + ','
        else:
            result += str(entity[k]) + ','

    result = re.sub('&.*;', ' ', result)
    return result.replace('\n', ' ')

def headers(entity):
    
    headers = ''
    for k, v in entity.items():
        headers+= ',' + str(k)

    headers = headers[1:]



    return headers
