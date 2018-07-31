import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas
from datetime import datetime
from config import getPath


def strsToDatetimes(strs):
    return list(map(lambda s: datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f"), strs))


def animate(i):
    path = getPath(stock)
    priceData = pandas.read_csv(path + '/price.csv', names=['timestamp', 'price'])
    buyData = pandas.read_csv(path + '/buy.csv', names=['timestamp', 'price'])
    sellData = pandas.read_csv(path + '/sell.csv', names=['timestamp', 'price'])

    stockPrices = priceData['price'].tolist()
    buyPrices = buyData['price'].tolist()
    sellPrices = sellData['price'].tolist()

    firstPrice = float(stockPrices[0])
    lastPrice = float(stockPrices[-1])
    transCount = len(sellPrices)
    profit = sum(sellPrices) - sum(buyPrices[0: transCount])
    actualYield = profit / firstPrice
    defaultYield = (lastPrice - firstPrice) / firstPrice
    extraYield = actualYield - defaultYield


    ax1.clear()
    ax1.set_title('Stock Chart')
    ax1.plot(strsToDatetimes(priceData['timestamp']), stockPrices)
    ax1.scatter(strsToDatetimes(buyData['timestamp']), buyPrices, color='g', marker='+')
    ax1.scatter(strsToDatetimes(sellData['timestamp']), sellPrices, color='r', marker='x')
    ax1.text(x=0.02, y=0.97, s="TransCount: {}".format(transCount), transform=ax1.transAxes)
    ax1.text(x=0.02, y=0.94, s="ExtraYield: {0:.4f}".format(extraYield), transform=ax1.transAxes)
    ax1.text(x=0.02, y=0.91, s="ActualYield: {0:.4f}".format(actualYield), transform=ax1.transAxes)
    ax1.text(x=0.02, y=0.88, s="DefaultYield: {0:.4f}".format(defaultYield), transform=ax1.transAxes)

stock = 'TQQQ'
# stock = 'PDD'
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
ani = animation.FuncAnimation(fig, animate, interval=2000)
plt.gcf().autofmt_xdate()
plt.show()