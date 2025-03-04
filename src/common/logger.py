import os.path
import logging
import sys
from datetime import datetime
import inspect
from common.config import common_config
from typing import Optional

logger: Optional[logging.Logger] = None

messageIgnore = ["^", " ", ":", "~"]

def setup_logger(log_file_path: str, disabled_console: bool) -> logging.Logger:
    global logger
    log_filename = os.path.join(log_file_path, f"{datetime.now().strftime('%Y_%m_%d_%H')}.log")
    handlers = [logging.FileHandler(log_filename)]
    
    if not disabled_console:
        handlers.append(logging.StreamHandler(sys.stdout))

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s" if common_config["ultraDebug"] else "%(asctime)s [%(levelname)s] %(message)s",
        handlers=handlers
    )
    logger = logging.getLogger("elyon")

    sys.stdout = LoggerWriter(logger, logging.INFO)
    sys.stderr = LoggerWriter(logger, logging.ERROR)
    
    return logger

def getLogger() -> logging.Logger:
    if logger is None:
        raise Exception("Logger is not initialized")
    return logger

class LoggerWriter:
    def __init__(self, logger: logging.Logger, log_level: int) -> None:
        self.logger = logger
        self.log_level = log_level
        self.buffer = ""

    def write(self, *messages: str) -> None:
        combined_message = " ".join(messages).strip()
        if combined_message and not combined_message in messageIgnore:
            frame = inspect.currentframe().f_back.f_back
            filename = frame.f_code.co_filename
            lineno = frame.f_lineno
            if common_config["ultraDebug"]:
                self.logger.log(self.log_level, f"[{filename}:{lineno}] {combined_message}")
            else:
                self.logger.log(self.log_level, combined_message)

    def flush(self) -> None:
        pass
