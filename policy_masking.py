import json
import sys

import google.auth
import google.auth.transport.requests
import requests

def get_payload_and_url(project_id, locationId, policytag):
    data_policy_id = policytag.split("/")[-1]
    policy_url = f"https://bigquerydatapolicy.googleapis.com/v1/projects/{project_id}/locations/{locationId}/dataPolicies"
    policy_payload = {
        "dataPolicyType": "DATA_MASKING_POLICY",
        "dataPolicyId": f"masking_policy_{data_policy_id}",
        "policyTag": policytag,
        "dataMaskingPolicy": {
            "predefinedExpression": "DEFAULT_MASKING_VALUE"
        }
    }

    print(policy_url)
    print(policy_payload)
    return policy_url, policy_payload


def get_auth_token():
    creds, project = google.auth.default()
    auth_req = google.auth.transport.requests.Request()
    creds.refresh(auth_req)
    return creds.token



def create_masking_policy(policy_url, policy_payload):
    token = "Bearer " + get_auth_token()
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json; charset=utf-8'
    }
    try:
        response = requests.post(policy_url, headers=headers, json=policy_payload)
        print("response",response)
        if response.status_code == 200:
            print(response.text)

        else:
            err_text = json.loads(response.text)
            raise Exception("%s" % (err_text["error"]["message"]))

    except Exception as e:
        print("[ERROR]: %s" % (e))

def create_policy_masking_method(project_id, locationId, policytag):
    print("insidethefunction")
    policy_url, policy_payload = get_payload_and_url(project_id, locationId, policytag)
    create_masking_policy(policy_url, policy_payload)