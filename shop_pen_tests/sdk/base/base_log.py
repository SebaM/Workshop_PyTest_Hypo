import functools
import logging
import time
import warnings

class LoggingObject(object):
    """base T! object"""
    def __init__(self):
        module_name = self.__module__
        if module_name == '__main__':
            module_name = 't!.main_file'
        self.log = logging.getLogger('%s.%s' % (module_name, self.__class__.__name__))


class WaitUntilException(Exception):
    def __init__(self, message, timeout, time_sleep, expected_return, method_name, args, kwargs, ret_history):
        self.message = message
        self.timeout = timeout
        self.time_sleep = time_sleep
        self.expected_return = expected_return
        self.method_name = method_name
        self.args = args
        self.kwargs = kwargs
        self.ret_history = ret_history
        self.last_ret = ret_history[-1] if ret_history else None

    def __str__(self):
        msg = self.message
        msg += "\n WaitUntil(%s, %s, %s, %s)(%s, %s, %s) = " % (
            self.message, self.timeout, self.time_sleep, self.expected_return,
            self.method_name, self.args, self.kwargs)
        try:
            msg += "%s" % self.last_ret
            msg += "\n historical values %s" % self.ret_history
        finally:
            return msg


class WaitUntil(LoggingObject):
    def __init__(self, exception_msg='Condition was not met, timeout', timeout=20, time_sleep=1, expected_return=None,
                 validate_return_method=None):
        """
        @param exception_msg: exception text message
        @param timeout: timeout
        @param time_sleep: time sleep between each execution
        @param expected_return: * when expected_return == None then waits until the method returns positive value
                                * when expected_return != None then waits until the method returns expected_return value
        @param validate_return_method: * wait until the method returns positive value on result of method
                                       * used only if expected_return is None
        @return: result of method(*args, **kwargs)
        """
        super(WaitUntil, self).__init__()
        self.exception_msg = exception_msg
        self.timeout = timeout
        self.time_sleep = time_sleep
        self.expected_return = expected_return
        self.validate_return_method = validate_return_method

    def __call__(self, method, *args, **kwargs):
        start_time = time.time()
        ret_history = []
        self.log.debug("Max wait time, %d" % self.timeout)
        while start_time + self.timeout > time.time():
            ret = method(*args, **kwargs)
            ret_history.append(ret)

            if self.expected_return is None:
                if self.validate_return_method is not None:
                    if self.validate_return_method(ret):
                        self.log.info("%s: ret = %s" % (method.__name__, ret))
                        return ret
                elif ret:
                        self.log.info("%s: ret = %s" % (method.__name__, ret))
                        return ret
            else:
                if ret == self.expected_return:
                    self.log.info("%s: ret = %s" % (method.__name__, ret))
                    return ret
            time.sleep(self.time_sleep)
            self.log.info("Retry (time left: %d), %s: ret = %s" % (start_time + self.timeout - time.time(),
                                                                   method.__name__, ret))

        else:
            raise WaitUntilException(self.exception_msg, self.timeout, self.time_sleep, self.expected_return,
                                     method.__name__, args, kwargs, ret_history)


def wait_until(timeout, time_sleep, method, *args, **kwargs):
    try:
        WaitUntil(timeout=timeout, time_sleep=time_sleep)(method, *args, **kwargs)
        return True
    except WaitUntilException:
        return False


def retry(except_list=[], polling_interval=0.5, polling_timeout=60):
    def decorator(wrapped):
        def wrapper(*args, **kwargs):
            log = logging.getLogger('%s.%s' % ('m!.sdk.base.base_log', __name__))
            timeout = kwargs.pop('timeout') if 'timeout' in kwargs else polling_timeout
            ret_history = []
            start_time = time.time()
            while (time.time() - start_time) < timeout:
                try:
                    log.debug("starting %s.%s method with args = %s and kwargs = %s" % (
                        wrapped.__module__, wrapped.__name__, args, kwargs))
                    result_w = wrapped(*args, **kwargs)
                    log.debug("%s.%s method finished, result_w = %s" % (wrapped.__module__, wrapped.__name__, result_w))
                    return result_w
                except Exception as _exp:
                    for rtr_str in except_list:
                        if rtr_str in str(_exp) or (hasattr(_exp, 'fault') and rtr_str in str(_exp.fault)):
                            log.info("sleeping ... %f s" % polling_interval)
                            ret_history.append(_exp)
                            break
                    else:
                        raise
                time.sleep(polling_interval)
            else:
                raise WaitUntilException('Too many retries, timeout', polling_timeout, polling_interval,
                                         str(except_list), __name__, args, kwargs, ret_history)

        result = wrapper
        result.__doc__ = wrapped.__doc__
        result.__name__ = wrapped.__name__
        result.__module__ = wrapped.__module__
        return result

    return decorator


def deprecated(func):
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn("Call to deprecated function %s.%s." % (func.__module__, func.__name__),
                      category=DeprecationWarning, stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)
    return new_func