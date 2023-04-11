import re
import sys
from functions import *

def settings(s):
    regex = "\n[\s]+[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)"
    mo = re.findall(regex, s)
    d = dict(mo)
    return d


def cli(options):
    args = sys.argv[1:]
    for k, v in options.items():
        v = str(v)
        for n, x in enumerate(args):
            if x == '-' + k[0] or x == '--' + k:
                if v == 'false':
                    v = 'true'
                elif v == 'true':
                    v = 'false'
                else:
                    v = args[n + 1]
            options[k] = coerce(v)
    return options
