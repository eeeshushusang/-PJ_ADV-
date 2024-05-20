# pj_adv/forms.py
from django import forms

from .fields import CompositeValue
from .widgets import CompositeWidget
from .models import Comments, Adv, Club, User


class CompositeFormField(forms.MultiValueField):
    widget = CompositeWidget

    def __init__(self, *args, **kwargs):
        fields = (
            forms.DecimalField(max_digits=5, decimal_places=2),
            forms.CharField(max_length=20),
        )
        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            # Ensure that the composite data is stored in the format 'decimal:char'
            return f"{data_list[0]}:{data_list[1]}"
        return None


class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=20,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'username',
                                                             'autofocus': ''}))
    password = forms.CharField(label='密码', max_length=20,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'password'}))


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):
    gender = (
        ('M', "男"),
        ('F', "女"),
    )
    username = forms.CharField(label="用户名", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=20,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=20,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    job = forms.CharField(max_length=20)
    photo = forms.ImageField(label='照片', required=False)
    sex = forms.ChoiceField(label='性别', choices=gender)


class ClubUpdateForm(forms.Form):
    username = forms.CharField(label="社团名", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    pub_date = forms.DateField(label="创立日期", widget=forms.DateInput(attrs={'class': 'form-control'}))
    photo = forms.ImageField(label='照片', required=False)


class AdvUpdateForm(forms.Form):
    club = forms.ModelChoiceField(
        queryset=Club.objects.all(),
        label="社团",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    title = forms.CharField(
        label="标题",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    pub_date = forms.DateField(
        label="发布日期",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    price = forms.DecimalField(
        label="价格",
        max_digits=6,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    platform = forms.CharField(
        label="平台",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    photo = forms.ImageField(
        label="照片",
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )


class CommentsForm(forms.ModelForm):
    decimal_part = forms.DecimalField(
        label="评分",
        max_digits=4,
        decimal_places=2,
        min_value=0,
        max_value=10,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="请输入0到10之间的值"
    )
    char_part = forms.CharField(
        label="评论内容",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="最多20个字符"
    )

    class Meta:
        model = Comments
        fields = ['adv', 'decimal_part', 'char_part']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.comments:
            self.fields['decimal_part'].initial = self.instance.comments.decimal_part
            self.fields['char_part'].initial = self.instance.comments.char_part

    def save(self, commit=True):
        instance = super(CommentsForm, self).save(commit=False)
        composite_value = CompositeValue(
            decimal_part=self.cleaned_data['decimal_part'],
            char_part=self.cleaned_data['char_part']
        )
        instance.comments = composite_value
        if commit:
            instance.save()
        return instance