import os
from typing import Generator
import github
from github.Repository import Repository
from github.PullRequest import PullRequest
import markdown_builder


def iteratePullRequests(repo: Repository, commit: str) -> Generator[PullRequest, None, None]:
    for pull in repo.get_pulls(state="open"):
        if pull.head.sha == commit:
            yield pull
    for pull in repo.get_pulls(state="closed"):
        if pull.head.sha == commit:
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
    tail = "\n\n###### Built by JUnitCloverPublisher"
    fullComment = markdown + tail
    g = github.Github(token)
    current_user_id = g.get_user().id
    repo = g.get_repo(repository)
    for pull in iteratePullRequests(repo, commitSha):
        print(pull)
        print("------")
        for comment in pull.get_issue_comments():
            if comment.user.id == current_user_id and comment.body.endswith(tail):
                print(comment)
        print("======")

if __name__ == "__main__":
    main()