import os
import markdown_builder
import publisher

def main():
    token = os.environ["INPUT_GITHUB_TOKEN"]
    cloverPath = os.environ["INPUT_CLOVER"]
    junitGlob = os.environ["INPUT_JUNIT"]
    repository = os.environ["GITHUB_REPOSITORY"]
    commitSha = os.environ["GITHUB_SHA"]
    workspace = os.environ["GITHUB_WORKSPACE"]

    codeUrl = "https://github.com/" + repository + "/blob/" + commitSha
    markdown = markdown_builder.buildMarkdown(codeUrl, workspace, cloverPath, junitGlob, commitSha)
    publisher.publish(markdown, token, commitSha, repository)

if __name__ == "__main__":
    main()