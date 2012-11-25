/*
  Copyright (c) 2012 Casati Romain
  All rights reserved.
  
  This file is part of Accolite.
  
  Accolite is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  
  Accolite is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  
  You should have received a copy of the GNU General Public License
  along with Accolite.  If not, see <http://www.gnu.org/licenses/>
*/

#include <cppunit/extensions/TestFactoryRegistry.h>
#include <cppunit/TextTestRunner.h>
int main( int argc, char **argv)
{
     (void) argc; // Avoid warning about unused parameter
     (void) argv; // Avoid warning about unused parameter
     CppUnit::TextTestRunner runner;
     CppUnit::TestFactoryRegistry &registry = CppUnit::TestFactoryRegistry::getRegistry();
     runner.addTest( registry.makeTest() );
     return !runner.run( "", false );
}
