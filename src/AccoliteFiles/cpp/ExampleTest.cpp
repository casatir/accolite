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

#include <cppunit/extensions/HelperMacros.h>

#define <ACCOLITE_PROJECT_NAME_UPPER>_TEST_NAME ExampleTest

class <ACCOLITE_PROJECT_NAME_UPPER>_TEST_NAME : public CppUnit::TestFixture
{
     
     CPPUNIT_TEST_SUITE( <ACCOLITE_PROJECT_NAME_UPPER>_TEST_NAME );
     CPPUNIT_TEST( test );
     CPPUNIT_TEST_SUITE_END();
     
public:
     inline void setUp() {
     }
     
     inline void tearDown() {
     }
     inline void test() {
	  CPPUNIT_ASSERT( true );
     }
     
};

CPPUNIT_TEST_SUITE_REGISTRATION( <ACCOLITE_PROJECT_NAME_UPPER>_TEST_NAME );

#include "TestRunner.h"
