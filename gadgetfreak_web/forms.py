from django import forms

import StringIO
from PIL import Image, ImageChops

from .models import Device, TechnicalSpecification, ForumTopic, Comment, UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(label="Username:", max_length=100, widget=forms.TextInput(attrs={"class": "ignore-calc"}))
    password = forms.CharField(label="Password:", max_length=100, widget=forms.PasswordInput(attrs={"class": "ignore-calc"}))

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['title', 'description', 'img_1', 'img_2', 'img_3', 'img_4']
        widgets = {'title': forms.TextInput(attrs={"class": "ignore-calc"})}

    def clean_img_1(self):
        return resize_img(self.cleaned_data["img_1"], 280, 420)

    def clean_img_2(self):
        if self.cleaned_data.get("img_2", None):
            return resize_img(self.cleaned_data["img_2"], 280, 420)

    def clean_img_3(self):
        if self.cleaned_data.get("img_3", None):
            return resize_img(self.cleaned_data["img_3"], 280, 420)

    def clean_img_4(self):
        if self.cleaned_data.get("img_4", None):
            return resize_img(self.cleaned_data["img_4"], 280, 420)

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

    def clean_image(self):
        if self.cleaned_data.get("image", None):
            return resize_img(self.cleaned_data["image"], 280, 420)

        return None

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['contents']

class UserImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_img']

    def clean_profile_img(self):
        return resize_img(self.cleaned_data["profile_img"], 60, 60)

def resize_img(image_field, rw, rh):
    image_file = StringIO.StringIO(image_field.read())
    image = Image.open(image_file)
    w, h = image.size

    ratio = min(float(rw)/w, float(rh)/h)

    # image = image.resize((int(w*ratio), int(h*ratio)), Image.ANTIALIAS)
    # image_size = image.size
    #
    # image = image.crop((0, 0, rw, rh))
    image.thumbnail((int(w*ratio), int(h*ratio)), Image.ANTIALIAS)
    image_size = image.size
    offset_x = max( (rw - image_size[0]) / 2, 0 )
    offset_y = max( (rh - image_size[1]) / 2, 0 )

    final_img = Image.new(mode="RGBA", size=(rw, rh), color=(70, 73, 76, 0))
    final_img.paste(image, (offset_x, offset_y))

    image_file = StringIO.StringIO()
    final_img.save(image_file, 'JPEG', quality=90)

    image_field.file = image_file

    return image_field
