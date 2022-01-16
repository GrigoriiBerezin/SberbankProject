import re
from pathlib import Path

import pandas as pd
import pymorphy2

from social_network_messages.models import Message
from social_network_messages.utils import get_learned_model

stopset_light = {'а', 'будто', 'бы', 'в', 'вам', 'вас', 'вдруг', 'ведь', 'во', 'вот',
                 'впрочем', 'все', 'всех', 'всю', 'вы', 'два', 'для', 'его', 'ее', 'ей', 'ему', 'ж', 'же',
                 'за', 'здесь', 'и', 'из', 'или', 'им', 'иногда', 'их', 'к', 'как', 'какая', 'какой',
                 'когда', 'конечно', 'кто', 'куда', 'ли', 'между', 'меня', 'мне', 'может',
                 'мой', 'моя', 'мы', 'на', 'над', 'надо', 'наконец', 'нас', 'него', 'нее', 'ней',
                 'нибудь', 'ним', 'них', 'но', 'ну', 'о', 'об', 'один',
                 'он', 'она', 'они', 'опять', 'от', 'перед', 'по', 'под', 'после', 'потом', 'потому', 'почти',
                 'при', 'про', 'раз', 'разве', 'с', 'сам', 'свою', 'себе', 'себя', 'сейчас', 'со', 'совсем',
                 'так', 'такой', 'там', 'тебя', 'тем', 'теперь', 'то', 'тогда', 'того', 'тоже', 'только',
                 'том', 'тот', 'три', 'тут', 'ты', 'у', 'уж', 'уже',
                 'чего', 'чем', 'что', 'чтоб', 'чтобы', 'эти', 'этого', 'этой', 'этом', 'этот', 'эту', 'я'}


# класс предназначен для определения эмоциональности текста
class DegreeEmotionality(object):
    def __init__(self, string_arr):
        self.EmotionalityTags = pd.DataFrame(columns=['emotionality'])
        for i, string in enumerate(string_arr):
            self.EmotionalityTags.at[i, 'emotionality'] = self.__upper_words(string) + self.__exclamation_marks(string)

    # функция подсчета количества слов в строке, которые подряд написаны капсом
    @staticmethod
    def __upper_words(string):
        count_upper_words = 0
        for word in string.split(" "):
            word = re.sub(r'[^а-яА-ЯёЁ]', ' ', word)
            if word.isupper() and len(word) > 1:
                count_upper_words += 1
                if count_upper_words >= 2:
                    return 1
            else:
                count_upper_words = 0
        return 0

    # функция поиска утроенных восклицательных и вопросительных знаков
    @staticmethod
    def __exclamation_marks(string):
        answer = 0
        count_exclamation_marks = 0
        count_question_marks = 0
        for symbol in string:
            if answer >= 2:
                break
            if (symbol == "!") and (count_exclamation_marks < 2):
                count_exclamation_marks += 1
                if count_exclamation_marks >= 2:
                    answer += 1
            elif (symbol == "?") and (count_question_marks < 2):
                count_question_marks += 1
                if count_question_marks >= 2:
                    answer += 1
            else:
                count_exclamation_marks = 0
                count_question_marks = 0
        return answer

    # функция получения предсказанных меток эмоциональности
    def get_emotionality_tags(self):
        return self.EmotionalityTags


# класс предназначен для определения тональности сообщения
class SentimentAnalysis(object):
    def __init__(self, column_text, clf, vectorizer):
        self.predictedSentimentTags = pd.DataFrame(columns=['content', 'tone'])
        for i, string in enumerate(column_text):
            preprocess_string = self.preprocess(string)
            self.predictedSentimentTags.at[i, 'content'] = string
            x_for_pred = vectorizer.transform([preprocess_string])
            self.predictedSentimentTags.at[i, 'tone'] = clf.predict(x_for_pred)[0]

    # функция удаления стоп-слов и лемматизации текста
    @staticmethod
    def __delete_stop_words(string):
        morph = pymorphy2.MorphAnalyzer()
        words = string.split()  # разбиваем текст на слова
        without_stopwords_string = [word for word in words if not word in stopset_light]
        lemmatized_string = list()
        for word in without_stopwords_string:
            lemmatized_string.append(morph.parse(word)[0].normal_form)
        string = ' '.join(lemmatized_string)
        return string

    # функция предобработки текста
    def preprocess(self, string):
        string = string.lower()  # приведение к нижнему регистру
        to_replace = ['р/с ', 'р/счет', 'р/сч ']  # замена сокращений
        regex = re.compile('|'.join(to_replace))
        string = re.sub(regex, 'расчетный счет ', string)
        string = re.sub(r'[^а-яё]', ' ', string)  # Удаление оставшихся знаков пунктуации и специальных символов
        string = re.sub(r'\s+', ' ', string).lstrip().rstrip()  # удаление лишних пробелов
        string = self.__delete_stop_words(string)
        return string

    # функция получения предсказанных меток тональности
    def get_sentiment_tags(self):
        return self.predictedSentimentTags


def detect_tone(data: pd.DataFrame) -> pd.DataFrame:
    clf, vectorizer = get_learned_model(Path("tone_detection") / "modelSVM.pkl")
    data.loc[:, 'tone'] = SentimentAnalysis(data.content, clf, vectorizer).get_sentiment_tags().tone
    data.loc[:, 'emotionality'] = DegreeEmotionality(data.content).get_emotionality_tags()
    data.status = Message.STATUS_CHOICES_DICT["Tone Detected"]
    return data
