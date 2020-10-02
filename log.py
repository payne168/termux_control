import logging
from logging import handlers

logging.root.setLevel(logging.NOTSET)

logger = logging.getLogger(__name__)

# Create formatter and add it to handlers
formatter = logging.Formatter('[%(asctime)s %(module)s %(levelname)s] %(message)s')

# Create handlers
console = logging.StreamHandler()
console.setFormatter(formatter)
console.setLevel(logging.INFO)

file = handlers.TimedRotatingFileHandler('log/app.log', 'd', 1, 7)
file.setFormatter(formatter)
file.setLevel(logging.INFO)

# Add handlers to the logger
logger.addHandler(console)
logger.addHandler(file)
