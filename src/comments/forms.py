from django import forms
from django.forms.widgets import HiddenInput, Textarea

class CommentForm(forms.Form):
    content_type = forms.CharField(widget=HiddenInput)
    object_id    = forms.IntegerField(widget=HiddenInput)
    #parent_id    = forms.IntegerField(widget=HiddenInput)
    content      = forms.CharField(widget=Textarea,label = 'Put Your Comments here.')
