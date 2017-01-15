from django import forms
from django.utils.translation import ugettext_lazy as _

import StringIO
from PIL import Image, ImageChops

from .models import Device, TechnicalSpecification, ForumTopic, Comment, UserProfile

class LoginForm(forms.Form):
    """Form used for logging user in.

    Form contains two fields, username and password, which are used by the django
    auth system to log user in.
    """
    username = forms.CharField(label="Username:", max_length=100, widget=forms.TextInput(attrs={"class": "ignore-calc"}))
    password = forms.CharField(label="Password:", max_length=100, widget=forms.PasswordInput(attrs={"class": "ignore-calc"}))

class DeviceForm(forms.ModelForm):
    """Form used for editing or adding a new device

    Form is a model form, containing fields title, description, img_1, img_2,
    img_3 and img_4.
    """
    class Meta:
        model = Device
        fields = ['title', 'description', 'img_1', 'img_2', 'img_3', 'img_4']
        widgets = {'title': forms.TextInput(attrs={"class": "ignore-calc"})}

    def clean_img_1(self):
        """Resizes image 1 to resolution 280x420, used by the application
        """
        return resize_img(self.cleaned_data["img_1"], 280, 420)

    def clean_img_2(self):
        """If it exists, resizes image 2 to resolution 280x420, used by the application
        """
        if self.cleaned_data.get("img_2", None):
            return resize_img(self.cleaned_data["img_2"], 280, 420)

    def clean_img_3(self):
        """If it exists, resizes image 3 to resolution 280x420, used by the application
        """
        if self.cleaned_data.get("img_3", None):
            return resize_img(self.cleaned_data["img_3"], 280, 420)

    def clean_img_4(self):
        """If it exists, resizes image 4 to resolution 280x420, used by the application
        """
        if self.cleaned_data.get("img_4", None):
            return resize_img(self.cleaned_data["img_4"], 280, 420)

class TechnicalSpecificationForm(forms.ModelForm):
    """Form used for adding or editing technical specification

    It is a model form, which contains fields name and value. After initialization
    it sets both fields required attribute to false, since form can also be blank.
    This is verified in the view, used for editing or adding a device.
    """
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
    """Form used for adding a forum topic

    It is a model form, using the fields name, topic_type, image, score and contents.
    """
    class Meta:
        model = ForumTopic
        fields = ['name', 'topic_type', 'image', 'score', 'contents']
        widgets = {
            "topic_type": forms.RadioSelect()
        }

    def clean_image(self):
        """Function used to resize forum topc image to resolution 280x420, if it exists.
        """
        if self.cleaned_data.get("image", None):
            return resize_img(self.cleaned_data["image"], 280, 420)

        return None

class CommentForm(forms.ModelForm):
    """Form used for adding a comment to the forum topic

    It is a model form, which contains only one field - contents.
    """
    class Meta:
        model = Comment
        fields = ['contents']

class UserImageForm(forms.ModelForm):
    """Form used for changing the profile picture

    It is a model form, containing only one field - profile_img
    """
    class Meta:
        model = UserProfile
        fields = ['profile_img']
        labels = {
            'profile_img': _("Profile image")
        }

    def clean_profile_img(self):
        """Function, used for resizing profile image to resolution 60x60, used by the application
        """
        return resize_img(self.cleaned_data["profile_img"], 60, 60)

def resize_img(image_field, rw, rh):
    """Resizes image in supplied image field

    Resizes image to the parameters rw and rh. If supplied image is too large,
    image is resized. Margins of color RGB(70, 73, 76) are added, if image is too
    small or aspect ratio of the image is not 1:1.

    Keyword arguments:
    image_field -- model field, containing the image to resize
    rw -- final width of the image
    rh -- final height of the image
    """
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
