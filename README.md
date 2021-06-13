# crypto-grid-trading

Crypto bot with DCA or GRID trading strategy

## Prerequisites

- Docker
- Exchange API Keys

## Exchanges

- Support all the exchanges supported by https://github.com/ccxt/ccxt

## Installation

```sh
git clone https://github.com/tradingalgobots/crypto-bot-trading
```

## Setup

Create exchange environment varibles.

```sh
export exchange_key=changethis # change this to exchange api key
export exchange_secret=changethis # change this to exchange api secret
export exchange_password=changethis # change this to exchange api password. Only some exchanges require this.
export exchange_name=coinbasepro # change this to exchange name
export exchange_env=test # Start with test and later move to prod when comfortable
```

## Running Program

```sh
cd crypto-bot-trading
docker-compose up
```

## Testing

- Navigate to http://localhost/
- Click on "Place A Trade" and place a trade order
