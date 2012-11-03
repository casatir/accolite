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
  ${EXAMPLES_PATH}/*.cpp
  )

##########################
# Add examples
message( "-- Adding examples" )
foreach( example ${example_sources} )
  get_filename_component( example_exe ${example} NAME_WE)
  add_executable( ${example_exe} ${example} )
  target_link_libraries( ${example_exe} <ACCOLITE_PROJECT_NAME_LOWER> )
  include( ExamplesLinks.cmake )
  message( "--   ${example_exe} done" )
endforeach( example ${example_sources} )
