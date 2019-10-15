from django.conf.urls import url
from django.shortcuts import render,redirect
from django.urls import reverse
from django.db.models import Q
from django.utils.safestring import mark_safe
from stark.utils.page import Pagination
from django.db.models.fields.related import ManyToManyField
from django.forms import ModelForm


# 展示页面
class ShowList(object):

    def __init__(self,config,data_list,request):
        self.config=config
        self.data_list=data_list
        self.request=request
        # 分页
        data_count=self.data_list.count()
        current_page=int(self.request.GET.get("page",1))
        base_path=self.request.path
        self.pagination=Pagination(current_page,data_count,base_path,self.request.GET,per_page_num=3, pager_count=11, )
        self.page_data=self.data_list[self.pagination.start:self.pagination.end]
        # action
        self.actions=self.config.new_actions() # [patch_init,]

    # 批量操作函数
    def get_action_list(self):
        temp = []
        for action in self.actions:
           temp.append({
               "name":action.__name__,
               "desc":action.short_description
           })  # [{"name":""patch_init,"desc":"批量初始化"}]

        return temp

    # 构建表头
    def get_header(self):
        header_list = []
        for field in self.config.new_list_play():
            if callable(field):
                val = field(self.config, header=True)
                header_list.append(val)
            else:
                if field == "__str__":
                    header_list.append(self.config.model._meta.model_name.upper())
                else:
                    val = self.config.model._meta.get_field(field).verbose_name
                    header_list.append(val)
        return header_list

    # 构造表单
    def get_body(self):
        # 构建表单数据
        new_data_list = []
        for obj in self.page_data:
            temp = []

            for filed in self.config.new_list_play():  # ["__str__",]      ["pk","name","age",edit]

                if callable(filed):
                    val = filed(self.config, obj)
                else:
                    try:
                        field_obj = self.config.model._meta.get_field(filed)
                        if isinstance(field_obj, ManyToManyField):
                            ret = getattr(obj, filed).all()
                            t = []
                            for mobj in ret:
                                t.append(str(mobj))
                            val = ",".join(t)
                        else:
                            if field_obj.choices:
                                val = getattr(obj, "get_" + filed + "_display")
                            else:
                                val = getattr(obj, filed)
                            if filed in self.config.list_display_links:
                                # "app01/userinfo/(\d+)/change"
                                _url = self.config.get_change_url(obj)

                                val = mark_safe("<a href='%s'>%s</a>" % (_url, val))

                    except Exception as e:
                        val = getattr(obj, filed)

                temp.append(val)

            new_data_list.append(temp)
        return new_data_list


