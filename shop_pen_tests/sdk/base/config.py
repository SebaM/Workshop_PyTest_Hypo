"""
module for configurations file management
"""
import os
import re
# from configparser import SafeConfigParser, NoOptionError, NoSectionError
from configparser import ConfigParser
from shop_pen_tests.sdk.base.base_log import LoggingObject
from shop_pen_tests.sdk.base.l import SP_Logging


class ConfigFileNotFoundError(Exception):
    pass


class GeneralConfigParser(ConfigParser, SP_Logging):
    """
    ConfigParser extension with import mechanism
        ALL Sections names are converted to upper cases, and section attributes name are converted to lower cases
        raises ConfigFileNotFoundError when file not found
    """

    def __init__(self, defaults=None, dict_type=dict):
        super(GeneralConfigParser, self).__init__(defaults=defaults, dict_type=dict_type)
        LoggingObject.__init__(self)

    # def get(self, section, option, default=DEFAULT_VALUE, raw=False, vars=None):
    #     try:
    #         return super(GeneralConfigParser, self).get(section.upper(), option.lower(), raw=raw, vars=vars)
    #     except (NoOptionError, NoSectionError):
    #         if default != DEFAULT_VALUE:
    #             return default
    #         else:
    #             raise

    def get_section(self, section):
        """
        Get whole section.
        """
        return super(GeneralConfigParser, self).items(section)

    # def set(self, section, option, value):
    #     if section:
    #         section = section.upper()
    #     super(GeneralConfigParser, self).set(section, option.lower(), value)

    # def update(self, update_dict):
    #     """
    #     Update Config with
    #     @param update_dict: dict of dict or  GeneralConfigParser
    #         e.g. { 'SECTION1':{'option1':'value1','option2':'value2'}}
    #     @type update_dict: dict, GeneralConfigParser
    #     """
    #     if type(update_dict) is dict:
    #         pass
    #     elif isinstance(update_dict, GeneralConfigParser):
    #         for default_key in update_dict._defaults.keys():
    #             for section in self._sections:
    #                 # remove sections attributes provided in update_dict defaults
    #                 if section in update_dict._sections:
    #                     self._sections[section].pop(default_key, None)
    #         self._defaults.update(update_dict._defaults)
    #         # update_dict = update_dict._sections
    #     else:
    #         raise TypeError('%s is not supported type for update update_dict parameter.' % type(update_dict))
    #     for section in update_dict.sections():
    #         if section != section.upper():
    #             update_dict.add_section(section.upper())
    #             update_dict[section.upper()] = update_dict[section]
    #             update_dict.remove_section(section)
    #
    #         # section_lower_keys_dict = dict([(i.lower(), j) for i, j in update_dict[section].items()])
    #         # if section.upper() in self._sections:
    #         #     self._sections[section.upper()].update(section_lower_keys_dict)
    #         # else:
    #         #     self._sections[section.upper()] = section_lower_keys_dict

    def read_conf_file(self, filename):
        """
        read config file with import mechanism
        @param filename: name of file to read
        @type filename: str
        """
        # conf_local = GeneralConfigParser()
        self._read_raise(filename)
        # not used feat: import before
        # import_options = conf_local._sections.pop('IMPORT', None)
        # if import_options and 'pre' in import_options:
        #     cfg_before = import_options.get('pre').split(',')
        #     for cfg_file in cfg_before:
        #         self.read_conf_file(cfg_file)
        ## self.update(conf_local)
        self.read(filename)
        # not used feat: import after
        # if import_options and 'post' in import_options:
        #     cfg_after = import_options.get('post').split(',')
        #     for cfg_file in cfg_after:
        #         self.read_conf_file(cfg_file)

    def _read_raise(self, filename):
        """
        default ConfigParser read extension raises exception when file not found
        @param filename: name of file to read
        @type filename: str
        """
        if os.path.exists(filename):
            self.log.debug('reading file %s' % (filename))
            self.read(filename)
        else:
            m_conf_path = os.getenv('SP_TEST_PATH')
            if m_conf_path is None:
                m_conf_path = os.path.join(self._get_tests_path(), 'etc')
            filename_def = os.path.join(m_conf_path, filename)
            self.log.debug('reading file %s' % (filename_def))
            if os.path.exists(filename_def):
                self.read(filename_def)
            else:
                raise ConfigFileNotFoundError('Missing files %s and %s' % (filename, filename_def))

    @staticmethod
    def _get_tests_path():
        """return path to directory modion_tests with all related structure"""
        # m_pck = __import__('tests')
        # return m_pck
        return GeneralConfigParser._get_generic_path("tests")

    @staticmethod
    def _get_generic_path(dir_to_find):
        m_pck = __import__('shop_pen_tests')
        m_path = os.path.abspath(os.path.dirname(m_pck.__file__))
        # if dir_to_find in m_path:
        #     m_path = m_path.rsplit(dir_to_find, 1)[0]
        # else:
        #     raise NotImplementedError('expected %s not found in your path %s' % (dir_to_find, m_path))
        return m_path

    # def __str__(self):
    #     result = ["[DEFAULTS]"]
    #     for k, v in self._defaults.items():
    #         result.append("%s = %s" % (k, v))
    #     result.append("")
    #     for k, v in self._sections.items():
    #         result.append("[%s]" % k)
    #         for key, value in v.items():
    #             result.append("%s = %s" % (key, value))
    #         result.append("")
    #     return "\n".join(result)

    def add_config(self, config_obj, config_name='DEFAULT'):
        self.cfgs[config_name] = config_obj

    def get_config(self, config='DEFAULT'):
        return self.cfgs[config]

    def get_re_config(self, config_name='.*'):
        return [(key, self.cfgs[key]) for key in self.cfgs.keys() if re.match(config_name, key)]
