import csv
import time
import numpy as np
from datetime import datetime
from config import USERNAME, PASSWORD, getPath
from Robinhood import Robinhood

class TradeInfo():
    prices = []
    buyPrices = []
    sellPrices = []
    isHeld = False
    preMin = 10000
    preMax = 0


class RobinhoodTrader():
    robin = None
    instrumentsToStockMap = {}

    def __init__(self):
        self.robin = Robinhood()
        print('log in with username: {}'.format(USERNAME))
        self.robin.login(USERNAME, PASSWORD)

    def logOut(self):
        self.robin.logout()

    def getInstrumentByStock(self, stock):
        if stock not in self.instrumentsToStockMap:
            self.instrumentsToStockMap[stock] = self.robin.instruments(stock)[0]['url']
        return {'symbol': stock, 'url': self.instrumentsToStockMap[stock]}

    def getLastPrice(self, stock):
        # return np.random.normal(63.0, 0.3)
        res = self.robin.quote_data(stock)
        return float(res['last_trade_price'])

    def buyStock(self, stock, quantity=1, price=0.0):
        instrument = self.getInstrumentByStock(stock)
        # {id, fees, state, cancel, reject_reason, ...}
        return self.robin.place_buy_order(instrument, quantity, price)

    def sellStock(self, stock, quantity=1, price=0.0):
        instrument = self.getInstrumentByStock(stock)
        return self.robin.place_sell_order(instrument, quantity, price)

    def cancelOrder(self, orderId):
        return self.robin.cancel_order(orderId)

    def recordQuote(self, stockList, intervalInSecond=5):
        stockToFileWriterMap = {}
        for stock in stockList:
            stockToFileWriterMap[stock] = csv.writer(open(getPath(stock) + 'price.csv', 'a', 0))
        while True:
            for stock in stockList:
                price = self.getLastPrice(stock)
                stockToFileWriterMap[stock].writerow([str(datetime.now()), price])
            time.sleep(intervalInSecond)

    def trade(self, stock, intervalInSecond=5, buyThresh=0.001, sellThresh=0.001):
        tradeInfo = TradeInfo()
        path = getPath(stock)
        with open(path + 'price.csv', 'a', 0) as priceFile, open(path + 'buy.csv', 'a', 0) as buyFile, open(path + 'sell.csv', 'a', 0) as sellFile:
            priceWriter = csv.writer(priceFile)
            buyWriter = csv.writer(buyFile)
            sellWriter = csv.writer(sellFile)
            while True:
                timestamp = str(datetime.now())
                price = self.getLastPrice(stock)

                tradeInfo.prices.append(price)
                if tradeInfo.isHeld:  # need to sell
                    if price >= tradeInfo.preMax: # continue hold it
                        tradeInfo.preMax = price
                    elif (tradeInfo.preMax - price) / tradeInfo.preMax >= sellThresh:  # or (buyPrices[-1] - price) / buyPrices[-1] >= sellThreshLastBuy: # sell it
                        tradeInfo.isHeld = False
                        tradeInfo.preMin = price
                        tradeInfo.sellPrices.append(price)
                        sellWriter.writerow([timestamp, tradeInfo.sellPrices[-1]])
                else: # need to buy
                    if price <= tradeInfo.preMin:
                        tradeInfo.preMin = price
                    elif (price - tradeInfo.preMin) / tradeInfo.preMin >= buyThresh or (len(tradeInfo.buyPrices) > 0 and price >= tradeInfo.buyPrices[-1]):
                        tradeInfo.isHeld = True
                        tradeInfo.preMax = price
                        tradeInfo.buyPrices.append(price)
                        buyWriter.writerow([timestamp, tradeInfo.buyPrices[-1]])

                priceWriter.writerow([timestamp, price])
                time.sleep(intervalInSecond)
