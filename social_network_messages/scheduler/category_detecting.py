import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import pymorphy2
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords

import configurations
from social_network_messages.utils import preprocess_text


def get_learned_model(name: str):
    model_path = Path(".") / "saved_models" / "category_detection" / name
    with open(model_path.as_posix(), 'rb') as file:
        model = pickle.load(file)
    return model


def detect_category(data: pd.DataFrame) -> pd.DataFrame:
    def _remove_stopwords(texts):
        return [[morph.normal_forms(word)[0] for word in simple_preprocess(str(doc))
                 if word not in russian_stopwords] for doc in texts]

    def _detect_topics(message, topic_dict, lemm_text, threshold=configurations.category_detect["threshold"]):
        prob = model.choose_best_label(lemm_text[message.id])
        topic = topic_dict[prob[0]] if prob[1] >= threshold else 0
        return [message.id, message.content, 3, message.problem_type, topic]

    def _create_cluster(word_sentences):
        def _detect_topic(words_with_populate):
            words = [word_with_populate[0] for word_with_populate in words_with_populate]
            # TODO: human-readable statuses
            return 3 if len(set(words).intersection(names_card)) else 4

        names_card = ('онлайн', 'приложение', 'мобильный', 'телефон', 'звонить')
        return [_detect_topic(words) for words in word_sentences]

    def _create_topic_dict(words_by_sentences):
        n_terms = len(set(sum(words_by_sentences, [])))
        model.fit(words_by_sentences, n_terms)

        doc_count = np.array(model.cluster_doc_count)
        top_index = doc_count.argsort()[-10:][::-1]
        top_words = [sorted(model.cluster_word_distribution[cluster].items(), key=lambda k: k[1], reverse=True)[:7] for
                     cluster in top_index]

        topic_names = _create_cluster(top_words)
        return {v: topic_names[k] for k, v in enumerate(top_index)}

    def _detect_fraud_category(data_fraud):
        content = data_fraud.content.values.tolist()
        # TODO: preprocess_text before all iterations for every module?
        clean_content = [preprocess_text(text) for text in content]
        words_by_sentences = _remove_stopwords(clean_content)
        words_by_sentences_dict = {k: v for k, v in zip(data_fraud.id.values.tolist(), words_by_sentences)}
        topic_dict = _create_topic_dict(words_by_sentences)
        return data_fraud.apply(lambda message: _detect_topics(message, topic_dict, words_by_sentences_dict), axis=1,
                                result_type='broadcast')

    morph = pymorphy2.MorphAnalyzer()
    model = get_learned_model("v3_k15.model")
    # TODO: load stopwords from db?
    russian_stopwords = stopwords.words("russian")
    russian_stopwords.extend(configurations.category_detect["stop_words"])

    # TODO: make human-readable types
    no_problem_data = data.loc[data.problem_type == 0]
    fraud_data = data.loc[data.problem_type == 1]
    breakdown_data = data.loc[data.problem_type == 2]

    # TODO: implement breakdown detection and merge with other categories
    fraud_data = _detect_fraud_category(fraud_data)
    return fraud_data
