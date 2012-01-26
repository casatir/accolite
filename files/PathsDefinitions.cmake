##########################
# <ACCOLITE_PROJECT_NAME> path
set( <ACCOLITE_PROJECT_NAME_UPPER>_PATH ${CMAKE_CURRENT_BINARY_DIR}/.. )

##########################
# Src path
set( SRC_PATH ${<ACCOLITE_PROJECT_NAME_UPPER>_PATH}/src )

##########################
# Examples path
set( EXAMPLES_PATH ${<ACCOLITE_PROJECT_NAME_UPPER>_PATH}/examples )

##########################
# Tests path
set( TESTS_PATH ${<ACCOLITE_PROJECT_NAME_UPPER>_PATH}/tests )

##########################
# Cmake configuration files path
set( CONFIGURATION_FILES_PATH ${<ACCOLITE_PROJECT_NAME_UPPER>_PATH}/cmake )

##########################
# Cmake created files path
set( BUILD_PATH ${<ACCOLITE_PROJECT_NAME_UPPER>_PATH}/build )

##########################
# Lib path
set( <ACCOLITE_PROJECT_NAME_UPPER>_LIB_PATH ${BUILD_PATH}/lib<ACCOLITE_PROJECT_NAME> )

##########################
# Executables files path
set( BIN_PATH ${<ACCOLITE_PROJECT_NAME_UPPER>_PATH}/bin )

##########################
# .cmake module files path
set( MODULE_PATH ${CONFIGURATION_FILES_PATH}/Modules )
set( CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${MODULE_PATH} )
