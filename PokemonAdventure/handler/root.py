from telegram_utilities.handler import Handler
from telegram_utilities.registry import Registry
from typing import List

from handler import start, mainmenu
from handler.goout import center
from handler.profile import _rootprofile
from handler.info import _rootinfo
from handler.daily import _rootdaily
from handler.goout import _rootgoout


class Root(Handler):
    def get_sub_handler(self) -> List['Handler']:
        return [
                start.Start(),
                mainmenu.Menu(),
                _rootprofile.RootProfile(),
                _rootgoout.RootGoOut(),
                _rootdaily.RootDaily(),
                _rootinfo.RootInfo()
                ]

    def register(self, registry: Registry):
        pass