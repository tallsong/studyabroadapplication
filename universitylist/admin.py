from django.contrib import admin

# Register your models here.
from .models import Question,Choice,Country,Province,University,Project

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Country)
admin.site.register(Province)
admin.site.register(University)
admin.site.register(Project)