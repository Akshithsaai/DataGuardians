import datacatalog as dco
import sys

def get_policy_tags(taxonomy_name, taxonomy_names, gcp_project, gcp_location, bq_column_list):
    bq_col_tags = "["
    for bq_column in bq_column_list:
        taxonomy_id = taxonomy_names.get(taxonomy_name)
        if not taxonomy_id:
            print(f"Taxonomy {taxonomy_name} does not exists in project {gcp_project} location {gcp_location}")
            continue

        args = '{"parent": "%s"}' % (taxonomy_id)
        print(args)
        policy_tags_list = dco.list_policy_tags(args)
        print(policy_tags_list)
        # sys.exit(-1)
        policy_tag_id = [d["name"] for d in policy_tags_list["policyTags"] if d["displayName"] == bq_column]
        if not policy_tag_id:
            print(f"Policy tag ({bq_column}) does not exist in the Taxonomy {taxonomy_name}")
            continue

        if len(bq_col_tags) > 1:
            bq_col_tags = bq_col_tags + ", "
            
        operation = "add"

        col_tags = '{"t_column": "%s", "tag_id": "%s", "operation": "%s"}' % (bq_column, policy_tag_id[0], operation)
        bq_col_tags = bq_col_tags + col_tags

    bq_col_tags = bq_col_tags + "]"
    print(bq_col_tags)
    return bq_col_tags

def bq_policy_tagging(gcp_project, gcp_location, vertex_pi_data, dataset_id):
    args = '{ "project_id": "%s", "location": "%s" }' % (gcp_project, gcp_location)

    # Fetch the Taxonomies
    project_taxonomies = dco.list_taxonomies(args)
    taxonomy_names = {i.get("displayName"): i.get("name") for i in project_taxonomies.get("taxonomies")}
    print(taxonomy_names)
    #taxonomy_names= {'bank_accounts': 'projects/ltc-reboot25-team-24/locations/europe-west2/taxonomies/1387064841247349444'}
    
#     taxonomy_names ={'bank_accounts': 'projects/ltc-reboot25-team-24/locations/europe-west2/taxonomies/1387064841247349444', 'credit_cards': 'projects/ltc-reboot25-team-24/locations/europe-west2/taxonomies/945163344233201182', 'insurance_policies': 'projects/ltc-reboot25-team-24/locations/europe-west2/taxonomies/2806330433700643833', 'orders': 'projects/ltc-reboot25-team-24/locations/europe-west2/taxonomies/1825501431617128605', 'payment_details': 'projects/ltc-reboot25-team-24/locations/europe-west2/taxonomies/1749023867972816388'}
    
    for bq_table_id in vertex_pi_data:
        if bq_table_id.startswith("# This is a line used for comments"):
            print("Line Starts with # and will be skipped as it is a comment line")
            continue
        if bq_table_id in taxonomy_names:
            bq_col_tags = get_policy_tags(bq_table_id, taxonomy_names, gcp_project, gcp_location, vertex_pi_data.get(bq_table_id))
            args = '{"project_id": "%s", "dataset_id": "%s", "table_id": "%s", "tags": %s}' % (gcp_project, dataset_id, bq_table_id, bq_col_tags)
            print(args)
            bq_tag = dco.tag_bq_tbl(args)
            print(f"Tag on BigQuery Table %s" % (bq_table_id))
            for  i in  bq_tag.get("schema")["fields"]:
                if i.get("policyTags") == None:
                    print(i)