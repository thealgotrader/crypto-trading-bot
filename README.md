# crypto-grid-trading

Crypto bot with DCA or GRID trading strategy

## Disclaimer

This trading bot is still in early stages of development. Please test with sandbox/paper trading accounts before using live account.

These strategies are for educational purposes only. Do not risk money which you are afraid to lose. USE THE SOFTWARE AT YOUR OWN RISK. THE AUTHORS AND ALL AFFILIATES ASSUME NO RESPONSIBILITY FOR YOUR TRADING RESULTS.

Always start by testing strategies with a backtesting then run the trading bot in Dry-run. Do not engage money before you understand how it works and what profit/loss you should expect.

## Important Notes:

- Please test this against exchange sandbox environment if sandbox environment is supported.
- Tested on Linux and Mac Environment
- Tested against Coinbasepro and Gemini Exchanges

## Prerequisites

- Docker
- Exchange API Keys

## Exchanges

- Support's all the exchanges supported by https://github.com/ccxt/ccxt

## Installation

```sh
git clone https://github.com/tradingalgobots/crypto-bot-trading
```

## Setup

Create exchange environment varibles

```sh
export EXCHANGE_KEY=changethis # change this to exchange api key
export EXCHANGE_SECRET=changethis # change this to exchange api secret
export EXCHANGE_PASSWORD=changethis # change this to exchange api password. Only some exchanges require this.
export EXCHANGE_NAME=coinbasepro # change this to exchange name
export EXCHANGE_ENV=test # Start with test and later move to prod when comfortable
export MONGODB_USERNAME=rootuser123 # change this
export MONGODB_PASSWORD=password123 # change this
export MONGODB_HOSTNAME=localhost # change this mongodb if you are docker
export MONGODB_PORT=27020 # change this this 27017 if you are using docker
```

## Running Program using docker

```sh
cd crypto-bot-trading
docker-compose up
```

## Running Program without docker

```sh
cd crypto-bot-trading
docker-compose up
```

## Testing

- Check https://github.com/tradingalgobots/crypto-bot-trading/wiki/DCA-Trade for placing DCA Trade
- Check https://github.com/tradingalgobots/crypto-bot-trading/wiki/GRID-Trade for placing GRID Trade

## Monitor

- Click Open Orders via ui

or

- To monitor orders via cli, run

```sh
docker logs monitor
```

## Issues

Report to contact@algobots.net
