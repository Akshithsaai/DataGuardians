import google.auth
import google.auth.transport.requests
import requests
import json

# Get default credentials
def get_auth_token():
    creds, project = google.auth.default()
    auth_req = google.auth.transport.requests.Request()
    creds.refresh(auth_req)
    return creds.token

# Create taxonomy
def create_taxonomy(args):
    p_args = json.loads(args)
    project_id = p_args["project_id"]
    location = p_args["location"]
    token = "Bearer " + get_auth_token()
    headers = {
        "Authorization": token,
        "Content-Type": "application/json; charset=utf-8"
    }
    url = f"https://datacatalog.googleapis.com/v1/projects/{project_id}/locations/{location}/taxonomies"

    display_name = p_args["display_name"]
    description = p_args["description"]
    activatedPolicyTypes = p_args["activatedPolicyTypes"]

    data = '{"activatedPolicyTypes": %s, "displayName": "%s", "description": "%s"}' % (
        json.dumps(activatedPolicyTypes), display_name, description)

    print(json.dumps(json.loads(data), indent=2))

    try:
        response = requests.post(url, headers=headers, data=data)
        print(response.text)

        if response.status_code == 200:
            print("Created Taxonomy: {}".format(display_name))
            ret_json = json.loads(response.text)
            return ret_json
        else:
            err_text = json.loads(response.text)
            raise Exception("%s" % (err_text["error"]["message"]))

    except Exception as ex:
        print("[ERROR]: %s" % ex)

# Delete taxonomy
def delete_taxonomy(args):
    p_args = json.loads(args)
    project_id = p_args.get("project_id")
    location = p_args.get("location")
    tax_id = p_args.get("tax_id")
    parent = p_args.get("parent")

    if parent == None:
        parent = f"projects/{project_id}/locations/{location}/taxonomies/{tax_id}"

    token = "Bearer " + get_auth_token()
    headers = {
        "Authorization": token,
        "Content-Type": "application/json; charset=utf-8"
    }

    url = f"https://datacatalog.googleapis.com/v1/{parent}"

    try:
        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            print("Deleted Taxonomy: {}".format(tax_id))
        else:
            err_text = json.loads(response.text)
            raise Exception("%s" % (err_text["error"]["message"]))

    except Exception as ex:
        print("[ERROR]: %s" % ex)

# List all taxonomies
def list_taxonomies(args):
    p_args = json.loads(args)
    project_id = p_args["project_id"]
    location = p_args["location"]
    token = "Bearer " + get_auth_token()
    headers = {
        "Authorization": token,
        "Content-Type": "application/json; charset=utf-8"
    }
    url = f"https://datacatalog.googleapis.com/v1/projects/{project_id}/locations/{location}/taxonomies"
    tax_response= {}
    print("list_toxo")
    try:
        response = requests.get(url, headers=headers)
        print(response.text)
        if response.status_code == 200:
            # ret_json = response.json()
            ret_json = json.loads(response.text)
            # print(response)
            #tax_response["taxonomies"] = ret_json
            return ret_json
        else:
            err_text = json.loads(response.text)
            raise Exception("%s" % (err_text["error"]["message"]))

    except Exception as ex:
        print("[ERROR]: %s" % ex)

# Create policy tag
def create_policy_tag(args):
    p_args = json.loads(args)
    project_id = p_args.get("project_id")
    location = p_args.get("location")
    taxonomy_id = p_args.get("taxonomy_id")
    parent = p_args.get("parent")

    if parent == None:
        parent = f"projects/{project_id}/locations/{location}/taxonomies/{taxonomy_id}"

    token = "Bearer " + get_auth_token()
    headers = {
        "Authorization": token,
        "Content-Type": "application/json; charset=utf-8"
    }
    url = f"https://datacatalog.googleapis.com/v1/{parent}/policyTags"
    print(url)
    display_name = p_args.get("display_name")
    description = p_args.get("description")
    parentPolicyTag = p_args.get("parentPolicyTag")

    data = '{"displayName": "%s", "description": "%s", "parentPolicyTag": "%s"}' % (
        display_name, description, parentPolicyTag)

    # try:
    response = requests.post(url, headers=headers, data=data)
    print(response)
    if response.status_code == 200:
        ret_json = json.loads(response.text)
        return ret_json
    else:
        err_text = json.loads(response.text)
        raise Exception("%s" % (err_text["error"]["message"]))

    # except Exception as ex:
        # print("[ERROR]: %s" % ex)

