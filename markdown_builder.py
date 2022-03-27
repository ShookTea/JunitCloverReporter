import os
import glob
import clover
import junit
import junit_builder

def buildMarkdown(codeUrl, workspace, cloverPath, junitGlob):
    cloverPath = os.path.join(workspace, cloverPath)
    cloverReport = clover.loadReport(cloverPath)
    cloverMarkdown = cloverReport.toMarkdownTable(codeUrl)

    junitGlob = os.path.join(workspace, junitGlob)
    junitReports = {}
    for file in glob.glob(junitGlob, recursive=True):
        junitReports[file] = junit.loadReport(file)
    junitMarkdown = junit_builder.buildMarkdown(junitReports)

    return junitMarkdown + "\n\n" + cloverMarkdown
