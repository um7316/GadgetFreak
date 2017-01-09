from django import forms

from .models import Device, TechnicalSpecification, ForumTopic

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

    def __init__(self, *args, **kwargs):
        super(TechnicalSpecificationForm, self).__init__(*args, **kwargs)

        for fk in self.fields:
            self.fields[fk].required = False

class ForumTopicForm(forms.ModelForm):
    class Meta:
        model = ForumTopic
        fields = ['name', 'topic_type', 'image', 'score', 'contents']
        widgets = {
            "topic_type": forms.RadioSelect()
        }
