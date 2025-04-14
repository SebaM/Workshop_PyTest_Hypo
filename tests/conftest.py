import pytest
"""
FIXTURE SCOPES:
- "function":	Default scope. The fixture is invoked once per test function.
- "class":   	The fixture is invoked once per test class.
- "module":     The fixture is invoked once per test module (file).
- "package" 	The fixture is invoked once per package.
- "session": 	The fixture is invoked once for the entire test session.
e.g.: @pytest.fixture(scope="class")
"""

@pytest.fixture(scope='session')
def ShoPen_client():
    """
    Pytest fixture to provide an authenticated ShoPenClient instance for tests.

    This fixture:
    - Loads configuration from 'localhost.conf'
    - Initializes the ShoPenClient with configuration from the 'ShoPen' section
    - Authenticates the client using OIDC (OpenID Connect)
    - Returns the ready-to-use client for use in integration or functional tests

    Scope:
        'session' — the client is created once per test session and reused.

    :return: Authenticated ShoPenClient instance
    :rtype: ShoPenClient
    """
    cfg = GeneralConfigParser()
    cfg.read_conf_file("localhost.conf")
    # simple create
    client = ShoPenClient(cfg['ShoPen'])
    client.authorization_oidc()
    return client


@pytest.fixture(scope='session')
def ShoPen_non_authorized_client():
    """
    Pytest fixture to provide an non-authenticated ShoPenClient instance for tests.

    This fixture:
    - Loads configuration from 'localhost.conf'
    - Initializes the ShoPenClient with configuration from the 'ShoPen' section
    - Returns the ready-to-use client for use in integration or functional tests

    Scope:
        'session' — the client is created once per test session and reused.

    :return: Authenticated ShoPenClient instance
    :rtype: ShoPenClient
    """
    cfg = GeneralConfigParser()
    cfg.read_conf_file("localhost.conf")
    # simple create
    client = ShoPenClient(cfg['ShoPen'])
    return client