from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q

import logging
import re

from .models import Device, TechnicalSpecification, ForumTopic, Comment, UserProfile
from .forms import LoginForm, DeviceForm, TechnicalSpecificationForm, ForumTopicForm, CommentForm, UserImageForm

# Create your views here.
logger = logging.getLogger(__name__)

def index(request):
    """Django view function for landing page

    Displays 5 newest reviews and devices, sorted by user score.
    The devices are paginated, pagination uses GET parameter 'offset'.
    If offset is set incorrectly, returns html error bad request.

    Keyword arguments:
    request -- django request object
    """
    sp = {
        "reviews": ForumTopic.objects.filter(topic_type="R").order_by("-date")[:5]
    }

    offset = int(request.GET.get("offset", "0"))
    q = sorted(Device.objects.all(), key=lambda e: -e.score)
    try:
        pagination = make_pagination(q, offset, list_name="devices")
    except:
        return HttpResponseBadRequest()
    sp.update(pagination)

    return render(request, "landing.html", sp)

def login_view(request):
    """Django view function for login page

    View accepts POST requests, in case of other types returns html error 404.
    It checks, if login form, sent in request, is valid and proceeds to login
    the user. If form validation or authentication fails, it redirects user to
    return url, sent in request.

    Keyword arguments:
    request -- django request object
    """
    if request.method == "POST" and request.POST["return_url"]:
        # request.POST -> slovar vsebine
        lf = LoginForm(request.POST)
        if lf.is_valid():
            u = authenticate(username=lf.cleaned_data["username"], password=lf.cleaned_data["password"])
            if u is not None:
                login(request, u) # poveze sejo z uporabnikom
        return HttpResponseRedirect(request.POST["return_url"])
    else:
        raise Http404

def logout_view(request):
    """Django view function for logout page

    View removes session from user, logging him out.
    After logout, user is redirected to landing page.

    Keyword arguments:
    request -- django request object
    """
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def device_info(request, device_id):
    """Django view function for device info page

    Checks if device id, sent in the argument, is valid. Otherwise returns 404 error.
    After that, it sets the main image of the view to the id, supplied in GET
    parameter 'img' or 1, if parameter is not present. Other images are set as
    subimages. It also returns all the technical specifications of the device.

    Keyword arguments:
    request -- django request object
    device_id -- device id to render
    """
    device = Device.objects.filter(id=device_id).first()
    if not device:
        raise Http404

    sp = {"device": device}

    sub_images = {i: e for i, e in enumerate([device.img_1, device.img_2, device.img_3, device.img_4], start=1) if e}
    print(sub_images)
    img_no = request.GET.get("img", "1")
    if img_no == "2" and device.img_2:
        sp["main_img"] = device.img_2
        del sub_images[2]
    elif img_no == "3" and device.img_3:
        sp["main_img"] = device.img_3
        del sub_images[3]
    elif img_no == "4" and device.img_4:
        sp["main_img"] = device.img_4
        del sub_images[4]
    elif device.img_1:
        sp["main_img"] = device.img_1
        del sub_images[1]

    sp["sub_images"] = sub_images

    sp["specs"] = TechnicalSpecification.objects.filter(device_id=device.id)
    return render(request, "device-info.html", sp)

