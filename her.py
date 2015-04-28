import requests
import re

def currency(tokens):
	url = "https://query.yahooapis.com/v1/public/yql?q=" \
		  "select+*+from+yahoo.finance.xchange+where+pair+=+%22USDRUB,EURRUB%22&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
	res = requests.get(url).json()
	rates = res["query"]["results"]["rate"]
	text = ", ".join(["{Name} {Rate}".format(**r) for r in rates])
	say(text)

def bitcoin(tokens):
	url = "https://api.bitcoinaverage.com/ticker/global/USD/"
	res = requests.get(url).json()
	say(res["24h_avg"], "USD")

def cmds(tokens):
	for cmd in WORDS:
		print(cmd)

def google(tokens):
	url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=" + " ".join(tokens[1:])
	results = requests.get(url).json()["responseData"]["results"]
	say("Вот что я нашла:")
	for res in results:
		print(res["titleNoFormatting"], " - ", res["unescapedUrl"])


def hn(tokens):
	url = "https://hacker-news.firebaseio.com/v0/topstories.json"
	top = requests.get(url).json()

	top_stories = []
	for i in range(5):
		surl = "https://hacker-news.firebaseio.com/v0/item/%s.json" % top[i]
		story = requests.get(surl).json()
		top_stories.append("{title} -- {url}".format(**story))
	say("Вот ТОП:")
	print ("\n".join(top_stories))


WORDS = {
	"hi": "хаюшки!",
	"привет": "Привет!",
	"как тебя зовут": "Я - Она, Она - Я",
	"как дела": "да не плохо",
	"курс|почем": currency,
	"команды": cmds,
	"биткоин|bitcoin": bitcoin,
	"смысл жизни": "42",
	"google|погугли": google,
	"hn|в тренде": hn
}

def say(*w):
	print("Она:", *w)

def do(a, tokens):
	if type(a) is str:
		say(a)
	else:
		try:
			a(tokens)
		except Exception as e:
			raise e
			say("Воу-воу-воу, потише! У меня даже что-то сломалось :/")

MAP = {}
for (rule, act) in WORDS.items():
	keys = rule.split("|")
	for key in keys:
		MAP[key] = act

def main():
	while True:
		try:
			phrase = input("Ты: ").lower()
		except EOFError:
			say("Пока 😘")
			break

		ntokens = re.sub(r"\.|,|\?|!", " ", phrase).split()
		nphrase = " ".join(ntokens)

		for word in MAP:
			if word in nphrase:
				do(MAP[word], ntokens)
				break

	#say("Я тебя не понимаю 😳")


if __name__ == '__main__':
	main()