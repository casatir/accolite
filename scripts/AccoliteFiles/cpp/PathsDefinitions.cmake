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
