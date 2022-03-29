from typing import Generator
import github
from github.Repository import Repository
from github.PullRequest import PullRequest


def publish(markdown: str, token: str, commit: str, repo: str):
    g = github.Github(token)
    repo = g.get_repo(repo)
    for pull in iteratePullRequests(repo, commit):
        publishForPull(pull, markdown)


def publishForPull(pull: PullRequest, markdown: str):
    tail = "\n\n###### Built by JUnitCloverPublisher"
    fullComment = markdown + tail
    commentToBeUpdated = findCommentToBeUpdated(pull, tail)
    if commentToBeUpdated is None:
        pull.create_issue_comment(fullComment)
    else:
        commentToBeUpdated.edit(fullComment)

def findCommentToBeUpdated(pull: PullRequest, tail: str):
    for comment in pull.get_issue_comments():
        if comment.user.login == 'github-actions[bot]' and comment.body.endswith(tail):
            return comment
    return None


def iteratePullRequests(repo: Repository, commit: str) -> Generator[PullRequest, None, None]:
    for pull in repo.get_pulls(state="open"):
        if pull.head.sha == commit:
            yield pull
    for pull in repo.get_pulls(state="closed"):
        if pull.head.sha == commit:
            yield pull