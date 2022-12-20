import os
from dotenv import load_dotenv
import logging

load_dotenv()


logFormatter = logging.Formatter(fmt='%(name)s:%(levelname)s:%(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
consoleHandler.setFormatter(logFormatter)

logger.addHandler(consoleHandler)


tweepy_config = dict(
    CONSUMER_KEY=os.getenv("CONSUMER_KEY"),
    CONSUMER_SECRET=os.getenv("CONSUMER_SECRET"),
    ACCESS_TOKEN=os.getenv("ACCESS_TOKEN"),
    ACCESS_TOKEN_SECRET=os.getenv("ACCESS_TOKEN_SECRET")
)

cover = "https://pbs.twimg.com/media/FkctbK8XEAAHCu-?format=jpg&name=medium"
