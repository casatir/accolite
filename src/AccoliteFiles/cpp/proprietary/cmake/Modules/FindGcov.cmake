set( GCOV_COMMAND "gcov" )

find_program ( GCOV_FOUND ${GCOV_COMMAND} )
if(NOT GCOV_FOUND)
  message (FATAL_ERROR "Could not find the gcov utilities! Please install them.")
else (NOT GCOV_FOUND)
  exec_program (${GCOV_COMMAND} ARGS --version OUTPUT_VARIABLE MY_TMP)
  string (REGEX REPLACE "[a-zA-Z\(\) ]* ([0-9].[0-9].[0-9]) .*" "\\1" GCOV_VERSION
	 "${MY_TMP}")
  message (STATUS "Found GCOV version: ${GCOV_VERSION}")
endif(NOT GCOV_FOUND)
