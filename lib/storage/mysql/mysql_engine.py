# -*- coding: utf-8 -*-

# Copyright (c) 2018 Michael Green
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pymysql as MySQLdb

from ..storage_engine import StorageEngine
from .entity_interface import EntityInterface as Entity
from config import LOGGER as logger
import config as app

class MySqlEngine(StorageEngine):
    """ Adapter to connect to MySQL db """

    def __init__(self, host, user, password, schema, port = 3306):
        """ MySQL authentication details """
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.schema = schema

    def get(self, entry):
        """
        fetch from storage,
        updating entry with data fetched
        and returning entry id
        """

        # force entity object
        if not isinstance(entry, Entity):
            raise TypeError("Entry must be of type Entity")

        # fetch entry from db
        with self._connect() as cur:
            query = entry.select_query()

            logger.debug('Getting object from db')
            logger.debug(query)

            count = cur.execute(query)

            # if entry exists update given entry
            if count > 0:
                data = self._toJson(cur.description, cur.fetchone())
                entry.update(**data)
                key = entry.primary_key()

            else: key = -1

        return key

    def get_all(self, entries):
        """ fetch all from storage """

        # force entries as list
        if not isinstance(entries, list):
            raise TypeError("Entities must be of type list")

        # get each
        for entry in entries:
            self.get(entry)

        return entries

    def add(self, entry):
        """add new entry to database and return new key"""

        # force entity object
        if not isinstance(entry, Entity):
            raise TypeError("Entry must be of type Entity")

        # add to db
        key = self._execute(entry.insert_query())

        # update entry
        if key != -1: entry.set_primary_key(key)

        return key

    def add_all(self, entries):
        """ add new entries (list) to relation """

        # force entries as list
        if not isinstance(entries, list):
            raise TypeError("Entities must be of type list")

        for entry in entries:
            # force entity object
            if not isinstance(entry, Entity): raise TypeError("Entry must be of type Entity")

            # add entry
            self.add(entry)

    def add_if_not_exists(self, entry):
        """
        if entry exists in database return its id else add it
        :return primary_key
        """

        # force entity object
        if not isinstance(entry, Entity):
            raise TypeError("Entry must be of type Entity")

        # make a copy to avoid change the origin object
        entry_copy = entry.copy()

        # get object and if exists return
        key = self.get(entry_copy)

        if key == -1: return self.add(entry)

    def remove(self, entry):
        """
        remove entry from relation
        :return removed entry
        """
        # force entity object
        if not isinstance(entry, Entity):
            raise TypeError("Entry must be of type Entity")

        # saving removed entry to object
        data = entry.copy()
        key = self.get(data)

        # no such key
        if key == -1:
            raise ValueError("entry does not exist")

        # delete entry
        with self._connect() as cur:
            conn = cur.connection
            query = entry.remove_query()

            logger.debug("deleting entry")
            logger.debug(query)

            cur.execute(query)
            conn.commit()

        # return removed entry
        return data

    def remove_all(self, entries):
        """
        remove list of entries
        :return removed entries
        """

        # force entries as list
        if not isinstance(entries, list):
            raise TypeError("Entities must be of type list")

        # removing entries
        removed = []
        for entry in entries: removed.append(self.remove(entry))

        return removed

    def update(self, entry):
        """ update entry data """

        # force entity object
        if not isinstance(entry, Entity):
            raise TypeError("Entry must be of type Entity")

        # update entry
        self._execute(entry.update_query())

    def update_all(self, entries):
        """ update all entries (list) """

        # force entries as list
        if not isinstance(entries, list):
            raise TypeError("Entities must be of type list")

        for entry in entries: self.update(entry)

    def update_if_exists_else_add(self, entry):
        """ update entry if exists, if not add it to storage """

        # force entity object
        if not isinstance(entry, Entity):
            raise TypeError("Entry must be of type Entity")

        key = self.get(entry)

        # if not exist add it
        if key == -1: return self.add(entry)

        # else update entry and return key
        self.update(entry)
        return entry.primary_key()

    def truncate(self):
        """ remove all entries from storage """

        # TODO fix query to truncate tables
        query = app.TRUNCATE_QUERY

        with self._connect() as cur:

            # getting connection object
            conn = cur.connection

            logger.debug("Execute query:")
            logger.debug(query)
            logger.debug(conn.__dict__)

            try:

                # execute & commit query
                cur.execute(query)
                conn.commit()

            except Exception as e:
                # rollback if error
                conn.rollback()
                logger.error(e)

    def live_update(self, relation, override = True):
        """ add more entries to relation """

        #TODO implement
        pass

    def _execute(self, query):
        """ execute query """

        # connect to db
        with self._connect() as cur:

            # getting connection object
            conn = cur.connection

            logger.debug("Execute query:")
            logger.debug(query)
            logger.debug(conn.__dict__)

            try:

                # execute & commit query
                cur.execute(query)
                conn.commit()

                # return last_id
                return cur.lastrowid

            except Exception as e:
                # rollback if error
                conn.rollback()
                logger.error(e)

        return -1

    def _connect(self):
        """ return connect to database """
        return MySQLdb.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            db=self.schema,
            port=self.port
        )

    def _toJson(self, desc, _tuple):
        """ tuple from select query to json """
        return dict(zip([_desc[0] for _desc in desc], _tuple))