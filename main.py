import os
from github import Github
import glob
import clover
import junit
import junit_builder

def main():
    token = os.environ["INPUT_GITHUB_TOKEN"]
    cloverPath = os.environ["INPUT_CLOVER"]
    junitGlob = os.environ["INPUT_JUNIT"]
    repository = os.environ["GITHUB_REPOSITORY"]
    commitSha = os.environ["GITHUB_SHA"]
    workspace = os.environ["GITHUB_WORKSPACE"]

    g = Github(token)

    codeUrl = "https://github.com/" + repository + "/blob/" + commitSha

    cloverPath = os.path.join(workspace, cloverPath)
    cloverReport = clover.loadReport(cloverPath)
    cloverMarkdown = cloverReport.toMarkdownTable(codeUrl)

    junitGlob = os.path.join(workspace, junitGlob)
    junitReports = {}
    for file in glob.glob(junitGlob, recursive=True):
        junitReports[file] = junit.loadReport(file)
    junitMarkdown = junit_builder.buildMarkdown(junitReports)
    print(junitMarkdown)


if __name__ == "__main__":
    main()