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
