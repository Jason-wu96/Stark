from django.test import TestCase

# Create your tests here.


# class  A(object):
#
#     x=12
#
#     def xxx(self):
#         print(self.x)
#
#
# class B(A):
#     y=5
#
# b=B()
# b.xxx()

#######################################

#
# class Person(object):
#     def __init__(self,name):
#         self.name=name
#
# alex=Person("alex")
#
# s="name"
#
#
# print(getattr(alex,s))

########################################

# class Person(object):
#     def __init__(self,name):
#         self.name=name
#
#     def eat(self):
#         print(self)
#         print("eat....")

# 实例方法
# egon=Person("egon")
# egon.eat()

# 函数
# Person.eat(123)

########################################

# class Person(object):
#
#     def __init__(self,name):
#         self.name=name
#
#     def __str__(self):
#         return self.name
#
# alex=Person("alex")
#
# print(alex.__str__())
# print(str(alex))

########################################


# def foo():
#     return
#
# print(foo.__name__)
#


########################################

# Book.objects.filter(Q(title="yuan")|Q(price=123))
#
#
# q=Q()
# q.connection="or"
# q.children.append(("title","yuan"))
# q.children.append(("price",123))


#         ret=self.model.objects.filter(title__startswith="py")
#         ret=self.model.objects.filter(price__in=[12,34,56,78,222])
#         ret=self.model.objects.filter(price__range=[10,100])
#         ret=self.model.objects.filter(title__contains="o")
#         ret=self.model.objects.filter(title__icontains="o")
#         print(ret)





#
# def foo():
#     print("ok")
#
#
# print(foo.__name__)
#
# foo.short_description="123"
# print(foo.short_description)

a=[1,2,3,4]

if isinstance(a,tuple):
    print('OK')
else:
    print('error')








