from typing import List

from telegram_utilities.registry import Registry


class Handler:
    def get_sub_handler(self) -> List['Handler']:
        raise NotImplementedError

    def register(self, registry: Registry):
        raise NotImplementedError

    def get_all_handler(self) -> List['Handler']:
        result = [self]
        for sub in self.get_sub_handler():
            result += sub.get_all_handler()
        return result
