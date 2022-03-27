import xml.etree.ElementTree as ET
import os

def loadReport(path):
    tree = ET.parse(path)
    root = tree.getroot().find("testsuite")
    return TestMainSuite(root)

class TestMainSuite:
    def __init__(self, root):
        self.tests = int(root.attrib["tests"])
        self.assertions = int(root.attrib["assertions"])
        self.errors = int(root.attrib["errors"])
        self.warnings = int(root.attrib["warnings"])
        self.failures = int(root.attrib["failures"])
        self.skipped = int(root.attrib["skipped"])
        self.time = float(root.attrib["time"])
        self.name = root.attrib["name"]
        self.suites = []

        while root.find("testsuite") is not None and "file" not in root.find("testsuite").attrib:
            root = root.find("testsuite")

        paths = []
        for file in root.findall("testsuite"):
            paths.append(file.attrib["file"])
        commonPath = os.path.commonpath(paths)
        basePath = os.path.basename(commonPath)

        for suite in root.findall("testsuite"):
            fullpath = suite.attrib["file"]
            basename = os.path.basename(fullpath)
            dirname = os.path.dirname(fullpath)
            simpleDirname = dirname.replace(commonPath, basePath, 1)
            self.suites.append(TestFileSuite(suite, simpleDirname, basename))

class TestFileSuite:
    def __init__(self, root, dirname, basename):
        self.tests = int(root.attrib["tests"])
        self.assertions = int(root.attrib["assertions"])
        self.errors = int(root.attrib["errors"])
        self.warnings = int(root.attrib["warnings"])
        self.failures = int(root.attrib["failures"])
        self.skipped = int(root.attrib["skipped"])
        self.time = float(root.attrib["time"])
        self.name = root.attrib["name"]
        self.dirname = dirname
        self.basename = basename
