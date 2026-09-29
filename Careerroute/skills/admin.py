from django.contrib import admin

from .models import Skill, StudentSkill, Resume, Career


admin.site.register(Skill)
admin.site.register(StudentSkill)
admin.site.register(Resume)
admin.site.register(Career)