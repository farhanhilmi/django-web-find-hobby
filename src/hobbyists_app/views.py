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
    context = {'page_title': page_title}
    return render(request, 'user/home.html', context)


@login_required(login_url='login_page')
def list_forum(request):
    page_title = "List Forum"
    forum = ListForum.objects.all()
    return render(request, 'user/forum/list-forum.html', {'forum': forum, 'page_title': page_title})


@login_required(login_url='login_page')
def save_forum_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            # form.user_id = User.objects.get(id=request.user.id)
            form.save()
            data['form_is_valid'] = True
            forum = ListForum.objects.all()
            data['html_list_forum'] = render_to_string('user/forum/list_data_forum.html', {
                'forum': forum
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(
        template_name, context, request=request)
    return JsonResponse(data)


@login_required(login_url='login_page')
def forum_add(request):
    if request.method == 'POST':
        form = FormForum(request.POST)
    else:
        form = FormForum()
    return save_forum_form(request, form, 'user/forum/forum_create.html')


@login_required(login_url='login_page')
def forum_update(request, pk):
    forum = get_object_or_404(ListTask, pk=pk)
    if request.method == 'POST':
        form = FormForum(request.POST, instance=forum)
    else:
        form = FormForum(instance=forum)
    return save_tugas_form(request, form, 'user/forum/update_forum.html')


@login_required(login_url='login_page')
def forum_delete(request, pk):
    forum = get_object_or_404(ListTask, pk=pk)
    data = dict()
    if request.method == 'POST':
        forum.delete()
        data['form_is_valid'] = True
        forum = ListForum.objects.all()
        data['html_list_forum'] = render_to_string('user/forum/list_data_forum.html', {
            'forum': forum
        })
    else:
        context = {'forum': forum}
        data['html_form'] = render_to_string(
            'user/forum/delete_forum.html', context, request=request)
    return JsonResponse(data)


@login_required(login_url='login_page')
def detail_forum(request):
    page_title = "Detail Forum"
    context = {'page_title': page_title}
    return render(request, 'user/forum/detail-forum.html', context)


@login_required(login_url='login_page')
def list_event(request):
    page_title = "List Event"
    context = {'page_title': page_title}
    return render(request, 'user/event/list-event.html', context)


@login_required(login_url='login_page')
def detail_event(request):
    page_title = "Detail Event"
    context = {'page_title': page_title}
    return render(request, 'user/event/detail-event.html', context)
