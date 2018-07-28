from django import forms
from .models import *

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('name', 'efile', )

class CompareGroupForm(forms.ModelForm):
    file1 = forms.ModelChoiceField(queryset=File.objects.all(), widget=forms.Select(attrs={'class':'form-control browser-default'}))
    file2 = forms.ModelChoiceField(queryset=File.objects.all(), widget=forms.Select(attrs={'class':'form-control browser-default'}))
    class Meta:
        model = Compare
        fields = ('title', 'file1', 'file2')