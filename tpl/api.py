# -*- coding: utf-8 -*-
'''
    tpl.api

    Generic API for TPL

    :license: MIT, see LICENSE for more details
'''
import requests
import json
import base64

from .exceptions import TPLAPIError


class TPLClient(object):
    """Generic API for TPL"""

    def __init__(self, base_url, auth_path, client_id=None, client_secret=None, tpl_key=None,
                 grant_type='client_credentials', user_login_id=None, session=None, verify_ssl=True):
        """
        Create an instance, get access token and update the headers

        :param base_url: base url to the TPL instance.
        :param auth_path: authentication service path.
        :param client_id: client id of TPL.
        :param client_secret: client secret key of TPL.
        :param tpl_key: WH specific TPL key.
        :param grant_type: by default 'client_credentials'.
        :param user_login_id: TPL user id.
        :param session: pass a custom requests Session.
        :param verify_ssl: skip SSL validation.
        
        :Example:

            from tpl import TPLClient

            api = TPLClient(base_url, auth_path, client_id, client_secret, tpl_key,
                            grant_type, user_login_id, session, verify_ssl)
            api.get("orders", "13654")
            
            payload = {}
            api.post("orders", data=payload)
        """
        self._base_url = base_url
        self._auth_path = auth_path
        self._client_id = client_id
        self._client_secret = client_secret
        self._tpl_key = tpl_key
        self._grant_type = grant_type
        self._user_login_id = user_login_id
        self._verify_ssl = verify_ssl

        if session is None:
            self.client = requests.Session()
            response = self._get_access_token()
            headers = {
                "Authorization": "%s %s" % (response['token_type'], response['access_token']),
                "Content-Type": "application/hal+json"
            }
            self.client.headers.update(headers)
        else:
            self.client = session

    def _get_access_token(self):
        """Get access token from server and returns it.

        :return: access token from the server.
        """
        authorization = base64.b64encode(
            "%s:%s" % (self._client_id, self._client_secret))
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic " + authorization
        }
        data = {
            "grant_type": self._grant_type,
            "tpl": "{%s}" % (self._tpl_key,),
            "user_login_id": self._user_login_id
        }
        return self.post(self._auth_path, data=data, add_headers=headers)

    def _parse_error(self, content):
        """Take the content and return as it is.

        :param content: content returned by the TPL server as string.
        :return: content.
        """
        return content

    def _check_status_code(self, status_code, content):
        """Take the status code and check it.

        Throw an exception if the server didn't return 200 or 201 or 202 code.

        :param status_code: status code returned by the server.
        :param content: content returned by the server.
        :return: True or raise an exception TPLAPIError.
        """
        message_by_code = {
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not Found',
            412: 'Precondition failed',
            428: 'Precondition required',
            500: 'Internal Server Error',
        }

        if status_code in (200, 201, 202):
            return True
        elif status_code in message_by_code:
            tpl_error_msg = self._parse_error(content)
            raise TPLAPIError(
                message_by_code[status_code], status_code, tpl_error_msg=tpl_error_msg)
        else:
            tpl_error_msg = self._parse_error(content)
            raise TPLAPIError('Unknown error', status_code,
                           tpl_error_msg=tpl_error_msg)

    def _execute(self, url, method, data=None, add_headers=None):
        """Perform the HTTP request and return the response back.

        :param url: full url to call.
        :param method: GET, POST.
        :param data: POST (add) only.
        :param add_headers: additional headers merged into instance's headers.
        :return: response in json format.
        """
        if add_headers is None:
            add_headers = {}

        request_headers = self.client.headers.copy()
        request_headers.update(add_headers)

        response = self.client.request(
            method,
            url,
            data=data,
            verify=self._verify_ssl,
            headers=request_headers
        )
        self._check_status_code(response.status_code, response.content)
        return response.json()

    def get(self, resource_path, resource_id=None, querystring=None, add_headers=None):
        """Retrieve (GET) a resource.

        :param resource_path: path of resource to retrieve.
        :param resource_id: optional resource id to retrieve.
        :param querystring: optional RQL querystring.
        :param add_headers: additional headers merged into instance's headers.
        :return: response in json format.
        """
        full_url = "%s/%s" % (self._base_url, resource_path)
        if resource_id is not None:
            full_url += "/%s" % (resource_id,)
        if querystring is not None:
            full_url += "?%s" % (querystring,)
        return self._execute(full_url, 'GET', add_headers=add_headers)

    def post(self, resource_path, data=None, add_headers=None):
        """Add (POST) a resource.

        :param resource_path: path of resource to create.
        :param data: full payload as dict of new resource.
        :param add_headers: additional headers merged into instance's headers.
        :return: response in json format.
        """
        if data is None:
            raise ValueError('Data Undefined.')
        full_url = "%s/%s" % (self._base_url, resource_path)
        return self._execute(full_url, 'POST', data=json.dumps(data), add_headers=add_headers)

