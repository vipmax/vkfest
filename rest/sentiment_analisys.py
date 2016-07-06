# coding=utf-8
import re
from polyglot.text import Text
from polyglot.detect import Detector
from polyglot.detect.base import Language
from polyglot.decorators import cached_property
import pycld2 as cld2
import pymorphy2

class MyDetector(Detector):
    def __init__(self, text, quiet=False):
        super(MyDetector, self).__init__(text, quiet=quiet)
        self.language = Language(('Russian', 'ru', 95, 500))

    def detect(self, text):
        t = text.encode("utf-8")
        reliable, index, top_3_choices = cld2.detect(t, bestEffort=False)
        self.language = [Language(x) for x in top_3_choices][0]
        return self.language


class MyText(Text):
    @cached_property
    def detected_languages(self):
        return MyDetector(self.raw, quiet=False)


morpher = pymorphy2.MorphAnalyzer()

def filter_text(text):
    words = [w for w in re.findall(u'[А-яёЁ]+|[0-9]+|[A-z]+', text)]
    return ' '.join(words)

def process(text):
    try:
        morphed_words = [morpher.parse(word)[0].normal_form for word in filter_text(text).split(' ')]
        text = MyText(' '.join(morphed_words))
        for word in text.words: print(word, word.polarity)

        spolarity = sum([word.polarity for word in text.words])
        morphed_words = [{'w': word, 'p': word.polarity} for word in text.words]

        return {'morphed_words': morphed_words, 'spolarity': spolarity}
    except:
        return {'morphed_words': [], 'spolarity': 0}


