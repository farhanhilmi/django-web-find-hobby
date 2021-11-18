import json
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
        print("NAME", username)
        print("NAME", password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("LOGIN")
            return redirect('home_page')
        else:
            print("TIDAK")
            messages.info(request, 'Username or Password Is Incorrect!')

    page_title = "Login | Find Hobby"
    context = {'page_title': page_title}
    return render(request, 'user/auth/login.html', context)


def register_page(request):
    form = FormUser()

    if request.method == 'POST':
        form = FormUser(request.POST)

        if form.is_valid():
            user = form.save(commit = False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user.password = make_password(password)

            usr = User.objects.latest('id')
            profile = Profile(user_id=user, name=first_name + " " + last_name)
            # profile = FormUser(request.POST['name'], instance=usr)
            user.save()
            profile.save()
            print('ZZAZ PROFILE: ', profile)
            messages.success(request, 'Account was created for ' + username)

            login(request, user)
            return redirect('home_page')

    page_title = "Register | Find Hobby"
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

    instance_profile = Profile.objects.get(id=account.id)
    form_profile = FormProfileUpdate(request.POST or None, instance=instance_profile)

    instance_user = User.objects.get(id=request.user.id)
    form_user = FormUserUpdate(request.POST or None, instance=instance_user)
    # print(instance_user)
    # print(instance_profile)
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
        else:
            if form_user.is_valid() and form_profile.is_valid():
                form_user.save()
                data = form_profile.save()
                data.name = form_user.cleaned_data['first_name'] + " " + form_user.cleaned_data['last_name']
                data.save()
                print('BERHASIL')
                return redirect('profile_url', username=username)
            else:
                print('JAJAJA')


    pwd = account.user_id.has_usable_password()
    context = {'account': account, 'pwd': pwd, 'page_title': page_title, 'form_user':form_user,'form_profile':form_profile}
    return render(request, 'user/profile/setting_profile.html', context)


def update_profile(request, pk):
    account = Profile.objects.get(user_id=request.user.id)
    page_title = f"{account.name} ~ @{account.user_id.username} - Find Hobbies"
    pwd = account.user_id.has_usable_password()

    profile = Profile.objects.get(user_id=request.user.id)
    # user = get_object_or_404(User, pk=pk)

    profile.phone = "081"
    profile.save()
    print("LALAL: ", profile)

    context = {'account': account, 'pwd': pwd, 'page_title': page_title}
    return render(request, 'user/profile/setting_profile.html', context)


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
    # instanceFORUM = ListForum.objects.get(id=id)
    

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

    instance = ListForum.objects.get(id=id)
    form_edit = FormForum(request.POST or None, instance=instance)

    sudahLike = 1

    jsonDec = json.decoder.JSONDecoder()
    like_user = jsonDec.decode(instance.like_user)
    print(len(like_user))

    if request.user.id in like_user:
        sudahLike = 1
    else:
        sudahLike = 0

    form = CreateInDiscussion()
    if request.method == 'POST':
        if request.POST['aksiForum'] == 'addKomen':
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
        
        elif request.POST['aksiForum'] == 'updateForum':
            if request.method == 'POST':
                form_edit = FormForum(request.POST, request.FILES, instance=instance)
                if form_edit.is_valid():
                    form_edit.save()
                    return redirect('detail_forum_url', id=id)
                else:
                    print('JAJAJA')

    context = {'page_title': page_title, 'like_user': len(like_user), 'sudahLike':sudahLike ,'forum': forum,
               'comment': comment, 'form': form, 'comment_count': comment_count, 'form_edit':form_edit}
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
            data['html_list_comment'] = render_to_string('user/forum/comments.html', {
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
    pk = request.POST['forumID']
    forum = ListForum.objects.get(id=pk)

    # if forum.user_id == request.user.id:
    forum.delete()

    return redirect('list_forum')


@ login_required(login_url='login')
def likePost(request, id):
    forum = ListForum.objects.get(id=id)
    # if forum.hadir == None:
    jsonDec = json.decoder.JSONDecoder()
    lds = jsonDec.decode(forum.like_user)
    # print(baru)
    if request.user.id in lds:
        if len(lds) == 1:
            # baru = lds.remove(request.user.id)
            forum.like_user = json.dumps([])
            forum.num_like = 0
            forum.save()
            return redirect('detail_forum_url', id=id)
        else:
            lds.remove(request.user.id)
            forum.like_user = json.dumps(lds)
            forum.num_like = forum.num_like - 1
            forum.save()
            return redirect('detail_forum_url', id=id)
    else:
        baru = lds + [request.user.id]
        forum.like_user = json.dumps(baru)
        forum.num_like = forum.num_like + 1
        forum.save()
    # baru = lds.remove(request.user.id)
    # print([baru])

# # 
#     forum = ListForum.objects.get(id=id)
#     if forum.user_like == request.user.id:
#         forum.num_like = forum.num_like - 1
#         forum.user_like = 0
#     else:
#         forum.num_like = forum.num_like + 1
#         forum.user_like = request.user.id

#     print(forum.user_like)
#     forum.save()

    return redirect('detail_forum_url', id=id)


@ login_required(login_url='login_page')
def list_event(request, msg='None'):
    page_title = "List Event"
    events = ListEvent.objects.filter().order_by('-date_created')
    form = FormEvent()

    page = request.GET.get('page', 1)
    paginator = Paginator(events, 9)

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    message = msg

    context = {'events': events,
               'page_title': page_title, 'form': form, 'message':message}
   
    return render(request, 'user/event/list-event.html', context)


@ login_required(login_url='login_page')
def tambah_event(request):
    form = FormEvent()
    # comment = updateCommentForm(request.POST, instance=forums)
    form = FormEvent(request.POST, request.FILES)
    instance = User.objects.get(id=request.user.id)

    if form.is_valid():
        data = form.save()
        # data.user_id = ListEvent(instance=instance)
        data.save()
    return redirect('list_event_url')

@login_required(login_url='login_page')
def hapus_event(request):
    pk = request.POST['eventID']
    event = ListEvent.objects.get(id=pk)

    # if event.user_id == request.user.id:
    event.delete()
    return redirect('list_event_url')

@login_required(login_url='login_page')
def detail_event(request, id):
    page_title = "Detail Event"
    events = ListEvent.objects.filter(id=id)
    # print(events.hadir)
    # print(ListEvent.get_hadir)
    event = ListEvent.objects.get(id=id)

    instance = ListEvent.objects.get(id=id)
    form_edit = FormEvent(request.POST or None, instance=instance)
    jsonDec = json.decoder.JSONDecoder()
    hadir = jsonDec.decode(event.hadir)
    print(len(hadir))

    sudahHadir = False

    if request.user.id in hadir:
        sudahHadir = True
    else:
        sudahHadir = False
    # request.FILES
    if request.method == 'POST':
        form_edit = FormEvent(request.POST, request.FILES, instance=instance)
        if form_edit.is_valid():
            form_edit.save()
            return redirect('detail_event_url', id=id)
        else:
            print('JAJAJA')

    context = {'page_title': page_title, 'events': events,
               'hadir': len(hadir), 'sudahHadir': sudahHadir, 'form_edit':form_edit}
    return render(request, 'user/event/detail-event.html', context)

@login_required(login_url='login')
def update_event(request):
    instance = ListEvent.objects.get(id=request.POST['userID'])
    form = MyForm(request.POST, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('list_event_url')
        
    return redirect('home_page')  

@login_required(login_url='login')
def hadirEvent(request, id):
    event = ListEvent.objects.get(id=id)
    # if event.hadir == None:
    jsonDec = json.decoder.JSONDecoder()
    lds = jsonDec.decode(event.hadir)
    baru = lds + [request.user.id]
    # print(baru)

    if request.user.id in lds:
        print('SUDAH HADIR')
    else:
        event.hadir = json.dumps(baru)
        event.kuota = event.kuota - 1
        event.save()

    return redirect('detail_event_url', id=id)
