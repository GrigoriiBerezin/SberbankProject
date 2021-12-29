import json
import re

import pandas as pd
from django.db.models import QuerySet

from social_network_messages.models import Message


def get_models(status: str, field: str) -> pd.DataFrame:
    status_int = [status_tuple[0] for status_tuple in Message.STATUS_CHOICES if status_tuple[1] == status]
    messages: QuerySet[Message] = Message.objects.filter(status__in=status_int)
    data_frame: pd.DataFrame = pd.DataFrame(list(messages.values_list('id', 'content', 'status', field)),
                                            columns=['id', 'content', 'status', field])
    return data_frame


def update_model(df: pd.DataFrame):
    json_list = json.loads(json.dumps(list(df.T.to_dict().values())))

    for dic in json_list:
        message = Message.objects.get(id=dic["id"])
        dic.pop("id")
        for (key, value) in dic.items():
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
