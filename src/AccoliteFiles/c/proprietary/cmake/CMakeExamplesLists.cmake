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

#################################################
# Examples
#################################################

# Avoid policy warning
set( NO_POLICY_SCOPE ON )

##########################
# Dependencies

##########################
# Example files
file(
  GLOB_RECURSE
  example_sources
  ${EXAMPLES_PATH}/*.c
  )

##########################
# Add examples
message( STATUS "Adding examples" )
foreach( example ${example_sources} )
  get_filename_component( example_exe ${example} NAME_WE)
  add_executable( ${example_exe} ${example} )
  target_link_libraries( ${example_exe} <ACCOLITE_PROJECT_NAME_LOWER> )
  include( ExamplesLinks.cmake )
  message( STATUS "  ${example_exe} done" )
endforeach( example ${example_sources} )