class ModelStark(object):
    list_display=["__str__",]
    list_display_links=[]
    modelform_class=None
    search_fields=[]
    actions = []
    list_filter=[]

    def patch_delete(self, request, queryset):
        queryset.delete()
    patch_delete.short_description = "批量删除"

    def __init__(self, model, site):
        self.model = model
        self.site = site

    # 编辑
    def edit(self, obj=None, header=False):
        if header:
            return "操作"
        _url = self.get_change_url(obj)
        return mark_safe("<a href='%s'>编辑</a>"%_url)

    # 删除
    def deletes(self, obj=None, header=False):
        if header:
            return "操作"
        _url = self.get_delete_url(obj)
        return mark_safe("<a href='%s'>删除</a>" % _url)

    # 复选框
    def checkbox(self, obj=None, header=False):
        if header:
            return mark_safe('<input id="choice" type="checkbox">')
        return mark_safe('<input class="choice_item" type="checkbox" name="selected_pk" value="%s">'%obj.pk)

    # 默认表单
    def get_modelform_class(self):
        if not self.modelform_class:

            class ModelFormDemo(ModelForm):
                class Meta:
                    model = self.model
                    fields = "__all__"
                    labels={
                        ""
                    }
            return ModelFormDemo
        else:
            return self.modelform_class

    # 添加视图
    def add_view(self, request):
        ModelFormDemo = self.get_modelform_class()
        if request.method == "POST":
            form = ModelFormDemo(request.POST)
            if form.is_valid():
                form.save()
                return redirect(self.get_list_url())
            return render(request, "add_view.html", locals())
        form=ModelFormDemo()
        return render(request, "add_view.html", locals())

    # 删除视图
    def delete_view(self, request, id):
        url = self.get_list_url()
        if request.method == "POST":
            self.model.objects.filter(pk=id).delete()
            return redirect(url)
        return render(request, "delete_view.html", locals())

    # 编辑视图
    def change_view(self, request, id):
        ModelFormDemo = self.get_modelform_class()
        edit_obj = self.model.objects.filter(pk=id).first()
        if request.method == "POST":
            form = ModelFormDemo(request.POST, instance=edit_obj)
            if form.is_valid():
                form.save()
                return redirect(self.get_list_url())
            return render(request, "add_view.html", locals())
        form = ModelFormDemo(instance=edit_obj)
        return render(request, "change_view.html", locals())

    # 新的展示字段
    def new_list_play(self):
        temp = []
        temp.append(ModelStark.checkbox)
        temp.extend(self.list_display)
        if not self.list_display_links:
            temp.append(ModelStark.edit)
        temp.append(ModelStark.deletes)
        return temp

    # 新的批量操作
    def new_actions(self):
        temp = []
        temp.append(ModelStark.patch_delete)
        temp.extend(self.actions)
        return temp

    # 反向解析之编辑url
    def get_change_url(self,obj):
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label
        _url = reverse("%s_%s_change" % (app_label, model_name), args=(obj.pk,))
        return _url

    # 反向解析之删除url
    def get_delete_url(self, obj):
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label
        _url = reverse("%s_%s_delete" % (app_label, model_name), args=(obj.pk,))
        return _url

    # 反向解析之添加url
    def get_add_url(self):
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label
        _url = reverse("%s_%s_add" % (app_label, model_name))
        return _url

    # 反向解析之展示url
    def get_list_url(self):
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label
        _url = reverse("%s_%s_list" % (app_label, model_name))
        return _url

    # 按字段查找
    def get_serach_conditon(self, request):
        key_word = request.GET.get("q", "")
        self.key_word = key_word
        search_connection = Q()
        if key_word:
            # self.search_fields # ["title","price"]
            search_connection.connector = "or"
            for search_field in self.search_fields:
                search_connection.children.append((search_field + "__contains", key_word))
        return search_connection

    # 展示页面
    def list_view(self, request):
        if request.method == "POST":  # action
            action = request.POST.get("action")       # patch_init
            selected_pk = request.POST.getlist("selected_pk")
            action_func = getattr(self, action)
            queryset = self.model.objects.filter(pk__in=selected_pk)
            ret = action_func(request, queryset)

        # 获取serach的Q对象
        search_connection = self.get_serach_conditon(request)

        # 筛选获取当前表所有数据
        data_list = self.model.objects.all().filter(search_connection)

        # 按这ShowList展示页面
        showlist = ShowList(self, data_list, request)

        # 构建一个查看URL
        add_url = self.get_add_url()
        return render(request, "list_view.html", locals())

    # 二级分发url
    def get_urls_2(self):
        temp = []
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label
        temp.append(url(r"^add/", self.add_view, name="%s_%s_add" % (app_label, model_name)))
        temp.append(url(r"^(\d+)/delete/", self.delete_view, name="%s_%s_delete" % (app_label, model_name)))
        temp.append(url(r"^(\d+)/change/", self.change_view, name="%s_%s_change" % (app_label, model_name)))
        temp.append(url(r"^$", self.list_view, name="%s_%s_list" % (app_label, model_name)))
        return temp

    @property
    def urls_2(self):
        return self.get_urls_2(), None, None


class StarkSite(object):
    def __init__(self):
        self._registry = {}

    def register(self, model, stark_class=None):
        if not stark_class:
            stark_class = ModelStark
        self._registry[model] = stark_class(model, self)

    def get_urls(self):
        temp = []
        for model, stark_class_obj in self._registry.items():
            model_name = model._meta.model_name
            app_label = model._meta.app_label
            # 分发增删改查
            temp.append(url(r"^%s/%s/" % (app_label, model_name), stark_class_obj.urls_2))
        return temp

    @property
    def urls(self):
       return self.get_urls(),None,None


site = StarkSite()












