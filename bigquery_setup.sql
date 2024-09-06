--Cloud RUn setup
- deploy cloud run container
- attach secret for GITHUB_ACCESS_TOKEN
- grant cloud run account access to the secret
- grant cloud run account access to BigQuery user
- grant bigquery connection cloud run invoker


CREATE OR REPLACE FUNCTION abis-345004.hackathon_grader.remote_add(x INT64, y INT64) RETURNS INT64
REMOTE WITH CONNECTION abis-345004.us-central1.hackathon_grader_functions
OPTIONS (
  endpoint = 'https://genai-hackathon-abi-function-uxu5wi2jpa-uc.a.run.app'
)