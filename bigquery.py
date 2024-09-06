from google.cloud import bigquery
import os

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "abis-345004")
LOCATION = os.getenv("REGION", "us-central1")

client = bigquery.Client(location=LOCATION)


def query_bigquery_to_dict(query):
    """Queries BigQuery and returns the results as a list of dictionaries.

    Args:
        query: The SQL query to execute.

    Returns:
        A list of dictionaries, where each dictionary represents a row in the result set.
    """

    query_job = client.query(query)
    results = query_job.result()

    # Convert the results to a list of dictionaries.
    rows = []
    for row in results:
        row_dict = {}
        for key in row.keys():
            row_dict[key] = row[key]
        rows.append(row_dict)

    return rows


def get_prompts() -> dict:
    query = """
    select prompt_id, prompt
    from  {PROJECT_ID}.hackathon_grader.prompts 
    where prompt_id = 'p_github';
    """

    return query_bigquery_to_dict(query.format(PROJECT_ID=PROJECT_ID))


# Example usage:
if __name__ == "__main__":
    print(get_prompts())
