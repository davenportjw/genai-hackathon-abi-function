from google.cloud import bigquery

def query_bigquery_to_dict(query):
    """Queries BigQuery and returns the results as a list of dictionaries.

    Args:
        query: The SQL query to execute.

    Returns:
        A list of dictionaries, where each dictionary represents a row in the result set.
    """

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # Execute the query.
    query_job = client.query(query)

    # Get the results.
    results = query_job.result()

    # Convert the results to a list of dictionaries.
    rows = []
    for row in results:
        row_dict = {}
        for key in row.keys():
            row_dict[key] = row[key]
        rows.append(row_dict)

    return rows

# Example usage:
if __name__ == "__main__":
    # Replace with your BigQuery project ID and table ID.
    project_id = "your-project-id"
    table_id = "your_dataset.your_table"

    # Example query.
    query = f"""
        SELECT *
        FROM `{project_id}.{table_id}`
        LIMIT 10
    """

    # Execute the query and print the results.
    results = query_bigquery_to_dict(query)
    print(results)
