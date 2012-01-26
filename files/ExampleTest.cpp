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
