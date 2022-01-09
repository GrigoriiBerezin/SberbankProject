import logging

import pandas as pd

from social_network_messages.scheduler.category_detecting import detect_category
from social_network_messages.scheduler.geocoding import detect_geo
from social_network_messages.scheduler.problem_detecting import detect_problem
from social_network_messages.utils import get_models, update_model

WORKFLOW_STATS = {
    "subject detecting": ("New Message", ["subject"], None),  # TODO: add model func to detecting subjects
    "problem detecting": ("Subject Detected", ["problem_type"], detect_problem),
    "category detecting": ("Problem Detected", ["problem_type", "category_type"], detect_category),
    "tone detecting": ("Category Detected", ["tone"], None),  # TODO: add model func to detecting tones
    "geo position detecting": ("Tone Detected", ["coordinates"], detect_geo),
}


def workflow():
    for (process_name, (status, additional_fields, process)) in WORKFLOW_STATS.items():
        try:
            data: pd.DataFrame = get_models(status, additional_fields)
            if len(data) != 0:
                new_data: pd.DataFrame = process(data)[["id", "status", *additional_fields]]
                update_model(new_data)
        except Exception as err:
            logging.error(f"Error on stage: {process_name}. Error: {err}")
