import logging
from termcolor import colored

SUCCESS = 1337
logging.addLevelName(SUCCESS, "SUCCESS")


class LogFormatter(logging.Formatter):
    def formatException(self, exc_info):
        """
        Format an exception so that it prints on a single line.
        """
        result = super(LogFormatter, self).formatException(exc_info)
        return repr(result)  # or format into one line however you want to

    def format(self, record):
        level_ptr = lambda msg: {
            SUCCESS: "[{}] {}".format(colored("+", "green", attrs=["bold"]), msg),
            logging.DEBUG: "[{}] {}".format(colored("d", "blue", attrs=["bold"]), msg),
            logging.WARNING: "[{}] {}".format(colored("!", "yellow", attrs=["bold"]), msg),
            logging.ERROR: "[{}] {}".format(colored("!", "red", attrs=["bold"]), msg),
            logging.CRITICAL: "[!] {}".format(colored(msg, "red", attrs=["bold"]))
        }.get(record.levelno, msg)
        return level_ptr(record.msg)

ch = logging.StreamHandler()
ch.setFormatter(LogFormatter())

logger = logging.getLogger("dirt")
logger.addHandler(ch)
logger.setLevel(logging.INFO)
logger.success = lambda msg: logger.log(SUCCESS, msg)


def getLogger():
    return logger


def bold(msg):
    return colored(msg, attrs=["bold"])

