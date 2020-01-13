from django.contrib import admin
from django.core.cache import cache
# Register your models here.
from universitylist.models import Question,Choice,Country,Province,University,Project
class BaseModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        '''新增或更新表中的数据时调用'''
        super().save_model(request, obj, form, change)
        # 发出任务，让celery worker重新生成首页静态页
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()
        # 清除首页的缓存数据
        cache.delete('index_page_data')
    def delete_model(self, request, obj):
        '''删除表中的数据时调用'''
        super().delete_model(request, obj)
        # 发出任务，让celery worker重新生成首页静态页
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()
        # 清除首页的缓存数据
        cache.delete('index_page_data')
class CountryAdmin(BaseModelAdmin):
    pass
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Country,CountryAdmin)
admin.site.register(Province)
admin.site.register(University)
admin.site.register(Project)