import json
import logging
from src.utils.string import string_utils
from datadog_api_client import Configuration, ApiClient
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.content_encoding import ContentEncoding
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem


class DatadogLogHandler(logging.StreamHandler):
    # datadog 로깅 설정
    ddsource = "ddsource"
    service = "appium_scraper"
    ddtags = {}
    hostname = f"{service}_pod"

    def __init__(self):
        logging.StreamHandler.__init__(self)

    def emit(self, record):
        self.send_log(record)

    def format_tags(self) -> str:
        return string_utils.remove_all(json.dumps(self.ddtags), ['{', '}', '"', "'"])

    def send_log(self, record):
        log_item = HTTPLogItem(
            message=self.format(record),
            ddsource=self.ddsource,
            ddtags=self.format_tags(),
            hostname=self.hostname,
            service=self.service
        )

        configuration = Configuration()
        with ApiClient(configuration) as api_client:
            api_instance = LogsApi(api_client)
            api_instance.submit_log(content_encoding=ContentEncoding.DEFLATE, body=HTTPLog([log_item]))
