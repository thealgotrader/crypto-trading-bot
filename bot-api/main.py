from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src import orders_router, info_router

app = FastAPI()

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
