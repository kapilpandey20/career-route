from django.db import models
from skills.models import Skill

class JobRole(models.Model):
    title = models.CharField(max_length=100)
    required_skills = models.ManyToManyField(Skill)

    def __str__(self):
        return self.title
