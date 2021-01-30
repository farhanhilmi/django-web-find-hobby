from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.forms.models import model_to_dict

from .forms import *
from .models import *

from django.contrib.auth.hashers import make_password

from django.urls import resolve
from django.http import HttpResponse, HttpResponseForbidden

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home_page')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_page')
        else:
            messages.info(request, 'Username or Password Is Incorrect!')

    page_title = "Login | Schedular"
    context = {'page_title': page_title}
    return render(request, 'user/auth/login.html', context)


def register_page(request):
    form = CreateUser()

    if request.method == 'POST':
        form = CreateUser(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            messages.success(request, 'Account was created for ' + username)
            user = authenticate(request, username=username, password=password)

            login(request, user)
            return redirect('home_page')

    page_title = "Register | Schedular"
    context = {'form': form, 'page_title': page_title}
    # return render(request, 'user/register.html', context)

    return render(request, 'user/auth/register.html', context)


def logout_page(request):
    logout(request)
    return redirect('login_page')


@login_required(login_url='login_page')
def home_page(request):
    page_title = "Home"
    events = ListEvent.objects.filter().order_by('-date_created')
    forum = ListForum.objects.all().order_by('-date_created')

    context = {'page_title': page_title, 'events': events, 'forum': forum}
    return render(request, 'user/home.html', context)


@login_required(login_url='login_page')
def data_profile(request, username):
    account = Profile.objects.get(user_id=request.user.id)
    page_title = f"{account.name} ~ @{account.user_id.username} - Find Hobbies"

    password = make_password('Madrid007')
    if account.user_id.password == password:
        print("SAMA")
    else:
        print("BEDA")

    if request.method == 'POST':
        if request.POST['chPwd'] == 'pwdChange':
            user = User.objects.get(id=request.user.id)
            user.set_password(request.POST['pwdChange'])
            user.save()

    pwd = account.user_id.has_usable_password()
    context = {'account': account, 'pwd': pwd, 'page_title': page_title}
    return render(request, 'user/profile/setting_profile.html', context)


def update_profile(request, pk):
    profile = get_object_or_404(ListForum, pk=pk)
    if request.method == 'POST':
        form = FormProfile(request.POST, instance=profile)
    else:
        form = FormProfile(instance=profile)
    return save_forum_form(request, form, 'user/forum/update_forum_form.html', pk)


@login_required(login_url='login_page')
def cari_page(request):
    name = request.POST['cari']
    page_title = "Pencarian"
    result_cari = request.POST['cari']

    events = ListEvent.objects.filter(Q(
        name__icontains=name) | Q(description__icontains=name) | Q(alamat__icontains=name)).order_by('-date_created')
    forum = ListForum.objects.filter(Q(topic__icontains=name) | Q(
        description__icontains=name)).order_by('-date_created')
    count_event = events.count()
    count_forum = forum.count()

    context = {'page_title': page_title, 'events': events, 'forum': forum,
               'count_event': count_event, 'count_forum': count_forum, 'result_cari': result_cari}
    return render(request, 'user/hasil_cari.html', context)


@ login_required(login_url='login_page')
def list_forum(request, forumID=None):
    page_title = "List Forum"
    forum = ListForum.objects.all().order_by('-date_created')
    category = ListCategory.objects.all().order_by('name')

    page = request.GET.get('page', 1)
    paginator = Paginator(forum, 5)

    # form = FormForum()
    # category = ListCategory.objects.all()

    form = FormForum()

    # instance = get_object_or_404(ListCategory, id=request.POST['category'])
    formUpdate = FormForum(request.POST, instance=forumID)
    # print(request.GET['id'])
    if request.method == 'POST':

        form = FormForum(request.POST)

        # comment = updateCommentForm(request.POST, instance=forums)
        # form = FormForum(request.POST)
        if form.is_valid():
            # dataComment = comment.save()
            data = form.save()
            # dataComment.num_comment = forums.num_comment + 1
            data.user_id = User.objects.get(id=request.user.id)
            # dataComment.save()
            data.save()

            return redirect('list_forum')

    try:
        forum = paginator.page(page)
    except PageNotAnInteger:
        forum = paginator.page(1)
    except EmptyPage:
        forum = paginator.page(paginator.num_pages)

    return render(request, 'user/forum/list-forum.html', {'formUpdate': formUpdate, 'category': category, 'forum': forum, 'page_title': page_title, 'form': form})


@ login_required(login_url='login_page')
def save_forum_form(request, form, template_name, pk):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            # form.user_id = User.objects.get(id=request.user.id)
            form.save()
            data['form_is_valid'] = True
            data['redirect'] = True
            forum = ListForum.objects.filter(id=pk)
            data['html_list_forum'] = render_to_string('user/forum/detail-forum.html', {
                'forum': forum
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(
        template_name, context, request=request)
    return JsonResponse(data)


def update_forum(request, pk):
    frm = get_object_or_404(ListForum, pk=pk)
    if request.method == 'POST':
        form = FormForum(request.POST, instance=frm)
    else:
        form = FormForum(instance=frm)

    return save_forum_form(request, form, 'user/forum/update_forum_form.html', pk)


@ login_required(login_url='login_page')
def detail_forum(request, id):
    page_title = "Detail Forum"
    forum = ListForum.objects.filter(id=id)
    comment = ForumDiscussion.objects.filter(
        forum_id=id).order_by('-date_created')
    comment_count = comment.count()

    form = CreateInDiscussion()
    if request.method == 'POST':
        # comment = updateCommentForm(request.POST, instance=forums)
        form = CreateInDiscussion(request.POST)
        if form.is_valid():
            # dataComment = comment.save()
            comment = ListForum.objects.get(id=id)
            comment.num_comment = comment.num_comment + 1
            comment.save()
            data = form.save()
            # dataComment.num_comment = forums.num_comment + 1
            data.forum_id = ListForum.objects.get(id=id)
            data.user_id = User.objects.get(id=request.user.id)

            # dataComment.save()
            data.save()

            return redirect('detail_forum_url', id=id)

    context = {'page_title': page_title, 'forum': forum,
               'comment': comment, 'form': form, 'comment_count': comment_count}
    return render(request, 'user/forum/detail-forum.html', context)


@login_required(login_url='login_page')
def save_comment_form(request, form, template_name, pk_forum):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            # form.user_id = User.objects.get(id=request.user.id)
            form.save()
            data['form_is_valid'] = True
            data['redirect'] = True
            comment = ForumDiscussion.objects.filter(forum_id=pk_forum)
            data['html_list_comment'] = render_to_string('user/forum/detail-forum.html', {
                'comment': comment
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(
        template_name, context, request=request)
    return JsonResponse(data)


@login_required(login_url='login')
def update_comment(request, pk):
    frm = get_object_or_404(ForumDiscussion, pk=pk)
    if request.method == 'POST':
        form = CreateInDiscussion(request.POST, instance=frm)
    else:
        form = CreateInDiscussion(instance=frm)
    pk_forum = frm.forum_id.id
    return save_comment_form(request, form, 'user/forum/update_comment_form.html', pk_forum)


@login_required(login_url='login')
def delete_comment(request):
    pk = request.POST['comment_id']
    cmt = ForumDiscussion.objects.get(id=pk)
    forum_id = cmt.forum_id
    if request.user.id == cmt.user_id.id:
        cmt.delete()
        comment = ListForum.objects.get(id=forum_id.id)
        comment.num_comment = comment.num_comment - 1
        comment.save()
        return redirect('detail_forum_url', id=forum_id.id)
    return HttpResponseForbidden()


@login_required(login_url='login')
def deleteForum(request):
    pk = request.POST['id_forum']
    forums = ListForum.objects.get(id=pk)

    # if forums.user_id == request.user.id:
    forums.delete()

    return redirect('list_forum')


@ login_required(login_url='login')
def likePost(request, id):
    forum = ListForum.objects.get(id=id)
    forum.num_like = forum.num_like + 1
    forum.save()

    return redirect('detail_forum_url', id=id)


@ login_required(login_url='login_page')
def list_event(request):
    page_title = "List Event"
    events = ListEvent.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(events, 9)

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    context = {'events': events,
               'page_title': page_title}
    return render(request, 'user/event/list-event.html', context)


@login_required(login_url='login_page')
def detail_event(request, id):
    page_title = "Detail Event"
    events = ListEvent.objects.filter(id=id)
    context = {'page_title': page_title, 'events': events}
    return render(request, 'user/event/detail-event.html', context)


@login_required(login_url='login')
def hadirEvent(request, id):
    event = ListEvent.objects.get(id=id)
    event.kuota = event.kuota - 1
    event.save()

    # hd = HadirEvent
    # hd.event_id = event.id
    # hd.user_id = request.user.id
    # hd.name = event.name

    # hd.save()

    return redirect('user/event/detail-event.html', id=id)
