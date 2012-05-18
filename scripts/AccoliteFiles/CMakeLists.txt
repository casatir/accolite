cmake_minimum_required(VERSION 2.6)

##########################
# Project name
project( <ACCOLITE_PROJECT_NAME> )

##########################
# Include paths definitions
include( PathsDefinitions.cmake )

# Add a sensible build type default and warning because empty means no optimization and no debug info.
if( NOT CMAKE_BUILD_TYPE )
  message( "WARNING: CMAKE_BUILD_TYPE is not defined!
"
    "         Defaulting to CMAKE_BUILD_TYPE=RelWithDebInfo."
    " Use ccmake to set a proper value." )
  set( CMAKE_BUILD_TYPE RelWithDebInfo CACHE STRING
    "Choose the type of build, options are:"
    " None Debug Release RelWithDebInfo MinSizeRel." FORCE )
endif( NOT CMAKE_BUILD_TYPE )

#add_definitions( -Wall -Werror )
set( CMAKE_CXX_FLAGS "-Wall -Werror" )

# Put executables in bin
set( EXECUTABLE_OUTPUT_PATH ${BIN_PATH} )

##########################
# Dependencies
include( Dependencies.cmake )


##########################
# Src files
file (
  GLOB_RECURSE
  lib_headers
  ${SRC_PATH}/*.h
  ${SRC_PATH}/*.hpp
  )
file (
  GLOB_RECURSE
  lib_defs
  ${SRC_PATH}/*.def
  )
file (
  GLOB_RECURSE
  lib_impls
  ${SRC_PATH}/*.impl
  )
file (
  GLOB_RECURSE
  lib_cpp
  ${SRC_PATH}/*.c
  ${SRC_PATH}/*.cpp
  )
include_directories ( ${SRC_PATH} )

##########################
# Library
add_library( <ACCOLITE_PROJECT_NAME_LOWER> SHARED
  ${lib_headers}
  ${lib_cpp}
  ${lib_defs}
  ${lib_impls}
  )
target_link_libraries( <ACCOLITE_PROJECT_NAME_LOWER> ${<ACCOLITE_PROJECT_NAME_UPPER>_LIB_DEPENDENCIES} )


##########################
# Library installation
set( CMAKE_INSTALL_PREFIX ${<ACCOLITE_PROJECT_NAME_UPPER>_LIB_PATH} )
foreach( header ${lib_headers} ${lib_defs} ${lib_impls} )
  # To preserve dyrectory hierarchy...
  string( REGEX REPLACE ${SRC_PATH}/ "" header_no_path ${header} )
  string( REGEX MATCH "(.*)[/\\]" header_dir ${header_no_path} )
  install( FILES ${header} DESTINATION include/${header_dir} )
endforeach( header ${lib_headers} ${lib_defs} ${lib_impls} )
install( TARGETS <ACCOLITE_PROJECT_NAME_LOWER> LIBRARY DESTINATION lib )


##########################
# Examples
include( CMakeExamplesLists.cmake )


##########################
# Tests
include( CMakeTestsLists.cmake )
