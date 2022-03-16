import csv

from social_network_messages.models import Message

with open("./scripts/comments_marked.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, ["content", "url", "coordinates", "problem_type", "category_type"])
    next(reader, None)
    for row in reader:
        message = Message(url=row["url"], content=row["content"])
        message.save()
