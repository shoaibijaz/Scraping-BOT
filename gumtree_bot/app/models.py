from django.db import models

class SearchLog(models.Model):
    text = models.TextField(blank=False,null=False)
    url = models.TextField(blank=False,null=False)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        db_table = u'app_search_logs'


class AdsLog(models.Model):
    search = models.ForeignKey(SearchLog,related_name='ads')
    text = models.TextField(blank=False,null=False)
    url = models.TextField(blank=False,null=False)
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