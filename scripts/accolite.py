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


# Get accolite install directory
def accoliteinstalldir():
    return os.path.dirname(sys.argv[0])


# Return possible accolite commands
def availablecommands():
    commands = []
    for cmd in os.listdir(accoliteinstalldir()):
        if cmd.startswith("accolite-"):
            commands.append(cmd[len("accolite-"):])
    return commands


# From an accolite commande to the path of its script
def scriptofcommand(cmd):
    return os.path.join(accoliteinstalldir(), "accolite-" + cmd)

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
            + "     return !runner.run( \"\", false );\n"
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


def pathsdefinitionsstring():
    pname = projectname()
    return ("##########################\n"
            + "# " + pname + " path\n"
            + "set( " + pname.upper() + "_PATH ${CMAKE_CURRENT_BINARY_DIR}/.. )\n"
            + "\n"
            + "##########################\n"
            + "# Src path\n"
            + "set( SRC_PATH ${" + pname.upper() + "_PATH}/" + relativedir("src") + " )\n"
            + "\n"
            + "##########################\n"
            + "# Examples path\n"
            + "set( EXAMPLES_PATH ${" + pname.upper() + "_PATH}/" + relativedir("examples") + " )\n"
            + "\n"
            + "##########################\n"
            + "# Tests path\n"
            + "set( TESTS_PATH ${" + pname.upper() + "_PATH}/" + relativedir("tests") + " )\n"
            + "\n"
            + "##########################\n"
            + "# Cmake configuration files path\n"
            + "set( CONFIGURATION_FILES_PATH ${" + pname.upper() + "_PATH}/" + relativedir("cmake") + " )\n"
            + "\n"
            + "##########################\n"
            + "# Cmake created files path\n"
            + "set( BUILD_PATH ${" + pname.upper() + "_PATH}/" + relativedir("build") + " )\n"
            + "\n"
            + "##########################\n"
            + "# Lib path\n"
            + "set( " + pname.upper() + "_LIB_PATH ${BUILD_PATH}/lib" + pname + " )\n"
            + "\n"
            + "##########################\n"
            + "# Executables files path\n"
            + "set( BIN_PATH ${" + pname.upper() + "_PATH}/" + relativedir("bin") + " )\n"
            + "\n"
            + "##########################\n"
            + "# .cmake module files path\n"
            + "set( MODULE_PATH ${CONFIGURATION_FILES_PATH}/Modules )\n"
            + "set( CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${MODULE_PATH} )\n")


def exampleslistsstring():
    return ("#################################################\n"
            + "# Examples\n"
            + "#################################################\n"
            + "\n"
            + "# Avoid policy warning\n"
            + "set( NO_POLICY_SCOPE ON )\n"
            + "\n"
            + "##########################\n"
            + "# Dependencies\n"
            + "\n"
            + "##########################\n"
            + "# Example files\n"
            + "file(\n"
            + "  GLOB_RECURSE\n"
            + "  example_sources\n"
            + "  ${EXAMPLES_PATH}/*.cpp\n"
            + "  )\n"
            + "\n"
            + "##########################\n"
            + "# Add examples\n"
            + "message( \"-- Adding examples\" )\n"
            + "foreach( example ${example_sources} )\n"
            + "  get_filename_component( example_exe ${example} NAME_WE)\n"
            + "  add_executable( ${example_exe} ${example} )\n"
            + "  target_link_libraries( ${example_exe} "
            + projectname().lower() + " )\n"
            + "  include( ExamplesLinks.cmake )\n"
            + "  message( \"--   ${example_exe} done\" )\n"
            + "endforeach( example ${example_sources} )\n")


def testconfigstring():
    return ("# Nothing to submit to Dart\n")


