import datetime

from django.db import models


def map_enum_to_dict(enum: list[tuple]) -> dict:
    return {v: k for k, v in enum}


# Create your models here.
class City(models.Model):
    DEFAULT_CITY_ID = 9999

    name = models.CharField(max_length=100, unique=True)
    x = models.FloatField()
    y = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'cities'


# TODO: add subject field
class Message(models.Model):
    PROBLEM_CHOICES = [
        (0, "No Problem"),
        (1, "Fraud"),
        (2, "Breakdown")
    ]
    PROBLEM_CHOICES_DICT = map_enum_to_dict(PROBLEM_CHOICES)
    CATEGORY_CHOICES = [
        (0, "Not Detected"),
        (1, "Cash Machine Breakdown"),
        (2, "App Breakdown"),
        (3, "Telephone Fraud"),
        (4, "Cash Machine Fraud")
    ]
    CATEGORY_CHOICES_DICT = map_enum_to_dict(CATEGORY_CHOICES)
    STATUS_CHOICES = [
        (0, "New Message"),
        (1, "Subject Detected"),
        (2, "Problem Detected"),
        (3, "Category Detected"),
        (4, "Tone Detected"),
        (5, "Coordinates Detected"),
        (6, "Marked Message")
    ]
    STATUS_CHOICES_DICT = map_enum_to_dict(STATUS_CHOICES)
    TONE_CHOICES = [
        (0, "Neutral"),
        (1, "Positive"),
        (2, "Negative")
    ]
    TONE_CHOICES_DIST = map_enum_to_dict(TONE_CHOICES)
    EMOTIONALITY_CHOICES = [
        (0, "Not Emotional"),
        (1, "Low Emotional"),
        (2, "High Emotional"),
        (3, "Very High Emotional")
    ]
    EMOTIONALITY_CHOICES_DICT = map_enum_to_dict(EMOTIONALITY_CHOICES)

    url = models.CharField(max_length=400, unique=True)
    name = models.CharField(max_length=400, default="Unnamed")
    content = models.TextField()
    source = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    probability = models.FloatField(null=True)
    coordinates = models.ForeignKey(City, on_delete=models.PROTECT, related_name='city', null=True)
    problem_type = models.IntegerField(choices=PROBLEM_CHOICES, null=True)
    category_type = models.IntegerField(choices=CATEGORY_CHOICES, null=True)
    tone = models.IntegerField(choices=TONE_CHOICES, null=True)
    emotionality = models.IntegerField(choices=EMOTIONALITY_CHOICES, null=True)
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"""{self.name} ({self.content[:20]}...) {self.created_at.strftime("%d.%m.%Y %H:%M")}"""

    class Meta:
        ordering = ['created_at']