@login_required(redirect_field_name=None, login_url="not_authorized")
def device_edit(request, device_id):
    """Django view function for devic editing page

    Checks if device id, sent in the argument, is valid. Otherwise returns 404 error.
    Creates correct form, used for editing the device. User can specify number of
    technical specification fields using GET parameter 'fields'. If parameter is set
    incorrectly, view returns html error bad request. If request is using method POST,
    this function checks, if set data is valid. If it is valid it saves the data and
    redirects user to edited device info page. Otherwise it displays device edit page again.

    User must be logged in to use this view.

    Keyword arguments:
    request -- django request object
    device_id -- device_id of device to edit
    """
    device = Device.objects.filter(id=device_id).first()
    if not device:
        raise Http404

    if request.method == "POST":
        device_form = DeviceForm(request.POST, request.FILES, instance=device)

        # check technical specs
        ts = []
        correct = 0
        for i in range(100):
            if str(i)+"-name" not in request.POST:
                break
            ts_form = TechnicalSpecificationForm(request.POST, prefix=str(i))
            if ts_form.is_valid():
                correct += 1
            ts.append(ts_form)

        if correct == len(ts) and device_form.is_valid():
            # vsi podatki so pravilni, lahko shranimo
            d = device_form.save()

            TechnicalSpecification.objects.filter(device_id=device.id).delete()
            for tsf in ts:
                ts_instance = tsf.save(commit=False)
                if ts_instance.name and ts_instance.value:
                    ts_instance.device_id = device.id
                    ts_instance.save()

            return HttpResponseRedirect(reverse("device_info", kwargs={"device_id": d.id}))

    else:
        device_form = DeviceForm(instance=device)

        ts = [TechnicalSpecificationForm(instance=ts, prefix=str(i)) for i, ts in enumerate(TechnicalSpecification.objects.filter(device_id=device.id))]
        fields = int(request.GET.get("fields", "0")) or len(ts) + 2
        if fields < len(ts) or fields > 100:
            return HttpResponseBadRequest()
        ts += [TechnicalSpecificationForm(prefix=str(i)) for i in range(len(ts), fields)]

    sp = {"device": device, "device_form": device_form, "specs": ts}

    return render(request, "add-device.html", sp)

@login_required(redirect_field_name=None, login_url="not_authorized")
def device_add(request):
    """Django view function for adding a device

    Creates form, used for adding a device. User can specify number of
    technical specification fields using GET parameter 'fields'. If parameter is set
    incorrectly, view returns html error bad request. If request is using method POST,
    this function checks, if set data is valid. If it is valid it saves the data and
    redirects user to added device info page. Otherwise it displays device add page again.

    User must be logged in to use this view.

    Keyword arguments:
    request -- django request object
    """
    if request.method == "POST":
        device_form = DeviceForm(request.POST, request.FILES)

        # check technical specs
        ts = []
        correct = 0
        for i in range(100):
            if str(i)+"-name" not in request.POST:
                break
            ts_form = TechnicalSpecificationForm(request.POST, prefix=str(i))
            if ts_form.is_valid():
                correct += 1
            ts.append(ts_form)

        if correct == len(ts) and device_form.is_valid():
            # vsi podatki so pravilni, lahko shranimo
            d = device_form.save()

            for tsf in ts:
                ts_instance = tsf.save(commit=False)
                if ts_instance.name and ts_instance.value:
                    ts_instance.device_id = d.id
                    ts_instance.save()

            return HttpResponseRedirect(reverse("device_info", kwargs={"device_id": d.id}))

    else:
        device_form = DeviceForm()
        fields = int(request.GET.get("fields", "4"))
        if fields > 100:
            return HttpResponseBadRequest()
        ts = [TechnicalSpecificationForm(prefix=str(i)) for i in range(fields)]

    sp = {"device": None, "device_form": DeviceForm(), "specs": ts}

    return render(request, "add-device.html", sp)

def device_forum(request, device_id):
    """Django view function for displaying device forum

    Checks if device id, sent in the argument, is valid. Otherwise returns 404 error.
    Displays all forum topics, created for the supplied device. It also uses pagination
    for displaying them. GET parameter, used for pagination is 'offset' and if set
    incorrectly, this view returns html error bad request. Topics are ordered by
    published date.

    Keyword arguments:
    request -- django request object
    device_id -- id of the device of which forum should be displayed
    """
    device = Device.objects.filter(id=device_id).first()
    if not device:
        raise Http404

    sp = {"device": device}

    offset = int(request.GET.get("offset", "0"))
    q = ForumTopic.objects.filter(device_id=device.id).order_by("date")
    try:
        pagination = make_pagination(q, offset, list_name="topics")
    except:
        return HttpResponseBadRequest()
    sp.update(pagination)

    for topic in sp.get("topics", []):
        topic.comments_no = Comment.objects.filter(forum_topic_id=topic.id).count()

    return render(request, "device-forum.html", sp)

