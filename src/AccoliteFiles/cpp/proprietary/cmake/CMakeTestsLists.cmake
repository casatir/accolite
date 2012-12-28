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
find_package(CppUnit REQUIRED)

##########################
# Test files
file(
  GLOB_RECURSE
  test_sources
  ${TESTS_PATH}/*.cpp
  ${TESTS_PATH}/*.cxx
  ${TESTS_PATH}/*.cc
  ${TESTS_PATH}/*.c
  )

##########################
# Add tests

message( "-- Adding tests" )
foreach( test ${test_sources} )
  #string(REGEX REPLACE .cpp "" test_exe ${test} )
  get_filename_component( test_exe ${test} NAME_WE)
  add_executable( ${test_exe} ${test} )
  target_link_libraries( ${test_exe} <ACCOLITE_PROJECT_NAME_LOWER> )
  target_link_libraries( ${test_exe} ${CppUnit_LIBRARIES} )
  include( TestsLinks.cmake )
  add_test( ${test_exe} ${<ACCOLITE_PROJECT_NAME_UPPER>_CMD_TEST_OPTION} ${BIN_PATH}/${test_exe} )
  message( "--   ${test_exe} done" )
endforeach( test ${test_sources} )

##########################
# Include CTestConfig.cmake
include( CTest )
