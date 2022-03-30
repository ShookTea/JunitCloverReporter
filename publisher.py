from typing import Generator
import github
from github.Repository import Repository
from github.PullRequest import PullRequest


def publish(markdown: str, token: str, commit: str, repo: str):
    print("Starting publishing for repo " + repo)
    g = github.Github(token)
    repo = g.get_repo(repo)
    for pull in iteratePullRequests(repo, commit):
        publishForPull(pull, markdown)


def publishForPull(pull: PullRequest, markdown: str):
    print("Publishing report for pull request #" + str(pull.number) + ", searching for comment to be updated...")
    tail = "\n\n###### Built by JUnitCloverPublisher"
    fullComment = markdown + tail
    commentToBeUpdated = findCommentToBeUpdated(pull, tail)
    if commentToBeUpdated is None:
        print("Publishing a new issue commit")
        pull.create_issue_comment(fullComment)
    else:
        print("Updating an existing issue commit")
        commentToBeUpdated.edit(fullComment)

def findCommentToBeUpdated(pull: PullRequest, tail: str):
    for comment in pull.get_issue_comments():

        validUser = comment.user.login == 'github-actions[bot]'
        validEnding = comment.body.endswith(tail)
        print("Comment by user \"" + comment.user.login + "\"; validUser = " + str(validUser) + "; validEnding = " + str(validEnding))
        if validUser and validEnding:
            return comment
    return None


def iteratePullRequests(repo: Repository, commit: str) -> Generator[PullRequest, None, None]:
    print("Search for pull request with head commit " + commit)
    for pull in repo.get_pulls(state="open"):
        print(pull.head.sha + " - PR #" + str(pull.number) + "\"" + pull.title + "\"")
        if pull.head.sha == commit:
            yield pull
    for pull in repo.get_pulls(state="closed"):
        print(pull.head.sha + " - PR #" + str(pull.number) + "\"" + pull.title + "\"")
        if pull.head.sha == commit:
            yield pull