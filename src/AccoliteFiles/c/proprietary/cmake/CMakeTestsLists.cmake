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

##############################################
# Tests
#################################################

# Avoid policy warning
set( NO_POLICY_SCOPE ON )

##########################
# Dependencies
find_package(CUnit QUIET)

if( CUNIT_FOUND )
  ##########################
  # Test files
  file(
    GLOB_RECURSE
    test_sources
    ${TESTS_PATH}/*.c
    )
  set_source_files_properties( ${test_sources}  PROPERTIES LANGUAGE C )

  ##########################
  # Add C tests

  message( STATUS "Adding C tests" )
  foreach( test ${test_sources} )
    get_filename_component( test_exe ${test} NAME_WE)
    add_executable( ${test_exe} ${test} )
    target_link_libraries( ${test_exe} <ACCOLITE_PROJECT_NAME_LOWER> )
    target_link_libraries( ${test_exe} ${CUNIT_LIBRARIES} )
    include( TestsLinks.cmake )
    add_test( ${test_exe} ${<ACCOLITE_PROJECT_NAME_UPPER>_CMD_TEST_OPTION} ${BIN_PATH}/${test_exe} )
    message( STATUS "  ${test_exe} done" )
  endforeach( test ${test_sources} )

else( CUNIT_FOUND )
  message( STATUS
    "WARNING: CUnit library not found, C tests will not be added." )
endif( CUNIT_FOUND )

##########################
# Include CTestConfig.cmake
include( CTest )
