#!/usr/bin/env python3

from contextlib import closing

import MySQLdb
import MySQLdb.cursors

from agriweather.basis.abc import BaseRDB
from agriweather.common.logging import AgriLogger


class RDBStorage(BaseRDB):
    _db_host = ""
    _db_port = 3306
    _db_user = ""
    _db_password = ""
    _db_name = ""

    def __init__(
        self,
        db_host: str,
        db_port: int,
        db_user: str,
        db_password: str,
        db_name: str,
        log_path: str,
        log_level: str,
    ) -> None:
        self._db_host = db_host
        self._db_port = int(db_port)
        self._db_user = db_user
        self._db_password = db_password
        self._db_name = db_name
        self._logger = AgriLogger(self.__class__.__name__, log_path, log_level)

        self._connect()

    @property
    def db_name(self):
        return self._db_name

    def _connect(self):
        try:
            self._conn = MySQLdb.connect(
                host=self._db_host,
                port=self._db_port,
                user=self._db_user,
                passwd=self._db_password,
                db=self._db_name,
                charset="utf8",
                cursorclass=MySQLdb.cursors.DictCursor,
            )
        except Exception as err:
            self._logger.error("Database connection fail!")
            self._logger.debug(
                "Exception: [{db_name}] connection error. {err_msg}.".format(
                    db_name=self._db_name,
                    err_msg=repr(err),
                )
            )

    def show_data(self, query: str):
        try:
            with closing(self._conn.cursor()) as cur:
                cur.execute(query)
                result = cur.fetchone()
        except Exception as err:
            self._logger.error(
                "Exception: [{db_name}] show_data function error. {err_msg}. SQL Statement: {sql_stmt}.".format(
                    db_name=self._db_name,
                    err_msg=repr(err),
                    sql_stmt=query,
                )
            )
        return result

    def index_many_data(self, query: str, offset: int, rows: int) -> list:
        try:
            query = "{qstr} LIMIT {offset},{rows}".format(
                qstr=query, offset=int(offset), rows=int(rows)
            )
            with closing(self._conn.cursor()) as cur:
                cur.execute(query)
                result = cur.fetchall()
        except Exception as err:
            self._logger.error(
                "Exception: [{db_name}] index_many_data function error. {err_msg}. SQL Statement: {sql_stmt}.".format(
                    db_name=self._db_name,
                    err_msg=repr(err),
                    sql_stmt=query,
                )
            )
        return result

    def index_all_data(self, query: str):
        try:
            with closing(self._conn.cursor()) as cur:
                cur.execute(query)
                result = cur.fetchall()
        except Exception as err:
            self._logger.error(
                "Exception: [{db_name}] index_all_data function error. {err_msg}. SQL Statement: {sql_stmt}.".format(
                    db_name=self._db_name,
                    err_msg=repr(err),
                    sql_stmt=query,
                )
            )
        return result

    def store_one(self, query: str, params: tuple):
        try:
            pass
        except Exception as err:
            self._logger.error(
                "Exception: [{db_name}] store_one function error. {err_msg}. SQL Statement: {sql_stmt}. Params: {params}".format(
                    db_name=self._db_name,
                    err_msg=repr(err),
                    sql_stmt=query,
                    params=params,
                )
            )

    def store_many(self, query: str, params: tuple):
        try:
            pass
        except Exception as err:
            self._logger.error(
                "Exception: [{db_name}] store_many function error. {err_msg}. SQL Statement: {sql_stmt}. Params: {params}".format(
                    db_name=self._db_name,
                    err_msg=repr(err),
                    sql_stmt=query,
                    params=params,
                )
            )

    def update_data(self, query: str, params: tuple):
        try:
            pass
        except Exception as err:
            self._logger.error(
                "Exception: [{db_name}] update_data function error. {err_msg}. SQL Statement: {sql_stmt}. Params: {params}".format(
                    db_name=self._db_name,
                    err_msg=repr(err),
                    sql_stmt=query,
                    params=params,
                )
            )

    def destroy_data(self, query: str) -> bool:
        try:
            with closing(self._conn.cursor()) as cur:
                cur.execute(query)
                self._conn.commit()
            return True
        except Exception as err:
            self._logger.error(
                "Exception: [{db_name}] destroy_data function error. {err_msg}. SQL Statement: {sql_stmt}.".format(
                    db_name=self._db_name,
                    err_msg=repr(err),
                    sql_stmt=query,
                )
            )
            return False

    def _disconnect(self):
        if self._conn.open:
            self._conn.close()

    def __del__(self):
        self._disconnect()
