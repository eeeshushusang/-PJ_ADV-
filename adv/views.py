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


def hash_code(s, salt="pj_adv"):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


class AdvViewSet(viewsets.ModelViewSet):
    queryset = Adv.objects.all()
    serializer_class = AdvSerializer


def index(request):
    pass
    return render(request, "index.html")


def login(request):
    if request.session.get("is_login", None):  # 不允许重复登录
        return redirect("/index/")

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")
            try:
                user = User.objects.get(name=username)
            except User.DoesNotExist:
                message = "用户不存在！"
                return render(request, "login.html", locals())

            if user.password == password:
                request.session["is_login"] = True
                request.session["user_id"] = user.id
                request.session["user_name"] = user.name

                # 获取 next 参数，如果没有则重定向到首页
                next_url = request.GET.get("next", "/index/")
                return redirect(next_url)
            else:
                message = "密码不正确！"
                return render(request, "login.html", locals())
        else:
            return render(request, "login.html", locals())

    login_form = LoginForm()
    return render(request, "login.html", locals())


def register(request):
    if request.session.get("is_login", None):
        return redirect("/index/")

    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST, request.FILES)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get("username")
            password1 = register_form.cleaned_data.get("password1")
            password2 = register_form.cleaned_data.get("password2")
            sex = register_form.cleaned_data.get("sex")
            job = register_form.cleaned_data.get("job")
            photo = register_form.cleaned_data["photo"]

            if password1 != password2:
                message = "两次输入的密码不同！"
                return render(request, "register.html", locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = "用户名已经存在"
                    return render(request, "register.html", locals())
                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.photo = photo
                new_user.sex = sex
                new_user.job = job  # 确保保存job字段
                new_user.save()
                return redirect("/login/")  # 注册成功，重定向到登录页面

        else:
            return render(request, "register.html", locals())
    register_form = forms.RegisterForm()
    return render(request, "register.html", locals())


def logout(request):
    if not request.session.get("is_login", None):
        return redirect("/login/")

    request.session.flush()
    # del request.session['is_login']
    return redirect("/login/")


def update_club(request):  # 上传某club信息
    if request.method == "POST":
        club_update_form = forms.ClubUpdateForm(request.POST, request.FILES)
        message = "请检查填写的内容！"
        if club_update_form.is_valid():
            username = club_update_form.cleaned_data.get("username")
            pub_date = club_update_form.cleaned_data.get("pub_date")
            photo = club_update_form.cleaned_data["photo"]

            same_name_user = models.Club.objects.filter(name=username)
            if same_name_user:
                message = "该社团名已经存在，请选择其他名称"
                return render(request, "update_club.html", locals())
            new_Club = models.Club()
            new_Club.name = username
            new_Club.pub_date = pub_date
            new_Club.photo = photo
            new_Club.save()
            return redirect("/index/")  # 上传成功
        else:
            return render(request, "update_club.html", locals())
    club_update_form = forms.ClubUpdateForm()
    return render(request, "update_club.html", locals())


def update_adv(request):
    if request.method == "POST":
        adv_form = forms.AdvUpdateForm(request.POST, request.FILES)
        message = "请检查填写的内容！"
        if adv_form.is_valid():
            club = adv_form.cleaned_data.get("club")
            title = adv_form.cleaned_data.get("title")
            pub_date = adv_form.cleaned_data.get("pub_date")
            price = adv_form.cleaned_data.get("price")
            platform = adv_form.cleaned_data.get("platform")
            photo = adv_form.cleaned_data["photo"]

            same_title_adv = models.Adv.objects.filter(title=title)
            if same_title_adv.exists():
                message = "该ADV名已经存在，请选择其他名称"
                return render(request, "update_adv.html", locals())

            new_adv = models.Adv(
                club=club,
                title=title,
                pub_date=pub_date,
                price=price,
                platform=platform,
                photo=photo,
            )
            new_adv.save()
            return redirect("/index/")  # 上传成功

        else:
            return render(request, "update_adv.html", locals())

    adv_form = forms.AdvUpdateForm()
    return render(request, "update_adv.html", locals())


def comments(request):
    if request.method == "POST":
        comments_form = CommentsForm(request.POST, request.FILES)
        if comments_form.is_valid():
            comment = comments_form.save(commit=False)
            user_name = request.session.get("user_name")
            if not user_name:
                message = "用户未登录或未找到"
                return render(
                    request,
                    "comments.html",
                    {"comments_form": comments_form, "message": message},
                )
            user = get_object_or_404(User, name=user_name)
            comment.user = user
            composite_value = CompositeValue(
                decimal_part=comments_form.cleaned_data["decimal_part"],
                char_part=comments_form.cleaned_data["char_part"],
            )
            comment.comments = composite_value
            comment.save()  # 调用 Comments 模型的 save 方法
            return redirect("/index/")
        else:
            message = "表单验证失败，请检查填写内容。"
            return render(
                request,
                "comments.html",
                {"comments_form": comments_form, "message": message},
            )
    else:
        comments_form = CommentsForm()
        return render(request, "comments.html", {"comments_form": comments_form})


def adv_list(request):
    advs = Adv.objects.all()
    return render(request, "adv_list.html", {"advs": advs})


def adv_detail(request, adv_title):
    adv = get_object_or_404(Adv, title=adv_title)
    comments = Comments.objects.filter(adv=adv).select_related(
        "user"
    )  # 确保包括关联的用户信息
    # 根据 ADV 的标题设置对应的 BGM
    bgm_files = {
        "高考恋爱一百天": "adv/bgm/Days - Nuit Silencieuse.mp3",
        "Summer Pockets": "adv/bgm/麻枝准 - Sea, You & Me.mp3",
        "樱之刻  在樱花之森下漫步": "adv/bgm/松本文紀 - 櫻ノ詩 -2023Mix inst ver-.mp3",
        "樱之诗  在樱花之森上飞舞": "adv/bgm/松本文紀 - 夢の歩みを見上げて.mp3",
        "战国兰斯": "adv/bgm/アリスソフト - My Glorious Days.mp3",
        "兰斯10 决战": "adv/bgm/アリスソフト - the end.mp3",
        "White Album": "adv/bgm/石川真也 - FILL YOU.mp3",
        "White Album2": "adv/bgm/石川真也 - あの頃のように.mp3",
        "Clannad": "adv/bgm/麻枝准 - 同じ高みへ.mp3",
    }
    bgm_file = bgm_files.get(adv.title, "默认 BGM 文件路径")

    context = {"adv": adv, "comments": comments, "bgm": bgm_file}
    return render(request, "adv_detail.html", context)


def club_list(request):
    clubs = Club.objects.all()
    return render(request, "club_list.html", {"clubs": clubs})


def club_detail(request, club_name):
    club = get_object_or_404(Club, name=club_name)
    advs = Adv.objects.filter(club=club)

    # 根据 club 的名称设置对应的 BGM
    bgm_files = {
        "Key": "adv/bgm/麻枝准,Key Sounds Label - 渚.mp3",
        "Leaf": "adv/bgm/上原れな - 届かない恋 (Instrumental).mp3",
        "橘子班": "adv/bgm/Days - Nuit Silencieuse.mp3",
        "AliceSoft": "adv/bgm/アリスソフト - かわいいのでてきた.mp3",
        "枕": "adv/bgm/松本文紀 - 夜の向日葵.mp3",
    }
    bgm_file = bgm_files.get(club.name, "默认 BGM 文件路径")

    context = {"club": club, "advs": advs, "bgm": bgm_file}
    return render(request, "club_detail.html", context)