# List policy tags
def list_policy_tags(args):
    p_args = json.loads(args)
    project_id = p_args.get("project_id")
    location = p_args.get("location")
    taxonomy_id = p_args.get("taxonomy_id")
    parent = p_args.get("parent")
    out_put= {}

    if parent == None:
        parent = f"projects/{project_id}/locations/{location}/taxonomies/{taxonomy_id}"

    token = "Bearer " + get_auth_token()
    headers = {
        "Authorization": token,
        "Content-Type": "application/json; charset=utf-8"
    }
    url = f"https://datacatalog.googleapis.com/v1/{parent}/policyTags?pageSize=100"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            ret_json = json.loads(response.text)
            return ret_json
        else:
            err_text = json.loads(response.text)
            raise Exception("%s" % (err_text["error"]["message"]))

    except Exception as e:
        print("[ERROR]: %s" % (e))

def get_policy_tags(args):
    p_args = json.loads(args)
    project_id = p_args['project_id']
    location = p_args['location']
    taxonomy_id = p_args['taxonomy_id']
    policytag = p_args['policytag']
    list_attr = p_args['list_attr']

    token = "Bearer " + "your-auth-token"  # Replace with actual token
    headers = {'Authorization': token, 'Content-Type': 'application/json; charset=utf-8'}
    url = f"https://datacatalog.googleapis.com/v1/projects/{project_id}/locations/{location}/taxonomies/{taxonomy_id}/policyTags/{policytag}"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            ret_json = json.loads(response.text)
            if len(list_attr) > 0:
                print(ret_json[list_attr])
            else:
                print(ret_json)
        else:
            err_text = json.loads(response.text)
            raise Exception(f"{err_text['error']['message']}")

    except Exception as e:
        print("[ERROR]: ", e)

def delete_policy_tag(args):
    p_args = json.loads(args)
    project_id = p_args.get('project_id')
    location = p_args.get('location')
    taxonomy_id = p_args.get('taxonomy_id')
    policytag = p_args.get('policytag')
    parent = p_args.get('parent')

    if parent is None:
        parent = f"projects/{project_id}/locations/{location}/taxonomies/{taxonomy_id}/policyTags/{policytag}"

    token = "Bearer " + "your-auth-token"  # Replace with actual token
    headers = {'Authorization': token, 'Content-Type': 'application/json; charset=utf-8'}
    url = f"https://datacatalog.googleapis.com/v1/{parent}"

    try:
        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            print("Deleted Taxonomy For Parent: {}".format(parent))
        else:
            err_text = json.loads(response.text)
            raise Exception(f"{err_text['error']['message']}")

    except Exception as e:
        print("[ERROR]: ", e)

def get_bq_schema(args):
    p_args = json.loads(args)
    project_id = p_args['project_id']
    dataset_id = p_args['dataset_id']
    table_id = p_args['table_id']

    token = "Bearer " + get_auth_token() # Replace with actual token
    headers = {'Authorization': token, 'Content-Type': 'application/json; charset=utf-8'}
    url = f"https://bigquery.googleapis.com/bigquery/v2/projects/{project_id}/datasets/{dataset_id}/tables/{table_id}"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            ret_json = json.loads(response.text)
            print(response)
            return ret_json
        else:
            err_text = json.loads(response.text)
            raise Exception(f"{err_text['error']['message']}")

    except Exception as e:
        print("[ERROR]: ", e)


