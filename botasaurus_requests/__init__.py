

import os


def detect_module() -> bool:

    import inspect

    stack: list = inspect.stack(2)
    if len(stack) < 2:
        return False
    prev, launch = stack[-2:]
    try:
        if (launch.function, prev.function) == ('_run_module_as_main', '_get_module_details'):
            return True
    except AttributeError:
        pass
    return False


# if detect_module():
#     os.environ['BOTASAURUS_REQUESTS_MODULE'] = '1'


from .response import Response, ProcessResponse
from .session import Session, TLSSession, chrome, firefox
from .reqs import *   
from  . import request_functions as request
from .headers import Headers
from .request_class import Request
