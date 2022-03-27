import os
from github import Github

def main():
    #token = os.environ["INPUT_GITHUB_TOKEN"]
    #g = Github(token)
    for key in os.environ:
        print(key + " = " + os.environ[key])
    #print("Hello from image!")


if __name__ == "__main__":
    main()