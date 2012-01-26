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
  add_test( ${test_exe} ${BIN_PATH}/${test_exe} )
  message( "--   ${test_exe} done" )
endforeach( test ${test_sources} )

##########################
# Include CTestConfig.cmake
include( CTest )
