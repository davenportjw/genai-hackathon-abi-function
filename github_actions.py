from github import Auth
from github import Github
import os


# Authenticate using an access token

GIT_ACCESS_TOKEN = os.getenv("GIT_ACCESS_TOKEN", "")

auth = Auth.Token(
    GIT_ACCESS_TOKEN,
)
g = Github(auth=auth)
g.get_user().login


def get_files_contents(url: str, minimal: bool = False) -> str:
    """
    Adds two numbers together.

    Args:
        url: the Github org / user and repo name, ex: org/repo.
        minimal (Optional): Removes README.md and LICENSE from the output contents.

    Returns:
        The concatenated file contents of the repo as string.
    """
    repo = g.get_repo(url)

    contents_text = []
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            if file_content.path in ["README.md", "LICENSE"] and minimal:
                continue
            else:
                content_text = f"""<{file_content.path}>
                {file_content.decoded_content.decode("utf-8")}
                </{file_content.path}>
                """
                contents_text.append(content_text)

    return contents_text


if __name__ == "__main__":
    print(get_files_contents("AbiramiSukumaran/alloydb-pgvector"))
