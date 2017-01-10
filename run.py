import asyncio
import logging
import multiprocessing
import sys

import paths
from bot import Bot


if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')

    # Setup the logging
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if len(sys.argv) > 1 and sys.argv[1] == 'debug' else logging.INFO)
    handler = logging.FileHandler(filename=paths.BOT_LOG, encoding='utf-8')
    handler.setFormatter(logging.Formatter('{asctime} {levelname} {name} {message}', style='{'))
    root_logger.addHandler(handler)

    log = logging.getLogger(__name__)
    log.info('Started with Python {0.major}.{0.minor}.{0.micro}'.format(sys.version_info))

    # Try to use uvloop, and fallback to a ProactorEventLoop on windows to be able to use subprocesses
    # See https://docs.python.org/3/library/asyncio-subprocess.html#windows-event-loop
    try:
        import uvloop
    except ImportError:
        if sys.platform == 'win32':
            asyncio.set_event_loop(asyncio.ProactorEventLoop())
    else:
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    # Create the bot
    log.info('Creating bot...')
    bot = Bot()

    # Start it
    try:
        log.info('Running bot...')
        bot.run()
    except Exception as e:
        log.exception('Exiting on exception : {}'.format(e))
    else:
        log.info('Exiting normally')
    finally:
        # Close logging handlers
        handlers = root_logger.handlers
        for handler in handlers:
            handler.close()
            root_logger.removeHandler(handler)

        exit(bot.do_restart)