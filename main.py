from flask import Flask, jsonify
import os
# import bigquery
# import github_actions

# Authenticate using an access token

app = Flask(__name__)

# Get latest templates


@app.route("/")
def hello_world():
    """Example Hello World route."""
    name = os.environ.get("NAME", "World")
    return f"Hello {name}!"

    # Get contents and write them to GCS if there are changes to the commit status

    # from GCS, pull the contents into the context window for evaluation

    # parse contents as needed

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))\
    
