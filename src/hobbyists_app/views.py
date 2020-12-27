from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import *
from .models import *


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
def cari_page(request, name):
    page_title = "Pencarian"
    events = ListEvent.objects.filter(
        name__contains=name).order_by('-date_created')
    forum = ListForum.objects.filter(
        topic__contains=name).order_by('-date_created')

    context = {'page_title': page_title, 'events': events, 'forum': forum}
    return render(request, 'user/hasil_cari.html', context)


@login_required(login_url='login_page')
def list_forum(request):
    page_title = "List Forum"
    forum = ListForum.objects.all()

    # form = FormForum()
    form = FormForum()
    category = ListCategory.objects.all()
    if request.method == 'POST':
        # comment = updateCommentForm(request.POST, instance=forums)
        form = FormForum(request.POST)
        if form.is_valid():
            # dataComment = comment.save()
            data = form.save()
            # dataComment.num_comment = forums.num_comment + 1
            data.user_id = User.objects.get(id=request.user.id)
            ct = request.POST['name']
            data.category = ct
            # dataComment.save()
            data.save()

            return redirect('list_forum')

    return render(request, 'user/forum/list-forum.html', {'category': category, 'forum': forum, 'page_title': page_title, 'form': form})


@ login_required(login_url='login_page')
def detail_forum(request, id):
    page_title = "Detail Forum"
    forum = ListForum.objects.filter(id=id)
    comment = ForumDiscussion.objects.filter(forum_id=id)

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
               'comment': comment, 'form': form}
    return render(request, 'user/forum/detail-forum.html', context)


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