def dashboardstring():
    return ("##########################\n"
            + "# Include paths definitions\n"
            + "include( ${CMAKE_CURRENT_BINARY_DIR}/../cmake/PathsDefinitions.cmake )\n"
            + "\n"
            + "##########################\n"
            + "# We need valgrind\n"
            + "find_package(Valgrind)\n"
            + "if( VALGRIND_FOUND )\n"
            + "  set( CTEST_MEMORYCHECK_COMMAND ${VALGRIND_PROGRAM} )\n"
            + "  set( CTEST_MEMORYCHECK_SUPPRESSIONS_FILE ${CONFIGURATION_FILES_PATH}/valgrind.supp )\n"
            + "  set( CTEST_MEMORYCHECK_COMMAND_OPTIONS\n"
            + "    \"-q --tool=memcheck --leak-check=full --show-reachable=yes --workaround-gcc296-bugs=yes --num-callers=50\"\n"
            + "    )\n"
            + "endif( VALGRIND_FOUND )\n"
            + "\n"
            + "##########################\n"
            + "# Model analysis\n"
            + "set( MODEL \"analysis\" )\n"
            + "\n"
            + "##########################\n"
            + "# CTest properies\n"
            + "set( CTEST_SOURCE_DIRECTORY ${CONFIGURATION_FILES_PATH} )\n"
            + "set( CTEST_BINARY_DIRECTORY ${BUILD_PATH} )\n"
            + "\n"
            + "#########################\n"
            + "# Processing tests\n"
            + "ctest_start( ${MODEL} TRACK ${MODEL} )\n"
            + "\n"
            + "\n"
            + "## -- UPDATE\n"
            + "#ctest_update( SOURCE \"${CTEST_SOURCE_DIRECTORY}\" RETURN_VALUE res )\n"
            + "\n"
            + "## -- CONFIGURE\n"
            + "#ctest_configure( BUILD  \"${CTEST_BINARY_DIRECTORY}\" RETURN_VALUE res )\n"
            + "\n"
            + "## -- BUILD\n"
            + "#ctest_build( BUILD \"${CTEST_BINARY_DIRECTORY}\" RETURN_VALUE res)\n"
            +"\n"
            + "## -- TEST\n"
            + "#ctest_test( BUILD  \"${CTEST_BINARY_DIRECTORY}\" RETURN_VALUE res)\n"
            + "if ( CTEST_MEMORYCHECK_COMMAND )\n"
            + "  ctest_memcheck( BUILD  \"${CTEST_BINARY_DIRECTORY}\" RETURN_VALUE res )\n"
            + "endif( CTEST_MEMORYCHECK_COMMAND )\n"
            + "if ( CTEST_COVERAGE_COMMAND )\n"
            + "  ctest_coverage( BUILD  \"${CTEST_BINARY_DIRECTORY}\" RETURN_VALUE res )\n"
            + "endif( CTEST_COVERAGE_COMMAND )\n"
            + "\n"
            + "## -- SUBMIT\n"
            + "#ctest_submit(                                              RETURN_VALUE res)\n")


