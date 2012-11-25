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

##########################
# Include paths definitions
include( ${CMAKE_CURRENT_BINARY_DIR}/../cmake/PathsDefinitions.cmake )

##########################
# We need valgrind
find_package(Valgrind)
if( VALGRIND_FOUND )
  set( CTEST_MEMORYCHECK_COMMAND ${VALGRIND_PROGRAM} )
  set( CTEST_MEMORYCHECK_SUPPRESSIONS_FILE ${CONFIGURATION_FILES_PATH}/valgrind.supp )
  set( CTEST_MEMORYCHECK_COMMAND_OPTIONS
    "-q --tool=memcheck --leak-check=full --show-reachable=yes --workaround-gcc296-bugs=yes --num-callers=50"
    )
endif( VALGRIND_FOUND )

##########################
# Model analysis
set( MODEL "analysis" )

##########################
# CTest properies
set( CTEST_SOURCE_DIRECTORY ${CONFIGURATION_FILES_PATH} )
set( CTEST_BINARY_DIRECTORY ${BUILD_PATH} )

#########################
# Processing tests
ctest_start( ${MODEL} TRACK ${MODEL} )

#########################
# Set timeout to 20 minutes
set(CTEST_TEST_TIMEOUT           "4800")


## -- UPDATE
#ctest_update( SOURCE "${CTEST_SOURCE_DIRECTORY}" RETURN_VALUE res )

## -- CONFIGURE
#ctest_configure( BUILD  "${CTEST_BINARY_DIRECTORY}" RETURN_VALUE res )

## -- BUILD
#ctest_build( BUILD "${CTEST_BINARY_DIRECTORY}" RETURN_VALUE res)

## -- TEST
#ctest_test( BUILD  "${CTEST_BINARY_DIRECTORY}" RETURN_VALUE res)
if ( CTEST_MEMORYCHECK_COMMAND )
  ctest_memcheck( BUILD  "${CTEST_BINARY_DIRECTORY}" RETURN_VALUE res )
  if( NOT ${res} EQUAL 0 )
    message( FATAL_ERROR "Some tests fail." )
  endif( NOT ${res} EQUAL 0 )
endif( CTEST_MEMORYCHECK_COMMAND )
if ( CTEST_COVERAGE_COMMAND )
  ctest_coverage( BUILD  "${CTEST_BINARY_DIRECTORY}" RETURN_VALUE res )
  if( NOT ${res} EQUAL 0 )
    message( FATAL_ERROR "Some coverages fail." )
  endif( NOT ${res} EQUAL 0 )
endif( CTEST_COVERAGE_COMMAND )

## -- SUBMIT
#ctest_submit(                                              RETURN_VALUE res)
