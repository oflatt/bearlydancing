import unittest        
import devoptions
devoptions.args.testsuitemode = True
devoptions.args.restart = True
import bearly_dancing
    
testsuite = unittest.TestSuite()

def add_test_module(m):
    newtests = unittest.defaultTestLoader.loadTestsFromModule(m)
    testsuite.addTests(newtests)

import tests.test_note_list_functions
add_test_module(tests.test_note_list_functions)
import tests.test_destructive
add_test_module(tests.test_destructive)
import tests.test_rdraw
add_test_module(tests.test_rdraw)
import tests.test_pointlist_functions
add_test_module(tests.test_pointlist_functions)
import tests.test_drawplant
add_test_module(tests.test_drawplant)
import tests.test_populate_map
add_test_module(tests.test_populate_map)


runner = unittest.TextTestRunner()
result = runner.run(testsuite)


