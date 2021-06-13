from src.exchangeInfo import get_exchange
from src import properties
import asyncio
import time


async def get_open_working_orders():
    properties.logger.info("working on open working orders")
    orders = properties.trading_collection.find({"open_status": "open"})
    for order in await orders.to_list(length=1000):
        properties.logger.debug(f"order: {order}")
        exchange_name = order["exchange"]
        open_order_id = order["open_order_id"]
        properties.logger.debug(f"exchange_name: {exchange_name}")
        exchange = get_exchange()
        order_status = exchange.fetch_order(open_order_id)
        properties.logger.info(f"checking status for {open_order_id}")
        properties.logger.debug(f"order_status: {order_status}")
        properties.logger.info(f"status: {order_status['status']}")
        if order_status["amount"] == order_status["filled"]:
            close_order = exchange.create_order(
                order["product_id"],
                "limit",
                order["close_side"],
                order["size"],
                order["close_price"],
            )
            properties.logger.debug(f"close_order: {close_order}")
            close_order_id = close_order["id"]
            properties.logger.debug(f"close_order_id: {close_order_id}")
            myquery = {"_id": order["_id"]}
            newvalues = {
                "$set": {
                    "open_status": "filled",
                    "close_status": "open",
                    "close_order_id": close_order_id,
                }
            }
            await properties.trading_collection.update_one(myquery, newvalues)


async def get_close_working_orders():
    properties.logger.info("working on close working orders")
    orders = properties.trading_collection.find(
        {
            "close_status": "open",
            "open_status": "filled",
        }
    )
    for order in await orders.to_list(length=1000):
        properties.logger.debug(f"order: {order}")
        exchange_name = order["exchange"]
        close_order_id = order["close_order_id"]
        properties.logger.debug(f"exchange_name: {exchange_name}")
        exchange = get_exchange()
        order_status = exchange.fetch_order(close_order_id)
        properties.logger.info(f"checking status for {close_order_id}")
        properties.logger.debug(f"order_status: {order_status}")
        properties.logger.info(f"status: {order_status['status']}")
        if order_status["amount"] == order_status["filled"]:
            myquery = {"_id": order["_id"]}
            newvalues = {
                "$set": {
                    "close_status": "filled",
                }
            }
            await properties.trading_collection.update_one(myquery, newvalues)


async def get_reopen__orders():
    properties.logger.info("working on reopen working orders")
    orders = properties.trading_collection.find(
        {"open_status": "filled", "close_status": "filled", "reopen": False}
    )
    for order in await orders.to_list(length=1000):
        properties.logger.debug(f"order: {order}")
        exchange_name = order["exchange"]
        exchange = get_exchange()
        open_order = exchange.create_order(
            order["product_id"],
            "limit",
            order["open_side"],
            order["size"],
            order["open_price"],
        )
        properties.logger.info(f"submitted order: {open_order}")
        open_order_id = open_order["id"]
        reopen_order = {
            "size": order["size"],
            "open_price": order["open_price"],
            "side": order["side"],
            "product_id": order["product_id"],
            "exchange": exchange_name,
            "reopen": False,
            "close_price": order["close_price"],
            "open_status": "open",
            "close_status": "not submitted",
            "open_order_id": open_order_id,
            "open_side": order["open_side"],
            "close_side": order["close_side"],
            "close_order_id": "",
        }
        await properties.trading_collection.insert_one(reopen_order)
        myquery = {"_id": order["_id"]}
        newvalues = {
            "$set": {
                "reopen": True,
            }
        }
        await properties.trading_collection.update_one(myquery, newvalues)


while True:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_open_working_orders())
    time.sleep(1)
    loop.run_until_complete(get_close_working_orders())
    time.sleep(1)
    loop.run_until_complete(get_reopen__orders())
    time.sleep(1)
