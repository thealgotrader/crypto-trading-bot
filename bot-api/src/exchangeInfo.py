import ccxt
from src import properties


def get_exchange_keys():
    return {
        "apiKey": properties.exchange_key,
        "secret": properties.exchange_secret,
        "password": properties.exchange_password,
        "verbose": False,
    }


def get_exchange():
    exchange = getattr(ccxt, properties.exchange_name)(get_exchange_keys())
    if properties.exchange_env != "prod":
        properties.logger.debug("setting env to test")
        exchange.urls["api"] = exchange.urls["test"]
    return exchange
