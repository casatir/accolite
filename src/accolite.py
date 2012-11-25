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
import os.path
import xml.dom.minidom
import re

# Levenstein score function
def levenshtein(a,b):
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n
        
    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)
            
    return current[n]


# Best possibility for an expr in a list
def levenshteinBestMatch(expr, possibles):
    minExp = possibles[0]
    min = levenshtein(expr, minExp)
    for e in possibles:
        score = levenshtein(expr,e)
        if score < min:
            min = score
            minExp = e
    return minExp


# Get accolite install directory
def installDir():
    return os.path.abspath(os.path.dirname(sys.argv[0]))


# Return possible accolite commands
def availableCommands():
    commands = []
    for cmd in os.listdir(installDir()):
        if cmd.startswith("accolite-"):
            commands.append(cmd[len("accolite-"):])
    return commands


# From an accolite commande to the path of its script
def scriptOfCommand(cmd):
    return os.path.join(installDir(), "accolite-" + cmd)


# Get working project dir
def workingDir():
    prevpath = ""
    currentpath = os.path.abspath(os.path.curdir)
    while not ( os.path.isdir(os.path.join(currentpath, ".accolite")) or currentpath == prevpath ):
        prevpath = currentpath
        currentpath = os.path.abspath(os.path.join(currentpath, os.path.pardir))
    if currentpath == prevpath and not os.path.isdir(os.path.join(currentpath, ".accolite")):
        return ""
    return currentpath


# Get the relative path of a project dir
def relativedir(directory):
    configxml = xml.dom.minidom.parse(os.path.join(workingDir(),
                                                   ".accolite","config.xml"))
    return configxml.getElementsByTagName(directory + "dir")[0].firstChild.data

# Get the absolute path of a project dir
def absdir(directory):
    return os.path.join(workingDir(), relativedir(directory))


# Get the project name
def projectName():
    configxml = xml.dom.minidom.parse(os.path.join(workingDir(),
                                                   ".accolite","config.xml"))
    return configxml.getElementsByTagName("projectname")[0].firstChild.data


# Get the project type
def projectType():
    configxml = xml.dom.minidom.parse(os.path.join(workingDir(),
                                                   ".accolite","config.xml"))
    elements = configxml.getElementsByTagName("projecttype")
    if elements.length > 0:
        return elements[0].firstChild.data
    else:
        return "cpp"


# Get the project name replacing non alphanumeric characters by sub
def projectNameAlphaNum(sub):
    listAlNum = []
    for c in projectName():
        if c.isalnum():
            listAlNum.append(c)
        else:
            listAlNum.append(sub)
    return "".join(listAlNum)


# Create a minidom xml default config file
def defaultxml(projectname,projecttype):
    configxml = xml.dom.minidom.getDOMImplementation().createDocument(None, "accoliteconfig", None)
    rootnode = configxml.childNodes[0]
    # Project name
    newnode = configxml.createElement("projectname")
    newnode.appendChild(configxml.createTextNode(projectname))
    rootnode.appendChild(newnode)
    # Project type
    newnode = configxml.createElement("projecttype")
    newnode.appendChild(configxml.createTextNode(projecttype))
    rootnode.appendChild(newnode)
    # Directories
    for directory in ["cmake","build","bin","tmp","src","tests","examples","doc"]:
        newnode = configxml.createElement(directory + "dir")
        newnode.appendChild(configxml.createTextNode(directory))
        rootnode.appendChild(newnode)
    return configxml
    

def stringFile(filename):
    filePath = os.path.abspath(os.path.join(installDir(), "AccoliteFiles/"+projectType(), filename))
    fileToRead = open(filePath, "r")
    fileString = fileToRead.read()
    fileToRead.close()
    pname = projectNameAlphaNum("_")
    fileString = re.sub("<ACCOLITE_PROJECT_NAME_LOWER>", pname.lower(), fileString)
    fileString = re.sub("<ACCOLITE_PROJECT_NAME_UPPER>", pname.upper(), fileString)
    fileString = re.sub("<ACCOLITE_PROJECT_NAME>", pname, fileString)
    return fileString
