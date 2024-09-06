from flask import Flask, jsonify, request
import os
import bigquery
import vertex
import github_actions
from datetime import datetime


app = Flask(__name__)

# TODO: make this work with BigQuery remote function syntax
@app.route("/", methods=['POST'])
def run_evaluation():

    replies = []
    request_json = request.get_json()
    calls = request_json['calls']
    
    code_prompt = bigquery.get_prompts()[0]['prompt']

    for call in calls:
        url = call[0]
        replies.append(url)

        # Placeholder
        code = "import vertexai"
        # try:
        #     github_actions.get_content(url)
        # except:
        #     return jsonify({"code": 403, 'data': {"errorMessage": "Received but not expected that the argument 0 be null"}})

        # Evaluate contents
        response = vertex.evaluate_code(code_prompt,code)

        replies.append(response)

    return jsonify( { "replies" :  replies } )

    # from GCS, pull the contents into the context window for evaluation

    # parse contents as needed

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))\
    