def cmakelistsstring():
    pname = projectname();
    return ("cmake_minimum_required(VERSION 2.6)\n"
            + "\n"
            + "##########################\n"
            + "# Project name\n"
            + "project( " + pname + " )\n"
            + "\n"
            + "##########################\n"
            + "# Include paths definitions\n"
            + "include( PathsDefinitions.cmake )\n"
            + "\n"
            + "# Add a sensible build type default and warning because empty means no optimization and no debug info.\n"
            + "if( NOT CMAKE_BUILD_TYPE )\n"
            + "  message( \"WARNING: CMAKE_BUILD_TYPE is not defined!\n\"\n"
            + "    \"         Defaulting to CMAKE_BUILD_TYPE=RelWithDebInfo.\"\n"
            + "    \" Use ccmake to set a proper value.\" )\n"
            + "  set( CMAKE_BUILD_TYPE RelWithDebInfo CACHE STRING\n"
            + "    \"Choose the type of build, options are:\"\n"
            + "    \" None Debug Release RelWithDebInfo MinSizeRel.\" FORCE )\n"
            + "endif( NOT CMAKE_BUILD_TYPE )\n"
            + "\n"
            + "set( CMAKE_CXX_FLAGS \"-Wall -Werror\" )\n"
            + "\n"
            + "# Put executables in bin\n"
            + "set( EXECUTABLE_OUTPUT_PATH ${BIN_PATH} )\n"
            + "\n"

            + "##########################\n"
            + "# Dependencies\n"
            + "include( Dependencies.cmake )\n"
            + "\n"
            + "\n"
            + "##########################\n"
            + "# Src files\n"
            + "file (\n"
            + "  GLOB_RECURSE\n"
            + "  lib_headers\n"
            + "  ${SRC_PATH}/*.h\n"
            + "  ${SRC_PATH}/*.hpp\n"
            + "  )\n"
            + "file (\n"
            + "  GLOB_RECURSE\n"
            + "  lib_defs\n"
            + "  ${SRC_PATH}/*.def\n"
            + "  )\n"
            + "file (\n"
            + "  GLOB_RECURSE\n"
            + "  lib_cpp\n"
            + "  ${SRC_PATH}/*.c\n"
            + "  ${SRC_PATH}/*.cpp\n"
            + "  )\n"
+ "include_directories ( ${SRC_PATH} )\n"
            + "\n"
            + "##########################\n"
            + "# Library\n"
+ "add_library( " + pname.lower() + " SHARED\n"
            + "  ${lib_headers}\n"
            + "  ${lib_cpp}\n"
+ "  )\n"
            + "target_link_libraries( " + pname.lower() + " )\n"
            + "\n"
            + "\n"
            + "##########################\n"
            + "# Library installation\n"
            + "set( CMAKE_INSTALL_PREFIX ${" + pname.upper() + "_LIB_PATH} )\n"
            + "foreach( header ${lib_headers} ${lib_defs} )\n"
            + "  # To preserve dyrectory hierarchy...\n"
            + "  string( REGEX REPLACE ${SRC_PATH}/ \"\" header_no_path ${header} )\n"
            + "  string( REGEX MATCH \"(.*)[/\\\\]\" header_dir ${header_no_path} )\n"
            + "  install( FILES ${header} DESTINATION include/${header_dir} )\n"
            + "endforeach( header ${lib_headers} ${lib_defs} )\n"
            + "install( TARGETS " + pname.lower() + " LIBRARY DESTINATION lib )\n"
            + "\n"
            + "\n"
            + "##########################\n"
            + "# Examples\n"
            + "include( CMakeExamplesLists.cmake )\n"
            + "\n"
            + "\n"
            + "##########################\n"
            + "# Tests\n"
            + "include( CMakeTestsLists.cmake )\n")


def testslistsstring():
    return ("##############################################\n"
            + "# Tests\n"
            + "#################################################\n"
            + "\n"
            + "# Avoid policy warning\n"
            + "set( NO_POLICY_SCOPE ON )\n"
            + "\n"
            + "##########################\n"
            + "# Dependencies\n"
            + "find_package(CppUnit REQUIRED)\n"
            + "\n"
            + "##########################\n"
            + "# Test files\n"
            + "file(\n"
            + "  GLOB_RECURSE\n"
            + "  test_sources\n"
            + "  ${TESTS_PATH}/*.cpp\n"
            + "  )\n"
            + "\n"
            + "##########################\n"
            + "# Add tests\n"
            + "\n"
            + "message( \"-- Adding tests\" )\n"
            + "foreach( test ${test_sources} )\n"
            + "  #string(REGEX REPLACE .cpp \"\" test_exe ${test} )\n"
            + "  get_filename_component( test_exe ${test} NAME_WE)\n"
            + "  add_executable( ${test_exe} ${test} )\n"
            + "  target_link_libraries( ${test_exe} " + projectname().lower() + " )\n"
            + "  target_link_libraries( ${test_exe} ${CppUnit_LIBRARIES} )\n"
            + "  include( TestsLinks.cmake )\n"
            + "  add_test( ${test_exe} ${BIN_PATH}/${test_exe} )\n"
            + "  message( \"--   ${test_exe} done\" )\n"
            + "endforeach( test ${test_sources} )\n"
            + "\n"
            + "##########################\n"
            + "# Include CTestConfig.cmake\n"
            + "include( CTest )\n")
