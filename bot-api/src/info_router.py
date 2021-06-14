from fastapi import APIRouter
from src import properties
from src.models import Product
from src.exchangeInfo import get_exchange
from fastapi.responses import JSONResponse

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