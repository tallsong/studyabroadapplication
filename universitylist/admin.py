from django.contrib import admin

# Register your models here.
from .models import Question,Choice,Country,Province,Universty,Project

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Country)
admin.site.register(Province)
admin.site.register(Universty)
admin.site.register(Project)