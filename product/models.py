from django.db import models
from PIL import Image
from io import BytesIO
from datetime import datetime
from django.core.files import File
# Create your models here.

class Category(models.Model):
    name = models.CharField( max_length=50)
    slug = models.SlugField()


    class Meta:
        ordering =('name',)

    def __str__(self) -> str:
        return self.name 
    def __repr__(self) -> str:
        return f'/{self.slug}/'
    
    # def get_absolute_url(self):
    #     return f'/{self.slug}/'


STATUS_CHOICES = [
    ("d", "Draft"),
    ("p", "Published"),
    ("w", "Withdrawn"),
]

class Product(models.Model):
    category = models.ForeignKey(Category,related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True,null=True )
    price = models.DecimalField(max_digits=6,decimal_places=2)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    dateinfo = models.DateField(null=False,default=datetime.now())
    class Meta:
        ordering = ('-date_added',)
     
    def __str__(self):
        return self.name
    
PLAN_CHOICES = [
    ("disabled", "Disabled"),
    ("premium", "Premium"),
]


class PlanName(models.Model):
    plan = models.CharField(max_length=255,choices=PLAN_CHOICES,null=True)
    def __str__(self):
        return self.plan

class PlanDates(models.Model):
    dates = models.DateField()
    price = models.DecimalField(max_digits=6,decimal_places=2,default=0)
    description = models.TextField(blank=True,null=True)
    plan_name = models.ForeignKey(PlanName,related_name='plan_name',on_delete=models.CASCADE)
    def __str__(self):
        return str(self.dates)
    

class Month(models.Model):
    plan_dates = models.ManyToManyField(PlanDates,related_name='plan_dates')
    plan_name = models.ManyToManyField(PlanName) 
    month = models.IntegerField()
    footer = models.TextField(blank=True,null=True)
    def __str__(self):
        return str(self.month)