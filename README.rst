TPL Python API
==============

A Python wrapper for the 3PL Central REST API

Usage
-----

.. code-block:: python

    from tpl import TPLClient

    api = TPLClient(base_url, auth_path, client_id, client_secret, tpl_key,
                    grant_type, user_login_id, session, verify_ssl)
    api.get("orders", "13654")
    
    payload = {}
    api.post("orders", data=payload)


Common Gotchas
--------------

This module has the following limitations:

 * This wrapper was developed by signing the 3PL Central REST Beta Agreement. Their API may change in the final release.
 * At this moment of writing, there will be no refresh token issued for the API calls and the expiry time is "0" means it will not expire.

.. code-block:: python

    {
        "access_token":"[access token will be here]",
        "token_type":"Bearer",
        "expires_in":0, // 0 means it doesn't expire, in future releases it might be non-zero
        "refresh_token":null, // if issued an expiring token, use this to refresh it
        "scope":null // ignore, this OAuth2 feature not used
    }

License
-------

MIT

See LICENSE for more details
