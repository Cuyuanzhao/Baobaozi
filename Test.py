import csv
import os
import time
from config import getPath
from random import uniform



def trade(stock):
    path = getPath(stock)

    with open(path + 'price.csv', 'w', 0) as priceFile, open(path + 'buy.csv', 'w', 0) as buyFile, open(path + 'sell.csv',
                                                                                                        'w', 0) as sellFile:
        priceWriter = csv.writer(priceFile)
        buyWriter = csv.writer(buyFile)
        sellWriter = csv.writer(sellFile)

        for i in range(100):
            timestamp = int(time.time())
            print(timestamp)
            price = uniform(60.0, 70.0)
            priceWriter.writerow([timestamp, price])
            if i % 4 == 0:
                buyWriter.writerow([timestamp, price])
            if i % 5 == 0:
                sellWriter.writerow([timestamp, price])

            time.sleep(1)

if __name__ == '__main__':
    trade('TQQQ')