from django import forms
from django.forms.fields import CharField
from django.forms.widgets import SelectDateWidget
from pagedown.widgets import PagedownWidget
from .models import Post

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget)
    publish = forms.DateField(widget=SelectDateWidget)

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'draft',
            'category',
            'publish'
        ]