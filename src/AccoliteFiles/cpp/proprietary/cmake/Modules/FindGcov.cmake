find_program ( GCOV gcov )
if(NOT GCOV)
  message (FATAL_ERROR "Could not find the gcov utilities! Please install them (e.g., 'gcov' for Fedora/RedHat).")
else (NOT GCOV)
  exec_program (gcov ARGS --version OUTPUT_VARIABLE MY_TMP)
  string (REGEX REPLACE "[a-zA-Z\(\) ]* ([0-9].[0-9].[0-9]) .*" "\\1" GCOV_VERSION
	 "${MY_TMP}")
  message (STATUS "Found GCOV version: ${GCOV_VERSION}")
  set( GCOV_FOUND "1" )
  set( GCOV_COMMAND "gcov" )
endif(NOT GCOV)
