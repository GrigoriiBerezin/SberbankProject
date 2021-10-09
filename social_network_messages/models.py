from django.db import models


# Create your models here.
class Message(models.Model):
    PROBLEM_CHOICES = [
        (1, "FRAUD"),
        (2, "BREAKDOWN")
    ]
    CATEGORY_CHOICES = [
        (1, "BREAKDOWN_CASH_MACHINE"),
        (2, "BREAKDOWN_APP"),
        (3, "BREAKDOWN_WEBSITE"),
        (4, "FRAUD_BANKING_CARD"),
        (5, "FRAUD_TELEPHONE"),
        (6, "FRAUD_CASH_MACHINE")
    ]

    url = models.CharField(max_length=400, unique=True)
    name = models.CharField(max_length=400)
    content = models.TextField()
    source = models.CharField(max_length=200, null=True)
    createdAt = models.DateTimeField()
    coordinates = models.CharField(max_length=100, null=True)
    problem_type = models.IntegerField(null=True, choices=PROBLEM_CHOICES)
    category_type = models.IntegerField(null=True, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"""
        "url": {self.url}
        "name": {self.name}
        "content": {self.content}
        "createdAt": {self.createdAt.strftime("%m/%d/%Y %H:%M:%S")}"""
