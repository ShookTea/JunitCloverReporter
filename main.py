import os
from github import Github
import glob

def main():
    token = os.environ["INPUT_GITHUB_TOKEN"]
    cloverPath = os.environ["INPUT_CLOVER"]
    junitGlob = os.environ["INPUT_JUNIT"]
    repository = os.environ["GITHUB_REPOSITORY"]
    commitSha = os.environ["GITHUB_SHA"]
    workspace = os.environ["GITHUB_WORKSPACE"]

    g = Github(token)

    cloverPath = os.path.join(workspace, cloverPath)
    junitGlob = os.path.join(workspace, junitGlob)

    with open(cloverPath, 'r') as f:
        print("Clover content:")
        print("============")
        print(f.readlines())
        print("============")

    for file in glob.glob(junitGlob, recursive=True):
        with open(file, 'r') as f:
            print("junit content in file " + file + ":")
            print("----------------------------------")
            print(f.readlines())
            print("----------------------------------")

if __name__ == "__main__":
    main()