from django.db import models
from django.db.models import Avg
from .fields import CompositeField


class Club(models.Model):
    name = models.CharField(max_length=20)
    pub_date = models.DateField('date published')
    rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Store the average rate
    photo = models.ImageField(upload_to="Club_images", blank=True)

    def update_average_rate(self):
        advs = self.adv_set.all()
        total_score = sum([adv.rate for adv in advs])
        count = advs.count()
        self.rate = total_score / count if count > 0 else 0
        self.save()

    def __str__(self):
        return self.name  # 添加此方法以显示友好的名称


class Adv(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    pub_date = models.DateField('date published')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    platform = models.CharField(max_length=20)
    rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Store the average rate
    photo = models.ImageField(upload_to="adv_images", blank=True)

    def update_average_rate(self):
        # 从 CompositeField 中提取 decimal_part 并计算平均值
        comments = self.Comments_set.all()
        total_score = sum([comment.comments.decimal_part for comment in comments])
        count = comments.count()
        self.rate = total_score / count if count > 0 else 0
        self.save()
        self.club.update_average_rate()  # 更新相关 Club 的评分

    def __str__(self):
        return self.title  # 添加此方法以显示友好的名称


class User(models.Model):
    name = models.CharField(max_length=20)  # 注册用户名
    password = models.CharField(max_length=20)
    job = models.CharField(max_length=20)
    sex = models.CharField(max_length=1, choices=[('M', '男'),  ('F', '女')], default='M', blank=True)
    photo = models.ImageField(upload_to="User_images", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Comments')
    comments = CompositeField()  # CompositeField to include rating and text comment
    adv = models.ForeignKey(Adv, on_delete=models.CASCADE, related_name='Comments_set')  # ForeignKey to relate to Adv

    def __str__(self):
        return f"{self.user} - {self.adv}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.adv.update_average_rate()
    # 商品评价，包含打分和字符串评价
    # DecimalField(max_digits=5, decimal_places=2)和CharField(max_length=20)
