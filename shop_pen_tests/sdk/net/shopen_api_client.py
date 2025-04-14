from shop_pen_tests.sdk.base.l import SP_Logging
from shop_pen_tests.sdk.net.rest_client import RestClient, RestConfigFromCfg
from urllib.parse import urljoin


class ShoPenApi(SP_Logging):
    """
    Base class for ShoPen API wrappers.

    Provides shared functionality for specific ShoPen API client classes
    (e.g., MUG, Application, Device clients) such as:
    - Logging support via SP_Logging
    - API version injection into endpoint URLs
    - Access to the shared RestClient instance (`self.m_client`)

    Child classes extend this to implement concrete operations for specific endpoints.
    """

    def __init__(self, rest_client, api_version):
        """
        Initialize the base ShoPen API client.

        :param rest_client: RestClient instance used to send HTTP requests
        :param api_version: API version string to append to each request URL
        """
        super(ShoPenApi, self).__init__()
        self.m_client = rest_client
        self.api_version = api_version

    def _add_api_version(self, url_str):
        return url_str + f'?api-version={self.api_version}'


class ShoPenClient(SP_Logging):
    """
    The class serves as a central client for accessing ShoPen API domains.

    The class acts as a unified interface to all ShoPen API components such as:
    - Application
    - Device
    - MUG
    - Update packages
    - Enrollment packages
    - Notifications
    - Device configurations
    - Actuators

    It also handles authentication via OIDC and configures the underlying REST client.
    """
    def __init__(self, ShoPen_config):
        """
         Initialize the ShoPenClient and its sub-clients.

         :param ShoPen_config: Dictionary of configuration values (e.g. from `localhost.conf`).
         """
        super(ShoPenClient, self).__init__()
        self.api_version = ShoPen_config["api.version"]
        self.ShoPen_config = ShoPen_config
        self.m_client = RestClient(RestConfigFromCfg().set_properties(ShoPen_config))
        self._access_token = None

        # # ACTUATOR
        # from ShoPen_tests.sdk.net.modion_actuator_api_client import ShoPenActuator
        # self.actuator = ShoPenActuator(self.m_client, self.api_version)

        # # APPLICATION
        # from ShoPen_tests.sdk.net.ShoPen_application_api_client import ShoPenApplication
        # self.application = ShoPenApplication(self.m_client, self.api_version)
        #
        # # DEVICE
        # from ShoPen_tests.sdk.net.ShoPen_device_api_client import ShoPenDevice
        # self.device = ShoPenDevice(self.m_client, self.api_version)
        #
        # # DEVICE CONFIG
        # from ShoPen_tests.sdk.net.ShoPen_device_configuration_api_client import ShoPenDeviceConfiguration
        # self.device_config = ShoPenDeviceConfiguration(self.m_client, self.api_version)
        #
        # # ENROLLMENT
        # from ShoPen_tests.sdk.net.ShoPen_enrollment_api_client import ShoPenEnrollmentPackage
        # self.enrollment = ShoPenEnrollmentPackage(self.m_client, self.api_version)
        #
        # # MUG
        # from ShoPen_tests.sdk.net.ShoPen_mug_api_client import ShoPenMug
        # self.mug = ShoPenMug(self.m_client, self.api_version)
        #
        # # NOTIFICATION CONTROLLER
        # from ShoPen_tests.sdk.net.ShoPen_notification_controller_api_client import NotificationController
        # self.notification = NotificationController(self.m_client, self.api_version)
        #
        # # PACKAGE
        # from ShoPen_tests.sdk.net.ShoPen_package_api_client import ShoPenPackage
        # self.package = ShoPenPackage(self.m_client, self.api_version)
        #
        # # UPDATE
        # from ShoPen_tests.sdk.net.modion_update_api_client import ShoPenUpdate
        # self.update = ShoPenUpdate(self.m_client, self.api_version)


    def authorization_oidc(self):
        self.m_client.get_final_kwargs()
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'client_id': self.ShoPen_config.get("client_id"),
            'username': self.ShoPen_config.get("username"),
            'password': self.ShoPen_config.get("password"),
            'grant_type': "password",
            'client_secret': self.ShoPen_config.get("client_secret")
        }
        uri = 'realms/ShoPen/protocol/openid-connect/token'
        netloc = self.m_client.config.protocol + '://' + self.m_client.config.host + ':' + str(
            self.m_client.config.auth_port)
        response = self.m_client.post(query=urljoin(netloc, uri), raw_query=True, data=data, headers=headers)
        self.m_client.check_status(response)

        response_json = response.json()

        assert 'access_token' in response_json
        access_token = 'Bearer ' + response_json['access_token']
        self._access_token = access_token
        headers = {
            'Authorization': access_token
        }
        self.m_client.default_kwargs.update({'headers': {'Authorization': access_token}})
        # self.m_client.session.auth = access_token

        assert 'token_type' in response_json
        assert response_json['token_type'] == 'Bearer'

        return response
