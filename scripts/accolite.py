#!/usr/bin/env python

import sys
import os.path
import xml.dom.minidom


# Levenstein score function
def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b."
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
def levenshteinbestmatch(expr, possibles):
    minExp = possibles[0]
    min = levenshtein(expr, minExp)
    for e in possibles:
        score = levenshtein(expr,e)
        if score < min:
            min = score
            minExp = e
    return minExp


# Get working project dir
def workingdir():
    prevpath = ""
    currentpath = os.path.abspath(os.path.curdir)
    while not ( os.path.isdir(os.path.join(currentpath, ".accolite")) or currentpath == prevpath ):
        prevpath = currentpath
        currentpath = os.path.abspath(os.path.join(currentpath, os.path.pardir))
    if currentpath == prevpath and not os.path.isdir(os.path.join(currentpath, ".accolite")):
        return ""
    return currentpath


# Get cmake dir
def relativecmakedir():
    configxml = xml.dom.minidom.parse(os.path.join(workingdir(),
                                                   ".accolite","config.xml"))
    return configxml.getElementsByTagName("cmakedir")[0].firstChild.data

# Get cmake dir absolute path
def abscmakedir():
    return os.path.join(workingdir(), relativecmakedir())


# Get build dir
def relativebuilddir():
    configxml = xml.dom.minidom.parse(os.path.join(workingdir(),
                                                   ".accolite","config.xml"))
    return configxml.getElementsByTagName("builddir")[0].firstChild.data

# Get build dir absolute path
def absbuilddir():
    return os.path.join(workingdir(), relativebuilddir())


# Get bin dir
def relativebindir():
    configxml = xml.dom.minidom.parse(os.path.join(workingdir(),
                                                   ".accolite","config.xml"))
    return configxml.getElementsByTagName("bindir")[0].firstChild.data

# Get bin dir absolute path
def absbindir():
    return os.path.join(workingdir(), relativebindir())


# Get tests dir
def relativetestsdir():
    configxml = xml.dom.minidom.parse(os.path.join(workingdir(),
                                                   ".accolite","config.xml"))
    return configxml.getElementsByTagName("testsdir")[0].firstChild.data

# Get tests dir absolute path
def abstestsdir():
    return os.path.join(workingdir(), relativetestsdir())


# Get examples dir
def relativeexamplesdir():
    configxml = xml.dom.minidom.parse(os.path.join(workingdir(),
                                                   ".accolite","config.xml"))
    return configxml.getElementsByTagName("examplesdir")[0].firstChild.data

# Get examples dir absolute path
def absexamplesdir():
    return os.path.join(workingdir(), relativeexamplesdir())


# Get src dir
def relativesrcdir():
    configxml = xml.dom.minidom.parse(os.path.join(workingdir(),
                                                   ".accolite","config.xml"))
    return configxml.getElementsByTagName("srcdir")[0].firstChild.data

# Get src dir absolute path
def abssrcdir():
    return os.path.join(workingdir(), relativesrcdir())


# Get doc dir
def relativedocdir():
    configxml = xml.dom.minidom.parse(os.path.join(workingdir(),
                                                   ".accolite","config.xml"))
    return configxml.getElementsByTagName("docdir")[0].firstChild.data

# Get doc dir absolute path
def absdocdir():
    return os.path.join(workingdir(), relativedocdir())


# Get tmp dir
def relativetmpdir():
    configxml = xml.dom.minidom.parse(os.path.join(workingdir(),
                                                   ".accolite","config.xml"))
    return configxml.getElementsByTagName("tmpdir")[0].firstChild.data

# Get tmp dir absolute path
def abstmpdir():
    return os.path.join(workingdir(), relativetmpdir())


# Return possible accolite commands
def availablecommands():
    commands = []
    for path in os.path.expandvars("$PATH").split(":"):
        for cmd in os.listdir(path):
            if cmd.startswith("accolite-"):
                commands.append(cmd[len("accolite-"):])
    return commands


# Create a minidom xml default config file
def defaultxml(projectname):
    configxml = xml.dom.minidom.getDOMImplementation().createDocument(None, "accoliteconfig", None)
    rootnode = configxml.childNodes[0]
    # Cmake dir
    newnode = configxml.createElement("cmakedir")
    newnode.appendChild(configxml.createTextNode("cmake"))
    rootnode.appendChild(newnode)
    # Build dir
    newnode = configxml.createElement("builddir")
    newnode.appendChild(configxml.createTextNode("build"))
    rootnode.appendChild(newnode)
    # Bin dir
    newnode = configxml.createElement("bindir")
    newnode.appendChild(configxml.createTextNode("bin"))
    rootnode.appendChild(newnode)
    # Tmp dir
    newnode = configxml.createElement("tmpdir")
    newnode.appendChild(configxml.createTextNode("tmp"))
    rootnode.appendChild(newnode)
    # Src dir
    newnode = configxml.createElement("srcdir")
    newnode.appendChild(configxml.createTextNode("src"))
    rootnode.appendChild(newnode)
    # Tests dir
    newnode = configxml.createElement("testsdir")
    newnode.appendChild(configxml.createTextNode("tests"))
    rootnode.appendChild(newnode)
    # Examles dir
    newnode = configxml.createElement("examplesdir")
    newnode.appendChild(configxml.createTextNode("examples"))
    rootnode.appendChild(newnode)
    # Doc dir
    newnode = configxml.createElement("docdir")
    newnode.appendChild(configxml.createTextNode("doc"))
    rootnode.appendChild(newnode)
    return configxml
    
