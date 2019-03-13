import unittest        
import devoptions

devoptions.args.novideomode = True

    
testsuite = unittest.TestSuite()

def addTestModule(m):
    newtests = unittest.defaultTestLoader.loadTestsFromModule(m)
    testsuite.addTests(newtests)

import tests.test_note_list_functions
addTestModule(tests.test_note_list_functions)
import tests.test_destructive
addTestModule(tests.test_destructive)
import tests.test_rdraw
addTestModule(tests.test_rdraw)
import tests.test_pointlist_functions
addTestModule(tests.test_pointlist_functions)
import tests.test_drawplant
addTestModule(tests.test_drawplant)


runner = unittest.TextTestRunner()
result = runner.run(testsuite)


