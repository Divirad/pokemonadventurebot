import logging
from threading import Lock
from functools import wraps

from telegram.ext import Updater

logger = logging.getLogger(__name__)


class BaseBot:
    """This is the Base Bot who is started in PokemonAdventure.py"""
    def __init__(self, token: str):
        """Initializes StartValues"""
        self.is_started = False
        self.token = token
        self.updater = None
        self.lock = Lock()

    def run_async(self):
        """
        Function decorator that will run the function in a new thread.
        Edited original telegram decorator to support multiple dispatchers
        """
        def decorator(func):
            """Decorates"""

            @wraps(func)
            def async_func(*args, **kwargs):
                """runs Async"""
                return self.updater.dispatcher.run_async(func, *args, **kwargs)

            return async_func
        return decorator

    def setup(self) -> bool:
        """Sets the bot up"""
        raise NotImplementedError()

    def unset(self):
        """unsets the bot"""
        raise NotImplementedError()

    def start(self) -> bool:
        """starts the admin bot"""
        with self.lock:
            if not self.is_started:
                logger.info("Starting " + self.__class__.__name__ + "...")
                self.updater = Updater(self.token)
                if not self.setup():
                    self.updater = None
                    logger.error("Starting of " + self.__class__.__name__ + " failed")
                    return False
                self.updater.dispatcher.add_error_handler(BaseBot.error)
                self.updater.start_polling()
                self.is_started = True
                logger.info("Started " + self.__class__.__name__ + ".")
            return True

    def stop(self):
        """stops the admin bot"""
        with self.lock:
            if self.is_started:
                logger.info("Stopping " + self.__class__.__name__ + "...")
                self.unset()
                self.updater.is_idle = False
                self.updater.stop()
                self.updater = None
                self.is_started = False
                logger.info("Stopped " + self.__class__.__name__ + ".")

    def idle(self):
        """
        idle state
        """
        self.updater.idle()

    @staticmethod
    def error(bot, update, err):
        """handles error"""
        if update is not None:
            logger.warning('Update "%s" caused error "%s"' % (update, err))
