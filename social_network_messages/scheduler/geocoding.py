import csv

import datrie
import numpy as np
import pandas as pd
from datrie import Trie

from social_network_messages.models import City, Message
from social_network_messages.utils import preprocess_text


def _get_cities_from_db() -> np.ndarray:
    cities = City.objects.all()
    return np.array([city for city in cities])


def detect_geo(data: pd.DataFrame) -> pd.DataFrame:
    cities: np.ndarray = _get_cities_from_db()
    trie: Trie = datrie.Trie(''.join([chr(x) for x in range(ord('а'), ord('я') + 1)]))

    # TODO: replace with apply (less memory)
    for table_index, message in data.iterrows():
        content = message.content
        # TODO: preprocess_text before all iterations for every module?
        content = preprocess_text(content)
        for index, word in enumerate(content.split()):
            trie[word] = index
        coordinates = City.DEFAULT_CITY_ID
        for city_with_coord in cities:
            city_name = city_with_coord.name
            city_base = city_name[:len(city_name) - 1]
            if trie.has_keys_with_prefix(city_base.lower()):
                coordinates = city_with_coord.id
                break
        data._set_value(table_index, 'coordinates', coordinates)
        data._set_value(table_index, 'status', 5)

    return data
