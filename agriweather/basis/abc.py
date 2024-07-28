#!/usr/bin/env python3

from abc import ABCMeta, abstractmethod


class BaseLogger(metaclass=ABCMeta):
    _msg_format = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
    _date_format = "%Y-%m-%d %H:%M:%S"
    _logger_name = ""
    _file_path = ""

    @property
    @abstractmethod
    def logger_name(self):
        return self._logger_name

    @logger_name.setter
    @abstractmethod
    def logger_name(self, logger_name):
        self._logger_name = logger_name

    @property
    @abstractmethod
    def file_path(self):
        return self._file_path

    @file_path.setter
    @abstractmethod
    def file_path(self, file_path=None):
        self._file_path = file_path


class BaseCrawler(metaclass=ABCMeta):
    _base_url = ""

    @property
    @abstractmethod
    def base_url(self):
        return self._base_url

    @base_url.setter
    @abstractmethod
    def base_url(self, base_url):
        self._base_url = base_url

    @abstractmethod
    def run(self):
        return NotImplemented


class BaseRDB(metaclass=ABCMeta):
    _db_name = None

    @property
    @abstractmethod
    def db_name(self):
        return self._db_name


class BaseServer(metaclass=ABCMeta):
    @property
    @abstractmethod
    def _base_url(self):
        pass

    @property
    @abstractmethod
    def _server_name(self):
        pass

    @property
    @abstractmethod
    def _ssl_verify(self):
        pass

    @abstractmethod
    def send_data(self, wand):
        """傳回 Wand 感測的數值至伺服器"""
        return NotImplemented


class BaseDevice(metaclass=ABCMeta):
    @property
    @abstractmethod
    def _device_id(self):
        pass

    @property
    @abstractmethod
    def _device_hash(self):
        pass

    @property
    @abstractmethod
    def _device_token(self):
        pass

    @property
    @abstractmethod
    def _data_timestamp(self):
        pass

    @property
    @abstractmethod
    def _data(self):
        pass

    @property
    @abstractmethod
    def _params(self):
        pass

    @abstractmethod
    def get_data(self):
        """
        傳回 Wand 感測的數值
        """
        return NotImplemented

    @abstractmethod
    def get_filtered_data(self):
        """
        取得依照 params 過濾後的 data
        """
        return NotImplemented
