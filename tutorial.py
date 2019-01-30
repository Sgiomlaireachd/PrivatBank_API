import requests
import matplotlib.pyplot as plt

def getAmount(month):
    if month == 2 : return 28
    if month <= 7 : 
        if month % 2 : return 31
        else: return 30
    else:
        if month % 2 : return 30
        else: return 31
        
def getNeededDictionary(l,currency):
    for d in l:
        if d['currency'] == currency:
            print('Found needed dictionary.')
            return d
    return {}
try:
    print('***The earliest period you can use is December of 2014***')
    print('***You can`t also get the information from the current month***')
    buys  = []
    sales = []
    month = int(input('-> Input the number of needed month:'))
    year = int(input('-> Input the needed year:'))
    choice = int(input('-> Do you wanna input restricted amount of days manually? (1/0):'))
    if not choice: amount = getAmount(month)
    else: amount = int(input('-> Input the amount of days you need:'))
    currency = input('-> Input the needed currency (CHF/RUB/GBP/USD/EUR/PLZ):')
    for day in range(1,amount+1):
        resp = requests.get('https://api.privatbank.ua/p24api/exchange_rates?json&date={}.{}.{}'.format(str(day),str(month),str(year)))
        if resp.status_code != 200:
            print('Error : {}'.format(resp.status_code))
            break
        else:
            print('Connected. ({}/{})'.format(day,amount))
        d = resp.json()['exchangeRate']
        data = getNeededDictionary(d[1:],currency)
        buys.append(data['purchaseRate'])
        sales.append(data['saleRate'])
    print(buys,sales)
    x = [i for i in range(amount)]
    plt.plot(x, buys, 'b-', label="purchaseRate")
    plt.plot(x, sales, 'r-', label="saleRate")
    plt.title('{} course for {}.{}'.format(currency,month,year))
    plt.legend()
    plt.show()
except Exception as e: 
    print('Error was occured.')
    print(e)
