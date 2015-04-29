import re
import random
from plugins import PLUGINS

WORDS = {
    r"hi": "хаюшки!",
    r"привет": "Привет!",
    r"пока|чмоки": "Пока 😘|Давай, увидимся!",
    r"как тебя зовут": "Я - Она, Она - Я|Скарлет Йохансен... шутка",
    r"как дела": "да неплохо|как сажа бела|да норм, че",
    r"заебись": "а то!",
    r"смысл жизни": "42"
}

WORDS.update(PLUGINS)

class Her(object):
    def __init__(self):
        self.buf = ""

    def tell(self, phrase):
        self.buf = ""
        found = False

        phrase = phrase.lower()
        ntokens = re.sub(r"\.|,|\?|!", " ", phrase).split()
        nphrase = " ".join(ntokens)

        for word in WORDS:
            m = re.search(word, nphrase)
            if m:
                self.do(WORDS[word], m)
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
                self.say("Воу-воу-воу, потише! У меня даже что-то сломалось :/")
                raise e

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