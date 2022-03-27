import os
from github import Github
import markdown_builder

def main():
    token = os.environ["INPUT_GITHUB_TOKEN"]
    cloverPath = os.environ["INPUT_CLOVER"]
    junitGlob = os.environ["INPUT_JUNIT"]
    repository = os.environ["GITHUB_REPOSITORY"]
    commitSha = os.environ["GITHUB_SHA"]
    workspace = os.environ["GITHUB_WORKSPACE"]

    g = Github(token)
    codeUrl = "https://github.com/" + repository + "/blob/" + commitSha
    markdown = markdown_builder.buildMarkdown(codeUrl, workspace, cloverPath, junitGlob)
    print(markdown)


if __name__ == "__main__":
    main()