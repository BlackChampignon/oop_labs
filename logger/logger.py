from datetime import datetime
import random
import re

class Logger:
    # Log levels (static)
    priorities = {
        "TRACE": 0,
        "INFO": 1,
        "WARN": 2,
        "ERROR": 3,
    }
    level = "INFO"

    format = "[%t] [%l] %n: %m"

    # this one is static too ig
    RANDOM_MESSAGES = [
        ("Entering method", "Step completed", "Checking internal state"),
        ("Operation completed", "Everything looks good", "Here is your result"),
        ("Something unexpected happened", "Value looks unusual", "Check the input"),
        ("Operation failed", "Invalid input", "Something went wrong"),
    ]

    def __init__(self, name):
        self.name = name

    @staticmethod
    def set_level(new_level):
        if new_level not in Logger.priorities:
            raise ValueError("Unknown log level")
        Logger.level = new_level

    @staticmethod
    def set_format(new_format):
        Logger.format = new_format

    def log(self, msg_level, message):
        if msg_level not in Logger.priorities:
            raise ValueError("Unknown log level")

        if Logger.priorities[msg_level] < Logger.priorities[Logger.level]:
            return

        values = {
            "%t": datetime.now().strftime("%H:%M:%S"),
            "%m": message,
            "%n": self.name,
            "%l": msg_level,
        }

        if "%r" in Logger.format:
            index = Logger.priorities[msg_level]
            values["%r"] = random.choice(Logger.RANDOM_MESSAGES[index])

        output = re.sub(
            r"%[tmnlr]",
            lambda match: values[match.group()],
            Logger.format,
        )
        print(output)

    def trace(self, message):
        self.log("TRACE", message)

    def info(self, message):
        self.log("INFO", message)

    def warn(self, message):
        self.log("WARN", message)

    def error(self, message):
        self.log("ERROR", message)
