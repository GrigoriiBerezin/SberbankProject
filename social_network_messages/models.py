from django.db import models


# Create your models here.
class Message(models.Model):
    url = models.CharField(max_length=400, unique=True)
    name = models.CharField(max_length=400)
    content = models.TextField()
    createdAt = models.DateTimeField()

    def __str__(self):
        return f"""
        "url": {self.url}
        "name": {self.name}
        "content": {self.content}
        "createdAt": {self.createdAt.strftime("%m/%d/%Y %H:%M:%S")}"""
