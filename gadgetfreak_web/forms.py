from django import forms

from .models import Device, TechnicalSpecification

class LoginForm(forms.Form):
    username = forms.CharField(label="Username:", max_length=100, widget=forms.TextInput(attrs={"class": "ignore-calc"}))
    password = forms.CharField(label="Password:", max_length=100, widget=forms.PasswordInput(attrs={"class": "ignore-calc"}))

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['title', 'description', 'img_1', 'img_2', 'img_3', 'img_4']
        widgets = {'title': forms.TextInput(attrs={"class": "ignore-calc"})}

class TechnicalSpecificationForm(forms.ModelForm):
    class Meta:
        model = TechnicalSpecification
        fields = ['name', 'value']
        widgets = {'name': forms.TextInput(attrs={"placeholder": "specification", "size": "10"}),
                   'value': forms.TextInput(attrs={"placeholder": "value", "size": "10"})}
