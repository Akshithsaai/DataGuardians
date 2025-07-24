import argparse
import os
import sys
import datacatalog as dco
from policy_masking import create_policy_masking_method
from vertex_api_handler import get_pi_info
from data_catalogue_bq_table import bq_policy_tagging

# Open the Parameter File and Read the Lines
def taxonomy(gcp_project, gcp_location, dataset_id):

    vertex_pi_data = get_pi_info(project_id, dataset_id, gcp_location)
    print(vertex_pi_data)
    #* Read All Lines, Skipping the First Line
    for taxonomy_name in vertex_pi_data:
        #* Building Args to Get Taxonomies in Data Project
        arguments = '{"project_id": "%s", "location": "%s"}' % (gcp_project, gcp_location)
        #arguments = {
        #"project_id": gcp_project,
        #"location": gcp_location
        #}
        #* Fetch the Taxonomies
        print(f"[INFO]: Fetching Taxonomies in Project {gcp_project} and location {gcp_location}")
        project_taxonomies = dco.list_taxonomies(arguments)
        #* Print The Taxonomies Fetched after making the call
        print("The following Taxonomies were listed: %s" % (project_taxonomies))

        #* Check if the Taxonomy Exists - If does not exist and operation is create - Create the Taxonomy
        taxo_names = [d["displayName"] for d in project_taxonomies["taxonomies"]] if project_taxonomies else []
        print("2")
        if not project_taxonomies or taxonomy_name not in taxo_names:
            print(f"Taxonomy {taxonomy_name} does not exists, creating....")
            activated_policy_types = "FINE_GRAINED_ACCESS_CONTROL"
            arguments = '{"project_id": "%s", "location": "%s", "display_name": "%s", "activatedPolicyTypes": "%s", "description": ""}' % (
                gcp_project, gcp_location, taxonomy_name, activated_policy_types)
            taxonomy_data = dco.create_taxonomy(arguments)
            taxonomy_id = taxonomy_data.get('name')
            print(f"[INFO]: Taxonomy {taxonomy_id} created")
        else:
            project_taxonomy = dco.list_taxonomies(arguments)
            taxonomy_id = [d["name"] for d in project_taxonomy["taxonomies"] if d["displayName"] == taxonomy_name][0]
            taxonomy_name = [d["displayName"] for d in project_taxonomy["taxonomies"] if d["displayName"] == taxonomy_name][0]
            print(f"[INFO]: Taxonomy {taxonomy_name} exists")

        #* Check if the Action is to Delete Taxonomy
        arguments_1 = '{"parent": "%s"}' % (taxonomy_id)
        policy_tags_list = dco.list_policy_tags(arguments_1)
        print("tag list" , policy_tags_list)
        polic_data = [d["displayName"] for d in policy_tags_list["policyTags"]] if policy_tags_list else []
        for policy_tag in vertex_pi_data[taxonomy_name]:
            if policy_tag not in polic_data:
                print(f"Policy Tag {policy_tag} does not exists in Taxonomy {taxonomy_name} creating....")
                arguments_2 = '{"parent": "%s", "display_name": "%s", "description": "", "parentPolicyTag": ""}' % (taxonomy_id,policy_tag)
                print("tax id" ,taxonomy_id)
                policy_tag_id = dco.create_policy_tag(arguments_2)
                print(f"[INFO]: Policy Tag {policy_tag_id} created")
                policy_tag_mak_id  = policy_tag_id["name"] if policy_tag_id["displayName"] == policy_tag else None
                create_policy_masking_method(project_id, location, policy_tag_mak_id)
                print("mask id ", policy_tag_mak_id)
                #args_policy_tag_id = dco.default_masking_policy_tag(args_policy_tag_id)
                print(f"[INFO]: updated masking for {policy_tag_id}")

    bq_policy_tagging(gcp_project, gcp_location, vertex_pi_data,dataset_id)

if __name__ == "__main__":

    # Configure Required Arguments
    parser = argparse.ArgumentParser(description='Data Masking')
    parser.add_argument('--gcp_bigquery_dataset', required=True)
    parser.add_argument('--project_id', required=True)
    parser.add_argument('--location', required=True)
    #parser.add_argument('--gcp_bigquery_project', required=True)

    # parser.add_argument('--taxonomy_file', required=True, type=validate_txt_file,
    # help='comma separated file in .txt format')

    # Parse the provided arguments to access
    args = parser.parse_args()
    dataset = args.gcp_bigquery_dataset
    project_id = args.project_id
    location = args.location
    # big_query_project = args.gcp_bigquery_project
    # taxonomy_file = args.taxonomy_file

    taxonomy(project_id, location, dataset)