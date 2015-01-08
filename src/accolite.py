#
# Copyright (c) 2012 Casati Romain
# All rights reserved.
#
# This file is part of Accolite.
#
# Accolite is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Accolite is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Accolite.  If not, see <http://www.gnu.org/licenses/>


import sys
import os
import xml.dom.minidom
import re

# Get the directory where accolite is installed
def installDir():
    return os.path.abspath(os.path.dirname(sys.argv[0]))

# Get the location of the current working directory
# or "" if we are not in an accolite project
def workingDir():
    def parDir(path):
        return os.path.abspath(os.path.join(path, os.path.pardir))
    def isAccoliteDir(path):
        return os.path.isdir(os.path.join(path, ".accolite"))
    def isRoot(path):
        return path == parDir(path)
    currentPath = os.path.abspath(os.path.curdir)
    while not ( isAccoliteDir(currentPath) or isRoot(currentPath) ):
        currentPath = parDir(currentPath)
    if isAccoliteDir(currentPath):
        return currentPath.decode('utf-8')
    return ''

# Is current directory inside an accolite project
def isInsideAccoliteProject():
    return workingDir() != ""

# Available commands in iDir
def availableCommandsInDir(iDir):
    commands = []
    for cmd in os.listdir(iDir):
        if cmd.startswith("accolite-"):
            commands.append(cmd[len("accolite-"):])
    return commands

# Available accolite commands
def availableCommands():
    return availableCommandsInDir(installDir())

# From an accolite commande to the path of its script
def scriptOfCommand(cmd):
    return os.path.join(installDir(), "accolite-" + cmd)

# Accolite project type
class AccoliteType:
    # Availables types
    C, CPP = range(2)
    # Conversions
    @staticmethod
    def fromTypeToStr(t):
        if t == AccoliteType.C:
            return "c"
        else:
            return "cpp"
    @staticmethod
    def fromStrToType(s):
        if s.lower() == "c":
            return AccoliteType.C
        else:
            return AccoliteType.CPP

