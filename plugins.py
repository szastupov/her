import requests
import re
import random
import wikipedia
import unicodedata as ud

PLUGINS = []

def plugin(regexp):
	def decorator(fn):
		PLUGINS.append((regexp, fn))
		return fn
	return decorator

http = requests.Session()

def yahoo_url(pairs):
    return "https://query.yahooapis.com/v1/public/yql?q=" \
          "select+*+from+yahoo.finance.xchange+where+pair+=+%22" + pairs + \
          "%22&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys";


@plugin(r"курс|почем|currency")
def currency(her, m):
    url = yahoo_url("USDRUB,EURRUB")
    res = http.get(url).json()
    rates = res["query"]["results"]["rate"]
    text = ", ".join(["{Name} {Rate}".format(**r) for r in rates])
    
    her.say(text)

@plugin(r"(\d+) (рубля|рублей|доллара|долларов|евро) к (рублю|доллару|евро)")
def currency_coversion(her, m):
    amount = m.group(1)
    source = m.group(2)
    target = m.group(3)

    table = {
        "USD": r"доллар??",
        "RUB": r"рубл??",
        "EUR": r"евро"
    }

    for (cur, expr) in table.items():
        if re.match(expr, source):
            source = cur
        if re.match(expr, target):
            target = cur

    url = yahoo_url(source+target)
    res = http.get(url).json()
    rates = res["query"]["results"]["rate"]

    converted = float(rates["Rate"]) * float(amount)

    her.say(converted, target)


@plugin(r"биткоин|bitcoin")
def bitcoin(her, m):
    url = "https://api.bitcoinaverage.com/ticker/global/USD/"
    res = http.get(url).json()
    her.say(res["24h_avg"], "USD")


@plugin("команды")
def cmds(her, m):
    for cmd in WORDS:
        her.write(cmd, "\n")


@plugin(r"(?:google|погугли|найди) (.*)")
def google(her, m):
    url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=" + m.group(1)
    results = http.get(url).json()["responseData"]["results"]
    items = ["{titleNoFormatting} -- {unescapedUrl}".format(**r) for r in results]

    her.say("Вот что я нашла:\n")
    her.write("\n".join(items))


@plugin(r"hn|в тренде")
def hn(her, m):
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    top = http.get(url).json()

    top_stories = []
    for i in range(5):
        surl = "https://hacker-news.firebaseio.com/v0/item/%s.json" % top[i]
        story = http.get(surl).json()
        top_stories.append("{title} -- {url}".format(**story))
    her.say("Вот ТОП:\n")
    her.write("\n".join(top_stories))


@plugin(r"напомни (.*)")
def remind(her, m):
    task = m.group(1)
    her.say("Я бы напомнила тебе '%s', но пока не умею" % task)


@plugin(r"создай встречу событие")
def schedule(her, m):
    pass


def get_language(msg):
    uname = ud.name(msg[0])
    if "CYRILLIC" in uname:
        return "ru"
    else:
        return "en"

@plugin(r"(?:что такое|what is|define) (.*)")
def summary(her, m):
    query = m.group(1)
    
    wikipedia.set_lang(get_language(query))
    res = wikipedia.summary(query, sentences=2)
    page = wikipedia.page(query)
    
    her.say("%s\n%s" % (res, page.url))


@plugin(r"(?:translate|переведи) (.*)")
def translate(her, m):
    message = m.group(1)
    lang = get_language(message)
    direction = "ru" if lang == "en" else "en"

    her.say("пока не умею переводить с %s на %s" % (lang, direction))