@login_required(redirect_field_name=None, login_url="not_authorized")
def add_topic(request, device_id):
    """Django view for page for adding forum topic

    Checks if device id, sent in the argument, is valid. Otherwise returns 404 error.
    Displays form for adding a forum topic. If request method is POST it checks,
    if sent form is valid and if it is, it saves the topic and redirects user to
    device forum page. Otherwise it displays form for adding the topic again.

    Keyword arguments:
    request -- django request object
    device_id -- device id of which the topic will be added
    """
    device = Device.objects.filter(id=device_id).first()
    if not device:
        raise Http404

    if request.method == "POST":
        topic_form = ForumTopicForm(request.POST, request.FILES)
        if topic_form.is_valid():
            ft_instance = topic_form.save(commit=False)
            if ft_instance.topic_type == ft_instance.COMMENT_TYPE or \
                    ft_instance.image and ft_instance.score:
                ft_instance.device_id = device.id
                ft_instance.author_id = request.user.id
                ft_instance.save()
                return HttpResponseRedirect(reverse("device_forum", kwargs={"device_id": device.id}))
    else:
        topic_form = ForumTopicForm()

    sp = {"device": device, "topic_form": topic_form}

    return render(request, "add-topic.html", sp)

def topic(request, device_id, topic_id):
    """Django view for displaying forum topic

    Checks if device id and forum topic id, sent in the argument, is valid.
    Otherwise returns 404 error. Displays the forum topic page with all comments.
    The comments are paginated. Pagination uses GET parameter 'offset'. If it is set
    incorrectly, view returns html error bad request. Page also supplies form for
    adding a comment to the topic. If request uses POST method, it checks if supplied
    comment form is valid and if it is, it redirects user to the topic page.
    Otherwise it displays same comment form again.

    User can add comment only, if he is logged in.

    Keyword arguments:
    request -- django request object
    device_id -- device id of forum to display
    topic_id -- topic id of topic to display
    """
    device = Device.objects.filter(id=device_id).first()
    topic = ForumTopic.objects.filter(id=topic_id).first()
    if not device or not topic:
        raise Http404

    if request.method == "POST" and request.user.is_authenticated():
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            cf_instance = comment_form.save(commit=False)
            cf_instance.forum_topic_id = topic.id
            cf_instance.author_id = request.user.id
            cf_instance.save()
            return HttpResponseRedirect(reverse("topic", kwargs={"device_id": device.id, "topic_id": topic.id}))
    else:
        comment_form = CommentForm()

    sp = {
        "device": device,
        "topic": topic,
        "comment_form": comment_form,
    }

    offset = int(request.GET.get("offset", "0"))
    q = Comment.objects.filter(forum_topic_id=topic.id).order_by("date")
    try:
        pagination = make_pagination(q, offset, list_name="comments")
    except:
        return HttpResponseBadRequest()
    sp.update(pagination)

    return render(request, "topic.html", sp)

@login_required(redirect_field_name=None, login_url="not_authorized")
def profile(request):
    """Django view for profile page

    Displays profile page with two forms - one for changing the password and other
    for changing the profile picture. If request method is POST, view checks which
    form is being sent. After that it checks form validness and if correct it updates
    user information. Otherwise it displays same forms again.

    User can access this page only, if he is logged in.

    Keyword arguments:
    request -- django request object
    """
    if request.method == "POST":
        if request.FILES.get("profile_img", None):
            user_image_form = UserImageForm(request.POST, request.FILES)
            if user_image_form.is_valid():
                uif_instance = user_image_form.save(commit=False)
                uif_instance.user_id = request.user.id

                UserProfile.objects.filter(user_id=request.user.id).delete()
                uif_instance.save()
                return HttpResponseRedirect(reverse("profile"))

            password_change_form = PasswordChangeForm(user=request.user)
        elif request.POST.get("old_password", None):
            password_change_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_change_form.is_valid():
                password_change_form.save()
                update_session_auth_hash(request, password_change_form.user)

                return HttpResponseRedirect(reverse("profile"))

            user_image_form = UserImageForm()
        else:
            return HttpResponseBadRequest()

    else:
        user_image_form = UserImageForm()
        password_change_form = PasswordChangeForm(user=request.user)

    sp = {
        "devices_created": Device.objects.filter(author_id=request.user.id).count(),
        "reviews_posted": ForumTopic.objects.filter(author_id=request.user.id, topic_type="R").count(),
        "comments_posted": ForumTopic.objects.filter(author_id=request.user.id, topic_type="C").count(),

        "user_image_form": user_image_form,
        "password_change_form": password_change_form
    }
    return render(request, "profile.html", sp)

