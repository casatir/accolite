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

cmake_minimum_required( VERSION 2.6 )

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

# Treat all warnings as errors
if( CMAKE_COMPILER_IS_GNUCC )
  set( CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wextra -Werror -Wconversion -std=gnu99" )
endif( CMAKE_COMPILER_IS_GNUCC )

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
  lib_c
  ${SRC_PATH}/*.c
  )
include_directories ( ${SRC_PATH} )

##########################
# Library
add_library( <ACCOLITE_PROJECT_NAME_LOWER> SHARED
  ${lib_headers}
  ${lib_c}
  ${lib_defs}
  ${lib_impls}
  )
set_target_properties( <ACCOLITE_PROJECT_NAME_LOWER> PROPERTIES LINKER_LANGUAGE C )
set_source_files_properties( ${lib_c}  PROPERTIES LANGUAGE C )
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