def tag_bq_tbl(args):
    print("stage1")
    p_args = json.loads(args)
    project_id = p_args["project_id"]
    dataset_id = p_args["dataset_id"]
    table_id = p_args["table_id"]
    tags = p_args["tags"]
    # t_column = tags["t_column"]
    # t_tag_id = tags["tag_id"]
    # t_operation = tags["operation"]

    token = "Bearer " + get_auth_token()
    headers = {
        "Authorization": token,
        "Content-Type": "application/json; charset=utf-8"
    }
    

    bq_schema_args = f'"project_id": "{project_id}","dataset_id": "{dataset_id}","table_id": "{table_id}"'
    

    bq_schema = get_bq_schema("{" +  bq_schema_args + "}")
    tagged_schema = []

    for t in bq_schema["schema"]["fields"]:
        t_field = t.copy()

        for jn in tags:
            if t["name"].lower() == jn['t_column'].lower() and t.get("fields") is None:
                if jn["operation"] == "add" and t.get("policyTags") is None:
                    t_field["policyTags"] = {}
                    t_field["policyTags"]["names"] =  [jn["tag_id"]]
                

            elif jn["t_column"].find(".") != -1 and t.get("fields") != None:
                name_sp = jn["t_column"].split(".")
                if name_sp[0].lower() == t["name"].lower():
                    t_field = nested_tag(t, name_sp, len(name_sp), 1, jn)
                    print("hola")

        tagged_schema.append(t_field)

    url = f"https://bigquery.googleapis.com/bigquery/v2/projects/{project_id}/datasets/{dataset_id}/tables/{table_id}"
    json_data = {"schema": {"fields": tagged_schema}}

    try:
        response = requests.patch(url, headers=headers, data=json.dumps(json_data).encode('utf-8'))
        if response.status_code == 200:
            ret_json = json.loads(response.text)
            return ret_json
        err_text = json.loads(response.text)
        raise Exception("X5 : %s" % (err_text["error"]["message"]))

    except Exception as e:
        print("[ERROR]: %s" % (e))


def set_iam_policy_tags_for_multiple_members(args):
    p_args = json.loads(args)

    project_id = p_args.get("project_id")
    location = p_args.get("location")
    taxonomy_id = p_args.get("taxonomy_id")
    tag_id = p_args.get("tag_id")
    parent = p_args.get("parent")

    if parent is None:
        parent = f"projects/{project_id}/locations/{location}/taxonomies/{taxonomy_id}/policyTags/{tag_id}"

    token = "Bearer " + get_auth_token()
    headers = {
        "Authorization": token,
        "Content-Type": "application/json; charset=utf-8"
    }

    url = f"https://datacatalog.googleapis.com/v1/{parent}:setIamPolicy"
    role = p_args.get("role")
    members = p_args.get("members").replace("|", ",")

    print("The List of Members requested to be configured are " + members)
    print("Final Request of Members to be sent in request will be -> " + members)

    a_json = {"policy": {"bindings": [{"members": members.split(","), "role": role}]}}
    print("Request JSON Data is :->", a_json)

    try:
        response = requests.post(url, headers=headers, data=json.dumps(a_json))
        if response.status_code == 200:
            ret_json = json.loads(response.text)
            return ret_json
        else:
            err_text = json.loads(response.text)
            raise Exception("X6 : %s" % (err_text["error"]["message"]))

    except Exception as e:
        print("[ERROR]: %s" % (e))


def nested_tag_bq(dictedit, name_sp, depth, c, j):
    for i in range(len(dictedit["fields"])):
        if name_sp[c].lower() == dictedit["fields"][i]["name"].lower():
            print("Check", dictedit)
            if c == depth - 1:
                if j["operation"] == "add" and dictedit["fields"][i].get("policyTags") is None:
                    dictedit["fields"][i]["policyTags"] = {"names": [j["tag_id"]]}
                elif j["operation"] == "remove" and dictedit["fields"][i].get("policyTags") is not None:
                    print("Remove", dictedit["fields"][i]["policyTags"]["names"])
                    dictedit["fields"][i]["policyTags"] = {}
                return dictedit
            else:
                dictedit["fields"][i] = nested_tag_bq(dictedit["fields"][i], name_sp, depth, c + 1, j)
    return dictedit
