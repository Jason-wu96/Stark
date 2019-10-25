from django.contrib import admin
from .models import *

# 自定义Book类
class BookConfig(admin.ModelAdmin):
    list_display = ["title","price"]

    # 将书的价钱修改成100
    def patch_init(self,request,queryset):
        print(queryset)
        queryset.update(price=100)
    patch_init.short_description = "批量初始化"
    actions = [patch_init]
    list_filter = ["title","publish","authors"]

admin.site.register(Book,BookConfig)
admin.site.register(Publish)
admin.site.register(Author)