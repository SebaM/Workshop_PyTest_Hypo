import logging.config
import os

@staticmethod
def get_tests_dir():
    return os.path.abspath(os.path.dirname(__file__))

@staticmethod
def get_tests_etc_dir():
    return os.path.join(get_tests_dir(), 'etc')
@staticmethod
def get_tests_root_dir():
    return os.path.join(get_tests_dir(), 'modino_tests')


log_conf = 'l.conf'
if os.path.exists(log_conf):
    log_config_path = log_conf
else:
    config_dir = get_tests_etc_dir()
    log_config_path = os.path.join(config_dir, log_conf)
logging.config.fileConfig(log_config_path)
