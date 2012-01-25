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
    for directory in ["cmake","build","bin","tmp","src","tests","examples","doc"]:
        newnode = configxml.createElement(directory + "dir")
        newnode.appendChild(configxml.createTextNode(directory))
        rootnode.appendChild(newnode)
    return configxml
    

def stringfile(filename):
    pname = projectname()
    pnameupper = pname.upper()
    pnamelower = pname.lower()
    if filename == "TestRunner.h":
        return ("#include <cppunit/extensions/TestFactoryRegistry.h>\n"
                + "#include <cppunit/TextTestRunner.h>\n"
                + "int main( int argc, char **argv)\n"
                + "{\n"
                + "     CppUnit::TextTestRunner runner;\n"
                + "     CppUnit::TestFactoryRegistry &registry = CppUnit::TestFactoryRegistry::getRegistry();\n"
                + "     runner.addTest( registry.makeTest() );\n"
                + "     return !runner.run( \"\", false );\n"
                + "}\n")
    elif filename == "ExampleTest.cpp":
        return ("#include <cppunit/extensions/HelperMacros.h>\n"
                + "\n"
                + "#define " + pnameupper + "_TEST_NAME ExampleTest\n"
                + "\n"
                + "class " + pnameupper + "_TEST_NAME : public CppUnit::TestFixture\n"
                + "{\n"
                + "     \n"
                + "     CPPUNIT_TEST_SUITE( " + pnameupper + "_TEST_NAME );\n"
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
                + "CPPUNIT_TEST_SUITE_REGISTRATION( " + pnameupper + "_TEST_NAME );\n"
                + "\n"
                + "#include \"TestRunner.h\"\n")
    elif filename == "valgrind.supp":
        return "\n"
    elif filename == "PathsDefinitions.cmake":
        return ("##########################\n"
                + "# " + pname + " path\n"
                + "set( " + pnameupper + "_PATH ${CMAKE_CURRENT_BINARY_DIR}/.. )\n"
                + "\n"
                + "##########################\n"
                + "# Src path\n"
                + "set( SRC_PATH ${" + pnameupper + "_PATH}/" + relativedir("src") + " )\n"
                + "\n"
                + "##########################\n"
                + "# Examples path\n"
                + "set( EXAMPLES_PATH ${" + pnameupper + "_PATH}/" + relativedir("examples") + " )\n"
                + "\n"
                + "##########################\n"
                + "# Tests path\n"
                + "set( TESTS_PATH ${" + pnameupper + "_PATH}/" + relativedir("tests") + " )\n"
                + "\n"
                + "##########################\n"
                + "# Cmake configuration files path\n"
                + "set( CONFIGURATION_FILES_PATH ${" + pnameupper + "_PATH}/" + relativedir("cmake") + " )\n"
                + "\n"
                + "##########################\n"
                + "# Cmake created files path\n"
                + "set( BUILD_PATH ${" + pnameupper + "_PATH}/" + relativedir("build") + " )\n"
                + "\n"
                + "##########################\n"
                + "# Lib path\n"
                + "set( " + pnameupper + "_LIB_PATH ${BUILD_PATH}/lib" + pname + " )\n"
                + "\n"
                + "##########################\n"
                + "# Executables files path\n"
                + "set( BIN_PATH ${" + pnameupper + "_PATH}/" + relativedir("bin") + " )\n"
                + "\n"
                + "##########################\n"
                + "# .cmake module files path\n"
                + "set( MODULE_PATH ${CONFIGURATION_FILES_PATH}/Modules )\n"
                + "set( CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${MODULE_PATH} )\n")
    elif filename == "ExamplesLinks.cmake":
        return "\n"
    elif filename == "CMakeExamplesLists.cmake":
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
                + pnamelower + " )\n"
                + "  include( ExamplesLinks.cmake )\n"
                + "  message( \"--   ${example_exe} done\" )\n"
                + "endforeach( example ${example_sources} )\n")
    elif filename == "CTestConfig.cmake":
        return ("# Nothing to submit to Dart\n")
    elif filename == "CTestDashboard.cmake":
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
    elif filename == "CMakeLists.txt":
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
                + "add_library( " + pnamelower + " SHARED\n"
                + "  ${lib_headers}\n"
                + "  ${lib_cpp}\n"
                + "  )\n"
                + "target_link_libraries( " + pnamelower + " ${" + pnameupper + "_LIB_DEPENDENCIES} )\n"
                + "\n"
                + "\n"
                + "##########################\n"
                + "# Library installation\n"
                + "set( CMAKE_INSTALL_PREFIX ${" + pnameupper + "_LIB_PATH} )\n"
                + "foreach( header ${lib_headers} ${lib_defs} )\n"
                + "  # To preserve dyrectory hierarchy...\n"
                + "  string( REGEX REPLACE ${SRC_PATH}/ \"\" header_no_path ${header} )\n"
                + "  string( REGEX MATCH \"(.*)[/\\\\]\" header_dir ${header_no_path} )\n"
                + "  install( FILES ${header} DESTINATION include/${header_dir} )\n"
                + "endforeach( header ${lib_headers} ${lib_defs} )\n"
                + "install( TARGETS " + pnamelower + " LIBRARY DESTINATION lib )\n"
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
    elif filename == "CMakeTestsLists.cmake":
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
                + "  target_link_libraries( ${test_exe} " + pnamelower + " )\n"
                + "  target_link_libraries( ${test_exe} ${CppUnit_LIBRARIES} )\n"
                + "  include( TestsLinks.cmake )\n"
                + "  add_test( ${test_exe} ${" + pnameupper
                + "_CMD_TEST_OPTION} ${BIN_PATH}/${test_exe} )\n"
                + "  message( \"--   ${test_exe} done\" )\n"
                + "endforeach( test ${test_sources} )\n"
                + "\n"
                + "##########################\n"
                + "# Include CTestConfig.cmake\n"
                + "include( CTest )\n")
    elif filename == "TestsLinks.cmake":
        return "\n"
    elif filename == "Dependencies.cmake":
        return "\n"
    elif filename == "FindCppUnit.cmake":
        return ("#-------------------------------------------------------------------\n"
                + "#-------------------------------------------------------------------\n"
                + "#\n"
                + "# - Try to find CppUnit\n"
                + "# Once done, this will define\n"
                + "#\n"
                + "# CppUnit_FOUND - system has CppUnit\n"
                + "# CppUnit_INCLUDE_DIRS - the CppUnit include directories\n"
                + "# CppUnit_LIBRARIES - link these to use CppUnit\n"
                + "\n"
                + "include(FindPkgMacros)\n"
                + "findpkg_begin(CppUnit)\n"
                + "\n"
                + "# Get path, convert backslashes as ${ENV_${var}}\n"
                + "getenv_path(CPPUNIT_HOME)\n"
                + "\n"
                + "# construct search paths\n"
                + "set(CppUnit_PREFIX_PATH ${CPPUNIT_HOME} ${ENV_CPPUNIT_HOME})\n"
                + "create_search_paths(CppUnit)\n"
                + "# redo search if prefix path changed\n"
                + "clear_if_changed(CppUnit_PREFIX_PATH\n"
                + "CppUnit_LIBRARY_FWK\n"
                + "CppUnit_LIBRARY_REL\n"
                + "CppUnit_LIBRARY_DBG\n"
                + "CppUnit_INCLUDE_DIR\n"
                + ")\n"
                + "\n"
                + "set(CppUnit_LIBRARY_NAMES cppunit)\n"
                + "get_debug_names(CppUnit_LIBRARY_NAMES)\n"
                + "\n"
                + "use_pkgconfig(CppUnit_PKGC cppunit)\n"
                + "\n"
                + "findpkg_framework(CppUnit)\n"
                + "\n"
                + "find_path(CppUnit_INCLUDE_DIR NAMES cppunit/Test.h HINTS ${CppUnit_INC_SEARCH_PATH} ${CppUnit_PKGC_INCLUDE_DIRS})\n"
                + "find_library(CppUnit_LIBRARY_REL NAMES ${CppUnit_LIBRARY_NAMES} HINTS ${CppUnit_LIB_SEARCH_PATH} ${CppUnit_PKGC_LIBRARY_DIRS})\n"
                + "find_library(CppUnit_LIBRARY_DBG NAMES ${CppUnit_LIBRARY_NAMES_DBG} HINTS ${CppUnit_LIB_SEARCH_PATH} ${CppUnit_PKGC_LIBRARY_DIRS})\n"
                + "make_library_set(CppUnit_LIBRARY)\n"
                + "\n"
                + "findpkg_finish(CppUnit)\n")
    elif filename == "FindValgrind.cmake":
        return ("# Find Valgrind.\n"
                + "#\n"
                + "# This module defines:\n"
                + "#### VALGRIND_INCLUDE_DIR, where to find valgrind/memcheck.h, etc.\n"
                + "# VALGRIND_PROGRAM, the valgrind executable.\n"
                + "# VALGRIND_FOUND, If false, do not try to use valgrind.\n"
                + "#\n"
                + "# If you have valgrind installed in a non-standard place, you can define\n"
                + "# VALGRIND_PREFIX to tell cmake where it is.\n"
                + "\n"
                + "message(STATUS \"Valgrind Prefix: ${VALGRIND_PREFIX}\")\n"
                + "\n"
                + "#find_path(VALGRIND_INCLUDE_DIR memcheck.h\n"
                + "#/usr/include /usr/include/valgrind /usr/local/include /usr/local/include/valgrind\n"
                + "#${VALGRIND_PREFIX}/include ${VALGRIND_PREFIX}/include/valgrind)\n"
                + "find_program(VALGRIND_PROGRAM NAMES valgrind PATH /usr/bin /usr/local/bin ${VALGRIND_PREFIX}/bin)\n"
                + "\n"
                + "include( FindPackageHandleStandardArgs )\n"
                + "\n"
                + "find_package_handle_standard_args(VALGRIND DEFAULT_MSG\n"
                + "#VALGRIND_INCLUDE_DIR\n"
                + "VALGRIND_PROGRAM)\n"
                + "\n"
                + "#mark_as_advanced(VALGRIND_INCLUDE_DIR VALGRIND_PROGRAM)\n"
                + "mark_as_advanced(VALGRIND_PROGRAM)\n")
    elif filename == "FindPkgMacros.cmake":
        return ("#-------------------------------------------------------------------\n"
                + "#-------------------------------------------------------------------\n"
                + "\n"
                + "##################################################################\n"
                + "# Provides some common functionality for the FindPackage modules\n"
                + "##################################################################\n"
                + "\n"
                + "# Begin processing of package\n"
                + "macro(findpkg_begin PREFIX)\n"
                + "  if (NOT ${PREFIX}_FIND_QUIETLY)\n"
                + "    message(STATUS \"Looking for ${PREFIX}...\")\n"
                + "  endif ()\n"
                + "endmacro(findpkg_begin)\n"
                + "\n"
                + "# Display a status message unless FIND_QUIETLY is set\n"
                + "macro(pkg_message PREFIX)\n"
                + "  if (NOT ${PREFIX}_FIND_QUIETLY)\n"
                + "    message(STATUS ${ARGN})\n"
                + "  endif ()\n"
                + "endmacro(pkg_message)\n"
                + "\n"
                + "# Get environment variable, define it as ENV_$var and make sure backslashes are converted to forward slashes\n"
                + "macro(getenv_path VAR)\n"
                + "   set(ENV_${VAR} $ENV{${VAR}})\n"
                + "   # replace won't work if var is blank\n"
                + "   if (ENV_${VAR})\n"
                + "     string( REGEX REPLACE \"\\\\\\\\\" \"/\" ENV_${VAR} ${ENV_${VAR}} )\n"
                + "   endif ()\n"
                + "endmacro(getenv_path)\n"
                + "\n"
                + "# Construct search paths for includes and libraries from a PREFIX_PATH\n"
                + "macro(create_search_paths PREFIX)\n"
                + "  foreach(dir ${${PREFIX}_PREFIX_PATH})\n"
                + "    set(${PREFIX}_INC_SEARCH_PATH ${${PREFIX}_INC_SEARCH_PATH}\n"
                + "      ${dir}/include ${dir}/include/${PREFIX} ${dir}/Headers)\n"
                + "    set(${PREFIX}_LIB_SEARCH_PATH ${${PREFIX}_LIB_SEARCH_PATH}\n"
                + "      ${dir}/lib ${dir}/lib/${PREFIX} ${dir}/Libs)\n"
                + "    set(${PREFIX}_BIN_SEARCH_PATH ${${PREFIX}_BIN_SEARCH_PATH}\n"
                + "      ${dir}/bin)\n"
                + "  endforeach(dir)\n"
                + "  set(${PREFIX}_FRAMEWORK_SEARCH_PATH ${${PREFIX}_PREFIX_PATH})\n"
                + "endmacro(create_search_paths)\n"
                + "\n"
                + "# clear cache variables if a certain variable changed\n"
                + "macro(clear_if_changed TESTVAR)\n"
                + "  # test against internal check variable\n"
                + "  if (NOT \"${${TESTVAR}}\" STREQUAL \"${${TESTVAR}_INT_CHECK}\")\n"
                + "    message(STATUS \"${TESTVAR} changed.\")\n"
                + "    foreach(var ${ARGN})\n"
                + "      set(${var} \"NOTFOUND\" CACHE STRING \"x\" FORCE)\n"
                + "    endforeach(var)\n"
                + "  endif ()\n"
                + "  set(${TESTVAR}_INT_CHECK ${${TESTVAR}} CACHE INTERNAL \"x\" FORCE)\n"
                + "endmacro(clear_if_changed)\n"
                +"\n"
                + "# Try to get some hints from pkg-config, if available\n"
                + "macro(use_pkgconfig PREFIX PKGNAME)\n"
                + "  find_package(PkgConfig)\n"
                + "  if (PKG_CONFIG_FOUND)\n"
                + "    pkg_check_modules(${PREFIX} ${PKGNAME})\n"
                + "  endif ()\n"
                + "endmacro (use_pkgconfig)\n"
                + "\n"
                + "# Couple a set of release AND debug libraries (or frameworks)\n"
                + "macro(make_library_set PREFIX)\n"
                + "  if (${PREFIX}_FWK)\n"
                + "    set(${PREFIX} ${${PREFIX}_FWK})\n"
                + "  elseif (${PREFIX}_REL AND ${PREFIX}_DBG)\n"
                + "    set(${PREFIX} optimized ${${PREFIX}_REL} debug ${${PREFIX}_DBG})\n"
                + "  elseif (${PREFIX}_REL)\n"
                + "    set(${PREFIX} ${${PREFIX}_REL})\n"
                + "  elseif (${PREFIX}_DBG)\n"
                + "    set(${PREFIX} ${${PREFIX}_DBG})\n"
                + "  endif ()\n"
                + "endmacro(make_library_set)\n"
                + "\n"
                + "# Generate debug names from given release names\n"
                + "macro(get_debug_names PREFIX)\n"
                + "  foreach(i ${${PREFIX}})\n"
                + "    set(${PREFIX}_DBG ${${PREFIX}_DBG} ${i}d ${i}D ${i}_d ${i}_D ${i}_debug ${i})\n"
                + "  endforeach(i)\n"
                + "endmacro(get_debug_names)\n"
                + "\n"
                + "# Add the parent dir from DIR to VAR \n"
                + "macro(add_parent_dir VAR DIR)\n"
                + "  get_filename_component(${DIR}_TEMP \"${${DIR}}/..\" ABSOLUTE)\n"
                + "  set(${VAR} ${${VAR}} ${${DIR}_TEMP})\n"
                + "endmacro(add_parent_dir)\n"
                + "\n"
                + "# Do the final processing for the package find.\n"
                + "macro(findpkg_finish PREFIX)\n"
                + "  # skip if already processed during this run\n"
                + "  if (NOT ${PREFIX}_FOUND)\n"
                + "    if (${PREFIX}_INCLUDE_DIR AND ${PREFIX}_LIBRARY)\n"
                + "      set(${PREFIX}_FOUND TRUE)\n"
                + "      set(${PREFIX}_INCLUDE_DIRS ${${PREFIX}_INCLUDE_DIR})\n"
                + "      set(${PREFIX}_LIBRARIES ${${PREFIX}_LIBRARY})\n"
                + "      if (NOT ${PREFIX}_FIND_QUIETLY)\n"
                + "        message(STATUS \"Found ${PREFIX}: ${${PREFIX}_LIBRARIES}\")\n"
                + "      endif ()\n"
                + "    else ()\n"
                + "      if (NOT ${PREFIX}_FIND_QUIETLY)\n"
                + "        message(STATUS \"Could not locate ${PREFIX}\")\n"
                + "      endif ()\n"
                + "      if (${PREFIX}_FIND_REQUIRED)\n"
                + "        message(FATAL_ERROR \"Required library ${PREFIX} not found! Install the library (including dev packages) and try again. If the library is already installed, set the missing variables manually in cmake.\")\n"
                + "      endif ()\n"
                + "    endif ()\n"
                + "\n"
                + "    mark_as_advanced(${PREFIX}_INCLUDE_DIR ${PREFIX}_LIBRARY ${PREFIX}_LIBRARY_REL ${PREFIX}_LIBRARY_DBG ${PREFIX}_LIBRARY_FWK)\n"
                + "  endif ()\n"
                + "endmacro(findpkg_finish)\n"
                + "\n"
                + "\n"
                + "# Slightly customised framework finder\n"
                + "MACRO(findpkg_framework fwk)\n"
                + "  IF(APPLE)\n"
                + "    SET(${fwk}_FRAMEWORK_PATH\n"
                + "      ${${fwk}_FRAMEWORK_SEARCH_PATH}\n"
                + "      ${CMAKE_FRAMEWORK_PATH}\n"
                + "      ~/Library/Frameworks\n"
                + "      /Library/Frameworks\n"
                + "      /System/Library/Frameworks\n"
                + "      /Network/Library/Frameworks\n"
                + "      /Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS3.0.sdk/System/Library/Frameworks/\n"
                + "    )\n"
                + "    FOREACH(dir ${${fwk}_FRAMEWORK_PATH})\n"
                + "      SET(fwkpath ${dir}/${fwk}.framework)\n"
                + "      IF(EXISTS ${fwkpath})\n"
                + "        SET(${fwk}_FRAMEWORK_INCLUDES ${${fwk}_FRAMEWORK_INCLUDES}\n"
                + "          ${fwkpath}/Headers ${fwkpath}/PrivateHeaders)\n"
                + "        if (NOT ${fwk}_LIBRARY_FWK)\n"
                + "          SET(${fwk}_LIBRARY_FWK \"-framework ${fwk}\")\n"
                + "        endif ()\n"
                + "      ENDIF(EXISTS ${fwkpath})\n"
                + "    ENDFOREACH(dir)\n"
                + "  ENDIF(APPLE)\n"
                + "ENDMACRO(findpkg_framework)\n")
    else:
        return "\n"

