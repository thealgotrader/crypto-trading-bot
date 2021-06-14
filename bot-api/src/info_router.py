from fastapi import APIRouter
from src import properties
from src.models import Product
from src.exchangeInfo import get_exchange
from fastapi.responses import JSONResponse
import pandas as pd
import requests
import concurrent.futures
import datetime

router = APIRouter()


def sortProducts(elem):
    sort_value = elem.split("/")[0]
    return sort_value


@router.get("/products")
async def products():
    try:
        exchange = get_exchange()
        products = exchange.fetch_markets()
        response = []
        for product in products:
            response.append(product["symbol"])
        response.sort(key=sortProducts)
        return response
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"{e}"})


@router.post("/quote")
async def tickers(product: Product):
    try:
        properties.logger.info(product)
        exchange = get_exchange()
        return exchange.fetch_ticker(product.symbol)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"{e}"})


### place to get data for later
def stats(id):
    response = requests.get(f"https://api.pro.coinbase.com/products/{id}/stats")
    return response.json()


def ohlcv(id):
    response = requests.get(
        f"https://api.pro.coinbase.com/products/{id[0]}/candles?granularity={id[1]}"
    )
    df = pd.DataFrame.from_records(
        response.json(), columns=["time", "low", "high", "open", "close", "volume"]
    )
    datetime_time = datetime.datetime.fromtimestamp(df["time"].iloc[-1])
    properties.logger.info(f"granularity: {id[1]} datetime_time: {datetime_time}")
    return {
        "id": id[0],
        "granularity": id[1],
        "high": df["high"].max(),
        "low": df["low"].min(),
        "date": datetime_time,
    }


@router.get("/history")
async def history():
    symbols = [
        ["BTC-USD", 60],
        ["BTC-USD", 300],
        ["BTC-USD", 900],
        ["BTC-USD", 3600],
        ["BTC-USD", 21600],
        ["BTC-USD", 86400],
    ]
    response = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(ohlcv, symbol): symbol for symbol in symbols}
        for future in concurrent.futures.as_completed(futures):
            try:
                data = future.result()
                response.append(data)
            except Exception as e:
                # print(f"data: {data}")
                print(f"Exception: {e} ")
                return None
    return response