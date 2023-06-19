"""logs configuration"""
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("app_logger")

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

max_log_bytes = 1024 * 1024 * 2  # 2MB
backups = 5

# App logger config
app_logger = RotatingFileHandler('./tmp/app.log', maxBytes=max_log_bytes, backupCount=backups)
app_logger.setLevel(logging.DEBUG)
app_logger.setFormatter(formatter)

logger.addHandler(app_logger)
