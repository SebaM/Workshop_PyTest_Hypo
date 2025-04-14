import logging


class SP_Logging(object):

    def __init__(self):
        module_name = self.__module__
        if module_name == '__main__':
            module_name = 't!.main_file'
        self.log = logging.getLogger('%s.%s' % (module_name, self.__class__.__name__))

    # @staticmethod
    # def get_logger(logger_name):
    #     return Logging(logger_name).log
    #
    # @staticmethod
    # def get_object_logger(_object):
    #     return Logging.get_logger('%s.%s' % (_object.__module__, _object.__class__.__name__))
