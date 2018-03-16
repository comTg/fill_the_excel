from WordTo_Excel import settings

import inspect

def log(**args):
    if settings.DEBUG:
        func = inspect.stack()[1][3]
        print('{func}---的位置:{args}'.format(func=func,args=args))

