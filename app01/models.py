from django.db import models

# 作者表
class Author(models.Model):
    nid = models.AutoField(primary_key=True)
    name=models.CharField( max_length=32)
    age=models.IntegerField()
    authorDetail=models.OneToOneField(to="AuthorDetail",on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# 作者详情表
class AuthorDetail(models.Model):
    nid = models.AutoField(primary_key=True)
    birthday=models.DateField()
    telephone=models.BigIntegerField()
    addr=models.CharField( max_length=64)

    def __str__(self):
        return self.telephone

# 出版社表
class Publish(models.Model):
    nid = models.AutoField(primary_key=True)
    name=models.CharField( max_length=32)
    city=models.CharField( max_length=32)
    email=models.EmailField()

    def __str__(self):
        return self.name

# 图书表
class Book(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField( max_length=32)
    publishDate=models.DateField()
    price=models.DecimalField(max_digits=5,decimal_places=2)
    publish=models.ForeignKey(to="Publish",to_field="nid",on_delete=models.CASCADE)
    authors=models.ManyToManyField(to='Author')

    def __str__(self):
        return self.title