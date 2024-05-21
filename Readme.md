# 视觉小说评价系统
## 一. 表结构设计:
    ADV信息表：包含ADV的书名、外键制作社团、发行日期、发售平台、价格、评价(分数+评论)、分数。
    评论信息表：包含外键用户评价(分数+评论)、外键ADV。
    用户信息表：包含用户名、密码、性别、职业、头像。
    社团信息表：包含名字、制作的adv、创立时间、评分(根据作品加权评分)、logo相片
## 二. 基本功能要求:
    1.用户注册和登录
    2.用户添加Adv信息，Club信息。
    3.用户评价ADV。
    4.查看ADV信息。
    5.查询社团信息
### 三.进阶功能：
    1.自由地通过链接查看Adv的Club，Club的Adv，在Adv详情页转向评论等。
    2.前端:
        2.1看板娘
        2.2为每个页面添加了独特的bgm.其中每个社团的bgm都是该社灵魂bgm，每个Adv同理。

## 项目网页：
报备不一定过，直连是可以的。
- http://49.235.184.91/index/
- http://www.adv.xn--6qq986b3xl/index/
- 项目github: 
 https://github.com/eeeshushusang/-PJ_ADV-

## 后端：
galgame信息：
wiki;CNGAL;DLsite;Steam;

## 前端：
- live2d最简单的抄法：
https://github.com/stevenjoezhang/live2d-widget
- 登陆,注册，上传信息等页面样式参考：
https://www.bilibili.com/video/BV1X3411y7of/?spm_id_from=333.880.my_history.page.click&vd_source=efbe71818b8135cefb115ae13d27eec1
- 山羊鼠标样式：
https://www.bilibili.com/video/BV1wb4y1a7uQ/?spm_id_from=333.880.my_history.page.click

### 图片：
-    全局背景图：Anmi
-    部分网页框内背景：Weri

### 音乐：
-    首页，上传信息页： MANYO,三輪学 - 黑猫さんの背伸び
-    橘子班/高考恋爱100天：Days - Nuit Silencieuse    
-    AliceSoft：アリスソフト - かわいいのでてきた
       兰斯10：アリスソフト - the end
       兰斯7 战国兰斯：アリスソフト - My Glorious Days
-    Leaf:上原れな - 届かない恋 (Instrumental)
        白色相簿1：石川真也 - FILL YOU
        白色相簿2：石川真也 - あの頃のように
-    枕社：松本文紀 - 夜の向日葵
        樱之诗：松本文紀 - 夢の歩みを見上げて
        樱之刻：松本文紀 - 櫻ノ詩 -2023Mix inst ver-
-    Key社：麻枝准,Key Sounds Label - 渚
        Summer Pockets:麻枝准 - Sea, You & Me
        Clannad:麻枝准 - 同じ高みへ

### 部署上线：   
腾讯云：服务器(学生折扣)10r/月;域名：首年10元(便宜的中文域名)
使用nginx绕过域名报备进行上线。麻烦的一批。

### 后续跟进计划：
- live2d，本打算从BA中扣一个乐队爱丽的小人模型下来，结果发现不会用相关库，不了了之。
- 音乐未实现，同一曲目在不同网页播放时，继承上个网页的播放进度
- 鼠标特效可以做的更好看点
