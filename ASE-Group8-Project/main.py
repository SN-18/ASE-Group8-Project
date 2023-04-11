import random
import sys
import math
import data_loader
from test_controller import *
from functions import *
from settings import *
from test_controller import *
from tables import *
from globals import the as the
from globals import help as help

import re
import os

def driver(options, help, funs):
    saved, fails, y = {}, 0, 0
    d=cli(settings(help))

    for key in d:
        val=d[key]
        options[key]=val


    saved = options

    if options['help'] is not False:

        print(help)
    else:
        for what, fun in funs.items():
            if options['go'] == 'all' or what == options['go']:

                for k, v in saved.items():
                    options[k] = v
                Seed = options['seed']
                random.seed(Seed)
                print("\n▶️ ",what,"-"*60)

                if funs[what]() == False:
                    fails = fails + 1

                    print(str(u'\u274C') + " fail: " + str(what))

                else:
                    y = y + 1
                    print(str(u'\u2705') + " pass: " + str(what))
    
    if y + fails > 0:
        print("\n🔆 pass=",y," fail=",fails," success=",100*y/(y+fails)//1,"\n")
    # rogues()
    
    sys.exit(fails)    












#Main
if __name__ == '__main__':
    unittest.main()
    # eg('the', 'show settings', the_test_1, help)
    # eg('rand', 'demo random number generation', rand_test_20, help)
    # eg('some', 'demo of reservoir sampling', some_test_21, help)
    # eg('nums', 'demo NUM', nums_test_22, help)
    # eg('sym', 'check syms', sym_test_3, help)
    # eg('csv', 'reading csv files', csv_5, help)
    # eg('data', 'showing data sets', data_test_6, help)
    # eg('clone', 'replicate stuctured of DATA', clone_test_8, help)
    # eg('cliffs', 'stats tests', cliffs_test_23, help)
    # eg('dist', 'distance test', dist_test_24, help)
    # eg('half', 'divide data in half', half_test_10, help)
    # eg('tree', 'make and show tree of clusters', tree_test_25, help)
    # eg('sway', 'optimizing', sway_test_26, help)
    # eg('bins', 'find deltas between best and rest', bins_test_27, help)
    # eg('xpln', 'explore explanation sets', xpln_test_28, help)

    driver(the, help, egs)




