#!/usr/bin/env python3.6
from time import sleep
from signal import signal, SIGINT, SIGTERM, SIGABRT

from admin.admin_bot import AdminBot


def main():
    """
    Main-Function
    """
    admin_bot = AdminBot()
    admin_bot.start()

    def signal_handler(signum, frame):
        """
        TODO Docs
        """
        nonlocal is_idle, admin_bot
        admin_bot.stop()
        is_idle = False

    for sig in (SIGINT, SIGTERM, SIGABRT):
        signal(sig, signal_handler)

    # auto start
    try:
        from private import auto_start
    except ImportError:
        auto_start = False
    if auto_start:
        admin_bot.mainBot.start()

    is_idle = True

    while is_idle:
        sleep(1)


if __name__ == '__main__':
    main()
