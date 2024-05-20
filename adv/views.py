# Create your views here.
from rest_framework import viewsets
from .fields import CompositeValue
from .forms import CommentsForm, LoginForm
from .models import Adv, Club, User, Comments
from adv.serializer import AdvSerializer
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from . import forms
from . import models
import hashlib
from django.contrib.auth.decorators import login_required


def hash_code(s, salt='pj_adv'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


class AdvViewSet(viewsets.ModelViewSet):
    queryset = Adv.objects.all()
    serializer_class = AdvSerializer


def index(request):
    pass
    return render(request, 'adv/index.html')


def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = User.objects.get(name=username)
            except User.DoesNotExist:
                message = '用户不存在！'
                return render(request, 'adv/login.html', locals())

            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name

                # 获取 next 参数，如果没有则重定向到首页
                next_url = request.GET.get('next', '/index/')
                return redirect(next_url)
            else:
                message = '密码不正确！'
                return render(request, 'adv/login.html', locals())
        else:
            return render(request, 'adv/login.html', locals())

    login_form = LoginForm()
    return render(request, 'adv/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST, request.FILES)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            sex = register_form.cleaned_data.get('sex')
            job = register_form.cleaned_data.get('job')
            photo = register_form.cleaned_data['photo']

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'adv/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'adv/register.html', locals())
                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.photo = photo
                new_user.sex = sex
                new_user.job = job  # 确保保存job字段
                new_user.save()
                return redirect('/login/')  # 注册成功，重定向到登录页面

        else:
            return render(request, 'adv/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'adv/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')

    request.session.flush()
    # del request.session['is_login']
    return redirect("/login/")


# TODO
def update_club(request):  # 上传某club信息
    if request.method == 'POST':
        club_update_form = forms.ClubUpdateForm(request.POST,request.FILES)
        message = "请检查填写的内容！"
        if club_update_form.is_valid():
            username = club_update_form.cleaned_data.get('username')
            pub_date = club_update_form.cleaned_data.get('pub_date')
            photo = club_update_form.cleaned_data['photo']

            same_name_user = models.Club.objects.filter(name=username)
            if same_name_user:
                message = '该社团名已经存在，请选择其他名称'
                return render(request, 'adv/update_club.html', locals())
            new_Club = models.Club()
            new_Club.name = username
            new_Club.pub_date = pub_date
            new_Club.photo = photo
            new_Club.save()
            return redirect('/index/')  # 上传成功
        else:
            return render(request, 'adv/update_club.html', locals())
    club_update_form = forms.ClubUpdateForm()
    return render(request, 'adv/update_club.html', locals())


def update_adv(request):
    if request.method == 'POST':
        adv_form = forms.AdvUpdateForm(request.POST, request.FILES)
        message = "请检查填写的内容！"
        if adv_form.is_valid():
            club = adv_form.cleaned_data.get('club')
            title = adv_form.cleaned_data.get('title')
            pub_date = adv_form.cleaned_data.get('pub_date')
            price = adv_form.cleaned_data.get('price')
            platform = adv_form.cleaned_data.get('platform')
            photo = adv_form.cleaned_data['photo']

            same_title_adv = models.Adv.objects.filter(title=title)
            if same_title_adv.exists():
                message = '该ADV名已经存在，请选择其他名称'
                return render(request, 'adv/update_adv.html', locals())

            new_adv = models.Adv(
                club=club,
                title=title,
                pub_date=pub_date,
                price=price,
                platform=platform,
                photo=photo
            )
            new_adv.save()
            return redirect('/index/')  # 上传成功

        else:
            return render(request, 'adv/update_adv.html', locals())

    adv_form = forms.AdvUpdateForm()
    return render(request, 'adv/update_adv.html', locals())


# TODO
def comments(request):
    if request.method == 'POST':
        comments_form = CommentsForm(request.POST, request.FILES)
        if comments_form.is_valid():
            comment = comments_form.save(commit=False)
            user_name = request.session.get('user_name')
            if not user_name:
                message = "用户未登录或未找到"
                return render(request, 'adv/comments.html', {'comments_form': comments_form, 'message': message})
            user = get_object_or_404(User, name=user_name)
            comment.user = user
            composite_value = CompositeValue(
                decimal_part=comments_form.cleaned_data['decimal_part'],
                char_part=comments_form.cleaned_data['char_part']
            )
            comment.comments = composite_value
            comment.save()  # 调用 Comments 模型的 save 方法
            return redirect('/index/')
        else:
            message = "表单验证失败，请检查填写内容。"
            return render(request, 'adv/comments.html', {'comments_form': comments_form, 'message': message})
    else:
        comments_form = CommentsForm()
        return render(request, 'adv/comments.html', {'comments_form': comments_form})


def adv_list(request):
    advs = Adv.objects.all()
    return render(request, 'adv/adv_list.html', {'advs': advs})


def adv_detail(request, adv_title):
    adv = get_object_or_404(Adv, title=adv_title)
    comments = Comments.objects.filter(adv=adv).select_related('user')  # 确保包括关联的用户信息
    return render(request, 'adv/adv_detail.html', {'adv': adv, 'comments': comments})


def club_list(request):
    clubs = Club.objects.all()
    return render(request, 'adv/club_list.html', {'clubs': clubs})


def club_detail(request, club_name):
    club = get_object_or_404(Club, name=club_name)
    advs = Adv.objects.filter(club=club)  # 获取以该社团为外键的所有Adv
    return render(request, 'adv/club_detail.html', {'club': club, 'advs': advs})