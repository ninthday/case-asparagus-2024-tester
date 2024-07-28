#!/usr/bin/env python3

import logging
from logging import handlers

from agriweather.basis.abc import BaseLogger


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


class AgriLogger(BaseLogger):
    _APP_NAME = "case-tester"

    @property
    def logger_name(self):
        return self._logger_name

    @logger_name.setter
    def logger_name(self, logger_name: str):
        if logger_name != "":
            self._logger_name = logger_name.lower()
        else:
            raise ValueError("The given logger name is empty!")

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path=None):
        if not file_path:
            self._file_path = file_path
        else:
            self._file_path = "/var/log/agriweather"

    def __init__(
        self,
        logger_name: str,
        log_rootpath: str,
        level: str = "INFO",
    ) -> None:
        """
        初始化

        Args:
            logger_name (str): Logger 名稱
            log_rootpath (str): Logger 放置位置根目錄
            appname (str, optional): 應用程式名稱. Defaults to "agriweather".
            level (str, optional): Logger 記錄級別. Defaults to "INFO".
        """
        file_formatter = logging.Formatter(super()._msg_format, super()._date_format)
        self.file_path = log_rootpath
        self._logger_name = logger_name
        filename = "{filepath}/{appname}/{loggername}.log".format(
            filepath=self._file_path,
            appname=self._APP_NAME,
            loggername=self._logger_name,
        )
        log_handler = logging.handlers.RotatingFileHandler(
            filename, maxBytes=1048576, backupCount=5
        )
        log_handler.setFormatter(file_formatter)
        self._logger = logging.getLogger(self._logger_name)
        self.set_level(level)
        self._logger.addHandler(log_handler)

    def set_level(self, level: str):
        log_level = {
            "NOTSET": 0,
            "DEBUG": 10,
            "INFO": 20,
            "WARNING": 30,
            "ERROR": 40,
            "CRITICAL": 50,
        }
        if level in log_level:
            self._logger.setLevel(log_level[level])
        else:
            raise ValueError("The given log level is empty!")

    def debug(self, msg: str):
        self._logger.debug(msg)

    def info(self, msg: str):
        self._logger.info(msg)

    def warning(self, msg: str):
        self._logger.warning(msg)

    def error(self, msg: str):
        self._logger.error(msg)

    def critical(self, msg: str):
        self._logger.critical(msg)


class ErrorLogger(AgriLogger):
    def __init__(
        self, log_rootpath: str, appname: str = "agriweather", level: str = "DEBUG"
    ):
        super().__init__("error", log_rootpath, appname, level)

    def error(self, msg):
        super().error(msg)


class EventLogger(AgriLogger):
    def __init__(
        self, log_rootpath: str, appname: str = "agriweather", level: str = "DEBUG"
    ):
        super().__init__("event", log_rootpath, appname, level)

    def event(self, msg):
        self._logger.info(msg)


class UploadLogger(AgriLogger):
    def __init__(
        self,
        server_name: str,
        log_rootpath: str,
        appname: str = "agriweather",
        level: str = "INFO",
    ):
        logger_name = "{0}_upload".format(server_name)
        super().__init__(logger_name, log_rootpath, appname, level)

    def sended(self, device_id: int, device_hash: str, payload: dict, response):
        if response.ok:
            super().info(
                "[Send Successfully] Device: {0} ({1}), Response Status: {2}".format(
                    device_id, device_hash, response.status_code
                )
            )
            super().debug("[Send Successfully] Message: {0}".format(response.text))
        else:
            super().error(
                "[Send Failed] Device: {0} ({1}), Response Status: {2}".format(
                    device_id, device_hash, response.status_code
                )
            )
            super().debug("[Send Failed] Message: {0}".format(response.text))
        super().debug("Payload: {}".format(payload))


class IDViewLogger(AgriLogger):
    def __init__(self, level: str = "INFO"):
        super().__init__("idview", "/var/log/agriweather", level)
        self._step = {
            1: "Step 1: Get Nearly image timestamp",
            2: "Step 2: Get Battery",
            3: "Step 3: Get LTE Signal",
            4: "Step 4: Server Rander and Download Image",
        }

    def auth_success(self, account: str):
        msg = "Get idview-token successfully."
        super().info(msg)
        super().debug("Account: {0}".format(account))

    def auth_failed(self, account: str, http_status: int, errmsg: str):
        msg = "Get idview-token failed."
        super().error(msg)
        super().error("Account: {0}".format(account))
        super().error("HTTP Status: {0}, Error: {1}".format(http_status, errmsg))

    def step_success(self, combine_id: str, step: int, addition_msg: str):
        super().info("{0} {1} - Success.".format(combine_id, self._step[step]))
        super().debug("{0} {1}".format(combine_id, addition_msg))

    def step_error(
        self, combine_id: str, step: int, http_status: int, resp_content: str
    ):
        super().error("{0} {1} - Error.".format(combine_id, self._step[step]))
        super().error(
            "{0} HTTP Status: {1}, Response: {2}".format(
                combine_id, http_status, resp_content
            )
        )

    def step_request_except(self, combine_id: str, step: int, errmsg: str):
        super().error("{0} {1} - Exception.".format(combine_id, self._step[step]))
        super().error("{0} {1}".format(combine_id, errmsg))


@singleton
class TransferLogger(AgriLogger):
    def __init__(self, level: str = "INFO"):
        super().__init__("transfer", "/var/log/agriweather", level)

    def devices_amount(self, amount: int):
        super().info("There are {0} devices to transfer.".format(amount))

    def device_info_error(self, device_id: int, device_hash: str, msg: str):
        super().error("{0}({1}) {2}".format(device_hash, device_id, msg))

    def del_uploaded_img(self, image_path: str):
        super().info("Delete uploaded image.")
        super().debug("Delete file name: {}".format(image_path))

    def idview_auth_success(self, account: str):
        msg = "Get idview-token successfully."
        super().info(msg)
        super().debug("Account: {}".format(account))

    def idview_auth_failed(self, account: str):
        msg = "Get idview-token Failed!"
        super().error(msg)
        super().debug("Account: {}".format(account))

    def start_transfer(self):
        super().info("-------- Start to Transfer --------")

    def trans_step_status(self, message: str):
        """
        記錄轉換階段步驟狀態

        Args:
            message (str): 步驟訊息內容
        """
        super().info(message)

    def upload_success(self, combine_id: str, addition_msg: str):
        super().info("{0} Upload Success.".format(combine_id))
        super().debug("{0} Image file: {1}".format(combine_id, addition_msg))

    def upload_failed(self, combine_id: str, http_status: int, resp_content: str):
        super().error("{0} Upload Failed.".format(combine_id))
        super().debug(
            "{0} HTTP Status: {1}, Response: {2}".format(
                combine_id, http_status, resp_content
            )
        )

    def upload_except(self, combine_id: str, errmsg: str):
        super().error("{0} Upload Exception.".format(combine_id))
        super().error("{0} {1}".format(combine_id, errmsg))
