import vertexai
import re
from google.cloud import bigquery
from vertexai.preview.generative_models import GenerativeModel

def get_schema_for_policy_tag(project_id, dataset_id):
    # Step 1: Initialize BigQuery client
    bq_client = bigquery.Client()

    # Step 2: Query the data column
    query = f"""
    SELECT table_schema, table_name, column_name
    FROM `{project_id}.{dataset_id}.INFORMATION_SCHEMA.COLUMNS`
    """
    query_job = bq_client.query(query)

    results = [
        {
            "table_schema": row["table_schema"],
            "table_name": row["table_name"],
            "column_name": row["column_name"]
        }
        for row in query_job
    ]
    return results

def get_prompt_from_vertexai(results, project_id, location_id):
    # Step 3: Initialize Vertex AI
    vertexai.init(project=project_id, location=location_id)

    # Step 4: Prepare prompt for Gemini
    prompt = f"""
Here is a sample of data from a table. Please identify which columns contain PII (Personally Identifiable Information).
Data sample:
{results}
"""
    return prompt

def get_prompt_response(prompt):
    # Step 5: Send to Gemini
    model = GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    # Step 6: Print response
    print("PII Columns Identified:")
    #print(response.text)
    return response.text

def get_output_dict(response):
    output_dict = {}
    for line in response.strip().splitlines():
        line = line.strip()
        if line.startswith("*"):
            #print("print 1", line)

            # Extract table name using regex
            table_match = re.search(r"\*\s*\*\*(.*?) table:", line)
            if not table_match:
                continue  # Skip if table name not found
            table_name = table_match.group(1).strip()

            # Extract all column names inside backticks
            columns = re.findall(r"`(.*?)`", line)

            if columns:
                output_dict[table_name] = columns

    print("output_dict", output_dict)
    return output_dict

def get_pi_info(project_id, dataset_id, location_id):
    info_schema_result = get_schema_for_policy_tag(project_id, dataset_id)
    prompt_data = get_prompt_from_vertexai(info_schema_result, project_id, location_id)
    prompt_responce = get_prompt_response(prompt_data)
    pi_info_data = get_output_dict(prompt_responce)
    return pi_info_data