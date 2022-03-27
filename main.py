import os
from github import Github
import glob

def main():
    token = os.environ["INPUT_GITHUB_TOKEN"]
    cloverGlob = os.environ["INPUT_CLOVER"]
    junitGlob = os.environ["INPUT_JUNIT"]
    repository = os.environ["GITHUB_REPOSITORY"]
    commitSha = os.environ["GITHUB_SHA"]
    workspace = os.environ["RUNNER_WORKSPACE"]

    g = Github(token)

    for file in os.listdir(workspace):
        print(file)


if __name__ == "__main__":
    main()