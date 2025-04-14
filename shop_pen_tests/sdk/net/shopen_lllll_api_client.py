import json
from shop_pen_tests.sdk.net.shopen_api_client import
from modino_tests.sdk.net.modino_api_client import ModinoApi
from modinoapi.api.actuator_api import ActuatorApi


# from modinoapi.models.actuator  # do not have model, yet?


class ModinoActuator(ModinoApi):
    modinoapi: ActuatorApi
    L_METRICS = '/metrics'
    G_METRICS = L_METRICS + "/%(required_metric_name)s"
    L_HEALTH = '/health'
    G_HEALTH = L_HEALTH + "/%(health_path)s"
    G_ABOUT = '/about'

    # L - list
    # C - create
    # G - get
    # U - update
    # D - delete

    def __init__(self, api_client, api_version):
        super(ModinoActuator, self).__init__(api_client, api_version)
        self.modinoapi = ActuatorApi()  # maybe to give ability to do serialize

    def list_metrics(self):
        """List Metrics"""
        response = self.m_client.get(self._add_api_version(ModinoActuator.L_METRICS))
        self.m_client.check_status(response)
        return response.json()

    def get_metric_by_name(self, metric_id):
        """Get Metric by its id"""
        response = self.m_client.get(self._add_api_version(ModinoActuator.G_METRICS % {"required_metric_name": metric_id}))
        self.m_client.check_status(response)
        return response.json()

    def list_health(self):
        """List Healths"""
        response = self.m_client.get(self._add_api_version(ModinoActuator.L_HEALTH))
        self.m_client.check_status(response)
        return response.json()

    def get_health_by_path(self, health_path='**'):
        """Get Health by Path"""
        response = self.m_client.get(self._add_api_version(ModinoActuator.G_HEALTH % {"health_path": health_path}))
        self.m_client.check_status(response)
        return response.json()

    def get_about(self):
        """Get About"""
        response = self.m_client.get(self._add_api_version(ModinoActuator.G_ABOUT))
        self.m_client.check_status(response)
        return response.json()
