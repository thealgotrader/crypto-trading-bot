from fastapi import APIRouter
from src.models import Trade
from src import properties
from src.exchangeInfo import get_exchange
from fastapi.responses import JSONResponse

router = APIRouter()


@router.delete("/orders")
async def delete_open_orders():
    try:
        exchange = get_exchange()
        open_status_orders = properties.trading_collection.find({"open_status": "open"})
        for order in await open_status_orders.to_list(length=1000):
            exchange.cancel_order(order["open_order_id"])
            await properties.trading_collection.delete_one(
                {"open_order_id": order["open_order_id"]}
            )
        close_status_orders = properties.trading_collection.find(
            {"close_status": "open"}
        )
        for order in await close_status_orders.to_list(length=1000):
            exchange.cancel_order(order["close_order_id"])
            await properties.trading_collection.delete_one(
                {"close_order_id": order["close_order_id"]}
            )
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"{e}"})


@router.get("/orders")
async def get_open_orders():
    try:
        response = []
        open_status_orders = properties.trading_collection.find({"open_status": "open"})
        for order in await open_status_orders.to_list(length=1000):
            response.append(
                {
                    "product": order["product_id"],
                    "price": order["open_price"],
                    "side": order["open_side"],
                    "size": order["size"],
                    "id": order["open_order_id"],
                    "id_type": "open_order_id",
                }
            )
        close_status_orders = properties.trading_collection.find(
            {"close_status": "open"}
        )
        for order in await close_status_orders.to_list(length=1000):
            response.append(
                {
                    "product": order["product_id"],
                    "price": order["close_price"],
                    "side": order["close_side"],
                    "size": order["size"],
                    "id": order["close_order_id"],
                    "id_type": "close_order_id",
                }
            )
        return response
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"{e}"})


@router.delete("/order/{id}/{type}")
async def delete_order(id, type):
    try:
        exchange = get_exchange()
        exchange.cancel_order(id)
        await properties.trading_collection.delete_one({type: id})
        return {"success": True}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"{e}"})


@router.post("/order")
async def create_order(trades: Trade):
    exchange = get_exchange()
    response = []
    try:
        for count in range(0, trades.count):
            if trades.side == "buy":
                open_price = trades.price - count * trades.diff
                if trades.strategy == "GRID":
                    close_price = open_price + trades.profit
                if trades.strategy == "DCA":
                    close_price = trades.price + trades.profit
                open_side = "buy"
                close_side = "sell"
            if trades.side == "sell":
                open_price = trades.price + count * trades.diff
                if trades.strategy == "GRID":
                    close_price = open_price - trades.profit
                if trades.strategy == "DCA":
                    close_price = trades.price - trades.profit
                open_side = "sell"
                close_side = "buy"
            request = {
                "size": trades.size,
                "open_price": open_price,
                "side": trades.side,
                "product_id": trades.symbol,
                "exchange": properties.exchange_name,
            }
            request["reopen"] = False
            request["close_price"] = close_price
            request["open_status"] = "open"
            request["close_status"] = "not submitted"
            order = exchange.create_order(
                trades.symbol, "limit", trades.side, trades.size, open_price
            )
            request["open_order_id"] = order["id"]
            request["open_side"] = open_side
            request["close_side"] = close_side
            result = await properties.trading_collection.insert_one(request)
            properties.logger.info(f"id: {str(result.inserted_id)}")
            request["db_id"] = str(result.inserted_id)
            response.append(
                {
                    "order_id": order["id"],
                    "side": trades.side,
                    "size": trades.size,
                    "open_price": open_price,
                    "close_price": close_price,
                    "product_id": trades.symbol,
                }
            )
        return response
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"{e}"})
