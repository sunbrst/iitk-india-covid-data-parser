from typing import List
import os
import json

import requests

from hospital import Hospital
from hospital import Resource


#https://www.getpostman.com/collections/ac744d6c750be50db61e
def resource_to_json(resource: Resource):
    return {
        "resourceType": resource.resource_type.name,
        "description": resource.resource_description,
        "quantity": resource.resource_qty
    }


def hospital_to_json(hospital: Hospital):
    h_id = "{}-{}-{}".format(hospital.state, hospital.city, hospital.name)
    resources_json_array = [
        resource_to_json(resource) for resource in hospital.resources
    ]
    json_obj = {
        "lastUpdatedAt": hospital.last_updated.isoformat(),
        "resources": resources_json_array,
        "vendor": {
            "name": hospital.name,
            "address": {
                "completeAddress": hospital.address,
                "city": hospital.city,
                "district": hospital.district,
                "state": hospital.state
            }
        }
    }

    return json_obj


def get_host():
    return os.environ.get('INDIA_COVID_HOST')


def get_headers():
    header_value = os.environ.get('INDIA_COVID_AUTH_HEADER')
    if not header_value:
        raise AssertionError(
            'Missing environment variable: INDIA_COVID_AUTH_HEADER')
    return {'authorization': header_value, 'Content-Type': 'application/json'}


def post_request(json_obj):
    host = get_host()
    url = "http://{}/dataLeads".format(host)
    headers = get_headers()
    # print(json.dumps(json_obj))
    return requests.post(url, json=json_obj, headers=headers)


def get_request():
    host = get_host()
    url = "http://{}/dataLeads".format(host)
    return requests.get(url)


def upload_hospitals(hospitals: List[Hospital]):
    for hospital in hospitals:
        json_hospital = hospital_to_json(hospital)
        resp = post_request(json_hospital)
        if resp.status_code != 200:
            raise AssertionError("Update failed with {}, {}".format(
                resp.status_code, resp.text))
