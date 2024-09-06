from flask import Flask, jsonify, request
import os
import bigquery
import vertex
import github_actions


app = Flask(__name__)


@app.route("/", methods=["POST"])
def run_evaluation():

    replies = []
    request_json = request.get_json()
    calls = request_json["calls"]

    code_prompt = bigquery.get_prompts()[0]["prompt"]

    for call in calls:
        url_list = call[0].split(",")

        github_urls = []

        for url in url_list:
            if "github.com" in url:
                github_urls.append(url.split("github.com/", 1)[1])

        code_list = []
        for url in github_urls:
            try:
                code_list.append(github_actions.get_files_contents(url))
            except:
                return jsonify(
                    {
                        "code": 403,
                        "data": {
                            "errorMessage": "Received but not expected that the argument 0 be null"
                        },
                    }
                )

        # print(code_list)

        code = "\n".join(code_list)

        token_count = vertex.count_tokens(code_prompt, code)
        print(f"Token count: {token_count}")

        if token_count < 2000000:
            pass
        else:
            code = github_actions.get_files_contents(url, True)

        # TODO: if minimal and tokens still >2M, then truncate past 2M and log

        response = vertex.evaluate_code(code_prompt, code)

        replies.append(response)

    print({"replies": replies})
    return jsonify({"replies": replies})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
