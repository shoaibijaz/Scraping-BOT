# -*- coding: utf-8 -*-

from django.db import models
from datetime import datetime


class Websites(models.Model):
    name = models.TextField(blank=True,null=True)
    url = models.TextField(blank=True,null=True)
    function = models.TextField(blank=True,null=True)
    search_url = models.TextField(blank=True,null=True)
    country = models.TextField(blank=True,null=True)
    comment_url = models.TextField(blank=True,null=True)
    order = models.IntegerField(null=True,default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = u'app_websites'


class Categories(models.Model):
    website = models.ForeignKey(Websites, null=True, blank=True)
    name = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    parent = models.ForeignKey("self", null=True, blank=True)
    order = models.IntegerField(default=0, null=True,blank=True)

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
    negative = models.TextField(blank=True,null=True)
    start_time = models.DateTimeField(blank=True,null=True)
    website = models.ForeignKey(Websites, blank=True, null=True)
    proxy = models.ForeignKey(Proxies, null=True,blank=True)
    type = models.TextField(blank=True, null=True)
    total_pages = models.IntegerField(default=0)
    total_ads = models.IntegerField(default=0)
    category = models.ForeignKey(Categories, blank=True, null=True)

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

            log.category = formData["category"]

            log.save()

            return log

        except Exception as ex:
            raise ex

    def __str__(self):
        return self.keywords

    class Meta:
        db_table = u'app_search_log'


class Tasks(models.Model):

    PENDING_STATUS = 1
    RUNNING_STATUS = 2
    STOPPED_STATUS = 3
    COMPLETE_STATUS = 4
    ERROR_STATUS = 5

    STATUS_CHOICES = (
        (PENDING_STATUS, 'Pending'),
        (RUNNING_STATUS, 'Running'),
        (STOPPED_STATUS, 'Stopped'),
        (COMPLETE_STATUS, 'Completed'),
        (ERROR_STATUS, 'Error'),
    )

    search = models.ForeignKey(SearchLog,related_name='search_tasks')
    start_time = models.DateTimeField(blank=True)
    modified_time = models.DateTimeField(blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES,default=PENDING_STATUS)

    def update_status(self, status):

        self.modified_time = datetime.now()
        self.status = status;
        self.save()

    @classmethod
    def update_status_log_tasks(cls, search_log, status):
        items = cls.objects.filter(search=search_log)

        count = 0

        for item in items:
            item.status = status
            item.modified_time = datetime.now()
            item.save()
            count += 1

        return count

    @classmethod
    def save_item(cls, search_item, status):
        item = cls()

        return type(search_item)
        
        if type(search_item) is int or type(search_item) is str:
            item.search_id = int(search_item)
        elif type(search_item) is SearchLog:
            item.search = search_item

        item.start_time = datetime.now()
        item.modified_time = datetime.now()
        item.status = status

        item.save()

        return item

    def __str__(self):
        return self.search

    class Meta:
        db_table = u'app_tasks'


class FetchedAds(models.Model):

    VISIBLE_STATUS = 1
    DELETE_STATUS = 2
    INVALID_STATUS = 3

    STATUS_CHOICES = (
        (VISIBLE_STATUS, 'VISIBLE'),
        (VISIBLE_STATUS, 'SOFT DELETE'),
        (INVALID_STATUS, 'INVALID'),
    )

    task = models.ForeignKey(Tasks, related_name='fetched_ads')

    ad_id = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null= True)
    posted_on = models.TextField(blank=True, null=True)
    price = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    page = models.IntegerField(blank=True, null=True, default=0)
    created_time = models.DateTimeField(blank=True)
    modified_time = models.DateTimeField(blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES,default=VISIBLE_STATUS)

    def __str__(self):
        return self.name

    class Meta:
        db_table = u'app_fetched_ads'


class AdsMessages(models.Model):

    SENT_STATUS = 1
    FAILED_STATUS = 2
    PENDING_STATUS = 3

    STATUS_CHOICES = (
        (SENT_STATUS, 'SENT'),
        (FAILED_STATUS, 'FAILED'),
        (PENDING_STATUS, 'PENDING'),
    )

    ad = models.ForeignKey(FetchedAds)

    message = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null= True)
    email = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    created_time = models.DateTimeField(blank=True)
    modified_time = models.DateTimeField(blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES,default=PENDING_STATUS)

    @classmethod
    def save_item(cls, form_data, ad, status):
        item = cls()

        if type(ad) is str:
            item.ad_id =ad
        else:
            item.ad = ad

        item.message = form_data['message']
        item.name = form_data['name']
        item.email = form_data['email']
        item.phone = form_data['phone']
        item.created_time = datetime.now()
        item.modified_time = datetime.now()
        item.status = status

        item.save()

    def __str__(self):
        return self.name

    class Meta:
        db_table = u'ads_messages'
