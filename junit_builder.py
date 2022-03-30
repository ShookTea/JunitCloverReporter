import os
from pathlib import Path
import junit

def buildMarkdown(units):
    print("Merging " + str(len(units)) + " JUnit report(s)")
    summary = buildSummary(units)
    details = buildDetailedErrorReport(units)
    markdown = "### Test results\n" + summary
    if details != "":
        markdown += "\n<details><summary>Errors list</summary>" + details + "</details>"
    return markdown

def buildDetailedErrorReport(units):
    common = getCommonPath(units)
    html = "<table><thead><tr><th>Type</th><th>Test</th><th>Target</th><th>Test name</th></tr></thead><tbody>"
    errorReportRows = ""
    for path in units:
        fileNameWithoutExt = Path(path).stem
        groupName = os.path.dirname(path)[(len(common) + 1):]
        result: junit.TestMainSuite = units[path]
        errorReportRows += buildDetailedErrorReportForMainSuite(result, fileNameWithoutExt, groupName)

    if errorReportRows == "":
        return ""

    return html + errorReportRows + "</tbody></table>"

def buildDetailedErrorReportForMainSuite(suite: junit.TestMainSuite, test, target):
    if suite.errors + suite.warnings + suite.failures + suite.skipped == 0:
        return ""
    result = ""
    for filesuite in suite.suites:
        result += buildDetailedErrorReportForFileSuite(filesuite, test, target)
    return result

def buildDetailedErrorReportForFileSuite(suite: junit.TestFileSuite, test, target):
    if suite.errors + suite.warnings + suite.failures + suite.skipped == 0:
        return ""
    return buildDetailedErrorReportForSuiteRoot(suite.root, test, target)

def buildDetailedErrorReportForSuiteRoot(suite, test, target):
    if suite.attrib["errors"] + suite.attrib["warnings"] + suite.attrib["failures"] + suite.attrib["skipped"] == "0000":
        return ""
    result = ""
    name = suite.attrib["name"]
    for child in suite.findall("testsuite"):
        result += buildDetailedErrorReportForSuiteRoot(child, test, target)
    for child in suite.findall("testcase"):
        result += buildDetailedErrorReportForCaseRoot(child, name, test, target)
    return result

def buildDetailedErrorReportForCaseRoot(case, testName, test, target):
    name = testName + "<br/>" + case.attrib["name"]
    result = ""
    for failure in case.findall("failure"):
        result += buildDetailerErrorReportForFailure(failure, "failure :bangbang:", name, test, target)
    for error in case.findall("error"):
        result += buildDetailerErrorReportForFailure(error, "error :exclamation:", name, test, target)
    for skipped in case.findall("skipped"):
        result += buildDetailerErrorReportForFailure(skipped, "skipped :zzz:", name, test, target)
    return result

def buildDetailerErrorReportForFailure(node, type, testName, test, target):
    html = "<tr><td>" + type + "</td><td>" + test + "</td><td>" + target + "</td><td>" + testName + "</td></tr>"
    text = node.text.strip()
    if text != "":
        summary = text.split("\n")[1]
        shortSummary = summary[0:50]
        if shortSummary != summary:
            shortSummary += "..."
        text = "<details><summary>" + shortSummary + "</summary>\n\n```\n" + text + "\n```\n</details>"
    html += "<tr><td colspan=4>" + text + "</td></tr>"
    return html

def buildSummary(units):
    common = getCommonPath(units)
    html = "<table><thead><tr><th>Test</th><th>Target</th>"
    html += "<th>Tests</th>"
    html += "<th>Assertions</th>"
    html += "<th>Errors</th>"
    html += "<th>Warnings</th>"
    html += "<th>Failures</th>"
    html += "<th>Skipped</th>"
    html += "<th>Time</th>"
    html += "</tr></thead><tbody>"

    for path in units:
        fileNameWithoutExt = Path(path).stem
        groupName = os.path.dirname(path)[(len(common) + 1):]
        result: junit.TestMainSuite = units[path]
        html += "<tr><td>" + fileNameWithoutExt + "</td><td>" + groupName + "</td>"
        html += makeCell(result.tests, "")
        html += makeCell(result.assertions, "")
        html += makeCell(result.errors, ":exclamation:")
        html += makeCell(result.warnings, ":gray_exclamation:")
        html += makeCell(result.failures, ":bangbang:")
        html += makeCell(result.skipped, ":zzz:")
        html += makeCell(result.time, " s :clock10:")

    return html + "</tbody></table>"

def makeCell(value, emoji):
    if value > 0:
        return "<td>" + str(value) + " " + emoji + "</td>"
    else:
        return "<td>0</td>"

def getCommonPath(units):
    paths = []
    for path in units:
        paths.append(path)
    return os.path.commonpath(paths)