import os
import logging
from fastapi.logger import logger
import motor.motor_asyncio

exchange_key = os.environ["EXCHANGE_KEY"]
exchange_secret = os.environ["EXCHANGE_SECRET"]
exchange_password = os.getenv("EXCHANGE_PASSWORD", None)
exchange_name = os.environ["EXCHANGE_NAME"]
exchange_env = os.environ["EXCHANGE_ENV"]
mongodb_username = os.environ["MONGODB_USERNAME"]
mongodb_password = os.environ["MONGODB_PASSWORD"]
mongodb_hostname = os.environ["MONGODB_HOSTNAME"]
mongodb_port = os.environ["MONGODB_PORT"]
logger.addHandler(logging.StreamHandler())
logger.setLevel(os.environ["LOG_LEVEL"])
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(
    f"mongodb://{mongodb_username}:{mongodb_password}@{mongodb_hostname}:{mongodb_port}/admin"
)
crypto_db = mongo_client.crypto
trading_collection = crypto_db.trading
