import csv

import datrie
import numpy as np
import pandas as pd
from datrie import Trie

from social_network_messages.utils import preprocess_text


# TODO: make new model City with oneToMany
def get_cities() -> np.ndarray:
    with open("cities.tsv", "r", encoding="utf-8") as cities_out:
        city_reader = csv.reader(cities_out, dialect='excel-tab')
        cities = np.array([city for city in city_reader])
    return cities


def detect_geo(data: pd.DataFrame) -> pd.DataFrame:
    cities: np.ndarray = get_cities()
    trie: Trie = datrie.Trie(''.join([chr(x) for x in range(ord('а'), ord('я') + 1)]))

    # TODO: replace with apply (less memory)
    for table_index, message in data.iterrows():
        content = message.content
        # TODO: preprocess_text before all iterations for every module?
        content = preprocess_text(content)
        for index, word in enumerate(content.split()):
            trie[word] = index
        coordinates = 'Without geo'
        for city_with_coord in cities:
            city = city_with_coord[0]
            city_base = city[:len(city) - 1]
            if trie.has_keys_with_prefix(city_base.lower()):
                coordinates = np.array2string(city_with_coord, separator=' ')
                break
        data._set_value(table_index, 'coordinates', coordinates)
        data._set_value(table_index, 'status', 5)

    return data