def register(request):
    """Django view for registration page

    This page displays form for registering the user. If request method is POST,
    it checks, if sent data is correct and if it is, it registers the user. Otherwise
    it displays same form again.

    Keyword arguments:
    request -- django request object
    """
    if request.method == "POST":
        user_creation_form = UserCreationForm(request.POST)
        user_image_form = UserImageForm(request.POST, request.FILES)
        if user_creation_form.is_valid() and user_image_form.is_valid():
            u = user_creation_form.save()
            ui = user_image_form.save(commit=False)
            ui.user = u
            ui.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        user_creation_form = UserCreationForm()
        user_image_form = UserImageForm()

    sp = {
        "user_creation_form": user_creation_form,
        "user_image_form": user_image_form
    }
    return render(request, "register.html", sp)

@login_required(redirect_field_name=None, login_url="not_authorized")
def search(request):
    """Django view for search results page

    View checks, if request contains GET parameter 'q'. If it is blank, it redirects
    user to landing page and if it is not supplied, it sends back html error bad request.
    Otherwise it searches every device's title and description for keywords in supplied
    parameter. It returns page with all found entries.

    User can access this page only, if he is logged in.

    Keyword arguments:
    request -- django request object
    """
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['title', 'description',])

        sp = { 'query_string': query_string }

        offset = int(request.GET.get("offset", "0"))
        q = Device.objects.filter(entry_query)
        try:
            pagination = make_pagination(q, offset, list_name="found_entries")
        except:
            return HttpResponseBadRequest()
        sp.update(pagination)

        return render(request, 'search.html', sp)
    elif ('q' in request.GET):
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseBadRequest()

@permission_required("gadgetfreak_web.delete_device", login_url="not_authorized")
def device_delete(request, device_id):
    """Django view used for deleting the device

    Checks if device id, sent in the argument, is valid. Otherwise returns 404 error.
    Deletes the device with supplied id and redirects user to the landing page.

    User can acces this view only if it has permission, to delete the
    device ('gadgetfreak_web.delete_device'). Permission is granted to users in group
    'Moderators'.

    Keyword arguments:
    request -- django request object
    device_id -- id of the device to delete
    """
    device = Device.objects.filter(id=device_id).first()
    if not device:
        raise Http404

    device.delete()

    return HttpResponseRedirect(reverse("index"))

def not_authorized(request):
    """Django view, used for displaying unauthorized error.

    Simple view, which displays html error 401 - unauthorized. It is used by
    decorators 'login_required' and 'permission_required' as the redirect page
    of unauthorized requests.

    Keyword arguments:
    request -- django request object
    """
    return HttpResponse("Unauthorized", status=401)














def make_pagination(query, offset, list_name="objects"):
    """Makes pagination of things supplied by the query.

    All objects, supplied in the query object are paginated. Current page is
    calculated using the offset parameter. Returns dictionary of four items, which
    should be combined with dictionary, sent to django render method. The dictionary
    contains list of objects on the current page, current page number, tuples of next
    pages and tuples of previous pages. Tuples are of the following format: (page_number, page_offset)

    To include pagination in the actual template, you should include 'pagintaion.html'
    in your template.

    Keyword arguments:
    query -- query of all the objects to paginate
    offset -- offset of current page
    list_name -- name of the list in dictionary, which contains objects on the current page
    """
    if type(query) == list:
        objs = len(query)
    else:
        objs = query.count()
    if objs == 0:
        return dict()
    if offset >= objs or offset%5 != 0:
        raise Exception("Bad request")

    page = offset/5 + 1
    prev_pages = list(enumerate(range(0, offset, 5), start=1))
    next_pages = list(enumerate(range(offset+5, objs, 5), start=page+1))

    d = {
        list_name: query[offset:offset+5],
        "page": page,
        "next_pages": next_pages,
        "prev_pages": prev_pages,
    }

    return d

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
