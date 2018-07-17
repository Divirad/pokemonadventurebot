import logging
from typing import List

import MySQLdb

from handler.root import Root
from private import token
from database.Data import get_const_data_from_database, unload_data, CorruptedDataError
from res.Stickerpacks import init as sticker_init
from database.db import Database
from telegram_utilities.base_bot import BaseBot
from telegram_utilities.handler import Handler
from telegram_utilities.registry import Registry
from handler.goout.rpg.map import load_map

logger = logging.getLogger(__name__)


class MainBot(BaseBot):
    """Le Main Bot for le Adventure"""

    def __init__(self):
        """Initializes the Main Bot for le Adventure"""
        super().__init__(token)
        self.registry: Registry = None
        self.handlers: List[Handler] = None

    def setup(self):
        """sets all the settings in le bot up"""
        sticker_init(self.updater.bot)
        try:
            get_const_data_from_database()
        except MySQLdb.Error as err:
            logger.error("MySQL Error while loading constant data from database: {}".format(err))
            return False
        except CorruptedDataError as err:
            logger.error("Error while loading constant data from database: {}".format(err))
            return False
        self.registry = Registry()

        root_handler = Root()
        self.handlers = root_handler.get_all_handler()

        for h in self.handlers:
            h.register(self.registry)
        self.registry.create_telegram_handler(self)

        load_map()

        return True

    def unset(self):
        """Close all Databases and unload all data"""
        Database.close_all()
        unload_data()
