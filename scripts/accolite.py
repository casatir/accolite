#!/usr/bin/env python

import sys
import os.path
import xml.dom.minidom


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
def levenshteinbestmatch(expr, possibles):
    minExp = possibles[0]
    min = levenshtein(expr, minExp)
    for e in possibles:
        score = levenshtein(expr,e)
        if score < min:
            min = score
            minExp = e
    return minExp


# Return possible accolite commands
def availablecommands():
    commands = []
    for path in os.path.expandvars("$PATH").split(":"):
        for cmd in os.listdir(path):
            if cmd.startswith("accolite-"):
                commands.append(cmd[len("accolite-"):])
    return commands


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


# Get the relative path of a project dir
def relativedir(directory):
    configxml = xml.dom.minidom.parse(os.path.join(workingdir(),
                                                   ".accolite","config.xml"))
    return configxml.getElementsByTagName(directory + "dir")[0].firstChild.data

# Get the absolute path of a project dir
def absdir(directory):
    return os.path.join(workingdir(), relativedir(directory))


# Get the relative path of a project dir
def projectname():
    configxml = xml.dom.minidom.parse(os.path.join(workingdir(),
                                                   ".accolite","config.xml"))
    return configxml.getElementsByTagName("projectname")[0].firstChild.data


# Create a minidom xml default config file
def defaultxml(projectname):
    configxml = xml.dom.minidom.getDOMImplementation().createDocument(None, "accoliteconfig", None)
    rootnode = configxml.childNodes[0]
    # Project name
    newnode = configxml.createElement("projectname")
    newnode.appendChild(configxml.createTextNode(projectname))
    rootnode.appendChild(newnode)
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
    
def testrunnerstring():
    return ("#include <cppunit/extensions/TestFactoryRegistry.h>\n"
            + "#include <cppunit/TextTestRunner.h>\n"
            + "int main( int argc, char **argv)\n"
            + "{\n"
            + "     CppUnit::TextTestRunner runner;\n"
            + "     CppUnit::TestFactoryRegistry &registry = CppUnit::TestFactoryRegistry::getRegistry();\n"
            + "     runner.addTest( registry.makeTest() );\n"
            + "     return !runner.run( "", false );\n"
            + "}\n")


def examplesstring():
    projectnameupper = projectname().upper()
    return ("#include <cppunit/extensions/HelperMacros.h>\n"
            + "\n"
            + "#define " + projectnameupper + "_TEST_NAME ExampleTest\n"
            + "\n"
            + "class " + projectnameupper + "_TEST_NAME : public CppUnit::TestFixture\n"
            + "{\n"
            + "     \n"
            + "     CPPUNIT_TEST_SUITE( " + projectnameupper + "_TEST_NAME );\n"
            + "     CPPUNIT_TEST( test );\n"
            + "     CPPUNIT_TEST_SUITE_END();\n"
            + "     \n"
            + "public:\n"
            + "     inline void setUp() {\n"
            + "     }\n"
            + "     \n"
            + "     inline void tearDown() {\n"
            + "     }\n"
            + "     inline void test() {\n"
            + "	  CPPUNIT_ASSERT( true );\n"
            + "     }\n"
            + "     \n"
            + "};\n"
            + "\n"
            + "CPPUNIT_TEST_SUITE_REGISTRATION( " + projectnameupper + "_TEST_NAME );\n"
            + "\n"
            + "#include \"TestRunner.h\"\n")
