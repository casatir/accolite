#include "test_runner.h"

#define <ACCOLITE_PROJECT_NAME_UPPER>_TEST_NAME example_test

/* return 0 iff set up is successfull */
static int set_up(void) { return 0; }

/* return 0 iff clean up is successfull */
static int tear_down(void) { return 0; }

static void test(void)
{
     <ACCOLITE_PROJECT_NAME_UPPER>_TEST_ASSERT( 1 != 0 );
}

<ACCOLITE_PROJECT_NAME_UPPER>_TEST_SUITE(<ACCOLITE_PROJECT_NAME_UPPER>_TEST_NAME, set_up, tear_down);
<ACCOLITE_PROJECT_NAME_UPPER>_TEST_ADD( test );
<ACCOLITE_PROJECT_NAME_UPPER>_TEST_SUITE_END();
