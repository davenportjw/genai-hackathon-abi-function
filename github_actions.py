from github import Auth
from github import Github
import os

from google.cloud import storage

client = storage.Client()

# Authenticate using an access token

GIT_ACCESS_TOKEN = os.getenv("GIT_ACCESS_TOKEN","")
GCS_BUCKET = os.getenv("GCS_BUCKET","gen-ai-weekly")

auth = Auth.Token(GIT_ACCESS_TOKEN)
g = Github(auth=auth)
g.get_user().login

storage_client = storage.Client()

def get_latest_status(org: str, repo : str) -> dict:
    config_status = {}

    # Get a specific repository
    repo = g.get_repo(f"{org}/{repo}")

    config_status["repo_name"] = repo.full_name

    branches = repo.get_branches()

    for branch in branches:
        if branch.name in ["main","master"]:
            config_status["main_branch"] = branch.name
            config_status["latest_commit_sha"] = branch.commit.sha

    return(config_status)


def get_file_content_from_gcs(bucket_name, file_path):

  bucket = storage_client.bucket(bucket_name)
  blob = bucket.blob(file_path)

  if blob.exists():
    content = blob.download_as_string().decode("utf-8")  # Decode bytes to string
    return content
  else:
    print(f"File not found: gs://{bucket_name}/{file_path}")
    return None

def write_to_gcs(bucket_name, file_path, content):
    """Writes content to a file in Google Cloud Storage.

    Args:
        bucket_name: The name of the GCS bucket.
        file_path: The path to the file within the bucket.
        content: The content to write to the file.
    """

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_path)
    blob.upload_from_string(content)

    print(f"Content written to gs://{bucket_name}/{file_path}")

def check_config(config_status: dict) -> bool:
    bucket = storage_client.get_bucket(GCS_BUCKET)
    try:
        current_config = get_file_content_from_gcs(GCS_BUCKET, f"{config_status["repo_name"]}/_config.json")
        if current_config["latest_commit_sha"] == config_status["latest_commit_sha"]:
            return True
        else:
            return False
    except:
        write_to_gcs(GCS_BUCKET, f"{config_status["repo_name"]}/_config.json", config_status)
        return False

def get_files_contents(config_status: dict) -> None:
    repo = g.get_repo(f"{config_status["repo_name"]}")

    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            print(file_content.decoded_content.decode("utf-8"))

if __name__ == "__main__":
    config_status = get_latest_status("davenportjw","gen-ai-weekly")
    action = check_config(config_status)
    if action:
        get_files_contents(config_status)