import logging
import traceback
import json_log_formatter
from pathlib import Path

from src.utils.log.domain.datadog_log_handler import DatadogLogHandler

json_handler = logging.FileHandler(filename=Path('./external-files/logs/log.json'))
json_handler.setFormatter(json_log_formatter.VerboseJSONFormatter())
logging.getLogger().addHandler(json_handler)

datadog_handler = DatadogLogHandler()
datadog_handler.setFormatter(json_log_formatter.VerboseJSONFormatter())
logging.getLogger().addHandler(datadog_handler)


class CustomLogger:
    logger = logging.Logger
    kwargs = {}

    def __init__(self):
        self.logger = logging.getLogger()

    def error(self, message: str = '', exception: Exception = None, *args, **kwargs):
        self.add_empty_extra()
        if exception is not None:
            self.add_exception_extra(exception)
        self.kwargs.update(**kwargs)
        CustomLogger().logger.setLevel(logging.ERROR)
        self.logger.error(message, *args, **self.kwargs)

    def warn(self, message: str = '', exception: Exception = None, *args, **kwargs):
        self.add_empty_extra()
        if exception is not None:
            self.add_exception_extra(exception)
        self.kwargs.update(**kwargs)
        CustomLogger().logger.setLevel(logging.WARN)
        self.logger.warn(message, *args, **self.kwargs)

    def info(self, message: str = '', *args, **kwargs):
        self.add_empty_extra()
        self.kwargs.update(**kwargs)
        CustomLogger().logger.setLevel(logging.INFO)
        self.logger.info(message, *args, **self.kwargs)

    def add_empty_extra(self):
        if 'extra' not in self.kwargs.keys():
            self.kwargs['extra'] = {}

    def add_exception_extra(self, exception: Exception):
        self.kwargs['extra']['exceptionName'] = exception.__class__.__name__
        self.kwargs['extra']['exceptionMessage'] = str(exception)
        self.kwargs['extra']['exceptionStackTrace'] = "".join(
            traceback.TracebackException.from_exception(exception).format())
