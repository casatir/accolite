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
