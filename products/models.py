from django.db import models
from django.db.models import CharField
from django.forms import ChoiceField
from django.urls import reverse



# Create your models here.
class product(models.Model):
    title= models.CharField(max_length=300,blank=True,null=True,verbose_name='عنوان کلاس')
    age_range = models.CharField(max_length=300,blank=True,null=True,verbose_name='رنج سنی')
    jalase_count = models.IntegerField(blank=True,null=True,verbose_name='تعداد جلسات')
    teacher = models.CharField(max_length=300,blank=True,null=True,verbose_name='نام مدرس')
    short_desc = models.CharField(max_length=500,blank=True,null=True,verbose_name='توضیحات کوتاه')
    long_desc = models.TextField(blank=True,null=True,verbose_name='توضیحات بلند')
    image= models.ImageField(upload_to='',null=True,blank=True,verbose_name='تصویر')
    slug = models.SlugField(default="", blank=True, db_index=True)

    def get_absolute_url(self):
        return reverse('detail', args=[self.slug])

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name='کلاس'
        verbose_name_plural= 'کلاس ها'

class pish_sabt(models.Model):
    age_choice = (
        ('3-6','سه الی شش سال'),
        ('6-8','شش الی هشت سال'),
        ('8-10','هشت الی ده سال'),
        ('10-15','ده الی پانزده سال'),
    )
    product_choice = models.ForeignKey(product,on_delete=models.CASCADE,blank=True
                                       ,null=True,related_name='relatedproduct',verbose_name='کلاس')
    std_name = models.CharField(max_length=300,verbose_name='نام فرزند')
    std_lastname = models.CharField(max_length=300,verbose_name='نام خانوادگی فرزند')
    age = models.CharField(max_length=300,choices=age_choice,verbose_name='رنج سنی')
    parent_name = models.CharField(max_length=300,verbose_name='نام ونام خانوادگی والد')
    mobile = models.CharField(max_length=11,verbose_name='شماره تماس')
    desc = models.TextField(verbose_name='توضیحات اضافی')
    is_read = models.BooleanField(default=False,verbose_name='خوانده شده')

    def __str__(self):
        return f'{self.std_name}'

    class Meta:
        verbose_name='پیش ثبت نام'
        verbose_name_plural= 'پیش ثبت نام ها'