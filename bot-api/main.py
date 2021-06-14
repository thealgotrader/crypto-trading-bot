from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src import orders_router, info_router

app = FastAPI(
    title="Crypto trading bot",
    description="Automated trading bot for GRID and DCA Strategies",
    version="0.0.1",
)

origins = [
    "http://localhost",
    "http://localhost:80",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:8082",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orders_router.router)
app.include_router(info_router.router)
