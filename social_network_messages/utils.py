import json
import re

import pandas as pd
from django.db.models import QuerySet

from social_network_messages.models import Message, City

FOREIGN_KEY_MAPPER = {
    "coordinates": City
}


def get_models(status: str, fields: list[str]) -> pd.DataFrame:
    status_int = [status_tuple[0] for status_tuple in Message.STATUS_CHOICES if status_tuple[1] == status]
    messages: QuerySet[Message] = Message.objects.filter(status__in=status_int)
    data_frame: pd.DataFrame = pd.DataFrame(list(messages.values_list('id', 'content', 'status', *fields)),
                                            columns=['id', 'content', 'status', *fields])
    return data_frame


def get_foreign_key(model, value):
    return model.objects.filter(id=value).first()


def update_model(df: pd.DataFrame):
    json_list = json.loads(json.dumps(list(df.T.to_dict().values())))

    for dic in json_list:
        message = Message.objects.get(id=dic["id"])
        dic.pop("id")
        for (key, value) in dic.items():
            foreign_key_id = FOREIGN_KEY_MAPPER.get(key)
            if foreign_key_id:
                setattr(message, key, get_foreign_key(foreign_key_id, value))
            else:
                setattr(message, key, value)
        message.save()


def preprocess_text(text: str) -> str:
    text = re.sub(r'[#,.!?():;\-…]', '', text)
    text = re.sub(r'&', ' ', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r' $', '', text)
    return text.lower()
