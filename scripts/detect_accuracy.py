import csv

from social_network_messages.models import Message

messages = Message.objects.all()
with open("./scripts/comments_marked.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, ["content", "url", "coordinates", "problem_type", "category_type", "tone",
                                "emotionality", "probability"])
    next(reader, None)

    size = messages.count()
    accuracy = {"coordinates": 0, "problem_type": 0, "category_type": 0, "emotionality": 0, "tone": 0, "probability": 0}

    for row in reader:
        message = messages.get(url=row["url"])
        if message.coordinates.name == row["coordinates"]: accuracy["coordinates"] = accuracy["coordinates"] + 1
        if message.problem_type == int(row["problem_type"]): accuracy["problem_type"] = accuracy["problem_type"] + 1
        if message.category_type == int(row["category_type"]): accuracy["category_type"] = accuracy["category_type"] + 1
        if message.emotionality == int(row["emotionality"]): accuracy["emotionality"] = accuracy["emotionality"] + 1
        if message.tone == int(row["tone"]): accuracy["tone"] = accuracy["tone"] + 1
        if message.probability == int(row["probability"]): accuracy["probability"] = accuracy["probability"] + 1

    for (key, value) in accuracy.items():
        print(f"{key} accuracy: {value / size * 100} %")
