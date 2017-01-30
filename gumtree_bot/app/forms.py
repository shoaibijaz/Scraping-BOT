from django import forms
from .models import *


class SearchForm(forms.Form):
    id = forms.IntegerField(widget = forms.HiddenInput, required=False)
    keywords = forms.CharField(max_length=200,required=True,initial='')
    category = forms.CharField(max_length=200,required=False,initial='')
    negative = forms.CharField(max_length=200,required=False,initial='')
    start_time = forms.CharField(max_length=50,required=False, initial='')
    end_time = forms.CharField(max_length=50,required=False, initial='')
    ads = forms.IntegerField(initial=0, required=False, widget= forms.HiddenInput)
    pages = forms.IntegerField(initial=0, required=False, widget= forms.HiddenInput)

    website = forms.ModelChoiceField(
        queryset=Websites.objects.all(),
        empty_label='Select a website',
        required=True
    )

    category = forms.ModelChoiceField(
        queryset=Categories.objects.all(),
        empty_label='Select a website',
        required=False
    )

    proxy = forms.ModelChoiceField(
        queryset=Proxies.objects.all() ,
        empty_label='Default',
        required=False
    )



class CommentForm(forms.Form):
    textarea_attr = {'placeholder': 'Message','class':'form-control', 'rows':3}
    message = forms.CharField(max_length=100, required=True, initial='', widget=forms.Textarea(attrs=textarea_attr))
    name = forms.CharField(max_length=100, required=True, initial='', widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.CharField(max_length=100,required=True,initial='', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=200,required=True,initial='', widget=forms.TextInput(attrs={'placeholder': 'Phone'}))
    ads = forms.CharField(required=False, initial='', widget=forms.HiddenInput)