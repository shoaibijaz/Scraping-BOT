from django.db import models
from datetime import datetime


class Websites(models.Model):
    name = models.TextField(blank=True,null=True)
    url = models.TextField(blank=True,null=True)
    function = models.TextField(blank=True,null=True)
    search_url = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = u'app_websites'


class Categories(models.Model):
    website = models.ForeignKey(Websites, null=True, blank=True)
    name = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    parent = models.ForeignKey("self", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = u'app_categories'


class Proxies(models.Model):
    IP = models.TextField(blank=True,null=True)
    port = models.TextField(blank=True,null=True)
    country = models.TextField(blank=True,null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.IP

    class Meta:
        db_table = u'app_proxies'


class SearchLog(models.Model):
    keywords = models.TextField(blank=True,null=True)
    category = models.TextField(blank=True,null=True)
    negative = models.TextField(blank=True,null=True)
    start_time = models.DateTimeField(blank=True,null=True)
    website = models.ForeignKey(Websites, blank=True, null=True)
    proxy = models.ForeignKey(Proxies, null=True,blank=True)
    type = models.TextField(blank=True, null=True)
    total_pages = models.IntegerField(default=0)
    total_ads = models.IntegerField(default=0)

    @classmethod
    def get_safe_single(cls, item_id):

        try:
            if item_id and int(item_id):
                print(cls.objects.get(pk=int(item_id)))
                return cls.objects.get(pk=int(item_id))

            return cls()

        except Exception as ex:
            return cls()

    @classmethod
    def save_item(cls, formData, pages, ads):
        try:
            log = cls()

            log.keywords = formData["keywords"]
            log.category = formData["category"]
            log.negative = formData["negative"]
            log.start_time = datetime.now()
            log.website = formData["website"]
            log.proxy = formData["proxy"]
            log.total_pages = pages
            log.total_ads = ads

            log.save()

            return log

        except Exception as ex:
            raise ex


    def __str__(self):
        return self.keywords

    class Meta:
        db_table = u'app_search_log'


class Tasks(models.Model):

    RUNNING_STATUS = 1
    STOPPED_STATUS = 2
    COMPLETE_STATUS = 3

    STATUS_CHOICES = (
        (RUNNING_STATUS, 'Running'),
        (STOPPED_STATUS, 'Stopped'),
        (COMPLETE_STATUS, 'Completed'),
    )

    search = models.ForeignKey(SearchLog,related_name='search_tasks')
    start_time = models.DateTimeField(blank=True)
    modified_time = models.DateTimeField(blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES,default=RUNNING_STATUS)

    @classmethod
    def save(cls, search_item):
        item = cls()

        item.search = search_item
        item.start_time = datetime.now()
        item.modified_time = datetime.now()

        item.save()

    def __str__(self):
        return self.search

    class Meta:
        db_table = u'app_tasks'