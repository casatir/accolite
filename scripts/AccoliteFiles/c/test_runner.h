#ifndef _<ACCOLITE_PROJECT_NAME_UPPER>_TEST_RUNNER_H_INCLUDED_
#define _<ACCOLITE_PROJECT_NAME_UPPER>_TEST_RUNNER_H_INCLUDED_

#include <CUnit/CUnit.h>
#include <CUnit/Basic.h>

#define <ACCOLITE_PROJECT_NAME_UPPER>_TEST_QUOTE(n) #n 

#define <ACCOLITE_PROJECT_NAME_UPPER>_TEST_SUITE(n,b,e)\
     int main(void)                             \
     {                                          \
          CU_set_error_action(CUEA_FAIL);       \
          CU_basic_set_mode(CU_BRM_VERBOSE);    \
          CU_pSuite suite;                      \
          CU_initialize_registry();             \
          suite = CU_add_suite(<ACCOLITE_PROJECT_NAME_UPPER>_TEST_QUOTE(n), b, e)
          
#define <ACCOLITE_PROJECT_NAME_UPPER>_TEST_ADD(n)    CU_ADD_TEST(suite, n)

#define <ACCOLITE_PROJECT_NAME_UPPER>_TEST_ASSERT(e) CU_ASSERT_FATAL(e)

#define <ACCOLITE_PROJECT_NAME_UPPER>_TEST_SUITE_END()\
          CU_basic_run_tests();                         \
          unsigned int nb_failures = CU_get_number_of_failures();       \
          CU_cleanup_registry();                        \
          return nb_failures != 0;                      \
      }                                                 \
      /* trick to allow semicolon at the end of the macro call */       \
      /* adding such variable is not costly, ... we are in tests... */  \
      static const char _<ACCOLITE_PROJECT_NAME_LOWER>_test_dummy_variable_

#endif // ! _<ACCOLITE_PROJECT_NAME_UPPER>_TEST_RUNNER_H_INCLUDED_
