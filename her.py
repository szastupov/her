import requests
import re
import random

http = requests.Session()

def currency(her, tokens):
	url = "https://query.yahooapis.com/v1/public/yql?q=" \
		  "select+*+from+yahoo.finance.xchange+where+pair+=+%22USDRUB,EURRUB%22&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
	res = http.get(url).json()
	rates = res["query"]["results"]["rate"]
	text = ", ".join(["{Name} {Rate}".format(**r) for r in rates])
	
	her.say(text)

def bitcoin(her, tokens):
	url = "https://api.bitcoinaverage.com/ticker/global/USD/"
	res = http.get(url).json()
	her.say(res["24h_avg"], "USD")

def cmds(her, tokens):
	for cmd in WORDS:
		her.write(cmd, "\n")

def google(her, tokens):
	url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=" + " ".join(tokens[1:])
	results = http.get(url).json()["responseData"]["results"]
	items = ["{titleNoFormatting} -- {unescapedUrl}".format(**r) for r in results]
	her.say("Вот что я нашла:\n")
	her.write("\n".join(items))


def hn(her, tokens):
	url = "https://hacker-news.firebaseio.com/v0/topstories.json"
	top = http.get(url).json()

	top_stories = []
	for i in range(5):
		surl = "https://hacker-news.firebaseio.com/v0/item/%s.json" % top[i]
		story = http.get(surl).json()
		top_stories.append("{title} -- {url}".format(**story))
	her.say("Вот ТОП:\n")
	her.write("\n".join(top_stories))


WORDS = {
	"hi": "хаюшки!",
	"привет": "Привет!",
	"пока|чмоки": "Пока 😘|Давай, увидимся!",
	"как тебя зовут": "Я - Она, Она - Я|Скарлет Йохансен... шутка",
	"как дела": "да неплохо|как сажа бела|да норм, че",
	"заебись": "а то!",
	"курс|почем|currency": currency,
	"команды": cmds,
	"биткоин|bitcoin": bitcoin,
	"смысл жизни": "42",
	"google|погугли": google,
	"hn|в тренде": hn
}

MAP = {}
for (rule, act) in WORDS.items():
	keys = rule.split("|")
	for key in keys:
		MAP[key] = act

class Her(object):
	def tell(self, phrase):
		self.buf = ""
		found = False

		phrase = phrase.lower()
		ntokens = re.sub(r"\.|,|\?|!", " ", phrase).split()
		nphrase = " ".join(ntokens)

		for word in MAP:
			if word in nphrase:
				self.do(MAP[word], ntokens)
				found = True
				break

		if not found:
			self.say("Я тебя не понимаю 😳")

		return self.buf

	def write(self, *args):
		self.buf += " ".join(args)

	def say(self, *w):
		strs = map(str, w)
		self.write("Она:", *strs)

	def do(self, a, tokens):
		if type(a) is str:
			variants = a.split("|")
			self.say(random.choice(variants))
		else:
			try:
				a(self, tokens)
			except Exception as e:
				raise e
				self.say("Воу-воу-воу, потише! У меня даже что-то сломалось :/")

def main():
	her = Her()
	while True:
		try:
			phrase = input("Ты: ")
		except EOFError:
			her.say("Пока 😘")
			break
		print(her.tell(phrase))


if __name__ == '__main__':
	main()