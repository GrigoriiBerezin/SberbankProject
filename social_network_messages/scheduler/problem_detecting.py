from pathlib import Path

import keras.models
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer

import configurations as conf
from social_network_messages.models import Message
from social_network_messages.utils import preprocess_text


def get_sequential_model(name: str) -> Sequential:
    model_path = Path(".") / "saved_models" / name
    model = keras.models.load_model(model_path.as_posix())
    return model


def detect_problem(data: pd.DataFrame) -> pd.DataFrame:
    # TODO: preprocess_text before all iterations for every module?
    def _preprocess_text(content: str) -> str:
        content = preprocess_text(content)
        content = ' '.join(word for word in content.split() if len(word) > conf.subject_detect["max_word_length"])
        return content

    def _map_problem_type(array: np.ndarray) -> np.ndarray:
        enumerate_array = (array > 0.5).astype(int)[0]
        problem_type_dict = dict(enumerate(enumerate_array))
        return list(problem_type_dict.keys())[list(problem_type_dict.values()).index(1)]

    def _detect_problem(message):
        content = message.content
        x = tokenizer.texts_to_sequences([content])
        x = pad_sequences(x, maxlen=conf.subject_detect["max_seq_length"])
        problem_type = model.predict(x)
        problem_type = _map_problem_type(problem_type)
        return [message.id, message.content, Message.STATUS_CHOICES_DICT["Problem Detected"], problem_type]

    model: Sequential = get_sequential_model("problem_detection")
    tokenizer = Tokenizer(num_words=conf.subject_detect["max_nb_words"],
                          filters=r'!"#$%&()*+,-./:;<=>?@[\]^_`{|}~',
                          lower=True)
    data.content = data.apply(lambda table: _preprocess_text(table.content), axis=1)
    tokenizer.fit_on_texts(data.content)
    data = data.apply(_detect_problem, axis=1, result_type='broadcast')
    return data
