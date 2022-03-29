import os
from typing import Generator
import github
from github.Repository import Repository
from github.PullRequest import PullRequest
import markdown_builder


def iteratePullRequests(repo: Repository) -> Generator[PullRequest, None, None]:
    for pull in repo.get_pulls(state="open"):
        yield pull
    for pull in repo.get_pulls(state="closed"):
        yield pull

def main():
    token = os.environ["INPUT_GITHUB_TOKEN"]
    cloverPath = os.environ["INPUT_CLOVER"]
    junitGlob = os.environ["INPUT_JUNIT"]
    repository = os.environ["GITHUB_REPOSITORY"]
    commitSha = os.environ["GITHUB_SHA"]
    workspace = os.environ["GITHUB_WORKSPACE"]

    codeUrl = "https://github.com/" + repository + "/blob/" + commitSha
    markdown = markdown_builder.buildMarkdown(codeUrl, workspace, cloverPath, junitGlob)

    g = github.Github(token)
    repo = g.get_repo(repository)
    for pull in iteratePullRequests(repo):
        print(pull)

if __name__ == "__main__":
    main()