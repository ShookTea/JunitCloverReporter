import os
from pathlib import Path
import junit

def buildMarkdown(units):
    return buildSummary(units)

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