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
set(CTEST_TEST_TIMEOUT           "1200")


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
