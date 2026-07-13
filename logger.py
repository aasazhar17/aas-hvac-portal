import logging
from logging.handlers import RotatingFileHandler
import os

# Configure log formatting
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(log_format)

# Configure log file handler with 5MB rotation
log_file = os.path.join(os.path.dirname(__file__), "app.log")
file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8")
file_handler.setFormatter(formatter)

# Setup root application logger
logger = logging.getLogger("aas_hvac")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

# Console logger stream fallback
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