class AccoliteProject:
    class AccoliteDir:
        def __init__(self, defaultName, realName):
            self.defaultName = defaultName
            self.realName = realName

    def __init__(self, projectName = "AccoliteProject", projectType = "cpp"):
        if isInsideAccoliteProject():
            self.initFromXML()
        else:
            self.initFromArgs(projectName, projectType)

    def initFromXML(self):
        # wdir
        self._workingDir = workingDir()
        configxml = xml.dom.minidom.parse(self.xmlLocation())
        # name
        self._name = configxml.getElementsByTagName("projectname")[0].firstChild.data
        # type
        self._type = AccoliteType.CPP
        elements = configxml.getElementsByTagName("projecttype")
        if elements.length > 0:
            self._type = AccoliteType.fromStrToType(elements[0].firstChild.data)
        # dirs
        self._dirs = []
        for d in self.relativeDirs():
            self._dirs.append(AccoliteProject.AccoliteDir(d, configxml.getElementsByTagName(\
                        d + "dir")[0].firstChild.data))

    def initFromArgs(self, projectName, projectType):
        # wdir
        self._workingDir = os.path.abspath(os.path.curdir)
        aDir = self.accoliteDir()
        if not os.path.isdir(aDir):
            os.makedirs(aDir)
        # name
        self._name = projectName
        # type
        self._type = AccoliteType.fromStrToType(projectType)
        # dirs
        self._dirs = []
        for d in self.relativeMandatoryDirs():
            self._dirs.append(AccoliteProject.AccoliteDir(d,d))
            dirPath = os.path.abspath(os.path.join(self.workingDir(), d))
            if not os.path.isdir(dirPath):
                os.makedirs(dirPath)
        for d in self.relativeCleanedDirs():
            self._dirs.append(AccoliteProject.AccoliteDir(d,d))
            
        # xml data
        configxmlfile = open(os.path.join(aDir, "config.xml"), 'w')
        self.toXML().writexml(configxmlfile)
        configxmlfile.close()

    # Get working project dir
    def workingDir(self):
        return self._workingDir

    def xmlLocation(self):
        return os.path.join(self.accoliteDir(), "config.xml")

    def accoliteDir(self):
        return os.path.abspath(os.path.join(self.workingDir(), ".accolite"))

    # Get the relative path of a project dir
    def relativeDir(self, directory):
        for d in self._dirs:
            if d.defaultName == directory:
                return d.realName
        return ""
    
    @staticmethod
    def relativeDirs():
        res = AccoliteProject.relativeMandatoryDirs()
        res.extend(AccoliteProject.relativeCleanedDirs())
        return res
    @staticmethod
    def relativeMandatoryDirs():
        return ["cmake","src","tests","examples","doc"]
    @staticmethod
    def relativeCleanedDirs():
        return ["bin","build","tmp"]

    # Get the absolute path of a project dir
    def absDir(self, directory):
        return os.path.join(self.workingDir(), self.relativeDir(directory))

    # Absolute paths to mandatory directorys
    def mandatoryAbsDirs(self):
        return map(self.absDir, self.relativeMandatoryDirs())

    # Get the project name
    def projectName(self):
        return self._name

    # Get the project type
    def projectType(self):
        return self._type

    # Get a pre/post scipt given by the cmd arg
    def prepostScript(self, cmd):
        return os.path.join(self.absDir('cmake'), 'PrePostScripts', cmd)

    # Get the project name replacing non alphanumeric characters by sub
    def projectNameAlphaNum(self, sub):
        listAlNum = []
        for c in self.projectName():
            if c.isalnum():
                listAlNum.append(c)
            else:
                listAlNum.append(sub)
        return "".join(listAlNum)

    # Create a minidom xml config file
    def toXML(self):
        configxml = xml.dom.minidom.getDOMImplementation().createDocument(None, "accoliteconfig", None)
        rootnode = configxml.childNodes[0]
        # Project name
        newnode = configxml.createElement("projectname")
        newnode.appendChild(configxml.createTextNode(self.projectName()))
        rootnode.appendChild(newnode)
        # Project type
        newnode = configxml.createElement("projecttype")
        newnode.appendChild(configxml.createTextNode(AccoliteType.fromTypeToStr(self.projectType())))
        rootnode.appendChild(newnode)
        # Directories
        for d in self._dirs:
            newnode = configxml.createElement(d.defaultName + "dir")
            newnode.appendChild(configxml.createTextNode(d.realName))
            rootnode.appendChild(newnode)
        return configxml
    
    # Convert a project file to a string with substitution
    def fileToString(self,fileName):
        filePath = os.path.join(installDir(), "AccoliteFiles/" \
                                    + AccoliteType.fromTypeToStr(self.projectType()), fileName)
        fileToRead = open(filePath, "r")
        fileString = fileToRead.read()
        fileToRead.close()
        pName = self.projectNameAlphaNum("_")
        fileString = re.sub("<ACCOLITE_PROJECT_NAME_LOWER>", pName.lower(), fileString)
        fileString = re.sub("<ACCOLITE_PROJECT_NAME_UPPER>", pName.upper(), fileString)
        fileString = re.sub("<ACCOLITE_PROJECT_NAME>", pName, fileString)
        return fileString

    def copyAccoliteFiles(self,dirName,erase):
        proprietaryPath = os.path.join(installDir(), "AccoliteFiles/",
                                       AccoliteType.fromTypeToStr(self.projectType()), dirName)
        for dirname, dirnames, filenames in os.walk(proprietaryPath):
            for f in filenames + [d for d in dirnames
                                  if os.path.islink(os.path.join(dirname, d))]:
                accoliteFilePath = os.path.join(dirname,f)
                pathList = accoliteFilePath[len(proprietaryPath)+1:].split('/')
                pathList[0] = self.absDir(pathList[0])
                filePath = "/".join(pathList)
                dirPath = os.path.dirname(filePath)
                if not os.path.isdir(dirPath):
                    os.makedirs(dirPath)
                if erase or not (erase or os.path.isfile(filePath)):
                    if not os.path.isfile(accoliteFilePath) and os.path.islink(accoliteFilePath):
                        if os.path.islink(filePath):
                            os.remove(filePath)
                        os.symlink(os.readlink(accoliteFilePath), filePath)
                    else:
                        permission = os.stat(accoliteFilePath).st_mode
                        with os.fdopen(os.open(filePath, os.O_WRONLY | os.O_CREAT,
                                               permission), 'w') as handle:
                            handle.truncate()
                            handle.write(self.fileToString(accoliteFilePath))

    def copyProprietaryFiles(self):
        self.copyAccoliteFiles("proprietary", True)

    def copyUserFiles(self):
        self.copyAccoliteFiles("user", False)
