from django.db import models
from datetime import datetime
import pytz

class SearchLog(models.Model):
    text = models.TextField(blank=False,null=False)
    url = models.TextField(blank=False,null=False)
    source = models.TextField(blank=True,null=True,default='manual')
    proxy = models.TextField(blank=True,null=True,default='')
    pages = models.IntegerField(blank=True,default=0)
    ads_count = models.IntegerField(blank=True,default=0)
    request_type = models.TextField(blank=True,null=True,default='')
    create_date = models.DateTimeField(default=datetime.now(pytz.utc))

    @classmethod
    def count_keyword(cls, keyword):
        return cls.objects.filter(text__icontains=keyword).count()


    @classmethod
    def first_by_keyword(cls, keyword):
        return cls.objects.filter(text__icontains=keyword).first()

    def __str__(self):
        return self.text

    class Meta:
        db_table = u'app_search_logs'


class AdsLog(models.Model):
    search = models.ForeignKey(SearchLog,related_name='ads')
    text = models.TextField(blank=False,null=False)
    url = models.TextField(blank=False,null=False)
    posted = models.TextField(blank=True,null=True)
    published_in = models.TextField(blank=True,null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        db_table = u'app_ads_logs'


class AdsComment(models.Model):
    ad = models.ForeignKey(AdsLog,related_name='Comments')
    text = models.TextField(blank=False,null=False)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        db_table = u'app_ads_comment'