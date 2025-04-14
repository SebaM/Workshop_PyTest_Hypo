from abc import ABCMeta
from urllib.parse import urlparse
from shop_pen_tests.sdk.base.l import SP_Logging
from requests import Session


# import requests


class RestClientException(Exception):
    pass


class HTTPException(Exception):
    def __init__(self, message=None, status=None, content=None, response=None):
        super(HTTPException, self).__init__()
        self.message = message
        self.status = status
        self.content = content
        self.response = response

    def __str__(self):
        return self.message if self.message else 'HTTP response: %d\n%s' % (self.status, self.content)


class RestConfig(SP_Logging):
    __metaclass__ = ABCMeta

    def __init__(self):
        super(RestConfig, self).__init__()
        self.connect_timeout = 15
        self.read_timeout = 10
        self.http_proxy = None
        self.https_proxy = None
        self.ssl_verify = False
        self.protocol = 'http'
        self.host = 'localhost'
        self.port = None
        self._url = None
        self.auth_port = None

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value
        if value is None:
            self.protocol = None
            self.host = None
            self.port = None
            return
        parsed_url = urlparse(value)
        self.protocol = parsed_url.scheme
        self.host = parsed_url.hostname
        self.port = parsed_url.port
        if self.port is None:
            if self.protocol == 'https':
                self.port = 443
            elif self.protocol == 'http':
                self.port = 80
            else:
                self.log.warning('Protocol {0} is not supported in port recognition'.format(self.protocol))

    def __set_schema_proxy(self, cfg_section, proxy_schema):
        proxy_key = '{}_proxy'.format(proxy_schema)
        proxy_value = None if proxy_key not in cfg_section else cfg_section[proxy_key]
        setattr(self, proxy_key, proxy_value)

    def set_http_proxy(self, cfg_section):
        self.__set_schema_proxy(cfg_section, 'http')

    def set_https_proxy(self, cfg_section):
        self.__set_schema_proxy(cfg_section, 'https')

    def set_ssl_verify(self, cfg):
        ssl_verify_key = 'ssl_verify'
        if ssl_verify_key in cfg:
            raise NotImplementedError("for ssl we need path to the certificate file")
        else:
            ssl_verify_value = False
        setattr(self, ssl_verify_key, ssl_verify_value)


class SimpleRestConfig(RestConfig):
    def set_properties(self, url, connect_timeout=15, read_timeout=10, http_proxy=None, https_proxy=None,
                       ssl_verify=False):
        self.url = url
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout
        self.http_proxy = http_proxy
        self.https_proxy = https_proxy
        self.ssl_verify = ssl_verify
        return self


class RestConfigFromCfg(RestConfig):

    # def set_properties(self, cfg, section):
    #     if 'url' in cfg[section]:
    #         self.url = cfg[section]["url"]
    #     elif 'host' in cfg[section] and 'modino.port' in cfg[section]:
    #         self.host = cfg[section]['host']
    #         self.port = cfg[section]['port']
    #         self.protocol = cfg[section].get('protocol', 'http')
    #     else:
    #         raise NotImplementedError('set_properties not implemented for section: {}, content: {}'.format(
    #             section, cfg[section]
    #         ))
    #     self.set_http_proxy(cfg[section])
    #     self.set_https_proxy(cfg[section])
    #     self.set_ssl_verify(cfg, section)
    #     return self

    def set_properties(self, cfg):
        if 'url' in cfg:
            self.url = cfg["url"]
            parsed_url = urlparse(self.url)
            self.host = parsed_url.hostname
            self.port = parsed_url.port
            if parsed_url.scheme != '':
                self.protocol = parsed_url.scheme
        elif 'host' in cfg and 'port' in cfg:
            self.host = cfg['host']
            self.port = cfg['port']
            self.protocol = cfg.get('protocol', 'http')
        else:
            raise NotImplementedError('set_properties not implemented for section: {}, content: {}'.format(cfg))
        if 'auth.port' in cfg:
            self.auth_port = cfg['auth.port']
        self.set_http_proxy(cfg)
        self.set_https_proxy(cfg)
        self.set_ssl_verify(cfg)
        return self


