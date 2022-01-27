import re
from pathlib import Path
from string import punctuation

import pandas as pd
from nltk.corpus import stopwords
from pymystem3 import Mystem

from social_network_messages.models import Message
from social_network_messages.utils import get_learned_model

russian_stopwords = stopwords.words("russian")


class RelevanceAnalysis(object):
    def __init__(self, column_text, clf, vectorizer, transformer, mystem):
        self.mystem = mystem
        self.predicted_relevance_tags = pd.DataFrame(columns=['content', 'probability'])
        for i, string in enumerate(column_text):
            preprocess_string = self.preprocess(string)
            self.predicted_relevance_tags.at[i, 'content'] = string
            x_for_pred = vectorizer.transform([preprocess_string])
            x_for_pred = transformer.transform(x_for_pred)
            self.predicted_relevance_tags.at[i, 'probability'] = clf.predict(x_for_pred)[0]

    def __normalize_text(self, string):
        tokens = self.mystem.lemmatize(string.lower())
        tokens = [token for token in tokens if
                  token not in russian_stopwords and token != " " and token.strip() not in punctuation]
        return " ".join(tokens)

    def preprocess(self, string: str) -> str:
        string = re.sub('\n', '. ', string)
        string = " ".join(re.sub(r'[^a-zA-Zа-яА-ЯёЁ0-9 ]', ' ', string).split())
        string = self.__normalize_text(string)
        return string

    def get_predicted_tags(self):
        return self.predicted_relevance_tags


def detect_probability(data: pd.DataFrame) -> pd.DataFrame:
    mystem = Mystem()
    clf, vectorizer, transformer = get_learned_model(Path("probability_detection") / "modelLGBM.pkl")
    data.loc[:, 'probability'] = RelevanceAnalysis(data.content, clf, vectorizer,
                                                   transformer, mystem).get_predicted_tags().probability
    data.status = Message.STATUS_CHOICES_DICT["Subject Detected"]
    return data
