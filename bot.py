from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
import logging
import requests
import json
import os
import redis
import emoji

logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
updater = None
r = redis.from_url(os.environ.get("REDIS_URL"))
#or r = redis.from_url("YOUR_REDIS_DB_URL")

def start(update, context):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.name   
    r.set(user_name, user_id) #sets key name as user_name and value as user_id
    __location__ = os.path.realpath(os.path.join(
        os.getcwd(), os.path.dirname(__file__)))
    f = open(os.path.join(__location__, 'tixl_bot_welcome.txt'))
    f_content = f.read()
    update.message.reply_text(f_content)
    f.close()


def price_bnb_function(update, context):
    r = requests.get(
        'https://dex.binance.org/api/v1/ticker/24hr?symbol=MTXLT-286_BNB')
    packages_json_bnb = r.json()
    tixlPrice = packages_json_bnb[0]['lastPrice']
    tixlPrice_aprox = "{:.2f}".format(float(tixlPrice))
    packages_str = json.dumps(packages_json_bnb, indent=2)
    p = "The price for one MTXLT is " + tixlPrice_aprox + " BNB"
    update.message.reply_text(p)


def price_usd_function(update, context):
    r = requests.get(
        'https://dex.binance.org/api/v1/ticker/24hr?symbol=MTXLT-286_BNB')
    packages_json_bnb = r.json()
    tixlPrice = float(packages_json_bnb[0]['lastPrice'])
    a = requests.get(
        'https://api.binance.com/api/v1/ticker/price?symbol=BNBUSDT')
    packages_json_usd = a.json()
    bnbPrice_usd = float(packages_json_usd['price'])
    tixlPrice_usd = "{:.2f}".format(bnbPrice_usd * tixlPrice)
    u = "The price for one MTXLT is" + " $" + str(tixlPrice_usd)
    update.message.reply_text(u)


def whitepaper(update, context):
    __location__ = os.path.realpath(os.path.join(
        os.getcwd(), os.path.dirname(__file__)))
    m = open(os.path.join(__location__, 'tixl_whitepaper.txt'))
    m_content = m.read()
    update.message.reply_text(m_content)
    m.close()


def testnet(update, context):
    __location__ = os.path.realpath(os.path.join(
        os.getcwd(), os.path.dirname(__file__)))
    t = open(os.path.join(__location__, 'tixl_testnet.txt'))
    t_content = t.read()
    update.message.reply_text(t_content)
    t.close()


def github(update, context):
    __location__ = os.path.realpath(os.path.join(
        os.getcwd(), os.path.dirname(__file__)))
    g = open(os.path.join(__location__, 'tixl_bot_github.txt'))
    g_content = g.read()
    update.message.reply_text(g_content)
    g.close()


def price(update, context):
    q = requests.get(
        'https://dex.binance.org/api/v1/ticker/24hr?symbol=MTXLT-286_BNB')
    packages_json = q.json()
    tixlPrice_bnb = packages_json[0]['lastPrice']
    highPrice = packages_json[0]['highPrice']
    lowPrice = packages_json[0]['lowPrice']
    priceChange =packages_json[0]['priceChangePercent']
    volume = packages_json[0]['quoteVolume']
    tixlPrice_bnb_float = "{:.2f}".format(float(tixlPrice_bnb)) 
    highPrice_float ="{:.3f}".format (float(highPrice)) 
    lowPrice_float = "{:.3f}".format(float(lowPrice))
    priceChange_float ="{:.2f}".format (float(priceChange))
    volume_float ="{:.2f}".format(float(volume))
    priceChange_int = int(float(priceChange_float))
    if (priceChange_int > 0):
       status_price_emoji = emoji.emojize( ":fire:")
    else:
        status_price_emoji = emoji.emojize( "📉")

    n = "Current price: " + tixlPrice_bnb_float + " BNB\n" + "Price change (24hrs): " + priceChange_float + "% " + status_price_emoji + "\n" + "Lowest price (24hrs): " + lowPrice_float + " BNB\n" + "Highest price (24hrs): " + highPrice_float + " BNB\n" + "Volume (24hrs): " + volume_float + " BNB" 
    update.message.reply_text(n)

def bugs(update, context):
    __location__ = os.path.realpath(os.path.join(
        os.getcwd(), os.path.dirname(__file__)))
    k = open(os.path.join(__location__, 'tixl_bot_bugs.txt'))
    k_content = k.read()
    update.message.reply_text(k_content)
    k.close()

def start_bot():
    global updater
    updater = Updater(
        '<TOKEN>', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('price_bnb', price_bnb_function))
    dp.add_handler(CommandHandler('price_usd', price_usd_function))
    dp.add_handler(CommandHandler('whitepaper', whitepaper))
    dp.add_handler(CommandHandler('testnet', testnet))
    dp.add_handler(CommandHandler('github', github))
    dp.add_handler(CommandHandler('price', price))
    dp.add_handler(CommandHandler('report_bugs', bugs))
    updater.start_polling()
    updater.idle()

start_bot()
