##############################################
# Tests
#################################################

# Avoid policy warning
set( NO_POLICY_SCOPE ON )

##########################
# Dependencies
find_package(CUnit REQUIRED)

##########################
# Test files
file(
  GLOB_RECURSE
  test_sources
  ${TESTS_PATH}/*.c
  )

##########################
# Add tests

message( "-- Adding tests" )
foreach( test ${test_sources} )
  #string(REGEX REPLACE .c "" test_exe ${test} )
  get_filename_component( test_exe ${test} NAME_WE)
  add_executable( ${test_exe} ${test} )
  target_link_libraries( ${test_exe} <ACCOLITE_PROJECT_NAME_LOWER> )
  target_link_libraries( ${test_exe} ${CUNIT_LIBRARIES} )
  include( TestsLinks.cmake )
  add_test( ${test_exe} ${<ACCOLITE_PROJECT_NAME_UPPER>_CMD_TEST_OPTION} ${BIN_PATH}/${test_exe} )
  message( "--   ${test_exe} done" )
endforeach( test ${test_sources} )

##########################
# Include CTestConfig.cmake
include( CTest )
