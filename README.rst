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


License
-------

MIT

See LICENSE for more details
