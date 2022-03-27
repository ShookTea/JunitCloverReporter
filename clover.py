from __future__ import annotations
import xml.etree.ElementTree as ET
import os

class CloverReport:
    def __init__(self, groups: list[CloverFileGroup]):
        self.groups = groups
        self.groups.sort(key=lambda group: group.dirname)

    def toMarkdownTable(self, topFileUrl):
        return self.summary() + "\n<details><summary>Detailed coverage report</summary>" + self.buildTable(topFileUrl) + "</details>"

    def summary(self):
        methods = self.sumMethods()
        statements = self.sumStatements()
        methodPercent = "-"
        statementPercent = "-"
        if methods > 0:
            methodPercent = "{:.2f}".format(100 * self.sumCoveredMethods() / methods) + "%"
        if statements > 0:
            statementPercent = "{:.2f}".format(100 * self.sumCoveredStatements() / statements) + "%"

        return "### Testing coverage\n<b>Lines</b>: " + statementPercent + "\n<b>Methods:</b> " + methodPercent

    def buildTable(self, topFileUrl):
        table = "<table><thead><tr><th>File</th><th>Methods %</th><th>Lines %</th><th>Skipped lines</th></tr></thead><tbody>"
        for entry in self.groups:
            table += entry.buildTableGroup(topFileUrl)
        return table + "</tbody></table>"

    def sumMethods(self):
        methods = 0
        for entry in self.groups:
            methods += entry.sumMethods()
        return methods

    def sumCoveredMethods(self):
        coveredMethods = 0
        for entry in self.groups:
            coveredMethods += entry.sumCoveredMethods()
        return coveredMethods

    def sumStatements(self):
        statements = 0
        for entry in self.groups:
            statements += entry.sumStatements()
        return statements

    def sumCoveredStatements(self):
        coveredStatements = 0
        for entry in self.groups:
            coveredStatements += entry.sumCoveredStatements()
        return coveredStatements


class CloverFileGroup:
    def __init__(self, entries: list[CloverEntry], dirname):
        self.entries = entries
        self.entries.sort(key=lambda entry: entry.basename)
        self.dirname = dirname

    def buildTableGroup(self, topFileUrl):
        rows = "<tr><td colspan=4><b>" + self.dirname + "</b></td></tr>"
        for entry in self.entries:
            rows += entry.buildTableRow(topFileUrl)
        return rows

    def sumMethods(self):
        methods = 0
        for entry in self.entries:
            methods += entry.methods
        return methods

    def sumCoveredMethods(self):
        coveredMethods = 0
        for entry in self.entries:
            coveredMethods += entry.coveredMethods
        return coveredMethods

    def sumStatements(self):
        statements = 0
        for entry in self.entries:
            statements += entry.statements
        return statements

    def sumCoveredStatements(self):
        coveredStatements = 0
        for entry in self.entries:
            coveredStatements += entry.coveredStatements
        return coveredStatements

class CloverEntry:
    def __init__(self, commonPath, basePath, file):
        path = file.attrib["name"]
        self.basename = os.path.basename(path)
        dirname = os.path.dirname(path)
        self.simpleDirname = dirname.replace(commonPath, basePath, 1)

        metrics = file.find("metrics")
        self.methods = int(metrics.attrib["methods"])
        self.coveredMethods = int(metrics.attrib["coveredmethods"])
        self.statements = int(metrics.attrib["statements"])
        self.coveredStatements = int(metrics.attrib["coveredstatements"])
        self.lineBlocks = self.loadLineBlocks(file)

    def buildTableRow(self, topFileUrl):
        fileUrl = topFileUrl + "/" + self.simpleDirname + "/" + self.basename
        entry = "<tr><td colspan><a href=\"" + fileUrl + "\">" + self.basename + "</a></td>"

        if self.methods > 0:
            methodPercent = "{:.2f}".format(100 * self.coveredMethods / self.methods) + "%"
            entry += "<td><b>" + methodPercent + "</b><br/>(" + str(self.coveredMethods) + " of " + str(self.methods) + ")</td>"
        else:
            entry += "<td>-</td>"

        if self.statements > 0:
            statementPercent = "{:.2f}".format(100 * self.coveredStatements / self.statements) + "%"
            entry += "<td><b>" + statementPercent + "</b><br/>(" + str(self.coveredStatements) + " of " + str(self.statements) + ")</td>"
        else:
            entry += "<td>-</td>"

        return entry + self.buildLineBlocksCell(fileUrl) +  "</tr>"

    def buildLineBlocksCell(self, fileUrl):
        parts = []
        for lineBlock in self.lineBlocks:
            firstLine = lineBlock[0]
            lastLine = lineBlock[len(lineBlock) - 1]
            if firstLine == lastLine:
                url = fileUrl + "#L" + str(firstLine)
                text = str(firstLine)
                parts.append("<a href=\"" + url + "\">" + text + "</a>")
            else:
                url = fileUrl + "#L" + str(firstLine) + "-L" + str(lastLine)
                text = str(firstLine) + "-" + str(lastLine)
                parts.append("<a href=\"" + url + "\">" + text + "</a>")

        return "<td>" + ",".join(parts) + "</td>"

    def loadLineBlocks(self, file):
        uncoveredLines = []
        currentBlock = []
        previous = -1
        previousNonCovered = -1
        for line in file.findall("line"):
            currentLine = int(line.attrib["num"])
            if line.attrib["type"] == "stmt" and line.attrib["count"] == "0":
                if (previous == previousNonCovered):  # same block of code
                    currentBlock.append(currentLine)
                else:  # new block of code
                    if len(currentBlock) > 0:
                        uncoveredLines.append(currentBlock)
                    currentBlock = [currentLine]
                previousNonCovered = currentLine
            previous = currentLine

        if len(currentBlock) > 0:
            uncoveredLines.append(currentBlock)

        return uncoveredLines


def loadReport(path):
    tree = ET.parse(path)
    root = tree.getroot()
    paths = []
    for file in root.find("project").findall("file"):
        paths.append(file.attrib["name"])
    commonPath = os.path.commonpath(paths)
    basePath = os.path.basename(commonPath)

    entries = {}
    for file in root.find("project").findall("file"):
        if file.find("class") is None:
            continue
        entry = CloverEntry(commonPath, basePath, file)
        dirname = entry.simpleDirname
        if dirname not in entries:
            entries[dirname] = []
        entries[dirname].append(entry)

    groups = []
    for dirname in entries:
        groups.append(CloverFileGroup(entries[dirname], dirname))

    return CloverReport(groups)
