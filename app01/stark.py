from stark.service.stark import site,ModelStark
from django.urls import reverse
from .models import *
from django.utils.safestring import mark_safe
from django.forms import ModelForm
from django.forms import widgets as wid
from django.shortcuts import HttpResponse

# 重写BookModelForm类
class BookModelForm(ModelForm):
    class Meta:
        model = Book
        fields = "__all__"

        labels={
            "title":"书籍名称",
            "price":"价格"
        }

# 自定义Book类
class BookConfig(ModelStark):
    # 展示字段
    list_display = ["title","price","publishDate","publish","authors"]
    # 展示字段链接
    list_display_links = ["title"]
    # 使用自定义的BookModelForm
    modelform_class=BookModelForm
    # 可查找字段
    search_fields=["title","price"]
    # 批量操作将价格修改为123
    def patch_init(self, request, queryset):
        print(queryset)
        queryset.update(price=123)
        return HttpResponse("批量初始化OK")
    patch_init.short_description = "批量初始化"
    actions = [patch_init]

site.register(Book,BookConfig)
site.register(Publish)
site.register(Author)
site.register(AuthorDetail)






