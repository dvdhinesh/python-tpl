# -*- coding: utf-8 -*-
'''
    tpl.exceptions

    Generic API for TPL

    :license: MIT, see LICENSE for more details
'''
class TPLBaseError(Exception):
    """Generic base exception class for TPL"""
    pass


class TPLAPIError(TPLBaseError):
    """Raised when TPL returns fault code"""

    def __init__(self, msg, error_code=None, tpl_error_msg=''):
        """Initialize the API error.

        :param msg: HTTP status message returned by the server.
        :param error_code: HTTP status code returned by the server.
        :param tpl_error_msg: Custom error msg returned by the server.
        """
        self.msg = msg
        self.error_code = error_code
        self.tpl_error_msg = tpl_error_msg

    def __str__(self):
        """Include custom msg"""
        return repr(self.msg + self.tpl_error_msg)
