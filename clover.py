import xml.etree.ElementTree as ET
import os

class CloverReport:
    def __init__(self, groups):
        self.groups = groups

class CloverFileGroup:
    def __init__(self, entries, dirname):
        self.entries = entries
        self.dirname = dirname

class CloverEntry:
    def __init__(self, commonPath, basePath, file):
        path = file.attrib["name"]
        self.basename = os.path.basename(path)
        dirname = os.path.dirname(path)
        self.simpleDirname = dirname.replace(commonPath, basePath, 1)

        metrics = file.find("metrics")
        self.methods = metrics.attrib["methods"]
        self.coveredMethods = metrics.attrib["coveredmethods"]
        self.statements = metrics.attrib["statements"]
        self.coveredStatements = metrics.attrib["coveredstatements"]
        self.lineBlocks = self.loadLineBlocks(file)

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
        entry = CloverEntry(commonPath, basePath, file)
        dirname = entry.simpleDirname
        if dirname not in entries:
            entries[dirname] = []
        entries[dirname].append(entry)

    groups = []
    for dirname in entries:
        groups.append(CloverFileGroup(entries[dirname], dirname))

    return CloverReport(groups)

if __name__ == "__main__":
    print(loadReport("/Users/shooktea/Projects/JunitCloverPublisher/artifacts/folder2/clover.xml"))