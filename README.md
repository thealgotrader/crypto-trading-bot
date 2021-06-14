# crypto-grid-trading

Crypto bot with DCA or GRID trading strategy

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
```

## Running Program

```sh
cd crypto-bot-trading
docker-compose up
```

## Testing

- Navigate to http://localhost/
- Click on "Place A Trade" and place a trade order

## Monitor

- To monitor orders, run

```sh
docker logs monitor
```

## Disclaimer

These strategies are for educational purposes only. Do not risk money which you are afraid to lose. USE THE SOFTWARE AT YOUR OWN RISK. THE AUTHORS AND ALL AFFILIATES ASSUME NO RESPONSIBILITY FOR YOUR TRADING RESULTS.

Always start by testing strategies with a backtesting then run the trading bot in Dry-run. Do not engage money before you understand how it works and what profit/loss you should expect.