class RestClient(SP_Logging):
    def __init__(self, rest_config):
        """
        :param rest_config:
        :type rest_config:  RestConfig
        """
        super(RestClient, self).__init__()
        self.config = rest_config
        self.url = rest_config.url.rstrip('/')
        self.timeout = (rest_config.connect_timeout, rest_config.read_timeout)
        self.proxies = {'http': rest_config.http_proxy,
                        'https': rest_config.https_proxy}

        self.default_kwargs = {'timeout': self.timeout,
                               'proxies': self.proxies,
                               }

        self.session = Session()
        # Disabling trust environment settings for proxy configuration, default authentication and similar.
        self.session.trust_env = False
        self.session.verify = rest_config.ssl_verify

        def log_roundtrip(response, *args, **kwargs):
            is_binary = False
            if response.request.headers.get('Content-Type', ';').split(';')[0] in ('application/octet-stream',
                                                                              'multipart/form-data'):
                is_binary = True

            self.log.debug(
                f"\n----------------------------------------------------------------------------------------")
            self.log.debug(f"{response.request.method} {response.url}")
            self.log.debug(f"Status Code: {response.status_code}")
            filtered_req_headers = {k: (v[:15] + '...' + v[-10:] if len(v) > 20 else v) if k == 'Authorization' else v
                                    for k, v in response.request.headers.items()}
            self.log.debug(f"Request Headers: {filtered_req_headers}")
            if is_binary is True:
                self.log.debug(f"Binary payload - logging skipped")
            else:
                self.log.debug(f"Request Body: {response.request.body}") if response.request.body is not None else False
            self.log.debug(f"Response Headers: {response.headers}")
            self.log.debug(f"Response Body: {response.text}") if response.text != '' else None

        # Create a session and add the hook
        self.session.hooks["response"].append(log_roundtrip)

    def __uri(self, query):
        while query.startswith('/'):
            query = query[1:]
        return self.url + '/' + query

    def _get_raw_url(self):
        parsed_url = urlparse(self.url)
        return "%s://%s" % (parsed_url.scheme, parsed_url.netloc)

    @staticmethod
    def is_2xx_ok(status):
        return status / 100 == 2

    @staticmethod
    def is_2x1_created(status):
        return status == 201

    @staticmethod
    def is_2x2_accepted(status):
        return status == 202

    @staticmethod
    def is_2x4_deleted(status):
        return status == 204

    @staticmethod
    def is_3xx_ok(status):
        return status / 100 == 3

    @staticmethod
    def is_4xx_bad_request(status):
        return status / 100 == 4

    def check_status(self, response, is_ok_method='is_2xx_ok'):
        if is_ok_method is None:
            is_ok = getattr(self, 'is_2xx_ok')
        elif hasattr(self, is_ok_method):
            is_ok = getattr(self, is_ok_method)
        else:
            raise RestClientException("%s is_ok_method does not exist" % is_ok_method)
        if not is_ok(response.status_code):
            raise HTTPException(status=response.status_code, content=response.content, response=response,
                                message=response.text)

    def get_final_kwargs(self, **kwargs):
        """Method is used in all HTTP methods to set default kwargs if they are not passed:
               {'timeout' : (connect_timeout, read_timeout)}"""
        final_kwargs = {}
        final_kwargs.update(self.default_kwargs)
        final_kwargs.update(**kwargs)
        return final_kwargs

    def get(self, query, raw_query=False, **kwargs):
        if raw_query:
            return self.session.get(query, **self.get_final_kwargs(**kwargs))
        else:
            return self.session.get(self.__uri(query), **self.get_final_kwargs(**kwargs))

    def post(self, query, raw_query=False, data=None, json=None, **kwargs):
        if raw_query:
            return self.session.post(query, data=data, json=json, **self.get_final_kwargs(**kwargs))
        else:
            return self.session.post(self.__uri(query), data=data, json=json, **self.get_final_kwargs(**kwargs))

    def put(self, query, raw_query=False, data=None, **kwargs):
        if not raw_query:
            query = self.__uri(query)
        return self.session.put(query, data=data, **self.get_final_kwargs(**kwargs))

    def delete(self, query, raw_query=False, **kwargs):
        if not raw_query:
            query = self.__uri(query)
        return self.session.delete(query, **self.get_final_kwargs(**kwargs))

    def head(self, query, raw_query=False, **kwargs):
        if not raw_query:
            query = self.__uri(query)
        return self.session.head(query, **self.get_final_kwargs(**kwargs))

    def options(self, query, raw_query=False, **kwargs):
        if not raw_query:
            query = self.__uri(query)
        return self.session.options(query, **self.get_final_kwargs(**kwargs))

    def patch(self, query, raw_query=False, data=None, **kwargs):
        if not raw_query:
            query = self.__uri(query)
        return self.session.patch(query, data=data, **self.get_final_kwargs(**kwargs))

    def __del__(self):
        self.session.close()
