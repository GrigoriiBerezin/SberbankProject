from django.db import models


# Create your models here.
# TODO: add subject field
# TODO: change category choices by Misha decision
class Message(models.Model):
    PROBLEM_CHOICES = [
        (0, "No problem"),
        (1, "Fraud"),
        (2, "Breakdown")
    ]
    CATEGORY_CHOICES = [
        (1, "Cash Machine Breakdown"),
        (2, "App Breakdown"),
        (3, "Website Breakdown"),
        (4, "Banking Card Fraud"),
        (5, "Telephone Fraud"),
        (6, "Cash Machine Fraud")
    ]
    STATUS_CHOICES = [
        (0, "New Message"),
        (1, "Subject Detected"),
        (2, "Problem Detected"),
        (3, "Category Detected"),
        (4, "Tone Detected"),
        (5, "Coordinates Detected"),
        (6, "Marked Message")
    ]

    url = models.CharField(max_length=400, unique=True)
    name = models.CharField(max_length=400)
    content = models.TextField()
    source = models.CharField(max_length=200, null=True)
    createdAt = models.DateTimeField()
    coordinates = models.CharField(max_length=100, null=True)
    problem_type = models.IntegerField(null=True, choices=PROBLEM_CHOICES)
    category_type = models.IntegerField(null=True, choices=CATEGORY_CHOICES)
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)

    def __str__(self):
        return f"""{self.name} ({self.content[:20]}...) {self.createdAt.strftime("%d.%m.%Y %H:%M")}"""
