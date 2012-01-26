#include <cppunit/extensions/TestFactoryRegistry.h>
#include <cppunit/TextTestRunner.h>
int main( int argc, char **argv)
{
     CppUnit::TextTestRunner runner;
     CppUnit::TestFactoryRegistry &registry = CppUnit::TestFactoryRegistry::getRegistry();
     runner.addTest( registry.makeTest() );
     return !runner.run( "", false );
}
