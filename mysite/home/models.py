from django.db import models
from django.conf import settings
import os
# Create your models here.
class Report(models.Model):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__)).strip('/')
    title = models.CharField(max_length = 40, default= "무제")
    company_name = models.CharField(max_length = 40, default = "-")
    company_code = models.CharField(max_length = 10, default= '-')
    date = models.DateField(auto_now_add=True)
    pdf = models.FileField(upload_to = os.path.join(BASE_DIR, 'home/pdf_file'))
    favorite = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Fav', related_name='favorite_reports') # Fav 통해서 어떤 user가 자신을 Fav로 등록했는지 확인

    def __str__(self):
        return self.company_name


class Fav(models.Model) : # db생각해보면 정규화 한다고 생각하면 됨
    
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='favs_users')

    # https://docs.djangoproject.com/en/4.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ('report', 'user')

    def __str__(self) :
        return '%s likes %s'%(self.user.username, self.report.company_name[:10])