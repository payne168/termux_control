import logging
from logging import handlers
import os

log_dir = 'log'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.root.setLevel(logging.NOTSET)

logger = logging.getLogger(__name__)

# Create formatter and add it to handlers
formatter = logging.Formatter('[%(asctime)s %(module)s %(levelname)s] %(message)s')

# Create handlers
console = logging.StreamHandler()
console.setFormatter(formatter)
console.setLevel(logging.INFO)

file = handlers.TimedRotatingFileHandler(os.path.join(log_dir, 'app.log'), 'd', 1, 7)
file.setFormatter(formatter)
file.setLevel(logging.INFO)

# Add handlers to the logger
logger.addHandler(console)
logger.addHandler(file)
