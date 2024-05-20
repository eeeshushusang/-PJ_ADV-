from django.contrib import admin
from .forms import CommentsForm

from .models import Adv
from .models import Club
from .models import User
from .models import Comments


class CommentsAdmin(admin.ModelAdmin):
    form = CommentsForm


admin.site.register(Adv)
admin.site.register(Club)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(User)
# Register your models here.
